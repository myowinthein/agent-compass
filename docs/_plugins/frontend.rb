require 'cgi'
require 'digest'
require 'fileutils'
require 'json'
require 'open3'
require 'rexml/document'

module CompassFrontend
  DIAGRAM = %r{<pre><code class="language-mermaid">(.*?)</code></pre>}m

  def self.replace_once(source, before, after)
    unless source.scan(Regexp.new(Regexp.escape(before))).size == 1
      raise ArgumentError, "Just the Docs theme changed: expected one #{before.strip.inspect}"
    end
    source.sub(before, after)
  end

  def self.initial_theme(html, base)
    default = "#{base}/assets/css/just-the-docs-default.css"
    link = %(<link rel="stylesheet" href="#{default}">)
    return html unless html.include?(link)

    replace_once(html, link, <<~HTML)
      <script>
        (() => {
          const light = #{JSON.generate("#{base}/assets/css/just-the-docs-light.css")};
          const dark = #{JSON.generate("#{base}/assets/css/just-the-docs-dark.css")};
          let mode = 'system';
          try {
            const saved = localStorage.getItem('agent-compass-theme');
            if (['system', 'light', 'dark'].includes(saved)) mode = saved;
          } catch {}
          const theme = mode === 'system' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : mode;
          const stylesheet = document.createElement('link');
          stylesheet.id = 'compass-theme-stylesheet';
          stylesheet.rel = 'stylesheet';
          stylesheet.setAttribute('blocking', 'render');
          stylesheet.href = theme === 'dark' ? dark : light;
          stylesheet.addEventListener('error', () => {
            if (stylesheet.href !== new URL(light, document.baseURI).href) {
              stylesheet.href = light;
              document.documentElement.style.colorScheme = 'light';
            }
          });
          document.head.append(stylesheet);
          document.documentElement.style.colorScheme = theme;
        })();
      </script>
      <noscript><link rel="stylesheet" href="#{default}"></noscript>
    HTML
  end

  def self.lazy_search(source)
    source = replace_once(source, 'function initSearch() {', <<~JS.chomp)
      let compassSearchStarted = false;
      function initSearch() {
        if (compassSearchStarted) return;
        compassSearchStarted = true;
    JS
    source = replace_once(source, '      searchLoaded(index, docs);', <<~JS.chomp)
            searchLoaded(index, docs);
            const input = document.getElementById('search-input');
            if (document.activeElement === input) input.dispatchEvent(new Event("focus"));
    JS
    source = replace_once(source,
      "      console.log('Error loading ajax request. Request status:' + request.status);",
      "      compassSearchStarted = false;\n      console.log('Error loading ajax request. Request status:' + request.status);")
    source = replace_once(source,
      "    console.log('There was a connection error');",
      "    compassSearchStarted = false;\n    console.log('There was a connection error');")
    source = replace_once(source, "  jtd.addEvent(searchInput, 'focus', function(){",
      "  searchInput.addEventListener('input', update);\n\n  jtd.addEvent(searchInput, 'focus', function(){")
    shortcut = source.match(%r{  // add event listener on ctrl[^\n]*\n  jtd\.addEvent\(document, 'keydown',[\s\S]*?\n  \}\);})
    source = source.sub(shortcut[0], '') if shortcut
    replace_once(source, '  initSearch();', <<~JS.chomp)
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
          searchInput.addEventListener("focus", initSearch);
          searchInput.addEventListener("input", initSearch);
          const mainHeader = document.getElementById('main-header');
          #{shortcut && shortcut[0]}
          if (document.activeElement === searchInput || searchInput.value) initSearch();
        }
    JS
  end

  def self.dimensions(svg)
    view_box = REXML::Document.new(svg).root.attributes['viewBox'].to_s.split.map { |number| Float(number) }
    unless view_box.size == 4 && view_box.all?(&:finite?) && view_box[2..].all?(&:positive?)
      raise ArgumentError, 'Invalid Mermaid diagram dimensions'
    end
    view_box[2..]
  end

  def self.optimize(site)
    pages = site.pages.select { |page| page.output_ext == '.html' }
    worker = File.join(site.source, 'scripts/render-diagrams.mjs')
    renderer = File.read(worker) + File.read(File.join(site.source, 'package-lock.json'))
    diagrams = {}
    pages.each do |page|
      page.output.scan(DIAGRAM).each do |match|
        source = CGI.unescapeHTML(match.first)
        id = Digest::SHA256.hexdigest(renderer + source)
        diagrams[id] = source
      end
    end
    cache = File.join(site.source, '.jekyll-cache/mermaid/assets/diagrams')
    FileUtils.mkdir_p(cache) unless diagrams.empty?
    missing = diagrams.reject { |id, _| File.file?(File.join(cache, "#{id}.svg")) }
    unless missing.empty?
      output, error, status = Open3.capture3('node', worker, stdin_data: JSON.generate(missing))
      raise "Diagram rendering failed: #{error}" unless status.success?
      rendered = JSON.parse(output)
      raise 'Incomplete Mermaid render result' unless rendered.keys.sort == missing.keys.sort
      rendered.each do |id, svg|
        dimensions(svg)
        File.write(File.join(cache, "#{id}.svg"), svg)
      end
    end
    diagrams.each_key do |id|
      site.static_files << Jekyll::StaticFile.new(site, File.join(site.source, '.jekyll-cache/mermaid'), '/assets/diagrams', "#{id}.svg")
    end
    pages.each do |page|
      html = initial_theme(page.output, site.baseurl.to_s)
      page.output = html.gsub(DIAGRAM) do
        source = CGI.unescapeHTML(Regexp.last_match(1))
        id = Digest::SHA256.hexdigest(renderer + source)
        width, height = dimensions(File.read(File.join(cache, "#{id}.svg")))
        label = CGI.escapeHTML("Workflow diagram for #{page.data['title']}")
        %(<figure class="mermaid"><img src="#{site.baseurl}/assets/diagrams/#{id}.svg" width="#{width.ceil}" height="#{height.ceil}" style="aspect-ratio: #{width} / #{height};" alt="#{label}" decoding="async"></figure>)
      end
    end
    site.pages.select { |page| page.url == '/assets/js/just-the-docs.js' }.each do |page|
      page.output = lazy_search(page.output) unless site.config['search_enabled'] == false
    end
  end
end

Jekyll::Hooks.register :site, :post_render do |site|
  CompassFrontend.optimize(site)
end
