require 'jekyll'
require 'json'
require_relative '../_plugins/frontend'

html = '<head><link rel="stylesheet" href="/agent-compass/assets/css/just-the-docs-default.css"></head>'
optimized = CompassFrontend.initial_theme(html, '/agent-compass')
raise 'Default CSS still loads before theme selection' if optimized.match?(/<head><link rel="stylesheet"/)
raise 'No-JavaScript CSS fallback lost' unless optimized.include?('<noscript><link rel="stylesheet"')
raise 'Theme must block rendering until its CSS is ready' unless optimized.include?('blocking')
raise 'Non-theme HTML changed' unless CompassFrontend.initial_theme('<head></head>', '/agent-compass') == '<head></head>'

source = <<~JS
  function initSearch() {
    var request = new XMLHttpRequest();
    request.onload = function(){
      if (request.status >= 200 && request.status < 400) {
        searchLoaded(index, docs);
      } else {
        console.log('Error loading ajax request. Request status:' + request.status);
      }
    };
    request.onerror = function(){
      console.log('There was a connection error');
    };
  }
  function searchLoaded(index, docs) {
    jtd.addEvent(searchInput, 'focus', function(){
      setTimeout(update, 0);
    });
    const updateSearchFocus = function(evt) {
      const nextFocusedElement = evt.relatedTarget;
      if (nextFocusedElement.id === 'search-input') return;
      if (nextFocusedElement.classList.contains('search-result')) return;
      hideSearch();
    };
  }
  jtd.onReady(function(){
    initSearch();
  });
JS
# The fixture retains the theme's actual indentation at each patch boundary.
source = source.sub('    searchLoaded(index, docs);', '      searchLoaded(index, docs);')
source = source.sub("    console.log('Error loading", "      console.log('Error loading")
source = source.sub("  console.log('There was", "    console.log('There was")
lazy = CompassFrontend.lazy_search(source)
raise 'Search still starts before interaction' unless lazy.include?('addEventListener("focus", initSearch)')
raise 'Typing during index loading would be lost' unless lazy.include?('dispatchEvent(new Event("focus"))')
raise 'Failed requests cannot be retried' unless lazy.scan('compassSearchStarted = false').size >= 3
begin
  CompassFrontend.lazy_search(source.sub('  initSearch();', '  startSearch();'))
  raise 'Unknown theme initialization accepted'
rescue ArgumentError => error
  raise unless error.message.include?('theme')
end

begin
  CompassFrontend.initial_theme(html + html, '/agent-compass')
  raise 'Duplicate theme stylesheet accepted'
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
puts 'Passed initial-theme, lazy-search contract and diagram sizing checks.'
