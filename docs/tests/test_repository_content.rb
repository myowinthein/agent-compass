require "jekyll"
require "tmpdir"
require "pathname"
require "nokogiri"
require_relative "../_plugins/repository_content"
require_relative "../_plugins/asset_digest"

Dir.mktmpdir("repository-docs-") do |temporary|
  root = Pathname(temporary).realpath
  docs = root.join("docs")
  docs.join("commands").mkpath
  docs.join("setup").mkpath
  docs.join("images").mkpath
  root.join("assets").mkpath
  root.join(".claude-plugin").mkpath
  root.join(".claude-plugin/plugin.json").write('{"version":"1.2.3"}')
  docs.join("_layouts").mkpath
  docs.join("_includes").mkpath
  docs.join("_includes/header_custom.html").write(File.read(File.expand_path('../_includes/header_custom.html', __dir__)))
  docs.join("_layouts/default.html").write('<head>{% seo %}</head><div class="site-header"><a href="/" class="site-title lh-tight">Fixture</a><button id="menu-button">Menu</button></div><div class="main-header">{% include header_custom.html %}</div>{{ content }}')
  readme = "---\nlayout: default\ntitle: Shared homepage\npermalink: /\n---\n# Shared homepage\n\nOne maintained source.\n"
  root.join("README.md").write(readme)
  root.join("assets/icon.svg").write('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
  root.join("private.md").write("Must not be published")
  docs.join("commands/example.md").write("---\nlayout: default\ntitle: Example\n---\n# Example\n")
  docs.join("setup/index.md").write("---\ntitle: Setup\n---\n# Setup\n")
  docs.join("commands/details.md").write("---\npermalink: /docs/custom/detailed.html\n---\n# Details\n")
  docs.join("sitemap.xml").write("---\nlayout: null\n---\n<urlset></urlset>\n")
  docs.join("images/banner.jpg").binwrite("Fixture image")
  site = Jekyll::Site.new(Jekyll.configuration(
    "source" => docs.to_s, "destination" => docs.join("_site").to_s,
    "plugins_dir" => [], "quiet" => true, "disable_disk_cache" => true,
    "title" => "Fixture", "tagline" => "Workflow documentation", "description" => "Fixture workflow documentation", "url" => "https://docs.example.invalid"
  ))
  site.process
  expected = %w[index.html docs/commands/example.html docs/setup/index.html docs/custom/detailed.html sitemap.xml assets/icon.svg docs/images/banner.jpg]
  expected.each { |path| raise "Published path changed: #{path}" unless docs.join("_site", path).file? }
  raise "Private repository content leaked" if docs.join("_site/private.html").exist?
  homepage = Nokogiri::HTML(docs.join("_site/index.html").read)
  raise "Homepage SEO still uses the navigation label" unless homepage.at_css('title').text == 'Fixture | Workflow documentation' && homepage.at_css('meta[property="og:title"]')['content'] == 'Fixture'
  raise "Duplicate README page" if docs.join("_site/README.html").exist?
  raise "README content lost" unless docs.join("_site/index.html").read.include?("One maintained source.")
  raise "Source README was changed" unless root.join("README.md").read == readme
  raise "Shared icon bytes changed" unless docs.join("_site/assets/icon.svg").binread == root.join("assets/icon.svg").binread
  raise "Banner bytes changed" unless docs.join("_site/docs/images/banner.jpg").binread == docs.join("images/banner.jpg").binread
  digest = Liquid::Template.parse("{{ '/docs/images/banner.jpg' | asset_digest }}").render!({}, registers: { site: site })
  raise "Legacy image URL has no digest" unless digest.match?(/\A[0-9a-f]{16}\z/)
  begin
    Liquid::Template.parse("{{ '/images/banner.jpg' | asset_digest }}").render!({}, registers: { site: site })
    raise "Accepted an unpublished image URL"
  rescue Liquid::ArgumentError
    # The source-relative path is not a public URL after migration.
  end
  rendered = docs.join("_site/docs/commands/example.html").read
  document = Nokogiri::HTML(rendered)
  header = document.at_css('.site-header')
  home = header&.at_css('a.site-title')
  release = document.at_css('.main-header .header-controls a.site-version')
  raise "Title must retain its homepage destination" unless home && home['href'] == '/' && home.text.strip == 'Fixture'
  raise "Version must follow the theme chooser as a separate release link" unless release && release.previous_element&.at_css('#theme-mode') && release['href'] == 'https://github.com/myowinthein/agent-compass/releases/tag/v1.2.3' && release.text == 'v1.2.3'
  raise "Version must not remain in the sidebar title" if header.at_css('.site-version')
  raise "Release must use the current tab" if release['target']
  raise "Release needs a meaningful accessible name" unless release['aria-label'] == 'Release v1.2.3 on GitHub'
  raise "Menu button must remain outside the title link" if home.at_css('#menu-button')
  root.join(".claude-plugin/plugin.json").write('{"version":"1.2.4"}')
  site.process
  updated = Nokogiri::HTML(docs.join("_site/docs/commands/example.html").read).at_css('.site-version')
  raise "Version and release did not follow the manifest" unless updated.text == 'v1.2.4' && updated['href'].end_with?('/releases/tag/v1.2.4')
  root.join(".claude-plugin/plugin.json").write('{"version":"1.2<3"}')
  site.process
  escaped = Nokogiri::HTML(docs.join("_site/docs/commands/example.html").read).at_css('.site-version')
  raise "Version label or release path was not escaped" unless escaped.text == 'v1.2<3' && escaped['href'].end_with?('/releases/tag/v1.2%3C3')
  root.join("README.md").unlink
  root.join("README.md").make_symlink(root.join("private.md"))
  begin
    RepositoryDocs.shared_file(root, "README.md")
    raise "Accepted redirected shared input"
  rescue ArgumentError
    # A shared input cannot redirect the build to a different repository file.
  end
end
puts "Passed docs-root builds, stable public paths, shared homepage/icon bytes and redirected-input rejection."
