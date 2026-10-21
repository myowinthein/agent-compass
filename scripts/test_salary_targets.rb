require "fileutils"
require "json"
require "open3"
require "pathname"
require "tmpdir"

# Exercise the actual consumer CLI against an independent Ruby Rational oracle.
root = Pathname(__dir__).parent
helper = root.join("helpers/salary_targets.py")
checks = 0
assert = lambda do |condition, message|
  raise message unless condition
  checks += 1
end
invoke = lambda do |input, script = helper, directory = root|
  Open3.capture3("python3", "-I", "-B", script.to_s, stdin_data: input, chdir: directory.to_s)
end
calculate = lambda do |input|
  output, error, status = invoke.call(JSON.generate(input))
  assert.call(status.success? && error.empty?, "Helper failed: #{error}")
  JSON.parse(output)
end
round_to = ->(value, step) { (value / step).round * step }
policy = JSON.parse(root.join("data/output-contracts.json").read(encoding: "UTF-8"))
annual_increment = policy.fetch("salary").fetch("annual_increment")
monthly_increment = policy.fetch("salary").fetch("monthly_increment")
fixtures = JSON.parse(root.join("scripts/fixtures/salary-targets-demo.json").read(encoding: "UTF-8"))

fixtures.fetch("cases").each do |fixture|
  input = fixture.fetch("input")
  result = calculate.call(input)
  assert.call(result.fetch("input") == input, "Input provenance was not preserved")
  input.fetch("segments").each do |name, segment|
    annual = Rational(segment.fetch("market_midpoint")) * (1 - Rational(segment.fetch("adjustment_percent")) / 100)
    actual = result.fetch("segments").fetch(name)
    assert.call(Rational(actual.fetch("raw_annual")) == annual, "Wrong raw annual: #{input['country']}/#{name}")
    assert.call(Rational(actual.fetch("raw_monthly")) == annual / 12, "Wrong raw monthly")
    assert.call(actual.fetch("annual_display") == round_to.call(annual, annual_increment), "Wrong annual rounding")
    assert.call(actual.fetch("monthly_display") == round_to.call(annual / 12, monthly_increment), "Wrong monthly rounding")
    input.fetch("comparisons", {}).each do |label, comparison|
      target = comparison.fetch("period") == "annual" ? annual : annual / 12
      amount = Rational(comparison.fetch("amount"))
      check = actual.fetch("comparisons").fetch(label)
      assert.call(check.fetch("meets") == (target >= amount), "Comparison must use raw amounts")
      assert.call(Rational(check.fetch("shortfall")) == [amount - target, 0].max, "Wrong exact shortfall")
      assert.call(Rational(check.fetch("target_in_period")) == target, "Wrong comparison period")
    end
    assert.call(actual.fetch("comparisons").keys == input.fetch("comparisons", {}).keys,
                "Helper invented a comparison for a non-numeric state")
  end
  next unless fixture["recalibration"]

  revised = Marshal.load(Marshal.dump(input))
  fixture.fetch("recalibration").each do |name, amount|
    revised.fetch("segments")[name] = { "raw_annual_target" => amount }
  end
  audited = calculate.call(revised)
  mainstream = audited.fetch("segments").fetch("mainstream")
  assert.call(mainstream.fetch("comparisons").fetch("visa").fetch("meets") !=
              result.fetch("segments").fetch("mainstream").fetch("comparisons").fetch("visa").fetch("meets"),
              "Recalibration did not recompute the visa warning")
  assert.call(audited.fetch("segments").fetch("premium") == result.fetch("segments").fetch("premium"),
              "Recalibration changed an unaffected segment")
end

base = fixtures.fetch("cases").first.fetch("input")
edge = Marshal.load(Marshal.dump(base))
edge["comparisons"] = {}
%w[0 250 60300 0.00000000000000000001 999999999999999999999999.9999 60299.999999999999999999 60300.000000000000000001].each do |amount|
  edge["segments"] = %w[mainstream premium].to_h { |name| [name, { "raw_annual_target" => amount }] }
  actual = calculate.call(edge).fetch("segments").fetch("mainstream")
  annual = Rational(amount)
  assert.call(actual.fetch("annual_display") == round_to.call(annual, annual_increment), "Edge annual rounding failed")
  assert.call(actual.fetch("monthly_display") == round_to.call(annual / 12, monthly_increment), "Edge monthly rounding failed")
end

guide = root.join("skills/salary-calculation-helper.md").read(encoding: "UTF-8")
documented = JSON.parse(guide.match(/```json\n(.*?)\n```/m)[1])
assert.call(calculate.call(documented).fetch("segments") ==
            calculate.call(base.reject { |key, _| key == "comparisons" }.merge("comparisons" => { "visa" => base.dig("comparisons", "visa") })).fetch("segments"),
            "The documented invocation no longer matches the demo calculation")

invalid = []
[nil, true, 1, 1.5, "", "NaN", "Infinity", "1e3", "1,000", "-1", "1/3", " 100", "9" * 101].each do |value|
  input = Marshal.load(Marshal.dump(base))
  input["segments"]["mainstream"]["market_midpoint"] = value
  invalid << JSON.generate(input)
