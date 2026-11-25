(() => {
  const initialize = () => {
    const observed = new WeakSet();
    const observer = new ResizeObserver(() => refresh());
    const observe = element => {
      if (element && !observed.has(element)) {
        observed.add(element);
        observer.observe(element);
      }
    };
    const position = status => {
      const empty = !status.textContent.trim();
      if (status.hidden !== empty) status.hidden = empty;
      if (empty || !status.getClientRects().length) return;
      const copy = status.classList.contains('copy-status');
      const theme = status.classList.contains('theme-status');
      const anchor = copy ? status.parentElement.querySelector('button') : document.querySelector(theme ? '#theme-mode' : '.search-input-wrap');
      if (!anchor) return;
      observe(status);
      observe(anchor);
      const viewport = window.visualViewport;
      const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
      const margin = Math.min(rem, (viewport?.height || innerHeight) / 8);
      const leftEdge = (viewport?.offsetLeft || 0) + margin;
      const topEdge = (viewport?.offsetTop || 0) + margin;
      const rightEdge = leftEdge + (viewport?.width || innerWidth) - 2 * margin;
      const bottomEdge = topEdge + (viewport?.height || innerHeight) - 2 * margin;
      const field = anchor.getBoundingClientRect();
      // Attached theme feedback leaves the screen with its dropdown.
      if (theme) {
        const offscreen = !anchor.getClientRects().length ||
          field.bottom <= topEdge - margin || field.top >= bottomEdge + margin ||
          field.right <= leftEdge - margin || field.left >= rightEdge + margin;
        status.style.visibility = offscreen ? 'hidden' : '';
        if (offscreen) return;
      }
      status.style.width = copy || theme ? 'max-content' : `${Math.min(field.width, rightEdge - leftEdge)}px`;
      status.style.maxWidth = `${Math.min(rightEdge - leftEdge, copy || theme ? 24 * rem : field.width)}px`;
      const style = getComputedStyle(status);
      const height = status.scrollHeight + parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
      const width = status.getBoundingClientRect().width;
      const left = Math.max(leftEdge, Math.min(copy || theme ? field.right - width : field.left, rightEdge - width));
      const gap = rem / 4;
      // Choose visible space around the control and any other focused element.
      let spaces = [{ top: topEdge, bottom: bottomEdge }];
      const avoid = box => {
        if (left >= box.right || left + width <= box.left) return;
        spaces = spaces.flatMap(space => {
          if (box.bottom + gap <= space.top || box.top - gap >= space.bottom) return [space];
          return [
            { top: space.top, bottom: Math.min(space.bottom, box.top - gap) },
            { top: Math.max(space.top, box.bottom + gap), bottom: space.bottom }
          ].filter(part => part.bottom > part.top);
        });
      };
      avoid(field);
      const focused = document.activeElement;
      if (focused && focused !== document.body && !anchor.contains(focused) && !status.contains(focused)) avoid(focused.getBoundingClientRect());
      if (!spaces.length) spaces = [{ top: topEdge, bottom: bottomEdge }];
      const preferredTop = field.bottom + gap;
      const fits = spaces.filter(space => space.bottom - space.top >= height);
      const candidates = fits.length ? fits : spaces;
      const distance = space => Math.abs(Math.max(space.top, Math.min(preferredTop, space.bottom - height)) - preferredTop);
      candidates.sort((a, b) => fits.length ? distance(a) - distance(b) : (b.bottom - b.top) - (a.bottom - a.top));
      const space = candidates[0];
      status.style.maxHeight = `${space.bottom - space.top}px`;
      status.style.overflowY = 'auto';
      status.style.overscrollBehavior = 'contain';
      const top = Math.max(space.top, Math.min(preferredTop, space.bottom - Math.min(height, space.bottom - space.top)));
      const parent = status.offsetParent;
      const origin = parent.getBoundingClientRect();
      status.style.left = `${left - origin.left - parent.clientLeft + parent.scrollLeft}px`;
      status.style.top = `${top - origin.top - parent.clientTop + parent.scrollTop}px`;
      status.style.right = 'auto';
      status.style.bottom = 'auto';
      if (status.scrollHeight > status.clientHeight + 1) status.tabIndex = 0;
      else status.removeAttribute('tabindex');
    };
    const refresh = () => {
      const retry = document.getElementById('search-retry');
      const input = document.getElementById('search-input');
      if (retry && input) {
        observe(retry);
        if (retry.hidden) input.style.removeProperty('padding-right');
        else input.style.paddingRight = `${retry.getBoundingClientRect().width + parseFloat(getComputedStyle(retry).right) + 4}px`;
      }
      document.querySelectorAll('.copy-status, .search-status, .theme-status').forEach(position);
    };
    new MutationObserver(refresh).observe(document.body, {
      childList: true, characterData: true, subtree: true, attributes: true, attributeFilter: ['hidden'],
    });
    window.addEventListener('resize', refresh);
    window.addEventListener('scroll', refresh, { passive: true, capture: true });
    window.visualViewport?.addEventListener('resize', refresh);
    window.visualViewport?.addEventListener('scroll', refresh);
    document.addEventListener('focusin', refresh);
    document.addEventListener('click', refresh);
    refresh();
  };
  if (document.readyState === 'complete') initialize();
  else document.addEventListener('DOMContentLoaded', initialize, { once: true });
})();
