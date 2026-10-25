(() => {
  document.querySelectorAll('[data-setup-tabs]').forEach(container => {
    const tabs = Array.from(container.querySelectorAll('[data-setup-tab]'));
    const panels = Array.from(container.querySelectorAll('[data-setup-panel]'));

    const activate = (selected, { focus = false, updateHash = false } = {}) => {
      tabs.forEach(tab => {
        tab.setAttribute('aria-selected', String(tab === selected));
        tab.tabIndex = tab === selected ? 0 : -1;
      });
      panels.forEach(panel => {
        panel.hidden = panel.id !== selected.getAttribute('aria-controls');
      });
      if (focus) selected.focus();
      if (updateHash) {
        window.history.replaceState(window.history.state, '', `#${selected.getAttribute('aria-controls')}`);
      }
    };

    const activateHash = () => {
      const target = document.getElementById(window.location.hash.slice(1));
      const index = panels.findIndex(panel => target && (panel === target || panel.contains(target)));
      if (index !== -1) activate(tabs[index]);
    };

    tabs.forEach((tab, index) => {
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', () => activate(tab, { updateHash: true }));
      tab.addEventListener('keydown', event => {
        let next;
        switch (event.key) {
          case 'ArrowRight': next = (index + 1) % tabs.length; break;
          case 'ArrowLeft': next = (index + tabs.length - 1) % tabs.length; break;
          case 'Home': next = 0; break;
          case 'End': next = tabs.length - 1; break;
          default: return;
        }
        event.preventDefault();
        activate(tabs[next], { focus: true, updateHash: true });
      });
    });

    activate(tabs[0]);
    activateHash();
    container.dataset.enhanced = 'true';
    container.querySelector('[data-setup-tablist]').hidden = false;
    window.addEventListener('hashchange', activateHash);
  });
})();
