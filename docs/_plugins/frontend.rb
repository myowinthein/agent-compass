require 'cgi'
require 'digest'
require 'fileutils'
require 'json'
require 'open3'
require 'rexml/document'
require 'tempfile'

module CompassFrontend
  DIAGRAM = %r{<pre><code class="language-mermaid">(.*?)</code></pre>}m

  def self.replace_once(source, before, after)
    unless source.scan(Regexp.new(Regexp.escape(before))).size == 1
      raise ArgumentError, "Just the Docs theme changed: expected one #{before.strip.inspect}"
    end
    source.sub(before) { after }
  end

  def self.initial_theme(html, base, viewer: false)
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
          if (#{viewer} && /^#theme-(light|dark)$/.test(location.hash)) {
            mode = location.hash.slice(7);
          }
          const theme = mode === 'system' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : mode;
          const stylesheet = document.createElement('link');
          stylesheet.id = 'compass-theme-stylesheet';
          stylesheet.rel = 'stylesheet';
          stylesheet.setAttribute('blocking', 'render');
          stylesheet.dataset.lightHref = light;
          stylesheet.dataset.darkHref = dark;
          stylesheet.href = theme === 'dark' ? dark : light;
          stylesheet.addEventListener('error', () => {
            stylesheet.dataset.themeLoadFailed = 'true';
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

  def self.lazy_search(source, library_url: nil)
    init = source.match(/function initSearch\(\) \{.*?(?=function searchLoaded\(index, docs\) \{)/m)&.to_s
    index_rules = init&.match(/      lunr\.tokenizer\.separator =.*?(?=      searchLoaded\(index, docs\);)/m)&.to_s
    query_rules = source.match(/    var results = index\.query\(function \(query\) \{.*?(?=    if \(results.length == 0\) \{)/m)&.to_s
    index_url = init&.match(/request\.open\('GET', '([^']+)', true\);/)&.[](1)
    unless init && index_rules && query_rules && index_url&.end_with?('/search-data.json')
      raise ArgumentError, 'Just the Docs theme changed: missing search initialization or query rules'
    end
    worker_url = index_url.sub(/search-data\.json\z/, 'search-worker.js')
    library_url ||= index_url.sub(/search-data\.json\z/, 'vendor/lunr.min.js')
    worker = File.read(File.expand_path('../_includes/search-worker.js', __dir__))
    worker = replace_once(worker, '/* INDEX_RULES */', replace_once(index_rules, 'var index = lunr(', 'index = lunr('))
    worker = replace_once(worker, '/* QUERY_RULES */', query_rules)
    client = File.read(File.expand_path('../_includes/search-client.js', __dir__))
    { '"/* WORKER_URL */"' => worker_url, '"/* LIBRARY_URL */"' => library_url, '"/* INDEX_URL */"' => index_url }.each do |marker, url|
      client = replace_once(client, marker, JSON.generate(url))
    end
    source = source.sub(init) { client + "\n\n" }
    source = replace_once(source, query_rules, <<~JS)
        var searchIndex = currentSearchIndex;
        index.search(input).then(function(reply) {
          if (searchIndex !== currentSearchIndex) return;
          var results = reply.results;
          docs = reply.docs;
    JS
    source = replace_once(source, '    function addResults(resultsList, results, start, batchSize, batchMillis, searchIndex) {', <<~JS.chomp)
        }).catch(function() {
          if (searchIndex !== currentSearchIndex) return;
          currentInput = undefined;
          searchResults.innerHTML = '';
        });

        function addResults(resultsList, results, start, batchSize, batchMillis, searchIndex) {
    JS
    source = replace_once(source, "    if (input === '') {\n      return;\n    }",
      "    if (input === '' || !compassSearchReady) {\n      return;\n    }")
    source = replace_once(source, '  var currentInput;', <<~JS.chomp)
        var currentInput;
        searchInput.addEventListener('docs-search-ready', function() {
          currentInput = undefined;
          update();
        });
    JS
    source = replace_once(source, "  jtd.addEvent(searchInput, 'focus', function(){",
      "  searchInput.addEventListener('input', update);\n\n  jtd.addEvent(searchInput, 'focus', function(){")
    source = replace_once(source, '    const nextFocusedElement = evt.relatedTarget;',
      "    const nextFocusedElement = evt.relatedTarget;\n    if (!nextFocusedElement) { hideSearch(); return; }")
    # Focus and repeated input events must not cancel unchanged result batches.
    source = replace_once(source, "    currentSearchIndex++;\n\n", '')
    source = replace_once(source, '    currentInput = input;',
      "    currentInput = input;\n    currentSearchIndex++;")
    source = replace_once(source, "  jtd.addEvent(searchInput, 'keydown', function(e){", <<~JS.chomp)
        function focusSearchResult(result) {
          result.focus({ preventScroll: true });
          result.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'instant' });
        }
        function handleSearchKeydown(e) {
          if (e.isComposing) return;
    JS
    source = replace_once(source, "            previous.classList.add('active');",
      "            previous.classList.add('active');\n            focusSearchResult(previous);")
    next_selection = "            next.classList.add('active');"
    unless source.scan(Regexp.new(Regexp.escape(next_selection))).size == 2
      raise ArgumentError, 'Just the Docs theme changed: expected two next-result selections'
    end
    source = source.gsub(next_selection, "#{next_selection}\n            focusSearchResult(next);")
    previous_selection = "            previous.classList.add('active');\n            focusSearchResult(previous);\n          }"
    source = replace_once(source, previous_selection,
      "#{previous_selection} else {\n            searchInput.focus();\n          }")
    keyboard_end = "        return;\n    }\n  });\n\n  jtd.addEvent(document, 'click', function(e){"
    source = replace_once(source, keyboard_end, <<~JS.chomp)
              return;
            case 27:
              e.preventDefault();
              searchInput.value = '';
              update();
              searchInput.focus();
              return;
          }
        }
        searchInput.addEventListener('keydown', handleSearchKeydown);
        searchResults.addEventListener('keydown', handleSearchKeydown);
        searchResults.addEventListener('focusin', event => {
          const result = event.target.closest('a.search-result');
          if (!result) return;
          const active = searchResults.querySelector('.search-result.active');
          if (active) active.classList.remove('active');
          result.classList.add('active');
        });

        jtd.addEvent(document, 'click', function(e){
    JS
    shortcut = source.match(%r{  // add event listener on ctrl[^\n]*\n  jtd\.addEvent\(document, 'keydown',[\s\S]*?\n  \}\);})
    source = source.sub(shortcut[0], '') if shortcut
    source = replace_once(source, '  initSearch();', <<~JS.chomp)
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
          compassSearchInput = searchInput;
          compassSearchStatus = document.getElementById('search-status');
          compassSearchRetry = document.getElementById('search-retry');
          const search = searchInput.closest('.search');
          // Keep the search field and recovery reachable before the index is ready.
          const showSearchShell = () => {
            if (!compassSearchReady) document.documentElement.classList.add('search-active');
          };
          search.addEventListener('focusin', showSearchShell);
          search.addEventListener('focusout', event => {
            if (!compassSearchReady && !search.contains(event.relatedTarget)) document.documentElement.classList.remove('search-active');
          });
          document.addEventListener('click', event => {
            if (!compassSearchReady && !search.contains(event.target)) document.documentElement.classList.remove('search-active');
          });
          searchInput.addEventListener("focus", initSearch);
          searchInput.addEventListener("input", () => {
            showSearchShell();
            if (!compassSearchFailedState) initSearch();
          });
          search.addEventListener("keydown", event => {
            if (event.key === 'Escape' && !compassSearchReady) {
              event.preventDefault();
              searchInput.value = '';
              clearCompassSearchFeedback();
              searchInput.focus();
              document.documentElement.classList.remove('search-active');
              searchInput.scrollIntoView({ block: 'nearest' });
            }
          });
          searchInput.addEventListener("keydown", event => {
            if (event.key === 'Enter' && !event.isComposing && !event.repeat && compassSearchFailedState) {
              event.preventDefault();
              initSearch(true);
            }
          });
          compassSearchRetry.addEventListener("click", () => {
            initSearch(true);
            searchInput.focus();
          });
          const mainHeader = document.getElementById('main-header');
          #{shortcut && shortcut[0]}
          if (document.activeElement === searchInput || searchInput.value) initSearch();
        }
    JS
    yield worker if block_given?
    source
  end

  def self.clipboard_feedback(source)
    source = replace_once(source, '  codeBlocks.forEach(codeBlock => {',
      "  let clearCopyConfirmation = null;\n  let clearCopyFailure = null;\n  codeBlocks.forEach(codeBlock => {")
    source = replace_once(source, "    copyButton.addEventListener('click', function () {", <<~JS.chomp)
          const feedback = document.createElement('span');
          feedback.className = 'interaction-feedback copy-status';
          feedback.setAttribute('role', 'status');
          codeBlock.append(feedback);
          let copying = false;
          const resetConfirmation = () => {
            clearTimeout(timeout);
            timeout = null;
            copyButton.innerHTML = svgCopy;
            feedback.textContent = '';
            if (clearCopyConfirmation === resetConfirmation) clearCopyConfirmation = null;
            if (clearCopyFailure === resetConfirmation) clearCopyFailure = null;
          };
          const dismissConfirmation = () => {
            if (document.activeElement === feedback) timeout = setTimeout(dismissConfirmation, 500);
            else resetConfirmation();
          };
          copyButton.addEventListener('click', async function () {
    JS
    source = replace_once(source, '      if(timeout === null) {', <<~JS.chomp)
            if (!copying) {
              if (clearCopyFailure) clearCopyFailure();
              clearTimeout(timeout);
              if (clearCopyConfirmation === resetConfirmation) clearCopyConfirmation = null;
              copying = true;
              copyButton.setAttribute('aria-busy', 'true');
              copyButton.setAttribute('aria-disabled', 'true');
              const pendingFeedback = setTimeout(() => {
                copyButton.innerHTML = svgCopy;
                feedback.textContent = 'Copying…';
              }, 200);
              try {
    JS
    source = replace_once(source, '        window.navigator.clipboard.writeText(code);',
      '        await window.navigator.clipboard.writeText(code);')
    source = replace_once(source, '        copyButton.innerHTML = svgCopied;', <<~JS.chomp)
            if (clearCopyConfirmation) clearCopyConfirmation();
            if (clearCopyFailure) clearCopyFailure();
            clearCopyConfirmation = resetConfirmation;
            copyButton.innerHTML = svgCopied;
            feedback.textContent = 'Copied';
    JS
    source = replace_once(source, '        var timeoutSetting = 4000;', '        var timeoutSetting = 2000;')
    replace_once(source, "        timeout = setTimeout(function () {\n          copyButton.innerHTML = svgCopy;\n          timeout = null;\n        }, timeoutSetting);", <<~JS.chomp)
              timeout = setTimeout(dismissConfirmation, timeoutSetting);
              } catch {
                if (clearCopyFailure) clearCopyFailure();
                clearCopyFailure = resetConfirmation;
                copyButton.innerHTML = svgCopy;
                feedback.textContent = 'Could not copy. Try again or select the code to copy it manually.';
                timeout = setTimeout(dismissConfirmation, 4000);
              } finally {
                clearTimeout(pendingFeedback);
                copying = false;
                copyButton.removeAttribute('aria-busy');
                copyButton.removeAttribute('aria-disabled');
              }
    JS
  end

  def self.dimensions(svg)
    raise ArgumentError, 'Invalid Mermaid diagram SVG' unless svg.is_a?(String)

    root = REXML::Document.new(svg).root
    raise ArgumentError, 'Invalid Mermaid diagram SVG' unless root && root.name == 'svg' && root.namespace == 'http://www.w3.org/2000/svg'

    view_box = root.attributes['viewBox'].to_s.split.map { |number| Float(number) }
    unless view_box.size == 4 && view_box.all?(&:finite?) && view_box[2..].all?(&:positive?)
      raise ArgumentError, 'Invalid Mermaid diagram dimensions'
    end
    view_box[2..]
  rescue REXML::ParseException
    raise ArgumentError, 'Invalid Mermaid diagram SVG', cause: nil
  end

  def self.cached_diagram(path)
    svg = File.read(path)
    dimensions(svg)
    svg
  rescue SystemCallError, IOError, ArgumentError
    nil
  end

  def self.cache_diagram(path, svg)
    FileUtils.mkdir_p(File.dirname(path))
    Tempfile.create(['.mermaid-', '.tmp'], File.dirname(path)) do |file|
      file.write(svg)
      file.close
      File.rename(file.path, path)
    end
  rescue SystemCallError, IOError => error
    Jekyll.logger.warn 'Mermaid cache:', "Could not save #{File.basename(path)} (#{error.class}); using rendered diagram."
  end

  def self.render_diagrams(site, worker, diagrams)
    cache = File.join(site.cache_dir, 'mermaid/assets/diagrams') unless site.config['disable_disk_cache'] || site.config['safe']
    rendered = {}
    diagrams.each_key do |id|
      svg = cached_diagram(File.join(cache, "#{id}.svg")) if cache
      rendered[id] = svg if svg
    end
    missing = diagrams.reject { |id, _| rendered.key?(id) }
    unless missing.empty?
      output, error, status = Open3.capture3('node', worker, stdin_data: JSON.generate(missing))
      raise "Diagram rendering failed: #{error}" unless status.success?
      fresh = JSON.parse(output)
      raise 'Incomplete Mermaid render result' unless fresh.is_a?(Hash) && fresh.keys.sort == missing.keys.sort

      fresh.each_value { |svg| dimensions(svg) }
      fresh.each do |id, svg|
        cache_diagram(File.join(cache, "#{id}.svg"), svg) if cache
        rendered[id] = svg
      end
    end
    rendered
  end

  def self.versioned_asset_url(base, asset)
    "#{base}#{asset.url}?v=#{Digest::SHA256.hexdigest(asset.output)[0, 16]}"
  end

  def self.version_assets(site)
    assets = site.pages.select { |page| page.url.start_with?('/assets/') && page.url.match?(/\.(?:css|js|json)\z/) }
    loader = assets.find { |page| page.url == '/assets/js/just-the-docs.js' }
    if loader && site.config['search_enabled'] != false
      index = assets.find { |page| page.url == '/assets/js/search-data.json' }
      raise 'Missing generated search index' unless index

      loader.output = replace_once(loader.output, "#{site.baseurl}#{index.url}", versioned_asset_url(site.baseurl, index))
      worker = assets.find { |page| page.url == '/assets/js/search-worker.js' }
      if worker
        loader.output = replace_once(loader.output, "#{site.baseurl}#{worker.url}", versioned_asset_url(site.baseurl, worker))
      end
    end
    urls = assets.to_h { |asset| ["#{site.baseurl}#{asset.url}", versioned_asset_url(site.baseurl, asset)] }
    return if urls.empty?

    references = /(?:#{Regexp.union(urls.keys)})(?=["'\s<>])/
    site.pages.select { |page| page.output_ext == '.html' }.each do |page|
      page.output = page.output.gsub(references) { |url| urls.fetch(url) }
    end
  end

  def self.diagram_viewer(site, guide, index, image_url, width, height)
    anchor = "compass-diagram-#{index}"
    name = "#{Digest::SHA256.hexdigest("#{guide.url}##{anchor}")[0, 16]}.html"
    viewer = Jekyll::PageWithoutAFile.new(site, site.source, 'diagrams', name)
    viewer.data.merge!(
      'layout' => 'diagram', 'nav_exclude' => true, 'search_exclude' => true,
      'sitemap' => false, 'title' => "#{guide.data['title']}: diagram #{index}",
      'guide_url' => "#{site.baseurl}#{guide.url}##{anchor}",
      'diagram_url' => image_url, 'diagram_width' => width, 'diagram_height' => height
    )
    viewer.output = initial_theme(viewer.renderer.run, site.baseurl.to_s, viewer: true)
    site.pages << viewer
    ["#{site.baseurl}#{viewer.url}", anchor]
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
    rendered = render_diagrams(site, worker, diagrams)
    rendered.each do |id, svg|
      asset = Jekyll::PageWithoutAFile.new(site, site.source, 'assets/diagrams', "#{id}.svg")
      asset.data.merge!('layout' => nil, 'sitemap' => false)
      asset.output = svg
      site.pages << asset
    end
    pages.each do |page|
      html = initial_theme(page.output, site.baseurl.to_s)
      if html.include?('id="search-input"')
        html = replace_once(html, %(<script src="#{site.baseurl}/assets/js/vendor/lunr.min.js"></script>), '')
        html = replace_once(html, '<div id="search-results" class="search-results"></div>',
          '<p id="search-status" class="interaction-feedback search-status" role="status"></p><div id="search-results" class="search-results"></div>')
        html = replace_once(html, 'id="search-input"', 'id="search-input" aria-describedby="search-status"')
        label = html.match(%r{<label for="search-input" class="search-label">.*?</label>}m)&.to_s
        raise ArgumentError, 'Just the Docs theme changed: missing search label' unless label
        html = replace_once(html, label,
          label + '<button id="search-retry" class="search-retry" type="button" aria-label="Search unavailable. Retry search." title="Search unavailable" hidden>Retry search</button>')
      end
      diagram_index = 0
      page.output = html.gsub(DIAGRAM) do
        diagram_index += 1
        source = CGI.unescapeHTML(Regexp.last_match(1))
        id = Digest::SHA256.hexdigest(renderer + source)
        width, height = dimensions(rendered.fetch(id))
        label = CGI.escapeHTML("Workflow diagram for #{page.data['title']}")
        url = "#{site.baseurl}/assets/diagrams/#{id}.svg"
        viewer_url, anchor = diagram_viewer(site, page, diagram_index, url, width, height)
        %(<figure class="mermaid"><img src="#{url}" width="#{width.ceil}" height="#{height.ceil}" style="aspect-ratio: #{width} / #{height};" alt="#{label}" decoding="async"><figcaption><a id="#{anchor}" href="#{viewer_url}" data-diagram-full-size>View full-size diagram</a></figcaption></figure>)
      end
    end
    site.pages.select { |page| page.url == '/assets/js/just-the-docs.js' }.each do |page|
      unless site.config['search_enabled'] == false
        library = site.static_files.find { |asset| asset.url == '/assets/js/vendor/lunr.min.js' }
        raise ArgumentError, 'Just the Docs theme changed: missing Lunr library' unless library

        library_url = "#{site.baseurl}#{library.url}?v=#{Digest::SHA256.file(library.path).hexdigest[0, 16]}"
        page.output = lazy_search(page.output, library_url: library_url) do |body|
          asset = Jekyll::PageWithoutAFile.new(site, site.source, 'assets/js', 'search-worker.js')
          asset.data.merge!('layout' => nil, 'sitemap' => false)
          asset.output = body
          site.pages << asset
        end
      end
      page.output = clipboard_feedback(page.output) unless site.config['enable_copy_code_button'] == false
    end
    version_assets(site)
  end
end

Jekyll::Hooks.register :site, :post_render do |site|
  CompassFrontend.optimize(site)
end
