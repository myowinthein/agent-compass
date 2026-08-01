require "html-proofer"

desc "Build the Jekyll site and validate it with HTML-Proofer"
task :test do
  sh "bundle exec jekyll build"

  HTMLProofer.check_directory(
    "./_site",
    disable_external: true,
    checks: %w[Html Images Scripts Links],
    swap_urls: { %r{^/claude-compass} => "" }
  ).run
end

task default: :test
