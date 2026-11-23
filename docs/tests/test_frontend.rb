require 'jekyll'
require 'json'
require 'tmpdir'
require_relative '../_plugins/frontend'

html = '<head><link rel="stylesheet" href="/agent-compass/assets/css/just-the-docs-default.css"></head>'
optimized = CompassFrontend.initial_theme(html, '/agent-compass')
raise 'Default CSS still loads before theme selection' if optimized.match?(/<head><link rel="stylesheet"/)
raise 'No-JavaScript CSS fallback lost' unless optimized.include?('<noscript><link rel="stylesheet"')
raise 'Theme must block rendering until its CSS is ready' unless optimized.include?('blocking')
raise 'Non-theme HTML changed' unless CompassFrontend.initial_theme('<head></head>', '/agent-compass') == '<head></head>'

source = <<~'JS'
function initSearch() {
  var request = new XMLHttpRequest();
  request.open('GET', '/fixture/assets/js/search-data.json', true);
  request.onload = function(){
    if (request.status >= 200 && request.status < 400) {
      var docs = JSON.parse(request.responseText);
      lunr.tokenizer.separator = /[\s\-/]+/

      var index = lunr(function(){
        this.ref('id');
        this.field('title', { boost: 200 });
        this.field('content', { boost: 2 });
        this.field('relUrl');
        this.metadataWhitelist = ['position']

        for (var i in docs) {

          this.add({
            id: i,
            title: docs[i].title,
            content: docs[i].content,
            relUrl: docs[i].relUrl
          });
        }
      });

      searchLoaded(index, docs);
    }
  };
}
function searchLoaded(index, docs) {
  var currentInput;
  function update() {
    var input = searchInput.value;
    currentSearchIndex++;

    if (input === currentInput) return;
    currentInput = input;
    if (input === '') {
      return;
    }
    var results = index.query(function (query) {
      var tokens = lunr.tokenizer(input)
      query.term(tokens, {
        boost: 10
      });
      query.term(tokens, {
        wildcard: lunr.Query.wildcard.TRAILING
      });
    });

    if ((results.length == 0) && (input.length > 2)) {
      var tokens = lunr.tokenizer(input).filter(function(token, i) {
        return token.str.length < 20;
      })
      if (tokens.length > 0) {
        results = index.query(function (query) {
          query.term(tokens, {
            editDistance: Math.round(Math.sqrt(input.length / 2 - 1))
          });
        });
      }
    }

    if (results.length == 0) {
      searchResults.innerHTML = '';
    }
    function addResults(resultsList, results, start, batchSize, batchMillis, searchIndex) {}
  }
  jtd.addEvent(searchInput, 'focus', function(){
    setTimeout(update, 0);
  });
  const updateSearchFocus = function(evt) {
    const nextFocusedElement = evt.relatedTarget;
    if (nextFocusedElement.id === 'search-input') return;
    if (nextFocusedElement.classList.contains('search-result')) return;
    hideSearch();
  };
  jtd.addEvent(searchInput, 'keydown', function(e){
    switch (e.keyCode) {
      case 38:
        if (active) {
          if (active.parentElement.previousSibling) {
            previous.classList.add('active');
          }
        }
        return;
      case 40:
        if (active) {
          if (active.parentElement.nextSibling) {
            next.classList.add('active');
          }
        } else {
          if (next) {
            next.classList.add('active');
          }
        }
        return;
      case 13:
        return;
    }
  });

  jtd.addEvent(document, 'click', function(e){
    hideSearch();
  });
}
jtd.onReady(function(){
  initSearch();
});
JS
worker = nil
lazy = CompassFrontend.lazy_search(source) { |body| worker = body }
raise 'Search still starts before interaction' unless lazy.include?('addEventListener("focus", initSearch)')
raise 'Typing during worker initialization would be lost' unless lazy.include?("dispatchEvent(new Event('docs-search-ready'))")
raise 'Index/query work remained on the page thread' if lazy.include?('lunr(') || lazy.include?('lunr.tokenizer')
raise 'Worker did not retain the theme index/query rules' unless worker.include?('index = lunr(') && worker.include?('editDistance:') && worker.include?('metadataWhitelist')
begin
  CompassFrontend.lazy_search(source.sub('  initSearch();', '  startSearch();'))
  raise 'Unknown theme initialization accepted'
rescue ArgumentError => error
  raise unless error.message.include?('theme')
end

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 720"><text>Start</text></svg>'
raise 'Wrong diagram dimensions' unless CompassFrontend.dimensions(svg) == [480.0, 720.0]
begin
  CompassFrontend.dimensions('<svg viewBox="0 0 0 0"></svg>')
  raise 'Zero-sized diagram accepted'
