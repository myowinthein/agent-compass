(() => {
  const storageKey = 'agent-compass-theme';
  const modes = ['system', 'light', 'dark'];
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let mode = 'system';

  try {
    const saved = localStorage.getItem(storageKey);
    if (modes.includes(saved)) mode = saved;
  } catch {
    // Browser storage may be blocked by privacy settings.
  }

  const applyTheme = () => {
    const theme = mode === 'system' ? (systemTheme.matches ? 'dark' : 'light') : mode;
    jtd.setTheme(theme);
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
