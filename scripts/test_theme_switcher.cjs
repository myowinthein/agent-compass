const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = readFileSync(path.join(__dirname, '../assets/js/theme-switcher.js'), 'utf8');

function loadSwitcher({ saved = null, dark = false, blockedStorage = false } = {}) {
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
  const themes = [];
  vm.runInNewContext(source, {
    document: {
      documentElement: { style },
      getElementById: () => selector,
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
    },
    jtd: { setTheme: theme => themes.push(theme) }
  });
  events.ready();
  return { storage, events, selector, container, media, themes, style };
}

for (const dark of [false, true]) {
  test(`system mode follows ${dark ? 'dark' : 'light'} appearance`, () => {
    const state = loadSwitcher({ dark });
    assert.deepEqual(
      [state.selector.value, state.themes.at(-1), state.style.colorScheme, state.container.hidden],
      ['system', dark ? 'dark' : 'light', dark ? 'dark' : 'light', false]
    );
  });
}

for (const saved of ['light', 'dark']) {
  test(`saved ${saved} mode overrides the system`, () => {
    const state = loadSwitcher({ saved, dark: saved === 'light' });
    assert.deepEqual([state.selector.value, state.themes.at(-1)], [saved, saved]);
  });
}

test('manual selection is applied and saved', () => {
  const state = loadSwitcher();
  state.selector.value = 'dark';
  state.events.change();
  assert.deepEqual([state.themes.at(-1), state.storage.get('agent-compass-theme')], ['dark', 'dark']);
});

test('system mode responds to appearance changes', () => {
  const state = loadSwitcher();
  state.media.matches = true;
  state.events.system();
  assert.equal(state.themes.at(-1), 'dark');
});

test('an explicit preference ignores appearance changes', () => {
  const state = loadSwitcher({ saved: 'light' });
  state.media.matches = true;
  state.events.system();
  assert.equal(state.themes.at(-1), 'light');
});

test('returning to system mode uses the current appearance', () => {
  const state = loadSwitcher({ saved: 'light', dark: true });
  state.selector.value = 'system';
  state.events.change();
  assert.deepEqual([state.themes.at(-1), state.storage.get('agent-compass-theme')], ['dark', 'system']);
});

test('invalid saved preferences fall back to system mode', () => {
  const state = loadSwitcher({ saved: 'invalid', dark: true });
  assert.deepEqual([state.selector.value, state.themes.at(-1)], ['system', 'dark']);
});

test('blocked browser storage does not prevent switching', () => {
  const state = loadSwitcher({ blockedStorage: true });
  state.selector.value = 'dark';
  state.events.change();
  assert.equal(state.themes.at(-1), 'dark');
});

test('preferences synchronise between open tabs', () => {
  const state = loadSwitcher();
  state.events.storage({ key: 'agent-compass-theme', newValue: 'dark' });
  assert.deepEqual([state.selector.value, state.themes.at(-1)], ['dark', 'dark']);
});

test('clearing a preference in another tab restores system mode', () => {
  const state = loadSwitcher({ saved: 'dark' });
  state.events.storage({ key: 'agent-compass-theme', newValue: null });
  assert.deepEqual([state.selector.value, state.themes.at(-1)], ['system', 'light']);
});

test('unrelated storage changes leave the preference alone', () => {
  const state = loadSwitcher({ saved: 'dark' });
  state.events.storage({ key: 'another-setting', newValue: 'light' });
  assert.deepEqual([state.selector.value, state.themes.at(-1)], ['dark', 'dark']);
});
