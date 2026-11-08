require "digest"

module CompassAssetFilters
  def asset_digest(path)
    site = @context.registers[:site]
    asset = site.static_files.find { |file| file.relative_path == path }
    raise ArgumentError, "Asset is not a published static file: #{path}" unless asset && asset.write?

    Digest::SHA256.file(asset.path).hexdigest[0, 16]
  end
end

Liquid::Template.register_filter(CompassAssetFilters)
