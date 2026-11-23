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

  def self.lazy_search(source)
    source = replace_once(source, 'function initSearch() {', <<~JS.chomp)
      let compassSearchStarted = false;
      let compassSearchReady = false;
      let compassSearchFailedState = false;
      let compassSearchPendingTimer;
      let compassSearchErrorTimer;
      let compassSearchInput;
      let compassSearchStatus;
      let compassSearchRetry;
      function clearCompassSearchFeedback() {
        clearTimeout(compassSearchPendingTimer);
        clearTimeout(compassSearchErrorTimer);
        compassSearchStatus.textContent = '';
      }
      function compassSearchFailed() {
        clearCompassSearchFeedback();
        compassSearchFailedState = true;
        compassSearchInput.removeAttribute('aria-busy');
        compassSearchRetry.hidden = false;
        compassSearchRetry.disabled = false;
        compassSearchStatus.textContent = 'Search unavailable. Press Enter or select Retry search.';
        const dismiss = () => {
          if (document.activeElement === compassSearchStatus) compassSearchErrorTimer = setTimeout(dismiss, 500);
          else compassSearchStatus.textContent = '';
        };
        compassSearchErrorTimer = setTimeout(dismiss, 4000);
      }
      function initSearch(retry = false) {
        if (compassSearchStarted || (compassSearchFailedState && retry !== true)) return;
        compassSearchStarted = true;
        compassSearchFailedState = false;
        clearCompassSearchFeedback();
        compassSearchRetry.disabled = true;
        compassSearchInput.setAttribute('aria-busy', 'true');
        compassSearchPendingTimer = setTimeout(() => { compassSearchStatus.textContent = 'Loading search…'; }, 200);
    JS
    source = replace_once(source, '      var docs = JSON.parse(request.responseText);',
      "      try {\n      var docs = JSON.parse(request.responseText);")
    source = replace_once(source, '      searchLoaded(index, docs);', <<~JS.chomp)
            searchLoaded(index, docs);
            compassSearchReady = true;
            clearCompassSearchFeedback();
            compassSearchRetry.hidden = true;
            compassSearchInput.removeAttribute('aria-busy');
            const input = document.getElementById('search-input');
            if (document.activeElement === input) input.dispatchEvent(new Event("focus"));
            } catch {
              compassSearchStarted = false;
              compassSearchFailed();
            }
    JS
    source = replace_once(source,
      "      console.log('Error loading ajax request. Request status:' + request.status);",
      "      compassSearchStarted = false;\n      compassSearchFailed();\n      console.log('Error loading ajax request. Request status:' + request.status);")
    source = replace_once(source,
      "    console.log('There was a connection error');",
      "    compassSearchStarted = false;\n    compassSearchFailed();\n    console.log('There was a connection error');")
    source = replace_once(source, "  jtd.addEvent(searchInput, 'focus', function(){",
      "  searchInput.addEventListener('input', update);\n\n  jtd.addEvent(searchInput, 'focus', function(){")
    source = replace_once(source, '    const nextFocusedElement = evt.relatedTarget;',
      "    const nextFocusedElement = evt.relatedTarget;\n    if (!nextFocusedElement) { hideSearch(); return; }")
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
    view_box = REXML::Document.new(svg).root.attributes['viewBox'].to_s.split.map { |number| Float(number) }
    unless view_box.size == 4 && view_box.all?(&:finite?) && view_box[2..].all?(&:positive?)
      raise ArgumentError, 'Invalid Mermaid diagram dimensions'
    end
    view_box[2..]
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
      if html.include?('id="search-input"')
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
        width, height = dimensions(File.read(File.join(cache, "#{id}.svg")))
        label = CGI.escapeHTML("Workflow diagram for #{page.data['title']}")
        url = "#{site.baseurl}/assets/diagrams/#{id}.svg"
        viewer_url, anchor = diagram_viewer(site, page, diagram_index, url, width, height)
        %(<figure class="mermaid"><img src="#{url}" width="#{width.ceil}" height="#{height.ceil}" style="aspect-ratio: #{width} / #{height};" alt="#{label}" decoding="async"><figcaption><a id="#{anchor}" href="#{viewer_url}" data-diagram-full-size>View full-size diagram</a></figcaption></figure>)
      end
    end
    site.pages.select { |page| page.url == '/assets/js/just-the-docs.js' }.each do |page|
      page.output = lazy_search(page.output) unless site.config['search_enabled'] == false
      page.output = clipboard_feedback(page.output) unless site.config['enable_copy_code_button'] == false
    end
  end
end

Jekyll::Hooks.register :site, :post_render do |site|
  CompassFrontend.optimize(site)
end
