require "open3"
require "pathname"
require "rbconfig"

# Checks validation and archive policy, not live workflow behavior.
root = Pathname(__dir__).parent
checks = 0
assert = lambda do |condition, message|
  raise message unless condition
  checks += 1
end

output, error, status = Open3.capture3(
  { "LC_ALL" => "C", "LANG" => "C" },
  RbConfig.ruby, "-EUS-ASCII:US-ASCII", root.join("scripts/validate_plugin.rb").to_s
)
assert.call(status.success?, "Validator failed under US-ASCII defaults: #{output}#{error}")

paths = %w[.claude/helm/example-log.json .in_use/example .claude/settings.local.json]
attributes, error, status = Open3.capture3("git", "-C", root.to_s, "check-attr", "export-ignore", "--", *paths)
assert.call(status.success?, "Could not check archive exclusions: #{error}")
paths.each do |path|
  assert.call(attributes.lines.any? { |line| line.strip == "#{path}: export-ignore: set" },
              "Local developer/host artifact is not excluded from Git archives: #{path}")
end

puts "Passed #{checks} validation and archive-policy checks (not live workflow tests)."
