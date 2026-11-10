require "pathname"

# Website sources live in docs/. Keep public paths and the two shared inputs
# stable without copying the plugin's instructions or GitHub README.
module RepositoryDocs
  class Image < Jekyll::StaticFile
    def url
      "/docs#{super}"
    end
  end

  def self.shared_file(root, relative)
    file = root.join(relative)
    unless file.file? && file.realpath == file
      raise ArgumentError, "Missing or redirected shared website input: #{relative}"
    end
    file
  end
end

Jekyll::Hooks.register :pages, :post_init do |page|
  next unless page.ext == ".md" && !page.data["permalink"]
  next unless File.file?(File.join(page.site.source, page.relative_path))

  relative = page.relative_path.sub(/\.md\z/, ".html").sub(/index\.html\z/, "")
  page.data["permalink"] = "/docs/#{relative}"
end

module RepositoryDocs
  class SharedContent < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      root = Pathname(site.source).realpath.parent
      readme = RepositoryDocs.shared_file(root, "README.md").read
      RepositoryDocs.shared_file(root, "assets/icon.svg")
      match = Jekyll::Document::YAML_FRONT_MATTER_REGEXP.match(readme)
      raise ArgumentError, "Shared README needs front matter" unless match

      homepage = Jekyll::PageWithoutAFile.new(site, site.source, "", "index.md")
      homepage.data.merge!(SafeYAML.load(match[1]))
      homepage.content = match.post_match
      site.pages << homepage
      site.static_files << Jekyll::StaticFile.new(site, root.to_s, "/assets", "icon.svg")
      site.static_files.map! do |asset|
        if asset.relative_path.start_with?("/images/")
          Image.new(site, site.source, File.dirname(asset.relative_path), asset.name)
        else
          asset
        end
      end
    end
  end
end
