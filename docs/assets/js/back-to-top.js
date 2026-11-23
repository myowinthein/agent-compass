(() => {
  const button = document.getElementById('back-to-top');
  if (!button) return;

  const updateVisibility = () => {
    button.hidden = window.scrollY <= 400;
  };

  button.addEventListener('click', () => {
    const heading = document.querySelector('#main-content h1');
    if (heading) {
      if (!heading.hasAttribute('tabindex')) {
        heading.setAttribute('tabindex', '-1');
        heading.addEventListener('blur', () => heading.removeAttribute('tabindex'), { once: true });
      }
      heading.focus({ preventScroll: true });
    }
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
    });
    updateVisibility();
  });

  window.addEventListener('scroll', updateVisibility, { passive: true });
  window.addEventListener('pageshow', updateVisibility);
  updateVisibility();
})();
