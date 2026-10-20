require "open3"
require "pathname"
require "rbconfig"
require "yaml"

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

# Published salary fixtures exercise the compact presentation, exact monthly
# arithmetic and threshold-warning examples, not live market/visa research.
salary_header = "| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |"
salary_examples = []
%w[
  prompts/salary-calculator/step4-table-calculation.md
  docs/commands/salary-calculator/step4-table-calculation.md
].each do |relative|
  text = root.join(relative).read(encoding: "UTF-8:UTF-8")
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
assert.call(salary_examples[0] == salary_examples[1], "Salary prompt and documentation examples differ")

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
  assert.call(text.include?(priority_header), "Missing five-column Country Finder header")
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
