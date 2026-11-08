require "jekyll"
require "pathname"
require "tmpdir"
require_relative "../_plugins/asset_digest"

Dir.mktmpdir("compass-asset-digest-") do |temporary|
  root = Pathname(temporary)
  asset = root.join("assets/js/app.js")
  asset.parent.mkpath
  asset.write("console.log('first');\n")
  root.join("excluded.txt").write("Not a published asset")
  root.join("unpublished.js").write("Not published")
  config = Jekyll.configuration(
    "source" => temporary, "destination" => root.join("_site").to_s,
    "quiet" => true, "plugins_dir" => [], "exclude" => ["excluded.txt"],
    "defaults" => [{ "scope" => { "path" => "unpublished.js" }, "values" => { "published" => false } }]
  )
  site = Jekyll::Site.new(config)
  site.read
  render = lambda do |path|
    Liquid::Template.parse('{{ asset | asset_digest }}').render!({ "asset" => path }, registers: { site: site })
  end

  first = render.call("/assets/js/app.js")
  raise "Missing content digest" unless first.match?(/\A[0-9a-f]{16}\z/)
  raise "Unchanged asset changed its digest" unless render.call("/assets/js/app.js") == first

  timestamp = Time.at(1_700_000_000)
  File.utime(timestamp, timestamp, asset)
  raise "Timestamp changed the content digest" unless render.call("/assets/js/app.js") == first

  asset.write("console.log('second');\n")
  File.utime(timestamp, timestamp, asset)
  raise "Changed content retained its old digest" if render.call("/assets/js/app.js") == first

  %w[/excluded.txt /unpublished.js /missing.js /../excluded.txt].each do |path|
    rejected = false
    begin
      render.call(path)
    rescue Liquid::ArgumentError => error
      raise unless error.message.include?("Asset is not a published static file:")
      rejected = true
    end
    raise "Unpublished asset accepted: #{path}" unless rejected
  end
end

puts "Passed stable content digests, byte-change invalidation and unpublished-asset rejection."
