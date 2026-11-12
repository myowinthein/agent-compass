desc "Build the Jekyll site and validate it with HTML-Proofer"
task :docs_test do
  ruby "docs/tests/test_repository_content.rb"
  ruby "docs/tests/test_asset_digest.rb"
  ruby "docs/tests/test_frontend.rb"
  ruby "docs/tests/test_human_guides.rb"
  sh "node --test docs/tests/test_theme_switcher.cjs"
  sh "node --test docs/tests/test_setup_tabs.cjs"
  require "html-proofer"
  require "yaml"
  Dir.chdir("docs") { sh "bundle exec jekyll build" }
  ruby "docs/tests/test_guide_views.rb"
  sh "node --test docs/tests/test_setup_redirects.cjs"
  sh "node --test docs/tests/test_site_navigation.cjs"
  sh "node docs/tests/browser_frontend.mjs"

  baseurl = YAML.safe_load_file("docs/_config.yml").fetch("baseurl", "").to_s
  url_swaps = baseurl.empty? ? {} : { /\A#{Regexp.escape(baseurl)}\// => "/" }

  HTMLProofer.check_directory(
    "./docs/_site",
    disable_external: true,
    swap_urls: url_swaps,
    checks: %w[Html Images Scripts Links]
  ).run
end
