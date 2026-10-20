(() => {
  const updateLinks = () => {
    document.querySelectorAll('a[href]').forEach(link => {
      if (!['http:', 'https:'].includes(link.protocol)) return;
      if (link.getAttribute('href').startsWith('#')) return;
      if (
        link.hash &&
        link.origin === window.location.origin &&
        link.pathname === window.location.pathname &&
        link.search === window.location.search
      ) return;

      link.target = '_blank';
      link.relList.add('noopener', 'noreferrer');
    });
  };

  updateLinks();
  new MutationObserver(updateLinks).observe(document.body, {
    childList: true,
    subtree: true
  });
})();
