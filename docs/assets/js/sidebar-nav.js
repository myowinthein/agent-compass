(() => {
  const navigation = document.getElementById('site-nav');
  if (!navigation) return;

  // Capture destinations before the theme removes the current page's href.
  const links = Array.from(navigation.querySelectorAll('a.nav-list-link[href]'),
    link => [link, link.getAttribute('href')]);

  const initialize = () => {
    links.forEach(([link, href]) => link.setAttribute('href', href));
    const rows = new Map();
    const synchronize = ({ button, link, item }) => {
      const expanded = String(item.classList.contains('active'));
      button.setAttribute('aria-expanded', expanded);
      link.setAttribute('aria-expanded', expanded);
    };

    navigation.querySelectorAll('.nav-list-expander').forEach((button, index) => {
      const item = button.parentElement;
      const link = item.querySelector(':scope > .nav-list-link');
      const submenu = item.querySelector(':scope > .nav-list');
      if (!link || !submenu) return;
      submenu.id ||= `compass-submenu-${index}`;
      button.tabIndex = -1;
      button.setAttribute('aria-controls', submenu.id);
      link.setAttribute('aria-controls', submenu.id);
      link.setAttribute('aria-keyshortcuts', 'ArrowLeft ArrowRight');
      const row = { button, link, item };
      rows.set(button, row);
      synchronize(row);

      link.addEventListener('keydown', event => {
        if (event.isComposing || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        const expand = event.key === 'ArrowRight';
        if (item.classList.contains('active') !== expand) button.click();
      });
    });

    // The theme's document handler toggles the submenu before this handler runs.
    document.addEventListener('click', event => {
      const row = rows.get(event.target.closest('.nav-list-expander'));
      if (row) synchronize(row);
    });
  };

  if (document.readyState === 'complete') initialize();
  else document.addEventListener('DOMContentLoaded', initialize, { once: true });
})();