end
[
  ->(input) { input["schema_version"] = true },
  ->(input) { input["schema_version"] = 2 },
  ->(input) { input["extra"] = "unexpected" },
  ->(input) { input.delete("country") },
  ->(input) { input["segments"].delete("premium") },
  ->(input) { input["segments"]["extra"] = {} },
  ->(input) { input["segments"]["mainstream"]["adjustment_percent"] = "15.01" },
  ->(input) { input["segments"]["premium"]["adjustment_percent"] = "5" },
  ->(input) { input["segments"]["mainstream"]["raw_annual_target"] = "60000" },
  ->(input) { input["comparisons"]["visa"]["period"] = "weekly" },
  ->(input) { input["comparisons"]["visa"]["currency"] = "USD" },
  ->(input) { input["comparisons"]["visa"].delete("period") },
  ->(input) { input["comparisons"]["visa"]["pay_basis"] = "net" },
  ->(input) { input["comparisons"]["visa"]["extra"] = true },
  ->(input) { input["comparisons"]["other"] = {} },
  ->(input) { input["comparisons"]["candidate_minimum"]["amount"] = true },
  ->(input) { input["comparisons"]["candidate_minimum"]["currency"] = "USD" },
  ->(input) { input["pay_basis"] = "net" },
  ->(input) { input["currency"] = "eur" },
  ->(input) { input["comparisons"] = nil }
].each do |mutate|
  input = Marshal.load(Marshal.dump(base))
  mutate.call(input)
  invalid << JSON.generate(input)
end
invalid.concat(["{", "[]", "null", '{"schema_version":1,"schema_version":2}', '{"value":NaN}', '{"value":Infinity}', " " * 65537])
invalid << JSON.generate(base).sub("Germany".b, "\xff".b)
invalid.each do |input|
  output, error, status = invoke.call(input)
  assert.call(status.exitstatus == 2 && output.empty? && JSON.parse(error).dig("error", "kind") == "invalid_input",
              "Invalid input was not rejected cleanly: #{input}")
end

output, error, status = Open3.capture3("python3", "-I", "-B", "-c", <<~PYTHON, helper.to_s)
  import runpy, sys
  sys.version_info = (3, 10)
  sys.argv = sys.argv[1:]
  runpy.run_path(sys.argv[0], run_name="__main__")
PYTHON
assert.call(status.exitstatus == 3 && output.empty? && JSON.parse(error).dig("error", "kind") == "runtime_unavailable",
            "An unsupported Python version must be distinguishable from invalid data")

Dir.mktmpdir("compass-helper-test-") do |temp|
  installation = Pathname(temp).join("installed plugin")
  workspace = Pathname(temp).join("candidate workspace")
  installation.mkpath
  workspace.mkpath
  FileUtils.cp_r(root.join("helpers"), installation)
  FileUtils.cp_r(root.join("data"), installation)
  installed_helper = installation.join("helpers/salary_targets.py")
  before = installation.glob("**/*").select(&:file?).to_h { |path| [path.relative_path_from(installation).to_s, path.binread] }
  installation.glob("**/*").reverse_each { |path| path.chmod(path.directory? ? 0o555 : 0o444) }
  installation.chmod(0o555)
  begin
    output, error, status = invoke.call(JSON.generate(base), installed_helper, workspace)
    assert.call(status.success? && error.empty? && JSON.parse(output).fetch("input") == base,
                "Relocated read-only helper failed: #{error}")
    after = installation.glob("**/*").select(&:file?).to_h { |path| [path.relative_path_from(installation).to_s, path.binread] }
    assert.call(after == before && workspace.children.empty? && installation.glob("**/__pycache__").empty?,
                "Helper wrote files or changed its installation")
  ensure
    installation.chmod(0o755)
    installation.glob("**/*").each { |path| path.chmod(path.directory? ? 0o755 : 0o644) }
  end
end

# Independent seeded comparisons also cover exact recurring FX normalization.
random = Random.new(2081)
100.times do
  low = random.rand(1..100_000)
  high = low + random.rand(0..20_000)
  amount = random.rand(1..10_000)
  rate = Rational(random.rand(1..1000), random.rand(1..1000))
  expected = amount * 12 * rate
  input = { "schema_version" => 1,
            "pay" => { "low" => low.to_s, "high" => high.to_s, "currency" => "EUR", "period" => "annual", "basis" => "gross_base" },
            "minimum" => { "amount" => amount.to_s, "currency" => "USD", "period" => "monthly", "basis" => "gross_base", "hard_floor" => true },
            "quotes" => [{ "base" => "USD", "quote" => "EUR", "rate" => rate.to_s, "date" => "2026-10-21", "source" => "https://example.invalid/dummy" }] }
  output, error, status = Open3.capture3("python3", "-I", "-B", root.join("helpers/compass.py").to_s, "compare", stdin_data: JSON.generate(input))
  assert.call(status.success?, "Comparison failed: #{error}")
  result = JSON.parse(output).fetch("result")
  assert.call(Rational(result.fetch("normalized_minimum")) == expected, "Recurring normalization differs from Ruby oracle")
  assert.call(result.fetch("outcome") == (low >= expected ? "pass" : high < expected ? "fail" : "uncertain"),
              "Range comparison differs from independent oracle")
end

puts "Passed #{checks} salary/FX-helper checks with fictional inputs and an independent Ruby oracle (not desktop install tests)."
