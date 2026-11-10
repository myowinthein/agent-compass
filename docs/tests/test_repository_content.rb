require "jekyll"
require "tmpdir"
require "pathname"
require_relative "../_plugins/repository_content"
require_relative "../_plugins/asset_digest"

Dir.mktmpdir("repository-docs-") do |temporary|
  root = Pathname(temporary).realpath
  docs = root.join("docs")
  docs.join("commands").mkpath
  docs.join("setup").mkpath
  docs.join("images").mkpath
  root.join("assets").mkpath
  readme = "---\ntitle: Shared homepage\npermalink: /\n---\n# Shared homepage\n\nOne maintained source.\n"
  root.join("README.md").write(readme)
  root.join("assets/icon.svg").write('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
  root.join("private.md").write("Must not be published")
  docs.join("commands/example.md").write("---\ntitle: Example\n---\n# Example\n")
  docs.join("setup/index.md").write("---\ntitle: Setup\n---\n# Setup\n")
  docs.join("commands/details.md").write("---\npermalink: /docs/custom/detailed.html\n---\n# Details\n")
  docs.join("sitemap.xml").write("---\nlayout: null\n---\n<urlset></urlset>\n")
  docs.join("images/banner.jpg").binwrite("Fixture image")
  site = Jekyll::Site.new(Jekyll.configuration(
    "source" => docs.to_s, "destination" => docs.join("_site").to_s,
    "plugins_dir" => [], "quiet" => true, "disable_disk_cache" => true
  ))
  site.process
  expected = %w[index.html docs/commands/example.html docs/setup/index.html docs/custom/detailed.html sitemap.xml assets/icon.svg docs/images/banner.jpg]
  expected.each { |path| raise "Published path changed: #{path}" unless docs.join("_site", path).file? }
  raise "Private repository content leaked" if docs.join("_site/private.html").exist?
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
