desc "Validate shared plugin entry points and packaged resources"
task :plugin_test do
  ruby "scripts/validate_plugin.rb"
end

desc "Build the Jekyll site and validate it with HTML-Proofer"
task :docs_test do
  require "html-proofer"
  sh "bundle exec jekyll build"

  HTMLProofer.check_directory(
    "./_site",
    disable_external: true,
    checks: %w[Html Images Scripts Links]
  ).run
end

desc "Validate the shared plugin and documentation site"
task test: %i[plugin_test docs_test]

task default: :test
