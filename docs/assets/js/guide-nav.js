(() => {
  const overview = document.currentScript.dataset.overviewUrl;

  const activate = () => {
    const navigation = document.getElementById('site-nav');
    if (!navigation || !overview) return;

    const link = Array.from(navigation.querySelectorAll('a[href]'))
      .find(candidate => candidate.getAttribute('href') === overview);
    if (!link) return;

    link.classList.add('active');
    link.setAttribute('aria-current', 'location');
    let item = link.closest('.nav-list-item');
    while (item) {
      item.classList.add('active');
      const expander = Array.from(item.children)
        .find(child => child.classList.contains('nav-list-expander'));
      if (expander) expander.setAttribute('aria-expanded', 'true');
      item = item.parentElement.closest('.nav-list-item');
    }
    navigation.dataset.guideNavReady = 'true';
    link.scrollIntoView({ block: 'nearest' });
  };

  if (document.readyState === 'complete') activate();
  else document.addEventListener('DOMContentLoaded', activate, { once: true });
})();
