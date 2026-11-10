require "jekyll"
require "nokogiri"
require "pathname"
require "tmpdir"
require_relative "../_plugins/guide_content"

def check(condition, message)
  raise message unless condition
end

Dir.mktmpdir("compass-guide-content-") do |temporary|
  root = Pathname(temporary)
  root.join("docs").mkpath()
  root.join("workflows").mkpath
  original = <<~MARKDOWN
    # example

    Preserve the complete introduction.

    ## Review

    Keep all conditions. See [the step](../prompts/example/step1-review.md#result),
    [the rule](../skills/policy.md), [this section](#review) and [a standard](https://example.invalid/spec).

    ```markdown
    [Literal example](../unchanged.md)
    ```

    ## Result

    Preserve completed work and disclose the remaining gaps.
  MARKDOWN
  root.join("workflows/example.md").write(original)
  root.join("workflows/no-title.md").write("A prerequisite must not disappear.\n\n## Review\n\nKeep this body.\n")
  site = Jekyll::Site.new(Jekyll.configuration("source" => root.join("docs").to_s, "quiet" => true,
    "plugins_dir" => [], "baseurl" => "/compass"))
  page = Struct.new(:data, :url).new({ "guide_sources" => ["prompts/example/step1-review.md"],
    "overview" => "/overview.html" }, "/step/detailed.html")
  site.pages << page

  markdown = CompassGuideContent.read_source(site, "workflows/example.md")
  check(markdown.start_with?("Preserve the complete introduction."), "Source title was duplicated or introduction lost")
  html = CompassGuideContent.render(site, "workflows/example.md", markdown, contents: true)
  document = Nokogiri::HTML.fragment(html)
  links = document.css("a").to_h { |a| [a.text, a["href"]] }
  check(links["the step"] == "/compass/step/detailed.html#result", "Step reference did not use its Detailed page")
  check(links["the rule"] == "#{CompassGuideContent::SOURCE_URL}skills/policy.md", "Supporting source reference changed")
  check(links["this section"] == "#review" && links["a standard"] == "https://example.invalid/spec", "Absolute or same-page URL changed")
  check(document.at_css("#markdown-toc a[href='#result']"), "Procedure section navigation is missing")
  check(document.at_css("code").text.include?("[Literal example](../unchanged.md)"), "Code was treated as navigation")
  check(document.css("h1").empty? && document.css("h2").size == 2, "Source headings were lost or duplicated")
  check(CompassGuideContent.read_source(site, "workflows/no-title.md").start_with?("A prerequisite"), "Heading-free source lost its introduction")
  excerpt = CompassGuideContent.section(site, "workflows/example.md", "Review")
  check(excerpt.include?("Keep all conditions.") && !excerpt.include?("## Result"), "Section extraction lost its boundary")
  begin
    CompassGuideContent.section(site, "workflows/example.md", "Missing")
    raise "Accepted a missing section"
  rescue ArgumentError
    # A changed source must fail rather than silently omit its procedure.
  end
  check(root.join("workflows/example.md").read == original, "Rendering modified authoritative instructions")

  Dir.mktmpdir("compass-guide-outside-") do |elsewhere|
    outside = Pathname(elsewhere).join("outside.md")
    outside.write("Outside the package")
    root.join("workflows/escape.md").make_symlink(outside)
    %w[.helm/test-log.json ../outside.md workflows/missing.md workflows/escape.md].each do |source|
      begin
        CompassGuideContent.read_source(site, source)
        raise "Accepted unavailable or unauthorized source: #{source}"
      rescue ArgumentError
        # Sources are restricted to declared, contained instruction paths.
      end
    end
  end
  begin
    CompassGuideContent.destination(site, "workflows/example.md", "../../outside.md")
    raise "Accepted a reference escaping the project"
  rescue ArgumentError
    # Never turn an escaped local path into a web source reference.
  end
  site.pages << page.dup
  begin
    CompassGuideContent.destination(site, "workflows/example.md", "../prompts/example/step1-review.md")
    raise "Accepted competing Detailed owners"
  rescue ArgumentError
    # A canonical source has one complete human view.
  end
end

puts "Passed complete guide rendering, link mapping, literal code, section boundaries and source isolation."
