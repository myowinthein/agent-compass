# Optional native discovery checks. Uses temporary installs, never model calls.
require "json"
require "open3"
require "tempfile"
require "timeout"
require_relative "validate_plugin"

root = Pathname(__dir__).parent.realpath
installed = ARGV == ["--installed"]
raise "Usage: ruby scripts/check_clients.rb [--installed]" unless ARGV.empty? || installed
manifest = JSON.parse(CompassValidation.read(root.join(".claude-plugin/plugin.json")))
name = manifest.fetch("name")
plugin_id = "#{name}@#{JSON.parse(CompassValidation.read(root.join('.claude-plugin/marketplace.json'))).fetch('name')}"
expected = root.glob("workflows/*.md").map { |file| file.basename(".md").to_s }.sort

Dir.mktmpdir("compass-client-check-") do |temp|
  run = lambda do |env, *command|
    output, status = Timeout.timeout(45) { Open3.capture2e(env, *command, chdir: temp) }
    CompassValidation.check(status.success?, "Client command failed (#{command.join(' ')}): #{output}")
    output
  end
  args = installed ? [] : ["--setting-sources", "", "--plugin-dir", root.to_s]
  output = run.call({}, "claude", *args, "plugin", "details", installed ? plugin_id : name)
  inventories = output.scan(/^\s+(Skills|Commands) \((\d+)\)\s*([^\n]*)/)
  names = inventories.flat_map { |_, count, entries| count.to_i.zero? ? [] : entries.split(", ") }
  CompassValidation.check(!inventories.empty? && inventories.sum { |_, count, _| count.to_i } == expected.length && names.sort == expected,
                          "Claude exposes missing or duplicate workflows: #{output}")
  puts "Claude: exactly four shared workflow commands."

  env = installed ? {} : { "CODEX_HOME" => File.join(temp, "codex") }
  unless installed
    FileUtils.mkdir_p(env.fetch("CODEX_HOME"))
    run.call(env, "codex", "plugin", "marketplace", "add", root.to_s)
    run.call(env, "codex", "plugin", "add", plugin_id)
  end
  Tempfile.create("compass-app-server-errors") do |errors|
    Open3.popen3(env, "codex", "app-server", chdir: temp) do |input, stream, error_stream, waiter|
      drainer = Thread.new { IO.copy_stream(error_stream, errors) }
      request = lambda do |id, method, params|
        input.puts(JSON.generate({ id: id, method: method, params: params }))
        input.flush
        Timeout.timeout(45) do
          loop do
            line = stream.gets
            raise "Codex closed before #{method}" unless line
            response = JSON.parse(line)
            next unless response["id"] == id
            raise "Codex #{method} failed: #{response['error']}" if response["error"]
            break response.fetch("result")
          end
        end
      end
      begin
        request.call(1, "initialize", { clientInfo: { name: "compass_discovery_check", version: "1.0.0" }, capabilities: { experimentalApi: true } })
        input.puts(JSON.generate({ method: "initialized" }))
        input.flush
        # plugin/read omits migrated commands. Check the actual session catalog.
        result = request.call(2, "skills/list", { cwds: [temp], forceReload: true })
        entries = result.fetch("data").fetch(0)
        CompassValidation.check(entries.fetch("errors").empty?, "Codex discovery errors: #{entries['errors']}")
        skills = entries.fetch("skills").select { |skill| skill["pluginId"] == plugin_id }
        CompassValidation.check(skills.map { |skill| skill.fetch("name") }.sort == expected.map { |entry| "#{name}:#{entry}" },
                                "Codex exposes missing, duplicate or migrated commands: #{skills.map { |skill| skill['name'] }}")
        skills.each do |skill|
          CompassValidation.check(skill.fetch("enabled") && Pathname(skill.fetch("path")).parent.parent.basename.to_s == "skills",
                                  "Codex must load an enabled shared skill: #{skill}")
          entry = Pathname(skill.fetch("path"))
          CompassValidation.check(entry.binread == root.join("skills", entry.parent.basename, "SKILL.md").binread,
                                  "Codex loaded a different skill source: #{entry}")
        end
        puts "Codex: exactly four enabled shared workflow commands, no migrated duplicates."
      ensure
        input.close
        Process.kill("TERM", waiter.pid) if waiter.alive?
        waiter.join(5)
        Process.kill("KILL", waiter.pid) if waiter.alive?
        drainer.join(5)
      end
    end
  end
end
