# Exercise the real read-only checker in disposable paired repositories.
require 'fileutils'
require 'json'
require 'open3'
require 'rbconfig'
require 'tmpdir'

source = File.expand_path('..', __dir__)
files = %w[documentation.md readme.md project-description.md mechanical-helper-audit.md].map { |name| "docs/standards/#{name}" }
files += %w[AGENTS.md scripts/check_standards.rb scripts/test_standards.rb]
checks = 0
verify = lambda do |condition, message|
  raise message unless condition
  checks += 1
end

Dir.mktmpdir('paired-standards-') do |directory|
  roots = %w[agent-helm agent-compass].map do |name|
    root = File.join(directory, name)
    files.each do |path|
      target = File.join(root, path)
      FileUtils.mkdir_p(File.dirname(target))
      FileUtils.cp(File.join(source, path), target)
    end
    FileUtils.mkdir_p(File.join(root, '.claude-plugin'))
    File.write(File.join(root, '.claude-plugin/plugin.json'), JSON.generate('name' => name))
    root
  end
  run = lambda do |local = roots[0], other = roots[1]|
    output, error, status = Open3.capture3(RbConfig.ruby, File.join(local, 'scripts/check_standards.rb'), other)
    [status.exitstatus, output + error]
  end
  change = lambda do |path, replacement, &block|
    original = File.binread(path)
    begin
      File.binwrite(path, replacement.call(original))
      block.call
    ensure
      File.binwrite(path, original)
    end
  end
  helper = File.join(roots[1], 'docs/standards/mechanical-helper-audit.md')
  change.call(helper, ->(text) { text + "\nLocal fixture: preserve this project's own helper write boundaries.\n" }) do
    [roots, roots.reverse].each do |local, other|
      code, output = run.call(local, other)
      verify.call(code == 0 && output.include?('Shared standards synchronized'), 'Different local guidance or reverse-direction invocation was rejected')
    end
  end
  files.first(3).each do |relative|
    change.call(File.join(roots[1], relative), ->(text) { text + "\n" }) do
      code, output = run.call
      verify.call(code == 1 && output.include?(relative), "Byte drift escaped detection: #{relative}")
    end
  end
  change.call(helper, ->(text) { text.sub('Prefer existing native tools', 'Always create a new helper') }) do
    code, output = run.call
    verify.call(code == 1 && output.include?('mechanical-helper-audit.md (shared block)'), 'Shared helper policy drift escaped detection')
  end
  [
    ->(text) { text + "\n<!-- shared-helper-standard:end -->\n" },
    ->(text) { text.sub('<!-- shared-helper-standard:start -->', '') },
    ->(text) { text.sub(/(?<=<!-- shared-helper-standard:start -->).*?(?=<!-- shared-helper-standard:end -->)/m, '') },
    ->(text) { text.split("\n\n## Project-specific requirements", 2).first }
  ].each do |replacement|
    change.call(helper, replacement) do
      code, output = run.call
      verify.call(code == 2 && output.include?('unverified'), 'Malformed helper boundaries were certified synchronized')
    end
  end
  change.call(File.join(roots[1], 'AGENTS.md'), ->(text) { text.sub('### Shared standards maintenance', '### Uncoordinated standards maintenance') }) do
    code, output = run.call
    verify.call(code == 1 && output.include?('AGENTS.md (shared block)'), 'Maintenance instruction drift escaped detection')
  end
  change.call(File.join(roots[1], 'scripts/check_standards.rb'), ->(text) { text + "\n# Changed fixture checker\n" }) do
    code, output = run.call
    verify.call(code == 1 && output.include?('scripts/check_standards.rb'), 'Checker drift escaped detection')
  end
  code, output = run.call(roots[0], File.join(directory, 'missing'))
  verify.call(code == 2 && output.include?('unverified'), 'Missing sibling was certified synchronized')
  code, output = run.call(roots[0], roots[0])
  verify.call(code == 2 && output.include?('Expected agent-compass'), 'Comparing a project with itself was accepted')
end
puts "Passed #{checks} paired-standards checks: shared drift, local tuning, both directions and unavailable/invalid inputs."
