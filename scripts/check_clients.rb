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
codex_manifest = JSON.parse(CompassValidation.read(root.join(".codex-plugin/plugin.json")))
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
  roles = output.scan(/^\s+Agents \((\d+)\)\s*([^\n]*)/)
  expected_roles = root.glob("agents/*.md").map { |file| file.basename(".md").to_s }.sort
  CompassValidation.check(roles.length == 1 && roles[0][0].to_i == expected_roles.length && roles[0][1].split(", ").sort == expected_roles,
                          "Claude exposes missing or duplicate specialists: #{output}")
  unless installed
    validation = run.call({}, "claude", "plugin", "validate", root.join(".claude-plugin/plugin.json").to_s)
    CompassValidation.check(!validation.match?(/Unknown field|unrecognized keys|No command files/i),
                            "Claude reports manifest compatibility warnings: #{validation}")
  end
  puts "Claude: exactly four shared skills and two specialists.#{installed ? '' : ' No manifest compatibility warnings.'}"

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
        params = { pluginName: name }
        if installed
          inventory = JSON.parse(run.call(env, "codex", "plugin", "list", "--json"))
          source = inventory.fetch("installed").find { |plugin| plugin["pluginId"] == plugin_id }&.fetch("marketplaceSource")
          CompassValidation.check(source, "Installed Codex marketplace source is unavailable")
          if source["sourceType"] == "local"
            params[:marketplacePath] = Pathname(source.fetch("source")).join(".claude-plugin/marketplace.json").to_s
          else
            params[:remoteMarketplaceName] = plugin_id.split("@", 2).last
          end
        else
          params[:marketplacePath] = root.join(".claude-plugin/marketplace.json").to_s
        end
        detail = request.call(3, "plugin/read", params).fetch("plugin")
        presentation = detail.fetch("summary").fetch("interface")
        CompassValidation.check(presentation.fetch("displayName") == codex_manifest.fetch("interface").fetch("displayName"),
                                "Codex did not load the expected display name: #{presentation}")
        %w[logo composerIcon].each do |field|
          path = Pathname(presentation.fetch(field))
          CompassValidation.check(path.file? && path.binread == root.join(codex_manifest.fetch("interface").fetch(field)).binread,
                                  "Codex did not resolve its #{field} to the packaged icon: #{path}")
        end
        puts "Codex: exactly four enabled shared skills, no migrated duplicates; display name and icons verified."
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
