(() => {
  const storageKey = 'agent-compass-theme';
  const modes = ['system', 'light', 'dark'];
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let stylesheet = document.getElementById('compass-theme-stylesheet') || document.querySelector('link[rel="stylesheet"]');
  let pendingStylesheet;
  let mode = 'system';

  try {
    const saved = localStorage.getItem(storageKey);
    if (modes.includes(saved)) mode = saved;
  } catch {
    // Browser storage may be blocked by privacy settings.
  }

  const applyTheme = () => {
    const theme = mode === 'system' ? (systemTheme.matches ? 'dark' : 'light') : mode;
    const href = new URL(`just-the-docs-${theme}.css`, stylesheet.href).href;
    pendingStylesheet?.remove();
    pendingStylesheet = null;

    if (stylesheet.href !== href) {
      // Keep the current styles active while the selected theme loads.
      const next = stylesheet.cloneNode();
      next.removeAttribute('id');
      next.href = href;
      next.addEventListener('load', () => {
        if (pendingStylesheet !== next) return;
        stylesheet.remove();
        stylesheet = next;
        stylesheet.id = 'compass-theme-stylesheet';
        pendingStylesheet = null;
      });
      next.addEventListener('error', () => {
        if (pendingStylesheet !== next) return;
        next.remove();
        pendingStylesheet = null;
        document.documentElement.style.colorScheme = stylesheet.href.endsWith('just-the-docs-dark.css') ? 'dark' : 'light';
      });
      pendingStylesheet = next;
      stylesheet.after(next);
    }

    document.documentElement.style.colorScheme = theme;
    const selector = document.getElementById('theme-mode');
    if (selector) selector.value = mode;
  };

  applyTheme();
  systemTheme.addEventListener('change', () => {
    if (mode === 'system') applyTheme();
  });

  window.addEventListener('storage', event => {
    if (event.key !== storageKey && event.key !== null) return;
    mode = modes.includes(event.newValue) ? event.newValue : 'system';
    applyTheme();
  });

  document.addEventListener('DOMContentLoaded', () => {
    const selector = document.getElementById('theme-mode');
    if (!selector) return;
    selector.value = mode;
    selector.closest('.theme-switcher').hidden = false;
    selector.addEventListener('change', () => {
      mode = selector.value;
      applyTheme();
      try {
        localStorage.setItem(storageKey, mode);
      } catch {
        // Switching still works when the preference cannot be saved.
      }
    });
  });
})();
