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
const pageUrl=path=>`${origin}/agent-compass/${path}`;
const background=expected=>page=>page.waitForFunction(expected=>{
 if(!document.body)return false;
 const color=getComputedStyle(document.body).backgroundColor;
 return expected==='dark'?color==='rgb(39, 38, 43)':color==='rgb(255, 255, 255)';
},expected);
let browser;
async function createContext(options = {}) {
 const context = await browser.newContext(options);
 await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
 return context;
}
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
   await checkThemeColors(page, scheme);
   const query=page.locator('#search-input');
   if(width===390)await page.locator('#menu-button').click();
   await query.fill('salary');
   await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
   assert.equal(requests.filter(url=>url.includes('search-data.json')).length,1,'Search initialized multiple times');
   await query.evaluate(input => input.blur());
   assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),false);
   await query.focus();
   await page.waitForFunction(()=>document.documentElement.classList.contains('search-active'));
   await query.press('Escape');
   assert.equal(await query.inputValue(),'');
   await page.locator('#theme-mode').selectOption(scheme==='light'?'dark':'light');
   await page.waitForFunction(expected=>document.querySelector('link[rel="stylesheet"]').href.endsWith(`just-the-docs-${expected}.css`),scheme==='light'?'dark':'light');
   await checkThemeColors(page, scheme==='light'?'dark':'light');
   assert.equal(errors.length,0,errors.join('\n'));
   console.log(`PASS ${width}px ${scheme}: one theme stylesheet, no initial index, static diagrams, CLS ${cls.toFixed(3)}, search and theme switching`);
   await context.close();
  }
 }
 // Manual appearance travels with full-size links, including blocked storage.
 for(const system of ['light','dark']) for(const blocked of [false,true]) {
  const context=await createContext({viewport:{width:390,height:900},colorScheme:system});
  if(blocked)await context.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));
  const page=await context.newPage();await page.goto(pageUrl('docs/commands/country-finder/detailed.html'));
  await page.locator('#menu-button').click();const manual=system==='light'?'dark':'light';
  await page.locator('#theme-mode').selectOption(manual);await background(manual)(page);
  const link=page.locator('[data-diagram-full-size]').first();
  assert((await link.getAttribute('href')).endsWith(`#theme-${manual}`));
  await link.click();await background(manual)(page);
  assert(await page.locator('.diagram-viewer__image').evaluate(el=>el.complete&&el.naturalWidth>0&&getComputedStyle(el).colorScheme===getComputedStyle(document.documentElement).colorScheme));
  await page.goBack();
  if(!await page.locator('#theme-mode').isVisible())await page.locator('#menu-button').click();
  await page.locator('#theme-mode').selectOption('system');
  await page.waitForFunction(()=>document.getElementById('theme-mode').value==='system'&&!document.querySelector('[data-diagram-full-size]').getAttribute('href').includes('#'));
  assert(!(await page.locator('[data-diagram-full-size]').first().getAttribute('href')).includes('#'),'System choice retained a manual diagram override');
  console.log(`PASS full-size ${manual} on ${system} system${blocked?', storage blocked':''}: manual theme retained and System clears it`);
  await context.close();
 }
 // Full-size viewers center fitting diagrams and return to the exact guide link.
 for(const width of [320,1280]) for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme,reducedMotion:'reduce'});
  const page=await context.newPage();
  const guide=pageUrl('docs/commands/country-finder/detailed.html');await page.goto(guide);
  const figures=page.locator('figure.mermaid');
  assert.equal(await figures.locator('figcaption a').count(),await figures.count());
  const figure=figures.nth(Math.min(1,await figures.count()-1));const image=figure.locator('img');const fullSize=figure.getByRole('link',{name:'View full-size diagram',exact:true});
  const authoredWidth=Number(await image.getAttribute('width'));
  const source=await image.getAttribute('src');const anchor=await fullSize.getAttribute('id');
  assert((await image.boundingBox()).width<=authoredWidth+1,'Diagram preview exceeds its authored size');
  assert.equal(await fullSize.getAttribute('target'),null,'Viewer unexpectedly opens another tab');
  await fullSize.focus();
  await page.keyboard.press('Shift+Tab');await page.keyboard.press('Tab');
  assert(await fullSize.evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle!=='none'),'Full-size link has no keyboard focus indication');
  await fullSize.evaluate(el=>el.scrollIntoView({block:'center',behavior:'instant'}));
  const scroll=await page.evaluate(()=>scrollY);
  const destination=new URL(await fullSize.getAttribute('href'),page.url()).href;
  await page.keyboard.press('Enter');await page.waitForURL(destination);
  const full=page.locator('.diagram-viewer__image');const canvas=page.locator('.diagram-viewer__canvas');const back=page.getByRole('link',{name:'Back to guide',exact:true});
  assert.equal(await full.getAttribute('src'),source);assert((await full.boundingBox()).width>=authoredWidth-1,'Viewer shrinks labels to fit the phone');
  await background(scheme)(page);
  assert.equal(await back.getAttribute('href'),`/agent-compass/docs/commands/country-finder/detailed.html#${anchor}`);
  const placement=await full.evaluate(el=>{const box=el.getBoundingClientRect(),canvas=el.parentElement,padding=parseFloat(getComputedStyle(canvas).paddingLeft);return {left:box.left,right:box.right,available:canvas.clientWidth,width:box.width,padding};});
  if(placement.width<=placement.available-2*placement.padding)assert(Math.abs(placement.left-(placement.available-placement.width)/2)<1,'Fitting diagram is not horizontally centered');
  else assert(Math.abs(placement.left-placement.padding)<1,'Wide diagram clips its left edge');
  await page.keyboard.press('Tab');assert(await back.evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')));
  await page.keyboard.press('Tab');assert(await canvas.evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')));
  await page.keyboard.press('ArrowDown');await page.waitForFunction(()=>document.querySelector('.diagram-viewer__canvas').scrollTop>0);
  if(placement.width>placement.available){await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>document.querySelector('.diagram-viewer__canvas').scrollLeft>0);}
  assert((await back.boundingBox()).y>=0,'Return control scrolled out of reach');
  if(width===320)await page.keyboard.press('Escape');else{await back.focus();await page.keyboard.press('Enter');}
  await page.waitForURL(guide);await page.waitForFunction(id=>document.activeElement.id===id,anchor);
  assert(Math.abs(await page.evaluate(()=>scrollY)-scroll)<2,'Return changed the guide scroll position');
  await page.keyboard.press('Enter');await page.waitForURL(destination);await page.goBack();
  await page.waitForFunction(id=>document.activeElement.id===id,anchor);
  assert(Math.abs(await page.evaluate(()=>scrollY)-scroll)<2,'Browser Back changed the guide scroll position');
  await page.goto(destination);await page.getByRole('link',{name:'Back to guide',exact:true}).click();
  await page.waitForURL(`${guide}#${anchor}`);await page.waitForFunction(id=>document.activeElement.id===id,anchor);
  assert.equal(context.pages().length,1);
  assert.equal(await page.evaluate(()=>Object.keys(localStorage).length),0,'Diagram navigation added stored state');
  console.log(`PASS ${width}px ${scheme}: native-size viewer, alignment, keyboard panning, Back/Escape, restored scroll/focus and direct-entry fallback`);
  await context.close();
 }
 // Static return links work without JavaScript; larger text keeps them reachable.
 for(const mode of ['no-js','large-text','legacy-navigation']) {
  const scripts=mode!=='no-js';
  const context=await createContext({viewport:{width:320,height:900},javaScriptEnabled:scripts});const page=await context.newPage();
  if(mode==='legacy-navigation')await context.addInitScript(()=>Object.defineProperty(window,'navigation',{value:undefined}));
  await page.goto(pageUrl('docs/commands/country-finder/detailed.html'));
  const link=page.locator('[data-diagram-full-size]').first();const anchor=await link.getAttribute('id');await link.click();
  await page.waitForURL(/\/diagrams\//);
  if(mode==='large-text')await page.addStyleTag({content:'html {font-size:32px!important;} * {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important;}'});
  const back=page.getByRole('link',{name:'Back to guide',exact:true});const box=await back.boundingBox();
  assert(box.x>=0&&box.x+box.width<=320&&box.y>=0&&box.y+box.height<=900,'Return link escapes the enlarged viewport');
  assert(await page.locator('.diagram-viewer__header').evaluate(el=>el.scrollWidth<=el.clientWidth),'Viewer header clips its contents');
  assert(await page.locator('.diagram-viewer__image').evaluate(el=>el.complete&&el.naturalWidth>0));
  await back.click();
  if(mode==='large-text')await page.waitForURL(pageUrl('docs/commands/country-finder/detailed.html'));else await page.waitForURL(`${pageUrl('docs/commands/country-finder/detailed.html')}#${anchor}`);
  if(scripts)await page.waitForFunction(id=>document.activeElement.id===id,anchor);
  console.log(`PASS viewer ${mode}: readable image and reachable guide return`);
  await context.close();
 }
 // The floating arrow appears after scrolling and leaves the article unobscured.
 for(const width of [320,390,800,1280]) for(const scheme of ['light','dark']) {
  const reducedMotion=width===320||width===800?'reduce':'no-preference';
  const context=await createContext({viewport:{width,height:800},colorScheme:scheme,reducedMotion});
  const page=await context.newPage();
  await page.addInitScript(()=>{
   const scroll=window.scrollTo.bind(window);
   window.scrollRequests=[];
   window.scrollTo=(...args)=>{window.scrollRequests.push(args);scroll(...args);};
  });
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
  const button=page.getByRole('button',{name:'Back to top',exact:true,includeHidden:true});
  assert.equal(await button.count(),1);
  assert.equal(await page.locator('a#back-to-top').count(),0,'Old footer link remains');
  assert.equal(await button.isVisible(),false,'Arrow appears before scrolling');
  await page.evaluate(()=>scrollTo({top:400,behavior:'instant'}));
  assert.equal(await button.isVisible(),false,'Arrow appears before the scroll threshold');
  await page.evaluate(()=>scrollTo({top:600,behavior:'instant'}));
  await button.waitFor({state:'visible'});
  const box=await button.boundingBox();
  const content=await page.locator('#main-content').boundingBox();
  assert(box.width>=44 && box.height>=44,'Arrow has an undersized touch target');
  assert(box.x>=content.x+content.width+8,'Arrow overlaps the article');
  assert(box.x+box.width<=width && box.y+box.height<=800,'Arrow is outside the viewport');
  assert.equal(await button.locator('svg').getAttribute('aria-hidden'),'true');
  await page.evaluate(()=>scrollTo({top:900,behavior:'instant'}));
  const scrolledBox=await button.boundingBox();
  assert.equal(scrolledBox.y,box.y,'Arrow moves with the article');
  await button.click();
  await page.waitForFunction(()=>scrollY===0);
  assert.equal(await button.isVisible(),false,'Arrow remains visible at the top');
  assert(await page.locator('#main-content h1').evaluate(el=>el===document.activeElement),'Focus did not return to the page heading');
  assert.equal(await page.evaluate(()=>window.scrollRequests.at(-1)[0].behavior),reducedMotion==='reduce'?'instant':'smooth');
  await page.evaluate(()=>scrollTo({top:900,behavior:'instant'}));
  await button.waitFor({state:'visible'});
  await page.locator('.footer-links a').last().focus();
  await page.keyboard.press('Tab');
  assert(await button.evaluate(el=>el===document.activeElement && el.matches(':focus-visible') && getComputedStyle(el).outlineStyle!=='none'),'Arrow has no keyboard focus indicator');
  await button.press(width===320||width===800?'Enter':'Space');
  await page.waitForFunction(()=>scrollY===0);
  assert.equal(await button.isVisible(),false);
  await page.evaluate(()=>scrollTo({top:900,behavior:'instant'}));
  await button.waitFor({state:'visible'});
  await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
  await button.waitFor({state:'hidden'});
  await page.evaluate(()=>scrollTo({top:900,behavior:'instant'}));
  await button.waitFor({state:'visible'});
  await page.reload();
  await button.waitFor({state:'visible'});
  await page.emulateMedia({media:'print'});
  assert.equal(await button.isVisible(),false,'Arrow appears in print');
  console.log(`PASS ${width}px ${scheme}: floating arrow, clear article gutter, scroll visibility, pointer/keyboard return, ${reducedMotion} motion, restored scroll and print`);
  await context.close();
 }
 // Late image bytes must not move text below the diagram.
 {
  const context=await createContext();const page=await context.newPage();
  await page.addInitScript(()=>{window.diagramShift=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.diagramShift+=e.value;}).observe({type:'layout-shift',buffered:true});});
  await page.route('**/assets/diagrams/*.svg',async route=>{await new Promise(resolve=>setTimeout(resolve,500));await route.continue();});
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
  assert(await page.evaluate(()=>window.diagramShift<0.01));
  console.log('PASS delayed diagram download: reserved space remains stable');await context.close();
 }
 // A slow first search must retain text typed before the index becomes ready.
 {
  const context=await createContext();const page=await context.newPage();let count=0;
  await page.route('**/search-data.json',async route=>{count++;await new Promise(resolve=>setTimeout(resolve,500));await route.continue();});
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.locator('#search-input').fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert.equal(await page.locator('#search-input').inputValue(),'country');assert.equal(count,1);
  console.log('PASS slow search: first query preserved, one request');await context.close();
 }
 // An unchanged failed index needs a deliberate retry, including network and parse failures.
 for(const fault of ['http','network','json']) {
  const context=await createContext({viewport:{width:390,height:800}});const page=await context.newPage();let count=0;
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.route('**/search-data.json',async route=>{
   count++;
   if(count>1)return route.continue();
   if(fault==='network')return route.abort();
   await route.fulfill({status:fault==='http'?503:200,body:fault==='json'?'{invalid':'Unavailable'});
  });
  await page.goto(pageUrl('docs/commands/country-finder.html'));
  await page.locator('#menu-button').click();
  const query=page.locator('#search-input');const retry=page.getByRole('button',{name:'Search unavailable. Retry search.',exact:true});
  await query.focus();await retry.waitFor({state:'visible'});
  await query.pressSequentially('country',{delay:40});
  assert.equal(count,1,'Typing retried a failed search prerequisite');
  assert.match(await page.locator('#search-status').textContent(),/Search unavailable/);
  assert(await page.locator('#search-status').evaluate(el=>{const box=el.getBoundingClientRect();return box.x>=0&&box.right<=innerWidth&&box.y>=0&&box.bottom<=innerHeight;}),'Search error escaped the viewport');
  if(fault==='network')await query.press('Enter');else {await query.press('Tab');assert(await retry.evaluate(el=>el===document.activeElement));await page.keyboard.press('Enter');}
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert.equal(await query.inputValue(),'country');assert.equal(count,2);assert.equal(await retry.isVisible(),false);
  assert.equal(await page.locator('#search-status').textContent(),'');assert.deepEqual(errors,[]);
  console.log(`PASS ${fault} search failure: visible feedback, no typing retries, keyboard retry and preserved query`);await context.close();
 }
 // Failed manual preferences never replace the working theme or get saved.
 for(const scheme of ['light','dark']) {
  const context=await createContext({colorScheme:scheme});const page=await context.newPage();const target=scheme==='light'?'dark':'light';let count=0;
  await page.goto(pageUrl('docs/commands/country-finder/detailed.html'));await background(scheme)(page);
  await page.route(`**/just-the-docs-${target}.css`,async route=>{count++;await new Promise(resolve=>setTimeout(resolve,300));if(count===1)await route.abort();else await route.continue();});
  const chooser=page.locator('#theme-mode');await chooser.selectOption(target);
  assert.equal(await page.evaluate(()=>localStorage.getItem('agent-compass-theme')),null,'Pending theme was persisted');
  await page.waitForFunction(()=>document.getElementById('theme-status').textContent.includes('unavailable'));
  assert.equal(await chooser.inputValue(),'system');await background(scheme)(page);
  assert.equal(await page.evaluate(()=>localStorage.getItem('agent-compass-theme')),null,'Failed theme was persisted');
  await chooser.selectOption(target);await background(target)(page);
  await page.waitForFunction(target=>localStorage.getItem('agent-compass-theme')===target,target);
  assert.equal(await page.locator('#theme-status').textContent(),'');
  assert((await page.locator('[data-diagram-full-size]').first().getAttribute('href')).endsWith(`#theme-${target}`));
  await page.reload();await background(target)(page);assert.equal(await chooser.inputValue(),target);
  console.log(`PASS failed ${target} preference: rollback, delayed persistence, successful retry, diagram links and reload`);await context.close();
 }
 // Automatic appearance failures keep System and later recover without saving an override.
 {
  const context=await createContext({colorScheme:'light'});const page=await context.newPage();let fail=true;
  await page.goto(pageUrl('docs/commands/country-finder.html'));await background('light')(page);
  await page.route('**/just-the-docs-dark.css',route=>fail?route.abort():route.continue());
  await page.emulateMedia({colorScheme:'dark'});
  await page.waitForFunction(()=>document.getElementById('theme-status').textContent.includes('unavailable'));
  assert.equal(await page.locator('#theme-mode').inputValue(),'system');await background('light')(page);
  fail=false;await page.emulateMedia({colorScheme:'light'});await page.waitForFunction(()=>document.getElementById('theme-status').textContent==='');await page.emulateMedia({colorScheme:'dark'});await background('dark')(page);
  assert.equal(await page.locator('#theme-mode').inputValue(),'system');assert.equal(await page.evaluate(()=>localStorage.getItem('agent-compass-theme')),null);
  console.log('PASS automatic theme failure: retained System, later recovery and no saved override');await context.close();
 }
 // Clipboard feedback follows settled writes and only the latest successful copy.
 for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,colorScheme:scheme});const page=await context.newPage();const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.addInitScript(()=>{
   window.copyWrites=[];
   Object.defineProperty(navigator,'clipboard',{value:{writeText:text=>new Promise((resolve,reject)=>window.copyWrites.push({text,resolve,reject}))}});
  });
  await page.goto(pageUrl('docs/setup/claude.html#terminal'));await page.locator('[data-setup-tabs][data-enhanced]').waitFor();
  await page.clock.install();await page.clock.pauseAt(new Date());
  const blocks=page.locator('div.highlighter-rouge:visible');const first=blocks.nth(0);const second=blocks.nth(1);
  const button=first.locator('button');const status=first.locator('.copy-status');const other=second.locator('.copy-status');
  assert.equal(await button.evaluate(el=>getComputedStyle(el).opacity),'1','Touch copy control needs hover');
  await button.click();await button.evaluate(el=>el.click());
  assert.equal(await page.evaluate(()=>window.copyWrites.length),1,'Pending copies were duplicated');
  assert.equal(await first.locator('use').getAttribute('xlink:href'),'#svg-copy');
  await page.clock.runFor(2500);assert.equal(await status.textContent(),'Copying…');
  await page.evaluate(()=>window.copyWrites[0].resolve());assert.equal(await status.textContent(),'Copied');
  await second.locator('button').click();assert.equal(await status.textContent(),'Copied','A pending write cleared another success');
  await page.evaluate(()=>window.copyWrites[1].reject(new Error('Clipboard denied')));
  assert.match(await other.textContent(),/Try again or select the code/);assert.equal(await status.textContent(),'Copied','A failed write cleared another success');
  await second.locator('button').click();assert.equal(await other.textContent(),'','A new attempt retained stale copy error');
  await page.evaluate(()=>window.copyWrites[2].resolve());assert.equal(await status.textContent(),'');assert.equal(await other.textContent(),'Copied');
  await page.clock.runFor(1999);assert.equal(await other.textContent(),'Copied');
  await page.clock.runFor(1);assert.equal(await other.textContent(),'');assert.deepEqual(errors,[]);
  await second.locator('button').focus();await page.keyboard.press('Tab');await page.keyboard.press('Shift+Tab');
  assert(await second.locator('button').evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle!=='none'));
  console.log(`PASS ${scheme} touch clipboard: visible control, pending deduplication, confirmed success, recoverable failure, latest confirmation and two-second timer`);await context.close();
 }
 // Enlarged text and off-screen anchors must keep recovery inside the viewport.
 for(const kind of ['copy','theme','search']) {
  const context=await createContext({viewport:{width:320,height:844},hasTouch:true,isMobile:true,colorScheme:'light'});const page=await context.newPage();
  if(kind==='copy')await page.addInitScript(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('Denied'))}}));
  if(kind==='search')await page.route('**/search-data.json',route=>route.abort());
  await page.goto(pageUrl(kind==='copy'?'docs/setup/claude.html#terminal':'docs/commands/country-finder.html'));
  await page.addStyleTag({content:'html{font-size:200%!important;}'});
  await page.waitForFunction(()=>document.documentElement.classList.contains('compass-compact'));
  if(kind==='copy')await page.locator('div.highlighter-rouge:visible > button').first().click();
  else {
   await page.locator('#menu-button').click();
   if(kind==='theme'){await page.route('**/just-the-docs-dark.css',route=>route.abort());await page.selectOption('#theme-mode','dark');}
   else await page.locator('#search-input').fill('country');
  }
  const selector=kind==='copy'?'.copy-status:not(:empty)':`#${kind}-status`;
  await page.waitForFunction(selector=>{
   const el=document.querySelector(selector);if(!el?.textContent.trim())return false;
   const box=el.getBoundingClientRect();return box.width>0&&box.x>=0&&box.right<=innerWidth&&box.y>=0&&box.bottom<=innerHeight;
  },selector);
  const status=page.locator(selector);
  await page.setViewportSize({width:390,height:600});
  await page.waitForFunction(selector=>{const box=document.querySelector(selector).getBoundingClientRect();return box.x>=0&&box.right<=innerWidth&&box.y>=0&&box.bottom<=innerHeight;},selector);
  assert(await status.isVisible());
  console.log(`PASS enlarged ${kind} feedback: viewport containment before and after resize`);await context.close();
 }
 for(const fault of ['no-js','storage-blocked','saved-light','saved-dark','dark-css-failed']) {
  const context=await createContext({javaScriptEnabled:fault!=='no-js',colorScheme:'dark'});const page=await context.newPage();
  if(fault==='storage-blocked')await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));
  if(fault.startsWith('saved-'))await page.addInitScript(mode=>localStorage.setItem('agent-compass-theme',mode),fault.slice(6));
  if(fault==='dark-css-failed')await page.route('**/just-the-docs-dark.css',route=>route.abort());
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
  if(fault==='no-js')assert.equal(await page.locator('#back-to-top').isVisible(),false,'Nonfunctional arrow appears without JavaScript');
  const expected=['no-js','saved-light','dark-css-failed'].includes(fault)?'light':'dark';
  await page.waitForFunction(expected=>{
   const color=getComputedStyle(document.body).backgroundColor;
   return expected==='dark'?color==='rgb(39, 38, 43)':color==='rgb(255, 255, 255)';
  },expected);
  assert(await page.locator('figure.mermaid img').evaluateAll(imgs=>imgs.every(img=>img.complete&&img.naturalWidth>0)));
  console.log(`PASS ${fault}: readable ${expected} theme and diagrams`);await context.close();
 }
 const shortcut = (await readFile(resolve(root, 'assets/js/just-the-docs.js'), 'utf8')).match(/add event listener on ctrl[^]*?e\.key === '([^']+)'/);
 if (shortcut) {
  const context=await createContext();const page=await context.newPage();
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  await page.keyboard.press(`Control+${shortcut[1]}`);
  assert.equal(await page.evaluate(()=>document.activeElement.id),'search-input');
  await page.locator('#search-input').fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  console.log('PASS configured search shortcut before index loading');await context.close();
 }
 // Enlarged text and spacing must leave setup controls, breadcrumbs and search reachable.
 for(const width of [320,800,1280]) for(const scheme of ['light','dark']) for(const mode of ['large-text','spacing']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme});const page=await context.newPage();
  for(const path of ['docs/setup/codex.html','docs/commands/salary-calculator/step4-table-calculation.html']) {
   await page.goto(pageUrl(path));
   await page.addStyleTag({content:mode==='large-text'?'html {font-size:200%!important;}':'* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important;} p {margin-bottom:2em!important;}'});
   await page.waitForFunction(()=>document.documentElement.classList.contains('compass-compact')===(!matchMedia('(min-width:50rem)').matches||innerWidth<50*parseFloat(getComputedStyle(document.documentElement).fontSize)));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Adjusted text causes horizontal page scrolling');
   assert(await page.locator('.breadcrumb-nav-list-item').evaluateAll(items=>items.every(el=>{
    const box=el.getBoundingClientRect(),parent=el.parentElement.getBoundingClientRect();return box.left>=parent.left-1&&box.right<=parent.right+1;
   })),'Breadcrumbs escape their available width');
   if(path.includes('/setup/')) {
    assert(await page.locator('[data-setup-tab]').evaluateAll(tabs=>tabs.every(el=>{
     const box=el.getBoundingClientRect(),parent=el.parentElement.getBoundingClientRect();return box.left>=parent.left-1&&box.right<=parent.right+1;
    })),'Setup tabs overflow');
    await page.locator('#desktop-tab').focus();await page.keyboard.press('End');
    assert.equal(await page.locator('#terminal-tab').getAttribute('aria-selected'),'true');
   }
  }
  const menu=page.locator('#menu-button');if(await menu.isVisible())await menu.click();
  assert(await page.locator('.header-controls').evaluate(el=>el.getBoundingClientRect().right<=innerWidth),'Header controls overflow');
  const query=page.locator('#search-input');await query.fill('salary');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert(await page.locator('#search-results').evaluate(el=>{
   const box=el.getBoundingClientRect();return box.left>=-1&&box.right<=innerWidth+1&&box.top>=0&&box.bottom<=innerHeight+1&&box.height>0;
  }),'Adjusted search results escape the viewport');
  await query.press('Escape');
  assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),false);
  console.log(`PASS ${width}px ${scheme} ${mode}: reflow, wrapping breadcrumbs/setup tabs, keyboard activation and contained search`);
  await context.close();
 }
 // A layout transition keeps active search and focus, including a disappearing menu button.
 {
  const context=await createContext({viewport:{width:1280,height:900}});const page=await context.newPage();
  await page.goto(pageUrl('docs/commands/country-finder.html'));
  const query=page.locator('#search-input');await query.fill('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  await query.press('ArrowDown');
  const focused=await page.evaluateHandle(()=>document.activeElement);
  await page.addStyleTag({content:'html {font-size:200%!important;}'});
  await page.waitForFunction(()=>document.documentElement.classList.contains('compass-compact'));
  assert(await focused.evaluate(el=>el===document.activeElement&&el.checkVisibility()),'Compact transition lost search focus');
  assert.equal(await query.inputValue(),'country');
  assert.equal(await page.locator('#menu-button').getAttribute('aria-expanded'),'true');
  await page.setViewportSize({width:800,height:900});
  await page.evaluate(()=>document.documentElement.style.setProperty('font-size','100%','important'));
  await page.waitForFunction(()=>!document.documentElement.classList.contains('compass-compact'));
  assert(await focused.evaluate(el=>el===document.activeElement&&el.checkVisibility()),'Desktop transition lost search focus');
  assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),true);
  await query.focus();await query.press('Escape');
  await page.setViewportSize({width:390,height:900});
  await page.waitForFunction(()=>document.documentElement.classList.contains('compass-compact'));
  await page.locator('#menu-button').focus();
  await page.setViewportSize({width:1280,height:900});
  await page.waitForFunction(()=>document.activeElement===document.querySelector('.site-title'));
  console.log('PASS responsive transitions: search, selected-result focus and menu focus remain usable');
  await context.close();
 }
 // The release follows the theme chooser while home remains a native sidebar link.
 for (const width of [320, 390, 800, 1024, 1280]) for (const scheme of ['light', 'dark']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
  await context.route('https://github.com/myowinthein/agent-compass/releases/tag/*', route=>route.fulfill({contentType:'text/html',body:'<!doctype html><title>Release fixture</title>'}));
  const page=await context.newPage();
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  const title=page.locator('.site-title');
  const version=page.locator('.header-controls .site-version');
  assert(await title.evaluate(el=>el.scrollWidth<=el.clientWidth+1),'Project title is truncated');
  await title.evaluate(el=>el.style.fontFamily='Verdana, sans-serif');
  assert(await title.evaluate(el=>el.scrollWidth<=el.clientWidth+1),`Project title is truncated with a wider fallback font at ${width}px ${scheme}`);
  await title.evaluate(el=>el.style.removeProperty('font-family'));
  const label=(await version.textContent()).trim();
  const release=`https://github.com/myowinthein/agent-compass/releases/tag/${label}`;
  assert.equal(await title.getAttribute('href'),'/agent-compass/');
  assert.equal(await version.getAttribute('href'),release);
  assert.equal(await version.getAttribute('target'),null);
  assert(await version.evaluate(a=>getComputedStyle(a,'::after').maskImage.includes('external-link.svg')));
  const box=await title.boundingBox();
  await page.mouse.click(box.x+box.width-3,box.y+box.height-3);
  await page.waitForURL(`${origin}/agent-compass/`);
  await page.goto(`${origin}/agent-compass/docs/commands/country-finder.html`);
  if(width<800)await page.locator('#menu-button').click();
  const chooser=page.getByRole('combobox',{name:'Theme',exact:true});
  const chooserBox=await chooser.boundingBox();
  const labelBox=await page.locator('label[for="theme-mode"]').boundingBox();
  assert(labelBox.width<=1 && labelBox.height<=1,'Theme label must be visually hidden');
  const versionBox=await version.boundingBox();
  assert(versionBox.height>=24 && versionBox.width>=24);
  assert(versionBox.x>=chooserBox.x+chooserBox.width,'Version must sit to the right of the theme chooser');
  assert(Math.abs(versionBox.y+versionBox.height/2-chooserBox.y-chooserBox.height/2)<1,'Version and theme chooser must align vertically');
  assert(versionBox.x+versionBox.width<=width,'Version overflows the viewport');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Header causes horizontal scrolling');
  await chooser.focus();
  await page.keyboard.press('Tab');
  const focused=page.locator('.header-controls .site-version');
  assert(await focused.evaluate(a=>a===document.activeElement && a.matches(':focus-visible') && getComputedStyle(a).outlineStyle!=='none'));
  await page.keyboard.press('Enter');
  await page.waitForURL(release);
  assert.equal(context.pages().length,1);
  console.log(`PASS ${width}px ${scheme}: home area, hidden theme label, version beside chooser, separate release link and keyboard activation`);
  await context.close();
 }
 console.log('Passed browser checks.');
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
