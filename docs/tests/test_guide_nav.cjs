const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = readFileSync(path.join(__dirname, '../assets/js/guide-nav.js'), 'utf8');
const overview = '/agent-compass/docs/commands/country-finder.html';

function element(classes = [], parentElement = null) {
  const node = {
    classes: new Set(classes),
    attributes: {},
    children: [],
    parentElement,
    classList: { add: name => node.classes.add(name), contains: name => node.classes.has(name) },
    setAttribute: (name, value) => { node.attributes[name] = value; },
    closest(selector) {
      const name = selector.slice(1);
      for (let current = node; current; current = current.parentElement) {
        if (current.classes.has(name)) return current;
      }
      return null;
    }
  };
  parentElement?.children.push(node);
  return node;
}

function link(parent, href) {
  const node = element([], parent);
  node.getAttribute = name => (name === 'href' ? href : null);
  node.scrolled = null;
  node.scrollIntoView = options => { node.scrolled = options; };
  return node;
}

// navigation > Commands item (with expander) > list > Country Finder item (with expander) > links
function buildNavigation() {
  const navigation = element();
  navigation.dataset = {};
  const section = element(['nav-list-item'], navigation);
  const sectionExpander = element(['nav-list-expander'], section);
  const list = element([], section);
  const page = element(['nav-list-item'], list);
  const pageExpander = element(['nav-list-expander'], page);
  const other = link(page, '/agent-compass/docs/commands/portal-finder.html');
  const current = link(page, overview);
  navigation.querySelectorAll = selector => {
    assert.equal(selector, 'a[href]');
    return [other, current];
  };
  return { navigation, section, sectionExpander, page, pageExpander, other, current };
}

function run({ navigation, overviewUrl = overview, readyState = 'complete' } = {}) {
  const listeners = {};
  vm.runInNewContext(source, {
    document: {
      currentScript: { dataset: overviewUrl === null ? {} : { overviewUrl } },
      readyState,
      getElementById: id => (id === 'site-nav' ? navigation ?? null : null),
      addEventListener: (name, handler, options) => { listeners[name] = { handler, options }; }
    }
  });
  return listeners;
}

test('the matching Overview link becomes the current location', () => {
  const nav = buildNavigation();
  run({ navigation: nav.navigation });
  assert.deepEqual(
    [nav.current.classes.has('active'), nav.current.attributes['aria-current'], nav.other.classes.has('active'), 'aria-current' in nav.other.attributes],
    [true, 'location', false, false]
  );
});

test('every ancestor navigation item is activated and expanded', () => {
  const nav = buildNavigation();
  run({ navigation: nav.navigation });
  assert.deepEqual(
    [nav.page.classes.has('active'), nav.section.classes.has('active'), nav.pageExpander.attributes['aria-expanded'], nav.sectionExpander.attributes['aria-expanded']],
    [true, true, 'true', 'true']
  );
});

test('the navigation is marked ready and the link scrolled into view', () => {
  const nav = buildNavigation();
  run({ navigation: nav.navigation });
  assert.deepEqual([nav.navigation.dataset.guideNavReady, nav.current.scrolled?.block], ['true', 'nearest']);
});

test('an Overview link that is not in the navigation leaves it untouched', () => {
  const nav = buildNavigation();
  run({ navigation: nav.navigation, overviewUrl: '/agent-compass/docs/commands/unknown.html' });
  assert.deepEqual(
    [nav.current.classes.has('active'), nav.page.classes.has('active'), 'guideNavReady' in nav.navigation.dataset],
    [false, false, false]
  );
});

test('a page without navigation or an Overview URL does nothing', () => {
  const nav = buildNavigation();
  assert.doesNotThrow(() => run({ navigation: undefined }));
  run({ navigation: nav.navigation, overviewUrl: null });
  assert.equal(nav.current.classes.has('active'), false);
});

test('a loading document activates once, after DOMContentLoaded', () => {
  const nav = buildNavigation();
  const listeners = run({ navigation: nav.navigation, readyState: 'loading' });
  assert.deepEqual([nav.current.classes.has('active'), listeners.DOMContentLoaded.options.once], [false, true]);
  listeners.DOMContentLoaded.handler();
  assert.equal(nav.current.attributes['aria-current'], 'location');
});
