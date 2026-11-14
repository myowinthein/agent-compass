import assert from 'node:assert/strict';
import { checkThemeColors } from './check-theme-colors.mjs';
import { chromium } from 'playwright-core';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(process.env.COMPASS_DOCS_SITE || resolve(dirname(fileURLToPath(import.meta.url)), '../_site'));
const mime = { html:'text/html',css:'text/css',js:'text/javascript',json:'application/json',svg:'image/svg+xml',jpg:'image/jpeg' };
const server=createServer(async(request,response)=>{
 try {
  let pathname=decodeURIComponent(new URL(request.url,'http://localhost').pathname).replace(/^\/agent-compass\//,'/');
  if(pathname.endsWith('/'))pathname+='index.html';
  const path=resolve(root,`.${pathname}`);
  if(!path.startsWith(root+sep))throw new Error('Outside site');
  response.setHeader('Content-Type',mime[path.split('.').at(-1)]||'application/octet-stream');
  response.end(await readFile(path));
 } catch {response.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
let browser;
async function createContext(options = {}) {
 const context = await browser.newContext(options);
 await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
 return context;
}
let assertions=0;
try {
 browser=await chromium.launch({executablePath:process.env.COMPASS_DOCS_CHROME||(process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome'),headless:true});
 for(const width of [1280,390]) {
  for(const scheme of ['light','dark']) {
   const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
   const page=await context.newPage();
   const requests=[];const errors=[];
   page.on('request',r=>requests.push(r.url()));
   page.on('pageerror',e=>errors.push(e.message));
   await page.addInitScript(()=>{window.shifts=[];new PerformanceObserver(list=>window.shifts.push(...list.getEntries().filter(e=>!e.hadRecentInput).map(e=>e.value))).observe({type:'layout-shift',buffered:true});});
   await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
   await page.waitForTimeout(300);
   assert(!requests.some(url=>url.includes('search-data.json')),'Search downloaded before interaction');
   assert(!requests.some(url=>url.includes('mermaid')),'Browser downloaded Mermaid');
   assert.equal(requests.filter(url=>/just-the-docs-(default|light|dark)\.css/.test(url)).length,1,'Duplicate initial theme stylesheets');
   assert(requests.some(url=>url.endsWith(`just-the-docs-${scheme}.css`)),'Wrong system theme');
   assert.equal(await page.locator('figure.mermaid img').evaluateAll(imgs=>imgs.every(img=>img.complete&&img.naturalWidth>0)),true,'Diagram not visible');
   const cls=await page.evaluate(()=>window.shifts.reduce((sum,n)=>sum+n,0));
   assert(cls<0.01,`Initial layout shifted: ${cls}`);
   assertions += await checkThemeColors(page, scheme);
   const query=page.locator('#search-input');
   if(width===390)await page.locator('#menu-button').click();
   await query.fill('salary');
   await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
   assert.equal(requests.filter(url=>url.includes('search-data.json')).length,1,'Search initialized multiple times');
   await query.evaluate(input => input.blur());
   assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),false);
   await query.focus();
   await page.waitForFunction(()=>document.documentElement.classList.contains('search-active'));
   assertions+=2;
   await query.press('Escape');
   assert.equal(await query.inputValue(),'');
   await page.locator('#theme-mode').selectOption(scheme==='light'?'dark':'light');
   await page.waitForFunction(expected=>document.querySelector('link[rel="stylesheet"]').href.endsWith(`just-the-docs-${expected}.css`),scheme==='light'?'dark':'light');
   assertions += await checkThemeColors(page, scheme==='light'?'dark':'light');
   assert.equal(errors.length,0,errors.join('\n'));
   console.log(`PASS ${width}px ${scheme}: one theme stylesheet, no initial index, static diagrams, CLS ${cls.toFixed(3)}, search and theme switching`);
   assertions+=9;
   await context.close();
  }
 }
 // Late image bytes must not move text below the diagram.
 {
  const context=await createContext();const page=await context.newPage();
  await page.addInitScript(()=>{window.diagramShift=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.diagramShift+=e.value;}).observe({type:'layout-shift',buffered:true});});
  await page.route('**/assets/diagrams/*.svg',async route=>{await new Promise(resolve=>setTimeout(resolve,500));await route.continue();});
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
  assert(await page.evaluate(()=>window.diagramShift<0.01));
  console.log('PASS delayed diagram download: reserved space remains stable');assertions++;await context.close();
 }
 // A slow first search must retain text typed before the index becomes ready.
 {
  const context=await createContext();const page=await context.newPage();let count=0;
  await page.route('**/search-data.json',async route=>{count++;await new Promise(resolve=>setTimeout(resolve,500));await route.continue();});
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.locator('#search-input').fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert.equal(await page.locator('#search-input').inputValue(),'country');assert.equal(count,1);
  console.log('PASS slow search: first query preserved, one request');assertions+=2;await context.close();
 }
 // Failed requests may be retried on the next search interaction.
 {
  const context=await createContext();const page=await context.newPage();let count=0;
  await page.route('**/search-data.json',async route=>{count++;if(count===1)await route.fulfill({status:503,body:'Unavailable'});else await route.continue();});
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.locator('#search-input').focus();await page.waitForTimeout(100);
  await page.locator('#search-input').fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert.equal(count,2);console.log('PASS failed search: retry succeeds');assertions++;await context.close();
 }
 for(const fault of ['no-js','storage-blocked','saved-light','saved-dark','dark-css-failed']) {
  const context=await createContext({javaScriptEnabled:fault!=='no-js',colorScheme:'dark'});const page=await context.newPage();
  if(fault==='storage-blocked')await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));
  if(fault.startsWith('saved-'))await page.addInitScript(mode=>localStorage.setItem('agent-compass-theme',mode),fault.slice(6));
  if(fault==='dark-css-failed')await page.route('**/just-the-docs-dark.css',route=>route.abort());
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
  const expected=['no-js','saved-light','dark-css-failed'].includes(fault)?'light':'dark';
  await page.waitForFunction(expected=>{
   const color=getComputedStyle(document.body).backgroundColor;
   return expected==='dark'?color==='rgb(39, 38, 43)':color==='rgb(255, 255, 255)';
  },expected);
  assert(await page.locator('figure.mermaid img').evaluateAll(imgs=>imgs.every(img=>img.complete&&img.naturalWidth>0)));
  console.log(`PASS ${fault}: readable ${expected} theme and diagrams`);assertions++;await context.close();
 }
 const shortcut = (await readFile(resolve(root, 'assets/js/just-the-docs.js'), 'utf8')).match(/add event listener on ctrl[^]*?e\.key === '([^']+)'/);
 if (shortcut) {
  const context=await createContext();const page=await context.newPage();
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.keyboard.press(`Control+${shortcut[1]}`);
  assert.equal(await page.evaluate(()=>document.activeElement.id),'search-input');
  await page.locator('#search-input').fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  console.log('PASS configured search shortcut before index loading');assertions++;await context.close();
 }
 // The header shares feedback while keeping home and release as native links.
 for (const width of [320, 390, 800, 1024, 1280]) for (const scheme of ['light', 'dark']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('https://github.com/myowinthein/agent-compass/releases/tag/*', route=>route.fulfill({contentType:'text/html',body:'<!doctype html><title>Release fixture</title>'}));
  const page=await context.newPage();
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  const brand=page.locator('.site-brand');
  const title=brand.locator('.site-title');
  const version=brand.locator('.site-version');
  assert(await brand.locator('.site-name').evaluate(el=>el.scrollWidth<=el.clientWidth+1),'Project title is truncated');
  const label=(await version.textContent()).trim();
  const release=`https://github.com/myowinthein/agent-compass/releases/tag/${label}`;
  assert.equal(await title.getAttribute('href'),'/agent-compass/');
  assert.equal(await version.getAttribute('href'),release);
  assert.equal(await version.getAttribute('target'),null);
  assert(await version.evaluate(a=>getComputedStyle(a,'::after').maskImage.includes('external-link.svg')));
  await title.hover();
  const highlight=await brand.evaluate(el=>getComputedStyle(el).backgroundImage);
  assert.notEqual(highlight,'none');
  await version.hover();
  assert.equal(await brand.evaluate(el=>getComputedStyle(el).backgroundImage),highlight);
  const box=await brand.boundingBox();
  const versionBox=await version.boundingBox();
  assert(versionBox.height>=24 && versionBox.width>=24);
  assert(versionBox.x>=box.x && versionBox.x+versionBox.width<=box.x+box.width);
  await page.mouse.click(box.x+box.width-3,box.y+box.height-3);
  await page.waitForURL(`${origin}/agent-compass/`);
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.locator('.site-brand .site-title').focus();
  await page.keyboard.press('Tab');
  const focused=page.locator('.site-brand .site-version');
  assert(await focused.evaluate(a=>a===document.activeElement && a.matches(':focus-visible') && getComputedStyle(a).outlineStyle!=='none'));
  await page.keyboard.press('Enter');
  await page.waitForURL(release);
  assert.equal(context.pages().length,1);
  console.log(`PASS ${width}px ${scheme}: shared header hover, home area, separate release link and keyboard activation`);
  assertions+=13;
  await context.close();
 }
 console.log(`Passed ${assertions} browser assertions.`);
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
