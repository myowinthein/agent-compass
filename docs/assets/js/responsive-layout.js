(() => {
  const initialize = () => {
    const root = document.documentElement;
    const navigation = document.getElementById('site-nav');
    const header = document.getElementById('main-header');
    const menu = document.getElementById('menu-button');
    const title = document.querySelector('.site-title');
    if (!navigation || !header || !menu || !title) return;

    const desktop = matchMedia('(min-width: 50rem)');
    const updateLayout = () => {
      // Media-query rems use the browser default, not an enlarged page font.
      const compact = !desktop.matches || innerWidth < 50 * parseFloat(getComputedStyle(root).fontSize);
      const wasCompact = root.classList.contains('compass-compact');
      const focused = document.activeElement;
      root.classList.toggle('compass-compact', compact);
      if (compact && !wasCompact && (navigation.contains(focused) || header.contains(focused))) {
        // Keep focused controls visible without a click dismissing active search.
        [menu, navigation, header].forEach(element => element.classList.add('nav-open'));
        menu.setAttribute('aria-expanded', 'true');
      }
      if (!compact && wasCompact && focused === menu) title.focus({ preventScroll: true });
    };

    updateLayout();
    window.addEventListener('resize', updateLayout);
    desktop.addEventListener('change', updateLayout);
    new ResizeObserver(updateLayout).observe(document.querySelector('.site-header'));
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
