require_relative "docs/tasks"

desc "Compare shared maintainer standards with the local sibling checkout (no network)"
task :standards_check do
  ruby "scripts/check_standards.rb"
end

desc "Test standards drift detection in disposable paired repositories"
task :standards_test do
  ruby "scripts/test_standards.rb"
end

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
task test: %i[standards_test plugin_test docs_test]

task default: :test
