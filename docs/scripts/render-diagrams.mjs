import { chromium } from 'playwright-core';
import { createServer } from 'node:http';
import { readFile, access } from 'node:fs/promises';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../node_modules/mermaid/dist');
const candidates = [
  process.env.COMPASS_DOCS_CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  process.env.PROGRAMFILES && join(process.env.PROGRAMFILES, 'Google/Chrome/Application/chrome.exe'),
].filter(Boolean);
let executablePath;
for (const path of candidates) {
  try { await access(path); executablePath = path; break; } catch {}
}
if (!executablePath) throw new Error('Chrome is required to build diagrams. Set COMPASS_DOCS_CHROME to its executable.');

let input = '';
for await (const chunk of process.stdin) input += chunk;
const diagrams = JSON.parse(input);
const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (pathname === '/') {
      response.setHeader('Content-Type', 'text/html');
      response.end('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
      return;
    }
    const path = resolve(root, `.${pathname}`);
    if (!path.startsWith(root + sep)) throw new Error('Outside the renderer directory');
    response.setHeader('Content-Type', 'text/javascript');
    response.end(await readFile(path));
  } catch {
    response.writeHead(404).end();
  }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
try {
  browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const origin = `http://127.0.0.1:${server.address().port}`;
  await page.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
  await page.goto(origin);
  const rendered = await page.evaluate(async diagrams => {
    const { default: mermaid } = await import('/mermaid.esm.min.mjs');
    mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose', deterministicIds: true });
    const output = {};
    for (const [id, source] of Object.entries(diagrams)) {
      const result = await mermaid.render(`diagram-${id}`, source);
      // Embedded SVG media queries inherit the page's selected color-scheme.
      const selector = `#diagram-${id}`;
      const colors = `<style>
        ${selector} {
          --diagram-text: #27262b;
          --diagram-surface: #f5f6fa;
          --diagram-line: #5c5962;
        }
        @media (prefers-color-scheme: dark) {
          ${selector} {
            --diagram-text: #e6e1e8;
            --diagram-surface: #302d36;
            --diagram-line: #a6a1ad;
          }
        }
        ${selector} text, ${selector} span, ${selector} p, ${selector} .label,
        ${selector} .cluster text, ${selector} .cluster span {
          fill: var(--diagram-text);
          color: var(--diagram-text);
        }
        ${selector} .node > :is(rect, circle, ellipse, polygon, path), ${selector} .cluster rect {
          fill: var(--diagram-surface);
          stroke: var(--diagram-line);
        }
        ${selector} .flowchart-link, ${selector} .edgePath .path {
          stroke: var(--diagram-line);
        }
        ${selector} .marker, ${selector} .arrowheadPath {
          fill: var(--diagram-line);
          stroke: var(--diagram-line);
        }
        ${selector} .edgeLabel, ${selector} .edgeLabel rect, ${selector} .labelBkg {
          background-color: var(--diagram-surface);
          fill: var(--diagram-surface);
          opacity: 1;
        }
      </style>`;
      output[id] = result.svg.replace('</svg>', `${colors}</svg>`);
    }
    return output;
  }, diagrams);
  process.stdout.write(JSON.stringify(rendered));
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
}
