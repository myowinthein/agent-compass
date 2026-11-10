require "jekyll"
require "nokogiri"
require "pathname"
require "yaml"
require_relative "../_plugins/guide_content"

root = Pathname(__dir__).parent.parent
base = YAML.safe_load_file(root.join("docs/_config.yml")).fetch("baseurl")
normal = ->(text) { text.gsub(/\s+/, " ").strip }
overviews = root.glob("docs/**/*.md").filter_map do |path|
  frontmatter = path.read.match(/\A---\n(.*?)\n---\n/m)
  data = frontmatter && YAML.safe_load(frontmatter[1])
  [path, data] if data && data["detailed"]
end
raise "Expected eighteen paired topics" unless overviews.size == 18

overviews.each do |source, data|
  detail_source = root.join(data.fetch("detailed").sub(%r{\A/}, "").sub(/\.html\z/, ".md"))
  detail_data = YAML.safe_load(detail_source.read.match(/\A---\n(.*?)\n---\n/m)[1])
  overview_url = data["permalink"] || "/#{source.relative_path_from(root).sub_ext('.html')}"
  raise "Detailed guide points to the wrong Overview: #{source}" unless detail_data["overview"] == overview_url
  raise "Detailed guide leaks into navigation: #{source}" unless detail_data["nav_exclude"]
  built_detail = nil
  [overview_url, data.fetch("detailed")].each do |url|
    document = Nokogiri::HTML(root.join("docs/_site", url.delete_prefix("/")).read)
    built_detail = document if url == data["detailed"]
    navigation = document.css("nav.guide-depth")
    raise "Missing or duplicate depth selector: #{url}" unless navigation.size == 1
    links = navigation.first.css("a")
    raise "Wrong view pair: #{url}" unless links.map { |a| a["href"] } == [base + overview_url, base + data["detailed"]]
    raise "Inconsistent labels: #{url}" unless links.map(&:text) == ["Overview", "Details"]
    raise "Forced new tab: #{url}" if links.any? { |a| a["target"] }
    current = links.select { |a| a["aria-current"] == "page" }
    raise "Wrong current view: #{url}" unless current.size == 1 && current.first["href"] == base + url
    raise "Duplicate title: #{url}" unless document.css("main h1").size == 1
    raise "Missing diagram: #{url}" unless document.at_css("code.language-mermaid")
    if url == data["detailed"]
      raise "Detailed sidebar activation missing: #{url}" unless document.at_css("script[data-overview-url='#{base + overview_url}']")
    end
  end
  sources = [detail_data["guide_source"], *Array(detail_data["guide_sources"])].compact
  raise "Detailed page has no canonical source: #{source}" if sources.empty?
  sources.each do |path|
    markdown = root.join(path).read.sub(/\A# [^\n]+\n+/, "")
    expected = Nokogiri::HTML.fragment(Kramdown::Document.new(markdown, input: "GFM").to_html).text
    unless normal.call(built_detail.at_css("main").text).include?(normal.call(expected))
      raise "Canonical procedure is incomplete: #{path}"
    end
  end
end

puts "Verified 18 pairs, 36 selectors, stable destinations and complete canonical procedures."
