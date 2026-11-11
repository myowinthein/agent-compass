require "jekyll"
require "nokogiri"
require "pathname"
require "yaml"

root = Pathname(__dir__).parent.parent
base = YAML.safe_load_file(root.join("docs/_config.yml")).fetch("baseurl")
overviews = root.glob("docs/**/*.md").filter_map do |path|
  frontmatter = path.read.match(/\A---\n(.*?)\n---\n/m)
  data = frontmatter && YAML.safe_load(frontmatter[1])
  [path, data] if data && data["detailed"]
end
repository = base.delete_prefix("/")
expected = { "agent-helm" => 19, "agent-compass" => 18 }.fetch(repository)
raise "Unexpected paired topic inventory" unless overviews.size == expected

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
    raise "Missing diagram: #{url}" if (url == data["detailed"] || repository == "agent-compass") && !document.at_css("code.language-mermaid")
    if url == data["detailed"]
      raise "Detailed sidebar activation missing: #{url}" unless document.at_css("script[data-overview-url='#{base + overview_url}']")
    end
  end
  explanation = built_detail.at_css("main").text
  raise "Details body or source navigation missing: #{source}" unless explanation.include?("Explore the source")
  raise "Unrendered source filter: #{source}" if explanation.match?(/guide_(?:intro|body|full|section)/)
end

puts "Verified #{expected} pairs, #{expected * 2} selectors, stable destinations and independently authored Details."
