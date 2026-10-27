const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const site = path.join(__dirname, '../_site');
const home = readFileSync(path.join(site, 'index.html'), 'utf8');
const canonical = home.match(/<link\b[^>]*rel="canonical"[^>]*href="([^"]+)"/);
assert.ok(canonical, 'The built home page must expose its canonical site URL');
const siteUrl = new URL(canonical[1]);
const basePath = siteUrl.pathname.replace(/\/$/, '');
const policies = [
  ['Privacy Policy', 'docs/legal/privacy-policy.html'],
  ['Disclaimer', 'docs/legal/disclaimer.html']
];

function links(html) {
  return Array.from(html.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g), match => ({
    href: match[1],
    label: match[2].replace(/<[^>]+>/g, '').trim()
  }));
}

for (const page of [
  'index.html',
  'docs/setup/claude.html',
  'docs/setup/codex.html',
  'docs/commands/country-finder.html',
  ...policies.map(([, file]) => file)
]) {
  test(`${page} keeps legal links in the footer and out of sidebar navigation`, () => {
    const html = readFileSync(path.join(site, page), 'utf8');
    const footer = html.match(/<footer\b[^>]*>([\s\S]*?)<\/footer>/);
    const navigation = html.match(/<nav\b[^>]*id="site-nav"[^>]*>([\s\S]*?)<\/nav>/);
    assert.ok(footer, 'The normal page layout must include a footer');
    assert.ok(navigation, 'The normal page layout must include sidebar navigation');

    for (const [label, file] of policies) {
      const matches = links(footer[1]).filter(link => link.label === label);
      assert.equal(matches.length, 1, `The footer must contain one ${label} link`);
      const target = new URL(matches[0].href, siteUrl);
      assert.equal(target.origin, siteUrl.origin);
      assert.equal(target.pathname, `${basePath}/${file}`);
      assert.match(readFileSync(path.join(site, file), 'utf8'), /<h1\b/,
        `${label} must remain an available content page`);
    }

    for (const link of links(navigation[1])) {
      assert.doesNotMatch(new URL(link.href, siteUrl).pathname, /\/docs\/legal(?:\/|$)/,
        'The Legal branch must stay out of sidebar navigation');
    }
    assert.doesNotMatch(navigation[1], /aria-label="Legal submenu"/);
  });
}
