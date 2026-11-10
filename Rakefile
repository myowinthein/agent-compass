require_relative "docs/tasks"

desc "Validate shared plugin entry points and packaged resources"
task :plugin_test do
  ruby "scripts/validate_plugin.rb"
  ruby "scripts/test_plugin.rb"
  ruby "scripts/test_salary_targets.rb"
  sh "python3 -B scripts/test_compass.py"
end

desc "Check native Claude and Codex command discovery with temporary installs"
task :client_test do
  ruby "scripts/check_clients.rb"
end

desc "Validate the shared plugin and documentation site"
task test: %i[plugin_test docs_test]

task default: :test
