require "fileutils"
require "json"
require "pathname"
require "rexml/document"
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
    check(manifest["commands"] == [], "Disable legacy command discovery so each shared skill appears only once")
    check(root.glob("commands/**/*.md").empty?, "Legacy command adapters must not be packaged")
    check(manifest.fetch("version").match?(/\A\d+\.\d+\.\d+\z/), "Invalid plugin version")
    entry = marketplace.fetch("plugins").find { |plugin| plugin["name"] == manifest["name"] }
    check(entry, "Marketplace does not expose the plugin")
    check(entry.fetch("source") == "./", "Marketplace must point to this package, not a second copy")
    check(entry.dig("policy", "installation") == "AVAILABLE", "Plugin is not installable in Codex")
    check(!entry.key?("version") && !entry.key?("description"), "Maintain metadata only in plugin.json")
    icon = resource(root, manifest.fetch("icon"))
    %w[logo composerIcon].each do |field|
      check(manifest.fetch("interface").fetch(field) == manifest.fetch("icon"),
            "Claude and Codex must reference the same icon file")
    end
    check(icon.extname == ".svg" && icon.size <= 5 * 1024 * 1024, "Plugin icon must be an SVG no larger than 5 MiB")
    begin
      document = REXML::Document.new(read(icon))
    rescue REXML::ParseException
      raise "Invalid plugin icon SVG XML"
    end
    svg = document.root
    check(svg && svg.name == "svg" && svg.namespace == "http://www.w3.org/2000/svg", "Invalid plugin icon SVG root")
    dimensions = %w[width height].map { |field| svg.attributes[field].to_s }
    check(dimensions.all? { |value| value.match?(/\A\d+(?:\.\d+)?\z/) && value.to_f.finite? && value.to_f >= 48 } &&
          dimensions.map(&:to_f).uniq.length == 1, "Plugin icon must have square numeric dimensions of at least 48 pixels")
    check(svg.attributes["viewBox"] == "0 0 #{dimensions.join(' ')}", "Plugin icon viewBox must match its dimensions")
    check(document.doctype.nil?, "Plugin icon must not declare external entities")
    document.elements.each("//*") do |element|
      check(!%w[image script foreignObject].include?(element.name), "Plugin icon must contain only static vector artwork")
      element.attributes.each_attribute do |attribute|
        check(!attribute.name.start_with?("on") && attribute.name != "href" && !attribute.value.include?("url("),
              "Plugin icon must not execute code or load external resources")
      end
    end
    resource(root, "helpers/salary_targets.py")
    resource(root, "helpers/compass.py")
    %w[common files money research state tables timezones].each { |name| resource(root, "helpers/compass_lib/#{name}.py") }
    registry = JSON.parse(read(resource(root, "data/workspace-files.json")))
    check(registry.fetch("schema_version") == 1 && registry.fetch("workflows").keys.sort == %w[country-finder salary-calculator],
          "Unknown workspace filename registry")
    filenames = []
    registry.fetch("workflows").each do |workflow, spec|
      check(spec.fetch("state") == ".#{workflow}-state.json", "Keep checkpoint filenames unchanged")
      artifacts = spec.fetch("artifacts")
      steps = artifacts.values.map { |artifact| artifact.fetch("step") }
      check(!steps.empty? && steps.all? { |step| step.is_a?(Integer) && step.positive? } && steps.uniq.sort == (1..steps.max).to_a &&
            artifacts.fetch("final-results").fetch("step") == steps.max, "Invalid artifact checkpoint membership")
      artifacts.each_value do |artifact|
        check(artifact.keys.sort == %w[current legacy step] &&
              artifact.fetch("current").match?(/\A#{workflow}-#{format('%02d', artifact.fetch('step'))}[ab]?-[a-z]+(?:-[a-z]+)*\.md\z/),
              "Invalid current artifact filename")
        check(artifact.fetch("legacy").match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\.md\z/), "Invalid legacy artifact filename")
        filenames.concat(artifact.values_at("current", "legacy"))
      end
    end
    check(filenames.uniq.length == filenames.length, "Artifact filenames must be globally unique")
    contract = JSON.parse(read(resource(root, "data/output-contracts.json")))
    check(contract.fetch("schema_version") == 1, "Unknown output contract")
    check(contract.fetch("salary").fetch("headers").length == 6 && contract.fetch("country").fetch("headers").length == 5,
          "Unexpected compact table contract")

    workflows = root.glob("workflows/*.md").map { |file| file.basename(".md").to_s }.sort
    skills = root.glob("skills/*/SKILL.md").map { |file| file.parent.basename.to_s }.sort
    check(workflows.length == 4 && workflows == skills,
          "Portable skills and workflows must expose the same four names")

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

    root.glob("{workflows,prompts,skills,agents}/**/*.md").each do |file|
      read(file).scan(%r{(?<![\w.-])(?:workflows|prompts|skills|agents|data|helpers)/[\w./-]+\.(?:md|py|json)}).uniq.each do |path|
        resource(root, path)
      end
      [contract.fetch("salary").fetch("caption"),
       "| #{contract.fetch('salary').fetch('headers').join(' | ')} |",
       "| #{contract.fetch('country').fetch('headers').join(' | ')} |"].each do |template|
        check(!read(file).include?(template), "Duplicate runtime template; reference output-contracts.json: #{file}")
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
      %w[.claude-plugin workflows prompts skills agents helpers data assets].each do |component|
        FileUtils.cp_r(Pathname(root).join(component), installation)
      end
      Dir.chdir(workspace) { validate(installation) }
      check(workspace.children.empty?, "Package validation wrote candidate workspace data")
    end
    puts "Validated four shared skill entry points, workflows, and a relocated package."
  end
end

if $PROGRAM_NAME == __FILE__
  CompassValidation.run(Pathname(__dir__).parent)
end
