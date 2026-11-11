require "pathname"
require "yaml"

root = Pathname(__dir__).parent.parent.realpath
config = YAML.safe_load_file(root.join("docs/_config.yml"))
repository = config.fetch("baseurl").delete_prefix("/")
expected_count = { "agent-helm" => 19, "agent-compass" => 18 }.fetch(repository)
source_url = "https://github.com/myowinthein/#{repository}/blob/main/"

def document(path)
  match = path.read.match(/\A---\n(.*?)\n---\n(.*)\z/m)
  raise "Missing front matter: #{path}" unless match
  [YAML.safe_load(match[1]), match[2]]
end

pairs = root.glob("docs/**/*.md").filter_map do |path|
  next if path.to_s.include?("/_site/")
  data, = document(path) if path.read.start_with?("---\n")
  [path, data] if data && data["detailed"]
end
raise "Unexpected paired-guide inventory" unless pairs.size == expected_count
raise "Source-injection plugin must not return" if root.join("docs/_plugins/guide_content.rb").exist?

pairs.each do |overview, data|
  url = data.fetch("detailed")
  detail = root.join(url.delete_prefix("/").sub(/\.html\z/, ".md"))
  meta, body = document(detail)
  overview_url = data["permalink"] || "/#{overview.relative_path_from(root).sub_ext('.html')}"
  raise "Broken view pair: #{detail}" unless meta["overview"] == overview_url && meta["permalink"] == url
  raise "Details leaked into the menu: #{detail}" unless meta["nav_exclude"]
  raise "Duplicate title or selector: #{detail}" unless body.scan(/^# /).size == 1 && body.scan("{% include guide-depth.html %}").size == 1
  raise "Selector must follow the title: #{detail}" unless body.match?(/\A\s*# [^\n]+\n\n\{% include guide-depth\.html %\}/)
  raise "Legacy source embedding returned: #{detail}" if meta.key?("guide_source") || meta.key?("guide_sources") || body.match?(/\|\s*guide_(?:intro|body|full|section)\b|include_relative/)
  unexpected_includes = body.scan(/\{%\s*(?:include|include_relative)\s+([^%\s]+)/).flatten - ["guide-depth.html"]
  raise "Unexpected content include: #{detail}" unless unexpected_includes.empty?
  raise "Missing authored explanation: #{detail}" unless body.match?(/^## (?!Flow\b|Explore the source\b).+/)
  sources = meta.fetch("source_files")
  raise "Missing source references: #{detail}" unless sources.is_a?(Array) && !sources.empty?
  sources.each do |source|
    raise "Invalid reference source: #{source}" unless source.is_a?(String) && source.match?(%r{\A(?:guides|rules|workflows|prompts|skills|agents)/[a-z0-9/-]+\.md\z})
    file = root.join(source)
    raise "Missing or escaped source: #{source}" unless file.file? && file.realpath.to_s.start_with?("#{root}/")
    raise "Missing existing-source link: #{detail}: #{source}" unless body.include?("#{source_url}#{source}")
  end
end

puts "Passed #{pairs.size} authored guide pairs, source-reference boundaries and no raw-prompt rendering."
