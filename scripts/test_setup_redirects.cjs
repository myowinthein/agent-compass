const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

for (const platform of ['claude', 'codex']) {
  for (const method of ['desktop', 'terminal']) {
    test(`${platform} ${method} legacy URL redirects to its tab and preserves section links`, () => {
      const html = readFileSync(path.join(__dirname, `../_site/docs/setup/${platform}/${method}.html`), 'utf8');
      const target = `/agent-compass/docs/setup/${platform}.html#${method}`;
      assert.ok(html.includes(`<meta http-equiv="refresh" content="0; url=${target}">`));
      assert.match(html, /<noscript>\s*<meta http-equiv="refresh"[^>]*>\s*<\/noscript>/);
      assert.ok(html.includes(`<a href="${target}">`));
      assert.ok(html.includes(`<link rel="canonical" href="https://myowinthein.github.io/agent-compass/docs/setup/${platform}.html">`));
      assert.doesNotMatch(html, /<h2[^>]*id="(?:install|update|uninstall)"/);

      const script = html.match(/<script>([\s\S]*?)<\/script>/);
      assert.ok(script, 'The redirect needs a history-replacing script');
      for (const hash of ['', '#install', '#update', '#uninstall', '#unknown']) {
        let destination;
        vm.runInNewContext(script[1], {
          URL,
          window: {
            location: {
              href: `http://localhost:4000/agent-compass/docs/setup/${platform}/${method}.html${hash}`,
              hash,
              replace(url) { destination = url; }
            }
          }
        });
        const section = ['#install', '#update', '#uninstall'].includes(hash) ? `-${hash.slice(1)}` : '';
        assert.equal(destination, `http://localhost:4000${target}${section}`);
        assert.ok(readFileSync(path.join(__dirname, `../_site/docs/setup/${platform}.html`), 'utf8')
          .includes(`id="${method}${section}"`), 'The destination tab or section must exist');
      }
    });
  }
}

test('Setup contents list current platform guides and saved-search guidance', () => {
  const html = readFileSync(path.join(__dirname, '../_site/docs/setup/index.html'), 'utf8');
  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/);
  assert.ok(main);
  assert.deepEqual(
    Array.from(main[1].matchAll(/href="(\/agent-compass\/docs\/setup\/[^"#]+)"/g), match => match[1]),
    ['/agent-compass/docs/setup/claude.html', '/agent-compass/docs/setup/codex.html',
      '/agent-compass/docs/setup/saved-searches.html']
  );
});

test('Legacy setup pages stay out of sidebar navigation and search', () => {
  const home = readFileSync(path.join(__dirname, '../_site/index.html'), 'utf8');
  const search = readFileSync(path.join(__dirname, '../_site/assets/js/search-data.json'), 'utf8');
  assert.doesNotMatch(home + search, /\/docs\/setup\/(?:claude|codex)\/(?:desktop|terminal)\.html/);
});
