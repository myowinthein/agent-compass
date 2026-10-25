const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

function loadTabs(hash = '') {
  const tablist = { hidden: true };
  const tabs = ['desktop', 'terminal'].map(id => ({
    id: `${id}-tab`,
    attributes: { 'aria-controls': id },
    events: {},
    setAttribute(name, value) { this.attributes[name] = value; },
    getAttribute(name) { return this.attributes[name]; },
    addEventListener(name, handler) { this.events[name] = handler; },
    focus() { this.focused = true; }
  }));
  const panels = ['desktop', 'terminal'].map(id => ({
    id,
    hidden: false,
    attributes: {},
    setAttribute(name, value) { this.attributes[name] = value; },
    contains(target) { return target.panel === id; }
  }));
  const container = {
    dataset: {},
    querySelector: () => tablist,
    querySelectorAll: selector => selector === '[data-setup-tab]' ? tabs : panels
  };
  const events = {};
  const location = { hash };
  const history = {
    state: null,
    replaceState(state, title, url) { location.hash = url; }
  };
  vm.runInNewContext(
    readFileSync(path.join(__dirname, '../assets/js/setup-tabs.js'), 'utf8'),
    {
      document: {
        querySelectorAll: () => [container],
        getElementById: id => panels.find(panel => panel.id === id) ||
          (id.match(/^(desktop|terminal)-(install|update|uninstall)$/) ?
            { panel: id.split('-')[0] } : null)
      },
      window: {
        location,
        history,
        addEventListener: (name, handler) => { events[name] = handler; }
      }
    }
  );
  return { tablist, tabs, panels, container, location, events };
}

test('desktop is selected by default with accessible tab and panel states', () => {
  const state = loadTabs();
  assert.deepEqual({
    listHidden: state.tablist.hidden,
    selected: state.tabs.map(tab => tab.attributes['aria-selected']),
    tabStops: state.tabs.map(tab => tab.tabIndex),
    hidden: state.panels.map(panel => panel.hidden),
    roles: state.panels.map(panel => panel.attributes.role),
    labels: state.panels.map(panel => panel.attributes['aria-labelledby']),
    panelStops: state.panels.map(panel => panel.tabIndex)
  }, {
    listHidden: false,
    selected: ['true', 'false'],
    tabStops: [0, -1],
    hidden: [false, true],
    roles: ['tabpanel', 'tabpanel'],
    labels: ['desktop-tab', 'terminal-tab'],
    panelStops: [0, 0]
  });
});

test('clicking a tab switches its panel and updates a shareable hash', () => {
  const state = loadTabs();
  state.tabs[1].events.click();
  assert.deepEqual(
    [state.panels.map(panel => panel.hidden), state.location.hash],
    [[true, false], '#terminal']
  );
});

for (const [hash, key, selected] of [
  ['', 'ArrowRight', 1],
  ['', 'ArrowLeft', 1],
  ['#terminal', 'ArrowRight', 0],
  ['#terminal', 'ArrowLeft', 0],
  ['', 'End', 1],
  ['#terminal', 'Home', 0]
]) {
  test(`${key} from ${hash || 'desktop'} selects and focuses the expected tab`, () => {
    const state = loadTabs(hash);
    let prevented = false;
    state.tabs[hash ? 1 : 0].events.keydown({
      key,
      preventDefault() { prevented = true; }
    });
    assert.deepEqual(
      [prevented, state.tabs[selected].focused, state.panels[selected].hidden],
      [true, true, false]
    );
  });
}

test('unrelated keys retain normal browser behaviour', () => {
  const state = loadTabs();
  let prevented = false;
  state.tabs[0].events.keydown({
    key: 'ArrowDown',
    preventDefault() { prevented = true; }
  });
  assert.deepEqual([prevented, state.location.hash, state.panels[0].hidden], [false, '', false]);
});

for (const hash of ['#terminal', '#terminal-install', '#terminal-update', '#terminal-uninstall']) {
  test(`${hash} opens the terminal panel directly`, () => {
    const state = loadTabs(hash);
    assert.deepEqual(state.panels.map(panel => panel.hidden), [true, false]);
  });
}

test('following a heading link activates its panel without taking keyboard focus', () => {
  const state = loadTabs();
  state.location.hash = '#terminal-update';
  state.events.hashchange();
  assert.deepEqual(
    [state.panels.map(panel => panel.hidden), state.tabs[1].focused, state.location.hash],
    [[true, false], undefined, '#terminal-update']
  );
});

test('an unknown hash keeps the currently selected panel', () => {
  const state = loadTabs('#terminal');
  state.location.hash = '#unknown';
  state.events.hashchange();
  assert.deepEqual(state.panels.map(panel => panel.hidden), [true, false]);
});

test('an unknown initial hash leaves the desktop panel selected', () => {
  const state = loadTabs('#unknown');
  assert.deepEqual(state.panels.map(panel => panel.hidden), [false, true]);
});
