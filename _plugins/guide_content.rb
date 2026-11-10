require "kramdown"
require "kramdown-parser-gfm"
require "pathname"
require "uri"

# Render the authoritative instruction sources without putting site markup in
# the plugin. Only declared package instruction paths may supply guide content.
module CompassGuideContent
  SOURCE_URL = "https://github.com/myowinthein/agent-compass/blob/main/".freeze
  SOURCE_PATH = %r{\A(?:workflows/[a-z-]+|prompts/[a-z-]+/[a-z0-9-]+|skills/[a-z-]+)\.md\z}
  module_function

  def read_source(site, source)
    raise ArgumentError, "Unknown guide source: #{source}" unless source.is_a?(String) && SOURCE_PATH.match?(source)

    root = Pathname(site.source).realpath
    file = root.join(source)
    unless file.file? && file.realpath.to_s.start_with?("#{root}/")
      raise ArgumentError, "Guide source is missing or outside the project: #{source}"
    end
    file.read(encoding: "UTF-8").sub(/\A# [^\n]+\n+/, "")
  end

  def section(site, source, heading)
    markdown = read_source(site, source)
    sections = markdown.split(/(?=^## )/)
    matches = sections.select { |part| part.lines.first.to_s.strip == "## #{heading}" }
    raise ArgumentError, "Missing or ambiguous guide section: #{source}: #{heading}" unless matches.length == 1

    matches.first
  end

  def destination(site, source, href)
    return href if href.start_with?("#", "/") || URI.parse(href).scheme

    uri = URI.parse(href)
    target = Pathname(source).parent.join(URI::DEFAULT_PARSER.unescape(uri.path)).cleanpath.to_s
    raise ArgumentError, "Guide reference escapes the project: #{href}" if target.start_with?("../")

    pages = site.pages.select do |candidate|
      sources = [candidate.data["guide_source"], *Array(candidate.data["guide_sources"])]
      candidate.data["overview"] && sources.include?(target)
    end
    raise ArgumentError, "Multiple detailed guides own #{target}" if pages.length > 1

    path = pages.first ? "#{site.baseurl}#{pages.first.url}" : "#{SOURCE_URL}#{target}"
    path += "?#{uri.query}" if uri.query
    path += "##{uri.fragment}" if uri.fragment
    path
  end

  def render(site, source, markdown, contents: false)
    markdown = "**In this procedure**\n\n* Contents\n{:toc}\n\n#{markdown}" if contents && markdown.match?(/^## /)
    document = Kramdown::Document.new(markdown, input: "GFM", syntax_highlighter: "rouge", toc_levels: "2")
    document.root.children.shift while %i[hr blank].include?(document.root.children.first&.type)
    walk = lambda do |element|
      if element.type == :a && element.attr["href"]
        element.attr["href"] = destination(site, source, element.attr["href"])
      end
      element.children.each { |child| walk.call(child) }
    end
    walk.call(document.root)
    document.to_html
  end
end

module CompassGuideFilters
  def guide_full(source)
    site = @context.registers[:site]
    CompassGuideContent.render(site, source, CompassGuideContent.read_source(site, source), contents: true)
  end

  def guide_section(source, heading)
    site = @context.registers[:site]
    CompassGuideContent.render(site, source, CompassGuideContent.section(site, source, heading))
  end
end

Liquid::Template.register_filter(CompassGuideFilters)
