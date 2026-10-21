desc "Validate shared plugin entry points and packaged resources"
task :plugin_test do
  ruby "scripts/validate_plugin.rb"
  ruby "scripts/test_plugin.rb"
  ruby "scripts/test_salary_targets.rb"
  sh "python3 -B scripts/test_compass.py"
end

desc "Build the Jekyll site and validate it with HTML-Proofer"
task :docs_test do
  sh "node --test scripts/test_theme_switcher.cjs"
  require "html-proofer"
  require "yaml"
  sh "bundle exec jekyll build"

  baseurl = YAML.safe_load_file("_config.yml").fetch("baseurl", "").to_s
  url_swaps = baseurl.empty? ? {} : { /\A#{Regexp.escape(baseurl)}\// => "/" }

  HTMLProofer.check_directory(
    "./_site",
    disable_external: true,
    swap_urls: url_swaps,
    checks: %w[Html Images Scripts Links]
  ).run
end

desc "Validate the shared plugin and documentation site"
task test: %i[plugin_test docs_test]

task default: :test
