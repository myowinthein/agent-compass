#!/usr/bin/env ruby
# Local, read-only comparison of the two projects' maintainer standards.
require 'json'

def shared_block(root, path, name, local_section: false)
  content = File.binread(File.join(root, path))
  first = "<!-- #{name}:start -->"
  last = "<!-- #{name}:end -->"
  unless content.scan(first).size == 1 && content.scan(last).size == 1
    raise ArgumentError, "#{root}/#{path}: expected one #{name} block"
  end
  prefix, remaining = content.split(first, 2)
  body, suffix = remaining.split(last, 2)
  unless suffix && !body.strip.empty?
    raise ArgumentError, "#{root}/#{path}: empty or reversed #{name} block"
  end
  if local_section && (!prefix.empty? || !suffix.start_with?("\n\n## Project-specific requirements\n\n") ||
      suffix.delete_prefix("\n\n## Project-specific requirements\n\n").strip.empty?)
    raise ArgumentError, "#{root}/#{path}: expected shared guidance followed by project-specific requirements"
  end
  body
end

if $PROGRAM_NAME == __FILE__
  begin
    raise ArgumentError, 'Usage: ruby scripts/check_standards.rb [sibling-repository]' if ARGV.size > 1
    local = File.expand_path('..', __dir__)
    names = %w[agent-helm agent-compass]
    name = JSON.parse(File.read(File.join(local, '.claude-plugin/plugin.json'))).fetch('name')
    raise ArgumentError, 'Run from an Agent Helm or Agent Compass source checkout' unless names.include?(name)

    other_name = (names - [name]).fetch(0)
    other = File.expand_path(ARGV.first || "../#{other_name}", local)
    identity = JSON.parse(File.read(File.join(other, '.claude-plugin/plugin.json'))).fetch('name')
    raise ArgumentError, "Expected #{other_name} at #{other}" unless identity == other_name

    exact = %w[
      docs/standards/documentation.md
      docs/standards/readme.md
      docs/standards/project-description.md
      scripts/check_standards.rb
      scripts/test_standards.rb
    ]
    differences = exact.reject { |path| File.binread(File.join(local, path)) == File.binread(File.join(other, path)) }
    [
      ['docs/standards/mechanical-helper-audit.md', 'shared-helper-standard', true],
      ['AGENTS.md', 'shared-standards-maintenance', false]
    ].each do |path, marker, local_section|
      left = shared_block(local, path, marker, local_section: local_section)
      right = shared_block(other, path, marker, local_section: local_section)
      differences << "#{path} (shared block)" unless left == right
    end
    unless differences.empty?
      warn "Standards synchronization failed:\n#{differences.map { |path| "- #{path}" }.join("\n")}"
      exit 1
    end
    puts 'Shared standards synchronized: three identical standards, helper core, maintenance instructions and checker/tests.'
    puts 'Project-specific helper requirements still need review; this check compares text only.'
  rescue SystemCallError, IOError, JSON::ParserError, KeyError, ArgumentError => error
    warn "Standards synchronization unverified: #{error.message}"
    exit 2
  end
end
