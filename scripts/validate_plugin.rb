require "fileutils"
require "json"
require "pathname"
require "tmpdir"
require "yaml"

module CompassValidation
  module_function

  def check(condition, message)
    raise message unless condition
  end

  def frontmatter(path)
    match = read(path).match(/\A---\n(.*?)\n---\n/m)
    check(match, "Missing frontmatter: #{path}")
    YAML.safe_load(match[1])
  end

  def read(path)
    Pathname(path).read(encoding: "UTF-8:UTF-8")
  end

  def resource(root, path)
    file = root.join(path).cleanpath
    check(file.file?, "Missing packaged resource: #{file}")
    resolved = file.realpath
    check(resolved.to_s.start_with?("#{root.realpath}/"), "Resource escapes package: #{file}")
    file
  end

  def validate(root)
    root = Pathname(root).realpath
    manifest = JSON.parse(read(resource(root, ".claude-plugin/plugin.json")))
    marketplace = JSON.parse(read(resource(root, ".claude-plugin/marketplace.json")))
    check(manifest.fetch("skills") == "./skills/", "Manifest must expose shared skill entry points")
    check(manifest.fetch("version").match?(/\A\d+\.\d+\.\d+\z/), "Invalid plugin version")
    entry = marketplace.fetch("plugins").find { |plugin| plugin["name"] == manifest["name"] }
    check(entry, "Marketplace does not expose the plugin")
    check(entry.fetch("source") == "./", "Marketplace must point to this package, not a second copy")
    check(entry.dig("policy", "installation") == "AVAILABLE", "Plugin is not installable in Codex")
    check(!entry.key?("version") && !entry.key?("description"), "Maintain metadata only in plugin.json")

    workflows = root.glob("workflows/*.md").map { |file| file.basename(".md").to_s }.sort
    commands = root.glob("commands/*.md").map { |file| file.basename(".md").to_s }.sort
    skills = root.glob("skills/*/SKILL.md").map { |file| file.parent.basename.to_s }.sort
    check(workflows.length == 4 && workflows == commands && commands == skills,
          "Claude commands, portable skills, and workflows must expose the same four names")

    skills.each do |name|
      skill = resource(root, "skills/#{name}/SKILL.md")
      metadata = frontmatter(skill)
      check(metadata["name"] == name && name.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/),
            "Invalid skill name: #{skill}")
      check(name.length <= 64, "Skill name exceeds 64 characters: #{skill}")
      check(metadata["description"].is_a?(String) && !metadata["description"].strip.empty?,
            "Missing skill description: #{skill}")
      check(metadata["description"].length <= 1024 && !metadata["description"].match?(/[<>]/),
            "Invalid skill description: #{skill}")
      links = read(skill).scan(/\[[^\]]+\]\(([^)]+)\)/).flatten
      targets = links.map { |link| resource(root, skill.parent.join(link).relative_path_from(root)).realpath }
      check(targets.include?(root.join("workflows/#{name}.md")), "Skill bypasses shared workflow: #{name}")
      check(targets.include?(root.join("prompts/shared/runtime.md")), "Skill omits shared runtime: #{name}")

      command = resource(root, "commands/#{name}.md")
      body = read(command).sub(/\A---\n.*?\n---\n/m, "").strip
      check(body.include?("${CLAUDE_PLUGIN_ROOT}/skills/#{name}/SKILL.md"),
            "Claude command does not load the shared skill: #{name}")
      check(body.lines.length <= 3, "Command duplicates orchestration instead of pointing to it: #{name}")
    end

    root.glob("agents/*.md").each do |agent|
      role = agent.basename(".md").to_s
      metadata = frontmatter(agent)
      check(metadata["name"] == role, "Agent name must match its shared role: #{role}")
      check(metadata["model"].is_a?(String) && !metadata["model"].empty?,
            "Missing Claude specialist model: #{role}")
      check(%w[high max].include?(metadata["effort"]),
            "Specialist must declare an explicit shared high/max effort: #{role}")
      procedure = resource(root, "prompts/shared/#{role}.md")
      check(read(agent).include?("${CLAUDE_PLUGIN_ROOT}/prompts/shared/runtime.md"),
            "Agent must load shared routing and step boundaries: #{role}")
      check(read(agent).include?("${CLAUDE_PLUGIN_ROOT}/prompts/shared/#{role}.md"),
            "Agent must reference its shared procedure: #{role}")
      check(!read(agent).include?(read(procedure).strip), "Agent duplicates specialist procedure: #{role}")
    end

    root.glob("{commands,workflows,prompts,skills,agents}/**/*.md").each do |file|
      read(file).scan(%r{(?<![\w.-])(?:workflows|prompts|skills|agents|data)/[\w./-]+\.md}).uniq.each do |path|
        resource(root, path)
      end
    end
    root.glob("docs/**/*.md").each do |file|
      frontmatter(file) if read(file).start_with?("---\n")
    end
    true
  end

  def run(root)
    validate(root)
    Dir.mktmpdir("compass-package-check-") do |temp|
      installation = Pathname(temp).join("installed plugin")
      workspace = Pathname(temp).join("candidate workspace")
      installation.mkpath
      workspace.mkpath
      %w[.claude-plugin commands workflows prompts skills agents data].each do |component|
        FileUtils.cp_r(Pathname(root).join(component), installation)
      end
      Dir.chdir(workspace) { validate(installation) }
      check(workspace.children.empty?, "Package validation wrote candidate workspace data")
    end
    puts "Validated four shared workflows, both entry-point sets, and a relocated package."
  end
end

if $PROGRAM_NAME == __FILE__
  CompassValidation.run(Pathname(__dir__).parent)
end
