(() => {
  const back = document.querySelector('.diagram-viewer__back');
  if (!back) {
    const links = Array.from(document.querySelectorAll('[data-diagram-full-size]'));
    if (!links.length) return;
    let returnLink;
    document.addEventListener('click', event => {
      if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const link = event.target.closest('[data-diagram-full-size]');
      if (link) returnLink = link;
    });
    const restoreFocus = () => {
      const navigation = window.navigation;
      if (!returnLink && performance.getEntriesByType('navigation')[0]?.type === 'back_forward' && navigation) {
        const next = navigation.entries().find(entry => entry.index === navigation.currentEntry.index + 1);
        if (next?.url) returnLink = links.find(link => new URL(link.href).pathname === new URL(next.url).pathname);
      }
      const fragment = document.getElementById(location.hash.slice(1));
      const link = returnLink || (links.includes(fragment) && fragment);
      if (link) requestAnimationFrame(() => {
        link.focus({ preventScroll: true });
        returnLink = undefined;
      });
    };
    window.addEventListener('pageshow', restoreFocus);
    restoreFocus();
    return;
  }

  const destination = new URL(back.href);
  let fromGuide = false;
  if (document.referrer) {
    const previous = new URL(document.referrer);
    fromGuide = previous.origin === destination.origin && previous.pathname === destination.pathname;
  }

  back.addEventListener('click', event => {
    if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (fromGuide && history.length > 1 && window.navigation) {
      event.preventDefault();
      history.back();
    }
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !event.isComposing && !event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
      event.preventDefault();
      back.click();
    }
  });
})();