rescue ArgumentError
end
Dir.mktmpdir('compass-diagram-cache-') do |directory|
  site = Struct.new(:cache_dir, :config).new(File.join(directory, 'custom-cache'), {})
  id = 'a' * 64
  diagrams = { id => 'graph TD; A-->B' }
  path = File.join(site.cache_dir, 'mermaid/assets/diagrams', "#{id}.svg")
  calls = 0
  failed = false
  invalid = false
  capture = Open3.method(:capture3)
  Open3.define_singleton_method(:capture3) do |*_, stdin_data:|
    calls += 1
    output = JSON.parse(stdin_data).transform_values { invalid ? '<not-svg viewBox="0 0 480 720"/>' : svg }
    [JSON.generate(output), 'Synthetic renderer failure', Struct.new(:success?).new(!failed)]
  end
  begin
    raise 'Cold cache did not render' unless CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams) == { id => svg } && calls == 1
    raise 'Configured cache directory ignored' unless File.read(path) == svg && !File.exist?(File.join(directory, '.jekyll-cache'))
    CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams)
    raise 'Warm cache called the renderer' unless calls == 1
    ['', '<svg', '<not-svg viewBox="0 0 480 720"/>', '<svg viewBox="0 0 480 720"/>'].each do |broken|
      File.write(path, broken)
      before = calls
      result = CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams)
      raise 'Invalid cache entry was not rebuilt' unless calls == before + 1 && result.fetch(id) == svg && File.read(path) == svg
    end
    rename = File.method(:rename)
    begin
      File.define_singleton_method(:rename) { |*_| raise Errno::EACCES, 'Synthetic cache write failure' }
      result = CompassFrontend.render_diagrams(site, 'fixture-worker', { 'b' * 64 => diagrams.fetch(id) })
      raise 'Cache failure discarded a rendered diagram' unless result.values == [svg]
      CompassFrontend.cache_diagram(path, svg.sub('Start', 'Changed'))
    ensure
      File.define_singleton_method(:rename, rename)
    end
    raise 'Failed atomic write damaged existing cache or left temporary files' unless File.read(path) == svg && Dir.children(File.dirname(path)) == ["#{id}.svg"]
    site.config['disable_disk_cache'] = true
    File.write(path, 'Opaque old cache')
    before = calls
    CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams)
    raise 'Disabled disk cache was reused or changed' unless calls == before + 1 && File.read(path) == 'Opaque old cache'
    site.cache_dir = File.join(directory, 'disabled-cache')
    CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams)
    raise 'Disabled disk cache created a directory' if File.exist?(site.cache_dir)
    site.config.clear
    [true, false].each do |renderer_failed|
      failed = renderer_failed
      invalid = !renderer_failed
      begin
        CompassFrontend.render_diagrams(site, 'fixture-worker', diagrams)
        raise 'Broken renderer output accepted'
      rescue ArgumentError
        raise if renderer_failed
      rescue RuntimeError => error
        raise unless renderer_failed && error.message.start_with?('Diagram rendering failed:')
      end
      raise 'Broken renderer output was cached' if File.exist?(site.cache_dir)
    end
  ensure
    Open3.define_singleton_method(:capture3, capture)
  end
end

asset_type = Struct.new(:url, :output, :output_ext)
style = asset_type.new('/assets/css/theme.css', 'body {color: black}', '.css')
index = asset_type.new('/assets/js/search-data.json', '{"title":"Before"}', '.json')
worker = asset_type.new('/assets/js/search-worker.js', 'self.onmessage = first', '.js')
loader = asset_type.new('/assets/js/just-the-docs.js', '', '.js')
page = asset_type.new('/guide.html', '', '.html')
site = Struct.new(:pages, :baseurl, :config).new([style, index, worker, loader, page], '/fixture', {})
render_versions = lambda do
  loader.output = "fetch('/fixture/assets/js/search-data.json'); new Worker('/fixture/assets/js/search-worker.js');"
  page.output = '<link href="/fixture/assets/css/theme.css"><script src="/fixture/assets/js/just-the-docs.js"></script>'
  CompassFrontend.version_assets(site)
  page.output.dup
end
original = render_versions.call
raise 'Asset content versions are unstable' unless render_versions.call == original
style.output += ' a {color: blue}'
changed_style = render_versions.call
raise 'Changed stylesheet retained its URL' if changed_style == original
loader_url = original[/src="([^"]+)"/, 1]
raise 'Unchanged loader was invalidated by unrelated CSS' unless changed_style.include?(loader_url)
index.output = '{"title":"After"}'
changed_index = render_versions.call
expected = Digest::SHA256.hexdigest(index.output)[0, 16]
raise 'Changed index did not update the loader request and HTML URL' unless loader.output.include?("search-data.json?v=#{expected}") && !changed_index.include?(loader_url)
raise 'HTML version does not match final loader bytes' unless changed_index.include?("just-the-docs.js?v=#{Digest::SHA256.hexdigest(loader.output)[0, 16]}")
worker.output = 'self.onmessage = changed'
changed_worker = render_versions.call
raise 'Changed worker did not invalidate its URL and loader' unless changed_worker != changed_index && loader.output.include?("search-worker.js?v=#{Digest::SHA256.hexdigest(worker.output)[0, 16]}")
site.baseurl = ''
loader.output = "fetch('/assets/js/search-data.json'); new Worker('/assets/js/search-worker.js');"
page.output = '<script src="/assets/js/just-the-docs.js"></script>'
CompassFrontend.version_assets(site)
raise 'Root preview lost content versions' unless loader.output.include?("/assets/js/search-data.json?v=#{expected}") && page.output.include?('/assets/js/just-the-docs.js?v=')

puts 'Passed initial-theme, lazy-search, diagram cache recovery/settings and generated-asset version checks.'
