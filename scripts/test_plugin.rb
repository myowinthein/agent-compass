require "open3"
require "json"
require "pathname"
require "rbconfig"
require "yaml"
require_relative "validate_plugin"

# Checks validation, published examples, and instruction contracts, not LLM behavior.
root = Pathname(__dir__).parent
checks = 0
assert = lambda do |condition, message|
  raise message unless condition
  checks += 1
end
round_to = ->(value, step) { (Rational(value) / step).round * step }

output, error, status = Open3.capture3(
  { "LC_ALL" => "C", "LANG" => "C" },
  RbConfig.ruby, "-EUS-ASCII:US-ASCII", root.join("scripts/validate_plugin.rb").to_s
)
assert.call(status.success?, "Validator failed under US-ASCII defaults: #{output}#{error}")

manifest = JSON.parse(root.join(".claude-plugin/plugin.json").read(encoding: "UTF-8"))
assert.call(root.glob("commands/**/*.md").empty?, "Remove unused legacy command adapters; shared skills are the only entry points")
assert.call(manifest["commands"] == [], "Disable legacy command discovery so each shared skill appears only once")
assert.call(manifest.fetch("name") == "agent-compass", "Keep the technical plugin name unchanged")
assert.call(manifest.fetch("displayName") == "Agent Compass", "Claude must display Agent Compass")
assert.call(manifest.fetch("interface").fetch("displayName") == manifest.fetch("displayName"),
            "Codex and Claude must use the same display name")
