require "yaml"

# Both guide tests share this expected count and the Overview inventory.
module GuidePairs
  EXPECTED_COUNTS = { "agent-helm" => 19, "agent-compass" => 18 }.freeze

  # Returns [path, front matter] for each Overview page that names a Details view.
  def self.overviews(root)
    root.glob("docs/**/*.md").filter_map do |path|
      next if path.to_s.include?("/_site/")

      match = path.read.match(/\A---\n(.*?)\n---\n/m)
      data = match && YAML.safe_load(match[1])
      [path, data] if data && data["detailed"]
    end
  end
end
