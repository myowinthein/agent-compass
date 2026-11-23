require 'json'
require 'nokogiri'
require 'set'
require 'uri'
require 'yaml'

root = File.expand_path(ARGV.fetch(0, '../_site'), __dir__)
config = YAML.safe_load_file(File.expand_path('../_config.yml', __dir__))
base = config.fetch('url') + config.fetch('baseurl', '')
canonicals = []
titles = []

Dir.glob(File.join(root, '**/*.html')).each do |path|
  document = Nokogiri::HTML(File.read(path))
  next if document.at_css('meta[name="robots"]')&.[]('content').to_s.include?('noindex')

  relative = path.delete_prefix(root)
  title = document.at_css('title')&.text.to_s.strip
  description = document.at_css('meta[name="description"]')&.[]('content').to_s.strip
  canonical = document.at_css('link[rel="canonical"]')&.[]('href')
  raise "Missing or duplicated SEO metadata: #{relative}" if title.empty? || description.empty? || document.css('link[rel="canonical"]').size != 1
  raise "Canonical left the project site: #{relative}" unless canonical.start_with?(base + '/')
  raise "Sharing URL differs from the canonical: #{relative}" unless document.at_css('meta[property="og:url"]')&.[]('content') == canonical
  data = document.css('script[type="application/ld+json"]').map { |node| JSON.parse(node.text) }
  raise "Missing or inconsistent structured data: #{relative}" unless data.size == 1 && data.first['url'] == canonical
  image = document.at_css('meta[property="og:image"]')&.[]('content').to_s
  raise "Missing or unpublished sharing image: #{relative}" unless image.start_with?(base + '/') && File.file?(File.join(root, URI(image).path.delete_prefix(config.fetch('baseurl', '')).delete_prefix('/')))
  if relative.start_with?('/docs/legal/')
    raise "Legal page inherited the product description: #{relative}" if description == config.fetch('description')
  end
  if relative == '/index.html'
    raise 'Homepage search title lost its product identity or purpose' unless title == "#{config.fetch('title')} | #{config.fetch('tagline')}"
    raise 'Homepage sharing title remained Home' unless document.at_css('meta[property="og:title"]')&.[]('content') == config.fetch('title')
    raise 'Homepage navigation label changed' unless document.at_css('#site-nav a[href="' + config.fetch('baseurl', '') + '/"]')&.text&.strip == 'Home'
  end
  canonicals << canonical
  titles << title
end
raise 'No indexable pages were checked' if canonicals.empty?
raise 'Duplicate page titles or canonical URLs' unless titles.uniq == titles && canonicals.uniq == canonicals
sitemap = Nokogiri::XML(File.read(File.join(root, 'sitemap.xml'))) { |parser| parser.strict }
urls = sitemap.xpath('//*[local-name()="loc"]').map(&:text)
raise 'Sitemap differs from the indexable canonical pages' unless urls.uniq == urls && urls.to_set == canonicals.to_set
puts "Passed metadata, sharing, homepage identity and sitemap checks for #{canonicals.size} indexable pages."
