const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = readFileSync(path.join(__dirname, '../assets/js/theme-switcher.js'), 'utf8');

function loadSwitcher({ saved = null, dark = false, blockedStorage = false, autoLoad = true, initialTheme = 'default' } = {}) {
  const storage = new Map(saved === null ? [] : [['agent-compass-theme', saved]]);
  const events = {};
  const selector = {
    value: 'system',
    addEventListener: (name, handler) => { events[name] = handler; },
    closest: () => container
  };
  const container = { hidden: true };
  const style = {};
  const media = {
    matches: dark,
    addEventListener: (name, handler) => { events.system = handler; }
  };
  const stylesheets = [];
  const requests = [];
  function stylesheet(href) {
    return {
      href,
      events: {},
      cloneNode() { return stylesheet(this.href); },
      removeAttribute(name) { delete this[name]; },
      addEventListener(name, handler) { this.events[name] = handler; },
      remove() {
        const index = stylesheets.indexOf(this);
        if (index !== -1) stylesheets.splice(index, 1);
      },
      after(next) {
        stylesheets.splice(stylesheets.indexOf(this) + 1, 0, next);
        requests.push(next);
        if (autoLoad) next.events.load();
      }
    };
  }
  stylesheets.push(stylesheet(`https://docs.example.invalid/agent-compass/assets/css/just-the-docs-${initialTheme}.css`));
  vm.runInNewContext(source, {
    URL,
    document: {
      documentElement: { style },
      querySelector: () => stylesheets[0],
      getElementById: id => id === 'theme-mode' ? selector : stylesheets.find(sheet => sheet.id === id) || null,
      addEventListener: (name, handler) => { events.ready = handler; }
    },
    window: {
      matchMedia: () => media,
      addEventListener: (name, handler) => { events.storage = handler; }
    },
    localStorage: {
      getItem: key => {
        if (blockedStorage) throw new Error('Storage blocked');
        return storage.get(key) ?? null;
      },
      setItem: (key, value) => {
        if (blockedStorage) throw new Error('Storage blocked');
        storage.set(key, value);
      }
    }
  });
  events.ready();
  const theme = () => new URL(stylesheets[0].href).pathname.match(/just-the-docs-(\w+)\.css$/)[1];
  return { storage, events, selector, container, media, theme, style, stylesheets, requests };
}

for (const dark of [false, true]) {
  test(`system mode follows ${dark ? 'dark' : 'light'} appearance`, () => {
    const state = loadSwitcher({ dark });
    assert.deepEqual(
      [state.selector.value, state.theme(), state.style.colorScheme, state.container.hidden],
      ['system', dark ? 'dark' : 'light', dark ? 'dark' : 'light', false]
    );
  });
}

for (const saved of ['light', 'dark']) {
  test(`saved ${saved} mode overrides the system`, () => {
    const state = loadSwitcher({ saved, dark: saved === 'light' });
    assert.deepEqual([state.selector.value, state.theme()], [saved, saved]);
  });
}

test('manual selection is applied and saved', () => {
  const state = loadSwitcher();
  state.selector.value = 'dark';
  state.events.change();
  assert.deepEqual([state.theme(), state.storage.get('agent-compass-theme')], ['dark', 'dark']);
});

test('system mode responds to appearance changes', () => {
  const state = loadSwitcher();
  state.media.matches = true;
  state.events.system();
  assert.equal(state.theme(), 'dark');
});

test('an explicit preference ignores appearance changes', () => {
  const state = loadSwitcher({ saved: 'light' });
  state.media.matches = true;
  state.events.system();
  assert.equal(state.theme(), 'light');
});

test('returning to system mode uses the current appearance', () => {
  const state = loadSwitcher({ saved: 'light', dark: true });
  state.selector.value = 'system';
  state.events.change();
  assert.deepEqual([state.theme(), state.storage.get('agent-compass-theme')], ['dark', 'system']);
});

test('invalid saved preferences fall back to system mode', () => {
  const state = loadSwitcher({ saved: 'invalid', dark: true });
  assert.deepEqual([state.selector.value, state.theme()], ['system', 'dark']);
});

test('blocked browser storage does not prevent switching', () => {
  const state = loadSwitcher({ blockedStorage: true });
  state.selector.value = 'dark';
  state.events.change();
  assert.equal(state.theme(), 'dark');
});

test('preferences synchronise between open tabs', () => {
  const state = loadSwitcher();
  state.events.storage({ key: 'agent-compass-theme', newValue: 'dark' });
  assert.deepEqual([state.selector.value, state.theme()], ['dark', 'dark']);
});

test('clearing a preference in another tab restores system mode', () => {
  const state = loadSwitcher({ saved: 'dark' });
  state.events.storage({ key: 'agent-compass-theme', newValue: null });
  assert.deepEqual([state.selector.value, state.theme()], ['system', 'light']);
});

test('unrelated storage changes leave the preference alone', () => {
  const state = loadSwitcher({ saved: 'dark' });
  state.events.storage({ key: 'another-setting', newValue: 'light' });
  assert.deepEqual([state.selector.value, state.theme()], ['dark', 'dark']);
});

test('clearing all storage in another tab restores system mode', () => {
  const state = loadSwitcher({ saved: 'dark' });
  state.events.storage({ key: null, newValue: null });
  assert.deepEqual([state.selector.value, state.theme()], ['system', 'light']);
});

test('current styles remain active until the replacement loads', () => {
  const state = loadSwitcher({ dark: true, autoLoad: false });
  const original = state.stylesheets[0];
  assert.equal(state.theme(), 'default');
  assert.equal(state.stylesheets.length, 2);
  state.requests[0].events.load();
  assert.equal(state.theme(), 'dark');
  assert.equal(state.stylesheets.length, 1);
  assert.ok(!state.stylesheets.includes(original));
});

test('a stylesheet failure preserves the working theme and allows retry', () => {
  const state = loadSwitcher({ dark: true, autoLoad: false });
  const original = state.stylesheets[0];
  state.requests[0].events.error();
  assert.deepEqual(state.stylesheets, [original]);
  state.selector.value = 'dark';
  state.events.change();
  state.requests.at(-1).events.load();
  assert.equal(state.theme(), 'dark');
  assert.equal(state.stylesheets.length, 1);
});

test('late loads and failures cannot override the latest selection', () => {
  const state = loadSwitcher({ autoLoad: false });
  const first = state.requests[0];
  state.selector.value = 'dark';
  state.events.change();
  const dark = state.requests.at(-1);
  state.selector.value = 'light';
  state.events.change();
  const light = state.requests.at(-1);
  first.events.load();
  dark.events.load();
  assert.equal(state.theme(), 'default');
  light.events.load();
  dark.events.error();
  assert.equal(state.theme(), 'light');
  assert.equal(state.selector.value, 'light');
  assert.equal(state.stylesheets.length, 1);
});

test('returning to the active theme cancels a pending replacement', () => {
  const state = loadSwitcher({ autoLoad: false });
  state.requests[0].events.load();
  const original = state.stylesheets[0];
  state.selector.value = 'dark';
  state.events.change();
  const dark = state.requests.at(-1);
  state.selector.value = 'light';
  state.events.change();
  dark.events.load();
  assert.deepEqual(state.stylesheets, [original]);
  assert.equal(state.theme(), 'light');
});

for (const mode of ['light', 'dark']) {
  test(`reuses the initial ${mode} stylesheet without another download`, () => {
    const state = loadSwitcher({ saved: mode, initialTheme: mode });
    assert.deepEqual([state.theme(), state.requests.length, state.stylesheets.length], [mode, 0, 1]);
  });
}