assert.call(root.join("README.md").read(encoding: "UTF-8").match?(/^# Agent Compass$/),
            "README heading must use the product display name")

registry = JSON.parse(root.join("data/workspace-files.json").read(encoding: "UTF-8"))
registry.fetch("workflows").each do |workflow, spec|
  prompt_text = root.glob("prompts/#{workflow}/*.md").map { |file| file.read(encoding: "UTF-8") }.join("\n")
  docs_text = root.glob("docs/commands/#{workflow}*.md").concat(root.glob("docs/commands/#{workflow}/*.md")).map { |file| file.read(encoding: "UTF-8") }.join("\n")
  spec.fetch("artifacts").each_value do |artifact|
    assert.call(prompt_text.include?(artifact.fetch("current")), "Prompt omits current artifact: #{artifact}")
    assert.call(docs_text.include?(artifact.fetch("current")), "Docs omit current artifact: #{artifact}")
    assert.call(!prompt_text.include?(artifact.fetch("legacy")), "Legacy alias mapping must stay in the registry")
    root.glob("helpers/compass_lib/*.py").each do |file|
      assert.call(!file.read(encoding: "UTF-8").include?(artifact.fetch("legacy")), "Python duplicates the filename registry: #{file}")
    end
  end
  assert.call(root.join("workflows/#{workflow}.md").read(encoding: "UTF-8").include?("skills/workspace-files.md"),
              "Workflow must resolve legacy filenames before accessing saved outputs")
end

assert.call(manifest.fetch("icon") == "./assets/icon.svg", "Claude must reference the shared SVG icon")
%w[logo composerIcon].each do |field|
  assert.call(manifest.fetch("interface").fetch(field) == manifest.fetch("icon"),
              "Codex #{field} must reference the same image as Claude")
end

Dir.mktmpdir("compass-icon-check-") do |temp|
  installation = Pathname(temp)
  %w[.claude-plugin workflows prompts skills agents helpers data assets].each do |component|
    FileUtils.cp_r(root.join(component), installation)
  end
  [nil, ["./commands/"]].each do |commands|
    changed_manifest = manifest.dup
    commands.nil? ? changed_manifest.delete("commands") : changed_manifest["commands"] = commands
    installation.join(".claude-plugin/plugin.json").write(JSON.pretty_generate(changed_manifest))
    rejected = begin
      CompassValidation.validate(installation)
      false
    rescue RuntimeError => error
      error.message == "Disable legacy command discovery so each shared skill appears only once"
    end
    assert.call(rejected, "Validator accepted duplicate legacy command discovery: #{commands.inspect}")
  end
  installation.join(".claude-plugin/plugin.json").write(JSON.pretty_generate(manifest))
  installation.join("commands/nested").mkpath
  legacy = installation.join("commands/nested/unused.md")
  legacy.write("Unused adapter")
  rejected = begin
    CompassValidation.validate(installation)
    false
  rescue RuntimeError => error
    error.message == "Legacy command adapters must not be packaged"
  ensure
    legacy.delete
  end
  assert.call(rejected, "Validator accepted a reintroduced legacy adapter")
  icon = installation.join("assets/icon.svg")
  original = icon.read(encoding: "UTF-8")
  {
    "missing" => nil,
    "malformed XML" => "<svg",
    "wrong root" => original.sub("<svg ", "<html ").sub("</svg>", "</html>"),
    "wrong namespace" => original.sub("http://www.w3.org/2000/svg", "https://example.com"),
    "non-square" => original.sub('height="512"', 'height="256"'),
    "too small" => original.gsub("512", "32"),
    "non-numeric dimensions" => original.sub('width="512"', 'width="512px"'),
    "mismatched viewBox" => original.sub('viewBox="0 0 512 512"', 'viewBox="0 0 256 256"'),
    "embedded bitmap" => original.sub("</svg>", '<image href="data:image/png;base64,AAAA"/></svg>'),
    "script" => original.sub("</svg>", "<script>alert(1)</script></svg>"),
    "event handler" => original.sub("<svg ", '<svg onload="alert(1)" '),
    "external paint" => original.sub('fill="#35251f"', 'fill="url(https://example.com/paint.svg#colour)"'),
    "document type" => '<!DOCTYPE svg [<!ENTITY colour "red">]>' + original,
    "external resource" => original.sub("</svg>", '<use href="https://example.com/icon.svg#needle"/></svg>'),
    "oversized file" => original.ljust(5 * 1024 * 1024 + 1, " ")
  }.each do |label, bytes|
    bytes ? icon.binwrite(bytes) : icon.delete
    rejected = begin
      CompassValidation.validate(installation)
      false
    rescue RuntimeError
      true
    end
    assert.call(rejected, "Validator accepted a #{label} plugin icon")
    icon.binwrite(original)
  end
end

# Published salary fixtures exercise the compact presentation, exact monthly
# arithmetic and threshold-warning examples, not live market/visa research.
contract = JSON.parse(root.join("data/output-contracts.json").read(encoding: "UTF-8"))
salary_header = "| #{contract.fetch('salary').fetch('headers').join(' | ')} |"
salary_examples = []
docs = root.join("docs/commands/salary-calculator/step4-table-calculation.md").read(encoding: "UTF-8:UTF-8")
render_input = { "schema_version" => 1, "rows" => [], "priority_order" => [] }
docs.lines.grep(/^\| [🇦-🇿]{2} /).each do |line|
  country, rule, annual, premium, = line.strip.split("|").drop(1).map(&:strip)
  name, currency = country.match(/\A(.*?) \(([A-Z]{3})\)\z/).captures
  render_input["priority_order"] << name
  visa = if (match = rule.match(/\A([\d,]+)\/(yr|mo)/))
    { "state" => "Verified numeric", "amount" => match[1].delete(","), "period" => match[2] == "yr" ? "annual" : "monthly", "currency" => currency, "pay_basis" => "gross_base" }
  else
    { "state" => contract.fetch("salary").fetch("visa_labels").key(rule), "reason" => "Fictional example only" }
  end
  render_input["rows"] << { "country" => name, "visa" => visa, "calculation" => {
    "schema_version" => 1, "country" => name, "currency" => currency, "pay_basis" => "gross_base",
    "segments" => { "mainstream" => { "raw_annual_target" => annual.delete(",") }, "premium" => { "raw_annual_target" => premium.delete(",") } } } }
end
rendered, error, status = Open3.capture3("python3", "-I", "-B", root.join("helpers/compass.py").to_s, "render-salary", stdin_data: JSON.generate(render_input))
assert.call(status.success?, "Documented salary rendering failed: #{error}")
{ "documentation" => docs, "consumer renderer" => JSON.parse(rendered).dig("result", "markdown") }.each do |relative, text|
  assert.call(text.include?(salary_header), "Missing compact salary header: #{relative}")
  assert.call(!text.include?("Lower Range =") && !text.include?("Upper Range ="),
              "Superseded automatic range formula remains: #{relative}")
  rows = text.lines.grep(/^\| [🇦-🇿]{2} /).map { |line| line.strip.split("|").drop(1).map(&:strip) }
  assert.call(rows.length == 6, "Expected six salary example countries in #{relative}")
  salary_examples << rows
  states = []
  rows.each do |cells|
    assert.call(cells.length == 6, "Salary row must have six cells: #{cells}")
    country, rule, *salary = cells
    assert.call(salary.all? { |cell| cell.match?(/\A\d{1,3}(?:,\d{3})*\z/) },
                "Salary cells must contain one comma-formatted number: #{country}")
    mainstream, premium, mainstream_monthly, premium_monthly = salary.map { |n| Integer(n.delete(",")) }
    [[mainstream, mainstream_monthly], [premium, premium_monthly]].each do |annual, monthly|
      assert.call(annual % 500 == 0, "Annual target is not rounded to 500: #{country}")
      assert.call(monthly == round_to.call(Rational(annual, 12), 50), "Wrong example monthly reference: #{country}")
    end
    if (match = rule.match(/\A([\d,]+)\/(yr|mo)( ⚠️)?\z/))
      threshold = Rational(match[1].delete(","))
      target_values = [mainstream, premium].map { |v| match[2] == "mo" ? Rational(v, 12) : Rational(v) }
      assert.call(!match[3].nil? == target_values.any? { |value| value < threshold },
                  "Wrong example visa warning: #{country}")
      states << "Verified numeric"
    else
      assert.call(["No fixed minimum", "Not applicable", "Unknown", "Blocked"].include?(rule),
                  "Ambiguous visa rule display: #{country}")
      states << rule
    end
  end
  assert.call(states.uniq.sort == ["Verified numeric", "No fixed minimum", "Not applicable", "Unknown", "Blocked"].sort,
              "Salary examples must cover all five underlying threshold states")
end
assert.call(salary_examples[0] == salary_examples[1], "Salary renderer and documentation examples differ")

# Independent raw/display reference: a rounded annual target must not feed
# monthly conversion or turn a real threshold shortfall into a false pass.
raw = Rational(58_250)
reference = [round_to.call(raw, 500), round_to.call(raw / 12, 50)]
assert.call(reference == [58_500, 4_850], "Raw/display rounding reference changed")
assert.call(raw < 58_275 && reference[0] >= 58_275, "Borderline threshold fixture is invalid")
assert.call(!(raw < 58_250), "Equality must clear a salary-minimum comparison")
assert.call(round_to.call(Rational(60_300, 12), 50) == 5_050, "Monthly halfway tie must round upward")

threshold_rules = root.join("skills/sponsorship-threshold-rules.md").read(encoding: "UTF-8:UTF-8")
audit_prompt = root.join("prompts/salary-calculator/step5b-final-verification.md").read(encoding: "UTF-8:UTF-8")
assert.call(threshold_rules.include?("Equality clears this salary-minimum comparison"), "Missing equality rule")
assert.call(threshold_rules.include?("unrounded computed values"), "Visa checks must use raw values")
assert.call(threshold_rules.include?("Legacy display compatibility"), "Missing legacy threshold compatibility")
assert.call(threshold_rules.include?("not overall visa eligibility"), "Salary check must not claim visa eligibility")
assert.call(audit_prompt.include?("Formatting-only normalization is not salary recalibration"),
            "Presentation-only changes must not count as salary recalibration")
assert.call(audit_prompt.include?("Leave the legacy Step 4 file untouched"), "Legacy pre-audit evidence must be preserved")
assert.call(audit_prompt.include?("standard caption and final table"), "Final delivery must include salary context")
assert.call(audit_prompt.include?("Read prompts/salary-calculator/step4-table-calculation.md"),
            "Final audit must load the canonical table contract")

# Country Finder is Markdown instructions, not an executable scoring engine.
# Check the declared contract and documentation fixtures; do not claim these
# assertions exercise a model's evidence judgments or live workflow behavior.
priority_header = "| Country | Priority | Remote Fit | Sponsorship Fit | Main limitation |"
old_header = "| Country | Tier | Remote Fit | Sponsorship Fit |"
final_prompt = root.join("prompts/country-finder/step6-final-ranking.md").read(encoding: "UTF-8:UTF-8")
final_docs = root.join("docs/commands/country-finder/step6-final-ranking.md").read(encoding: "UTF-8:UTF-8")
priorities = ["🥇 Focus", "🥈 Selective", "🥉 Monitor", "🎗️ Deprioritize", "Pending evidence"]
fits = %w[Strong Moderate Weak Excluded Unknown]
[final_prompt, final_docs].each do |text|
  assert.call(text.include?(priority_header) || text.include?("data/output-contracts.json"), "Missing Country Finder contract")
  assert.call(!text.include?(old_header), "Superseded Country Finder table header remains")
  priorities.each { |value| assert.call(text.include?(value), "Missing priority: #{value}") }
end
assert.call(final_prompt.include?('Keep the Summary\'s original wording and counts unchanged'),
            "Display labels must not change the authoritative Summary schema")
assert.call(final_prompt.include?('including candidates in its separate missing-data/ingestion notes'),
            "The final table must account for candidates with wholly missing research")
assert.call(final_prompt.include?('do not migrate or rewrite an older four-column result'),
            "Completed results must not be silently reformatted")
assert.call(final_prompt.include?('uses the Priority Table\'s row order'),
            "Salary Calculator ordering handoff must remain explicit")
scoring = root.join("prompts/country-finder/step5-scoring.md").read(encoding: "UTF-8:UTF-8")
assert.call(scoring.include?('never numerical scores, percentages, or a combined priority formula'),
            "Step 5 must not invent numerical fits or priorities")

examples = final_docs.lines.grep(/^\| 🏳️ Example /).map { |line| line.strip.split("|").drop(1).map(&:strip) }
assert.call(examples.length == 9, "Expected nine Country Finder presentation/edge-case fixtures")
examples.each do |cells|
  assert.call(cells.length == 5, "Country Finder example must contain five cells: #{cells}")
  country, priority, remote, sponsorship, limitation = cells
  assert.call(priorities.include?(priority), "Invalid example priority: #{country}")
  assert.call([remote, sponsorship].all? { |fit| fits.include?(fit) }, "Invalid example fit: #{country}")
  assert.call(!limitation.empty?, "Missing example limitation: #{country}")
  usable = [remote, sponsorship].any? { |fit| %w[Strong Moderate].include?(fit) }
  unknown = [remote, sponsorship].include?("Unknown")
  valid = if usable
            priorities.first(3).include?(priority)
          elsif unknown
            priority == "Pending evidence"
          else
            priority == "🎗️ Deprioritize"
          end
  assert.call(valid, "Example priority contradicts track states: #{country}")
end
assert.call(examples.map(&:first).uniq.length == examples.length, "Duplicate example country")
priority_order = examples.map { |cells| priorities.index(cells[1]) }
assert.call(priority_order == priority_order.sort, "Example priority groups are out of order")
assert.call(examples.map { |cells| cells[1] }.uniq == priorities, "Examples must cover every priority")
assert.call(examples.any? { |c| c[2..3].sort == %w[Strong Unknown] }, "Missing usable/unknown example")
assert.call(examples.any? { |c| c[2..3] == %w[Excluded Excluded] }, "Missing both-excluded example")
assert.call(examples.any? { |c| c[2..3] == %w[Unknown Weak] }, "Missing unknown/weak example")
assert.call(examples.any? { |c| c[2..3] == %w[Excluded Unknown] }, "Missing excluded/unknown example")
assert.call(examples.any? { |c| c[2..3] == %w[Unknown Unknown] }, "Missing wholly unresearched example")

paths = %w[.claude/helm/example-log.json .in_use/example .claude/settings.local.json]
attributes, error, status = Open3.capture3("git", "-C", root.to_s, "check-attr", "export-ignore", "--", *paths)
assert.call(status.success?, "Could not check archive exclusions: #{error}")
paths.each do |path|
  assert.call(attributes.lines.any? { |line| line.strip == "#{path}: export-ignore: set" },
              "Local developer/host artifact is not excluded from Git archives: #{path}")
end

deployment = YAML.safe_load_file(root.join(".github/workflows/docs.yml"))
assert.call(deployment.fetch("on").keys.sort == %w[pull_request push workflow_dispatch],
            "Docs must build on pushes, pull requests and manual runs without a schedule")
assert.call(deployment.dig("on", "push", "branches") == ["main"], "Only main pushes should deploy docs")
assert.call(deployment.fetch("permissions") == { "contents" => "read" }, "Build tokens must remain read-only")
build_steps = deployment.dig("jobs", "build", "steps")
assert.call(build_steps.any? { |step| step["run"] == "bundle exec rake test" },
            "Deployment must run the full project checks")
theme_resolution = build_steps.find { |step| step.fetch("run", "").include?("/releases/latest") }&.fetch("run")
assert.call(theme_resolution && theme_resolution.include?("COMPASS_THEME_TAG"),
            "Deployment must resolve a stable theme tag before building")
["", "main", "v0.12.0-rc.1"].each do |tag|
  output, status = Open3.capture2e("bash", "-e", "-o", "pipefail", "-c", <<~BASH)
    gh() { printf '%s' '#{tag}'; }
    bundle() { echo 'Unexpected build'; }
    #{theme_resolution}
  BASH
  assert.call(!status.success? && !output.include?("Unexpected build"),
              "Invalid release #{tag.inspect} must stop before the build")
end
output, status = Open3.capture2e("bash", "-e", "-o", "pipefail", "-c", <<~BASH)
  gh() { return 1; }
  bundle() { echo 'Unexpected build'; }
  #{theme_resolution}
BASH
assert.call(!status.success? && !output.include?("Unexpected build"),
            "Failed release lookup must stop before the build")
upload = build_steps.find { |step| step.fetch("uses", "").start_with?("actions/upload-pages-artifact@") }
assert.call(upload && upload.fetch("if").include?("refs/heads/main") &&
                     upload.fetch("if").include?("github.event_name != 'pull_request'"),
            "Only main deployment runs may upload the tested site")
assert.call(build_steps.index(upload) > build_steps.index { |step| step["run"] == "bundle exec rake test" },
            "The site must pass checks before artifact upload")
assert.call(deployment.dig("jobs", "deploy", "needs") == "build", "Deployment must depend on a successful build")
assert.call(deployment.dig("jobs", "deploy", "if") == upload.fetch("if"),
            "Pull requests and other branches must never deploy")
assert.call(deployment.dig("jobs", "deploy", "permissions") == { "pages" => "write", "id-token" => "write" },
            "Only the deploy job should receive deployment permissions")
assert.call(deployment.fetch("jobs").values.flat_map { |job| job.fetch("steps") }.all? { |step|
  !step.key?("uses") || step.fetch("uses").match?(/@[0-9a-f]{40}\z/)
}, "Deployment actions must be pinned to immutable commits")

puts "Passed #{checks} validator, salary-example, country-table contract/example, archive-policy and deployment checks (not live workflow tests)."
