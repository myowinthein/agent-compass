import assert from 'node:assert/strict';
import { checkListCounterContrast, checkThemeColors } from './check-theme-colors.mjs';
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
async function openCompactMenu(page) {
 const menu=page.locator('#menu-button');
 await menu.waitFor({state:'visible'});
 if(await menu.getAttribute('aria-expanded')!=='true')await menu.click();
}
try {
 browser=await chromium.launch({executablePath:process.env.COMPASS_DOCS_CHROME||(process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome'),headless:true});
 // Short theme feedback fits its text and sits close to the dropdown itself.
 for(const width of [390,800,1280]) for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
  const page=await context.newPage();let release;
  const download=new Promise(resolve=>{release=resolve;});
  try {
   await page.goto(pageUrl(''));
   if(await page.locator('#menu-button').isVisible())await openCompactMenu(page);
   const target=scheme==='light'?'dark':'light';
   await page.route(`**/just-the-docs-${target}.css?v=*`,async route=>{await download;await route.abort();});
   await page.locator('#theme-mode').selectOption(target);
   await page.waitForFunction(()=>document.getElementById('theme-status').textContent==='Loading theme…');
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
   const layout=await page.locator('#theme-status').evaluate(el=>{
    const box=el.getBoundingClientRect(),field=document.getElementById('theme-mode').getBoundingClientRect();
    const style=getComputedStyle(el),range=document.createRange();range.selectNodeContents(el);
    const padding=parseFloat(style.paddingLeft)+parseFloat(style.paddingRight);
    const border=parseFloat(style.borderLeftWidth)+parseFloat(style.borderRightWidth);
    return {extra:box.width-range.getBoundingClientRect().width-padding-border,gap:box.top-field.bottom,expectedGap:parseFloat(getComputedStyle(document.documentElement).fontSize)/4};
   });
   assert(Math.abs(layout.extra)<1,'Theme loading box reserves unused width');
   assert(Math.abs(layout.gap-layout.expectedGap)<1,'Theme loading box is detached from the dropdown');
   await page.evaluate(()=>scrollTo(0,8));
   await page.waitForFunction(()=>scrollY===8);
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(resolve)));
   assert(await page.locator('#theme-status').evaluate(el=>Math.abs(el.getBoundingClientRect().top-document.getElementById('theme-mode').getBoundingClientRect().bottom-parseFloat(getComputedStyle(document.documentElement).fontSize)/4)<1),'Theme feedback detached while its dropdown scrolled');
   for(const message of ['Loading theme…','Theme unavailable. Choose a theme to try again.']) {
    if(message.startsWith('Theme unavailable')) {
     release();
     await page.waitForFunction(()=>document.getElementById('theme-status').textContent==='Theme unavailable. Choose a theme to try again.');
    }
    await page.evaluate(()=>scrollTo(0,document.getElementById('theme-mode').getBoundingClientRect().bottom+scrollY+50));
    await page.waitForFunction(()=>document.getElementById('theme-mode').getBoundingClientRect().bottom<=0);
    await page.locator('#theme-status').waitFor({state:'hidden'});
    assert.equal(await page.locator('#theme-status').textContent(),message,'Scrolling cleared the theme result');
    await page.evaluate(()=>scrollTo(0,0));
    await page.locator('#theme-status').waitFor({state:'visible'});
    assert(await page.locator('#theme-status').evaluate(el=>Math.abs(el.getBoundingClientRect().top-document.getElementById('theme-mode').getBoundingClientRect().bottom-parseFloat(getComputedStyle(document.documentElement).fontSize)/4)<1),'Theme feedback did not return beside the dropdown');
   }
   await page.unroute(`**/just-the-docs-${target}.css?v=*`);
   await page.locator('#theme-mode').selectOption(target);
   await background(target)(page);
   assert.equal(await page.locator('#theme-status').textContent(),'');
   console.log(`PASS ${width}px ${scheme}: content-sized theme feedback follows its dropdown on scroll, hides offscreen and returns`);
  } finally {release();await context.close();}
 }
 for(const width of [1280,390]) {
  for(const scheme of ['light','dark']) {
   const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
   const page=await context.newPage();
   const requests=[];const errors=[];
   context.on('request',r=>requests.push(r.url()));
   page.on('pageerror',e=>errors.push(e.message));
   await page.addInitScript(()=>{window.shifts=[];new PerformanceObserver(list=>window.shifts.push(...list.getEntries().filter(e=>!e.hadRecentInput).map(e=>e.value))).observe({type:'layout-shift',buffered:true});});
   await page.goto(`${origin}/agent-compass/docs/commands/country-finder/detailed.html`);
   await page.waitForTimeout(300);
   assert(!requests.some(url=>url.includes('search-data.json')),'Search downloaded before interaction');
   assert(!requests.some(url=>url.includes('mermaid')),'Browser downloaded Mermaid');
   assert(!requests.some(url=>/search-worker\.js|vendor\/lunr/.test(url)),'Search code loaded before interaction');
   assert.equal(requests.filter(url=>/just-the-docs-(default|light|dark)\.css/.test(url)).length,1,'Duplicate initial theme stylesheets');
   assert(requests.some(url=>new URL(url).pathname.endsWith(`just-the-docs-${scheme}.css`)),'Wrong system theme');
   for(const url of requests.filter(url=>/\/assets\/(?:css\/.*\.css|js\/just-the-docs\.js)(?:\?|$)/.test(url)))assert(/^[0-9a-f]{16}$/.test(new URL(url).searchParams.get('v')||''),'Generated stylesheet or loader has no content version');
   assert.equal(await page.locator('figure.mermaid img').evaluateAll(imgs=>imgs.every(img=>img.complete&&img.naturalWidth>0)),true,'Diagram not visible');
   const cls=await page.evaluate(()=>window.shifts.reduce((sum,n)=>sum+n,0));
   assert(cls<0.01,`Initial layout shifted: ${cls}`);
   await checkThemeColors(page, scheme);
   const query=page.locator('#search-input');
   if(width===390)await page.locator('#menu-button').click();
   await query.fill('salary');
   await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
   assert.equal(requests.filter(url=>url.includes('search-data.json')).length,1,'Search initialized multiple times');
   assert(/^[0-9a-f]{16}$/.test(new URL(requests.find(url=>url.includes('search-data.json'))).searchParams.get('v')||''),'Search index has no content version');
   await query.evaluate(input => input.blur());
   assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),false);
   await query.focus();
   await page.waitForFunction(()=>document.documentElement.classList.contains('search-active'));
   await query.press('Escape');
   assert.equal(await query.inputValue(),'');
   await page.locator('#theme-mode').selectOption(scheme==='light'?'dark':'light');
   await page.waitForFunction(expected=>new URL(document.querySelector('link[rel="stylesheet"]').href).pathname.endsWith(`just-the-docs-${expected}.css`),scheme==='light'?'dark':'light');
   await checkThemeColors(page, scheme==='light'?'dark':'light');
   assert(/^[0-9a-f]{16}$/.test(new URL(await page.locator('#compass-theme-stylesheet').getAttribute('href'),page.url()).searchParams.get('v')||''),'Theme change lost its content version');
   assert.equal(errors.length,0,errors.join('\n'));
   await page.goto(pageUrl('docs/setup/codex.html'));
   await checkListCounterContrast(page, scheme==='light'?'dark':'light');
   console.log(`PASS ${width}px ${scheme}: one theme stylesheet, no initial index, static diagrams, CLS ${cls.toFixed(3)}, search, theme switching and list-counter contrast`);
   await context.close();
  }
 }
 // Exercise the worker's real tokenizer, prefix/fuzzy matching and preview metadata.
 {
  const context=await createContext();const page=await context.newPage();
  const loader=await readFile(resolve(root,'assets/js/just-the-docs.js'),'utf8');
  const workerUrl=JSON.parse(loader.match(/new Worker\(("[^"]+")\)/)[1]);
  const libraryUrl=JSON.parse(loader.match(/libraryUrl: ("[^"]+")/)[1]);
  const fixture={
   a:{title:'Refactor',doc:'Refactor',content:'Preserve behavior and improve project code.',relUrl:'/refactor',url:'/fixture/refactor'},
   b:{title:'A guide',doc:'A guide',content:'Refactor project modules safely.',relUrl:'/guide',url:'/fixture/guide'},
   c:{title:'Work flow',doc:'Work flow',content:'A separate process for a release.',relUrl:'/work-flow',url:'/fixture/work-flow'}
  };
  await context.route('**/fixtures/search.json',route=>route.fulfill({contentType:'application/json',body:JSON.stringify(fixture)}));
  await page.goto(pageUrl('docs/commands/country-finder.html'));
  assert.equal(await page.evaluate(()=>typeof window.lunr),'undefined','Lunr loaded on the page thread');
  const replies=await page.evaluate(async({workerUrl,libraryUrl,indexUrl})=>{
   const worker=new Worker(workerUrl);const pending=new Map();let ready;
   const initialized=new Promise(resolve=>{ready=resolve;});
   worker.onmessage=({data})=>{if(data.type==='ready')ready();else if(data.type==='results'){pending.get(data.id)(data);pending.delete(data.id);}};
   worker.postMessage({type:'init',libraryUrl,indexUrl});await initialized;
   const replies=[];for(const input of ['refac','refctor','work/flow','zzzzzzzzzzzzzzzzzzzzzzzz']){
    const id=replies.length+1;const reply=new Promise(resolve=>pending.set(id,resolve));worker.postMessage({type:'query',id,input});replies.push(await reply);
   }
   worker.terminate();return replies;
  },{workerUrl,libraryUrl,indexUrl:pageUrl('fixtures/search.json')});
  for(const reply of replies.slice(0,2))assert.equal(reply.results.map(r=>r.ref).sort().join(','),'a,b','Prefix or fuzzy search changed');
  assert.equal(replies[0].results[0].ref,'a','Exact title boost changed');
  assert(Object.values(replies[0].results[0].matchData.metadata).some(m=>m.title?.position?.some(p=>p[0]===0&&p[1]===8)),'Worker lost title highlight positions');
  assert.equal(replies[2].results.map(r=>r.ref).join(','),'c','Slash-separated search changed');
  assert.equal(replies[3].results.length,0);
  for(const reply of replies)assert.equal(Object.keys(reply.docs).sort().join(','),reply.results.map(r=>r.ref).sort().join(','),'Worker returned unrelated documents');
  console.log('PASS search worker: prefix/fuzzy matching, title boost, separators, highlight metadata and matched documents');await context.close();
 }
 // A late response must not replace newer results or reopen cleared search.
 {
  const context=await createContext();const page=await context.newPage();
  await page.addInitScript(()=>{
   const Native=Worker;window.workerReplies=[];window.holdSearchReply=false;
   window.Worker=class extends Native{
    constructor(...args){
     super(...args);
     this.addEventListener('message',event=>{
      if(event.data.type!=='results')return;
      if(window.holdSearchReply){
       event.stopImmediatePropagation();
       window.heldSearchReply={worker:this,data:event.data};
       return;
      }
      workerReplies.push(event.data.id);
     });
    }
   };
  });
  await context.route('**/search-worker.js?v=*',async route=>{const response=await route.fetch();await route.fulfill({response,body:(await response.text())+"\nconst send=self.postMessage.bind(self);self.postMessage=data=>{if(data.type==='results'&&data.id===1)setTimeout(()=>send(data),250);else send(data);};"});});
  await page.goto(pageUrl('docs/commands/country-finder.html'));const query=page.locator('#search-input');
  await query.fill('country');await page.waitForFunction(()=>!document.getElementById('search-input').hasAttribute('aria-busy'));
  await query.fill('salary');await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  const latest=await page.locator('#search-results a').evaluateAll(links=>links.map(a=>a.href));
  await page.waitForFunction(()=>workerReplies.includes(1)&&workerReplies.includes(2));
  assert.equal(await page.locator('#search-results > ul').count(),1,'Late worker results appended an obsolete list');
  assert.equal((await page.locator('#search-results a').evaluateAll((links,length)=>links.slice(0,length).map(a=>a.href),latest.length)).join('|'),latest.join('|'),'Late worker results replaced the latest query');
  await query.press('Escape');assert.equal(await page.locator('#search-results a').count(),0);assert.equal(await query.inputValue(),'');
  await page.evaluate(()=>{window.holdSearchReply=true;});
  await query.fill('portal');await page.waitForFunction(()=>window.heldSearchReply);
  assert(await page.evaluate(()=>window.heldSearchReply.data.results.length>0),'Held query had no results to repopulate search');
  await query.press('Escape');
  await page.evaluate(()=>{
   window.holdSearchReply=false;
   const {worker,data}=window.heldSearchReply;
   worker.dispatchEvent(new MessageEvent('message',{data}));
  });
  await page.waitForFunction(()=>workerReplies.includes(3));
  assert.equal(await query.inputValue(),'','Late reply restored the cleared query');
  assert.equal(await page.locator('#search-results a').count(),0,'Late reply repopulated cleared results');
  assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('search-active')),false,'Late reply reopened search');
  console.log('PASS search worker: out-of-order replies keep the latest results and a reply after Escape cannot reopen search');await context.close();
 }
 // Startup failure and a later crash retain an explicit retry with one UI binding.
 for(const failure of ['startup','query']) {
  const context=await createContext();const page=await context.newPage();let workers=0;
  await context.route('**/search-worker.js?v=*',async route=>{
   workers++;if(workers===1&&failure==='startup')return route.abort();
   const response=await route.fetch();let body=await response.text();
   if(workers===1&&failure==='query')body+="\nconst handle=self.onmessage;self.onmessage=event=>{if(event.data.type==='query'&&event.data.input==='crash-fixture')throw new Error('Fixture worker failure');return handle(event);};";
   await route.fulfill({response,body});
  });
  await page.goto(pageUrl('docs/commands/country-finder.html'));const query=page.locator('#search-input');await query.fill('country');
  if(failure==='query'){await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);await query.fill('crash-fixture');}
  await page.waitForFunction(()=>document.getElementById('search-status').textContent.includes('Search unavailable'));
  await query.fill('salary');assert.equal(workers,1,'Typing restarted a failed worker');
  await page.locator('#search-retry').click();await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  assert.equal(workers,2);assert.equal(await query.inputValue(),'salary');assert.equal(await page.locator('#search-retry').isVisible(),false);
  await query.press('ArrowDown');assert(await page.locator('#search-results a').first().evaluate(a=>a===document.activeElement),'Retry installed duplicate keyboard handlers');
  console.log(`PASS worker ${failure} failure: preserved input, deliberate retry and one keyboard binding`);await context.close();
 }
 // The closing fade must not swallow the next navigation click.
 for(const scheme of ['light','dark']) for(const reducedMotion of ['no-preference','reduce']) {
  const context=await createContext({viewport:{width:1280,height:900},colorScheme:scheme,reducedMotion});
  const page=await context.newPage();const guide=pageUrl('docs/commands/country-finder.html');await page.goto(guide);
  const query=page.locator('#search-input'),overlay=page.locator('.search-overlay'),link=page.locator('.guide-depth a').nth(1);
  const destination=new URL(await link.getAttribute('href'),page.url()).href;
  await query.fill('salary');await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  await overlay.evaluate(el=>el.getAnimations().forEach(animation=>animation.finish()));
  let box=await page.locator('#site-nav').getByRole('link',{name:'Home',exact:true}).boundingBox();
  await page.mouse.click(box.x+box.width/2,box.y+box.height/2);
  await page.waitForFunction(()=>!document.documentElement.classList.contains('search-active'));
  assert.equal(page.url(),guide,'The active search overlay allowed navigation instead of dismissing search');
  await query.focus();await page.waitForFunction(()=>document.documentElement.classList.contains('search-active'));
  await overlay.evaluate(el=>el.getAnimations().forEach(animation=>animation.finish()));
  await query.press('Escape');
  // Hold the fade in progress so this check cannot pass by waiting it out.
  if(reducedMotion==='no-preference') {
   await overlay.evaluate(el=>el.getAnimations().forEach(animation=>animation.pause()));
   assert(await overlay.evaluate(el=>parseFloat(getComputedStyle(el).opacity)>0),'The closing fade was removed');
  }
  box=await link.boundingBox();await page.mouse.click(box.x+box.width/2,box.y+box.height/2);
  await page.waitForURL(destination);
  console.log(`PASS ${scheme} ${reducedMotion}: active overlay dismisses search, closing overlay releases navigation immediately`);
  await context.close();
 }
 // Arrow navigation uses real link focus and keeps the selected result visible.
 for(const width of [390,1280]) for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width,height:390},colorScheme:scheme,reducedMotion:'reduce'});
  const page=await context.newPage();await page.goto(pageUrl('docs/commands/country-finder.html'));
  if(width<800)await page.locator('#menu-button').click();
  const query=page.locator('#search-input');await query.pressSequentially('country');
  await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>12);
  for(let i=0;i<12;i++)await page.keyboard.press('ArrowDown');
  const selected=page.locator('.search-result.active');
  assert(await selected.evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')),'Search selection has no real keyboard focus');
  assert(await selected.evaluate(el=>{const a=el.getBoundingClientRect(),r=document.getElementById('search-results').getBoundingClientRect();return a.top>=r.top-1&&a.bottom<=r.bottom+1;}),'Keyboard selection is outside the visible result list');
  assert(await page.locator('#search-results').evaluate(el=>el.scrollTop>0));
  await page.keyboard.press('Escape');
  assert(await query.evaluate(el=>el===document.activeElement));assert.equal(await query.inputValue(),'');
  assert.equal(await page.locator('#search-results').isVisible(),false);
  await query.fill('salary');await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  await page.keyboard.press('Tab');
  assert(await page.locator('.search-result.active').evaluate(el=>el===document.activeElement),'Tab focus and selected result diverged');
  const destination=new URL(await page.locator('.search-result.active').getAttribute('href'),page.url()).href;
  await page.keyboard.press('Enter');await page.waitForURL(destination);
  console.log(`PASS ${width}px ${scheme}: typed search, result scrolling, real link focus, Escape, Tab and Enter`);
  await context.close();
 }
 // Expanded search must fit even when the header has wrapped with larger text.
 for(const width of [800,1280]) for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width,height:390},colorScheme:scheme,reducedMotion:'reduce'});
  const page=await context.newPage();await page.goto(pageUrl('docs/commands/country-finder.html'));
  await page.addStyleTag({content:'html {font-size:32px!important;}'});
  await openCompactMenu(page);
  await page.locator('#search-input').fill('salary');await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
  for(const selector of ['#search-input','#search-results']) {
   const box=await page.locator(selector).boundingBox();
   assert(box.x>=0&&box.x+box.width<=width+1,`${selector} overflows with enlarged text`);
   assert(box.height>0&&box.y+box.height<=390+1,`${selector} is clipped in a short viewport`);
  }
  const title=await page.locator('.search-result-title').first().boundingBox();
  const preview=await page.locator('.search-result-previews').first().boundingBox();
  const stacked=await page.locator('#search-results').evaluate(el=>el.clientWidth<=28*parseFloat(getComputedStyle(document.documentElement).fontSize));
  if(stacked)assert(preview.y>=title.y+title.height-1,'Enlarged result columns did not stack in the narrow panel');
  else assert(preview.x>=title.x+title.width-1,'Wide result columns overlap');
  console.log(`PASS ${width}px ${scheme}: enlarged search field and results stay in the visible viewport`);
  await context.close();
 }
 // CSS masks retain the system link color in forced-colors palettes.
 for(const scheme of ['light','dark']) {
  const context=await createContext({colorScheme:scheme,forcedColors:'active'});const page=await context.newPage();
  await page.goto(pageUrl('docs/commands/country-finder.html'));
  const link=page.locator('.footer-links a[href^="https://github.com"]').first();
  const colors=await link.evaluate(el=>({text:getComputedStyle(el).color,icon:getComputedStyle(el,'::after').backgroundColor,body:getComputedStyle(document.body).backgroundColor}));
  assert.equal(colors.icon,colors.text);assert.notEqual(colors.icon,colors.body);
  console.log(`PASS forced colors ${scheme}: external icons retain the system link color`);await context.close();
 }
 // A label color regression must fail even while diagram lines/surfaces remain.
 for(const scheme of ['light','dark']) {
  const context=await createContext({colorScheme:scheme});const page=await context.newPage();
  await page.route('**/assets/diagrams/*.svg',async route=>{
   const response=await route.fetch();
   const body=(await response.text()).replace(/--diagram-text:\s*#[0-9a-f]+;/gi,'--diagram-text: var(--diagram-surface);');
   await route.fulfill({response,body});
  });
  await page.goto(pageUrl('docs/commands/country-finder/detailed.html'));await background(scheme)(page);
  await assert.rejects(()=>checkThemeColors(page,scheme),/diagram labels have insufficient contrast/);
  console.log(`PASS ${scheme}: unreadable diagram labels are rejected with unchanged lines and surfaces`);
  await context.close();
 }
 // Compact text links and focus indicators must leave surrounding words readable.
 for(const width of [320,800,1280]) for(const scheme of ['light','dark']) for(const forcedColors of ['none','active']) for(const enlarged of [false,true]) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme,forcedColors,reducedMotion:'reduce'});
  const page=await context.newPage();
  for(const [path,selectors] of [
   ['docs/commands/country-finder.html',['main p a[href$="#run-a-command"]','figcaption a','.footer-links a:first-child','.site-footer a:visible,footer .d-md-none a:visible']],
   ['', ['main a[href*="/docs/commands/country-finder.html"]','div.highlight[tabindex]']],
   ['docs/commands.html',['td a']],
   ['docs/known-issues.html',['details p a','summary']],
  ]) {
   await page.goto(pageUrl(path));
   if(enlarged)await page.addStyleTag({content:'html {font-size:200%!important;} * {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important;} p {margin-bottom:2em!important;}'});
   await page.locator('details').evaluateAll(details=>details.forEach(el=>el.open=true));
   for(const selector of selectors) {
    const target=page.locator(selector).first();
    const before=await target.evaluate(el=>({top:el.getBoundingClientRect().top+scrollY,height:document.documentElement.scrollHeight,background:getComputedStyle(el).backgroundColor}));
    await target.focus();
    // Let scroll-driven controls settle before checking the adjacent Tab stops.
    await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
    await page.keyboard.press('Shift+Tab');await page.keyboard.press('Tab');
    const result=await target.evaluate(el=>{
     const style=getComputedStyle(el);
     const textLink=el.matches('a:not([class]):not(.guide-depth a)');
     const width=parseFloat(style.outlineWidth),offset=parseFloat(style.outlineOffset);
     const luminance=color=>color.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
     let surface=el;while(getComputedStyle(surface).backgroundColor==='rgba(0, 0, 0, 0)')surface=surface.parentElement;
     const [low,high]=[style.outlineColor,getComputedStyle(surface).backgroundColor].map(luminance).sort((a,b)=>a-b);
     const contrast=(high+.05)/(low+.05);
     const frames=Array.from(el.getClientRects(),r=>({left:r.left-offset-width,right:r.right+offset+width,top:r.top-offset-width,bottom:r.bottom+offset+width,innerLeft:r.left-offset,innerRight:r.right+offset,innerTop:r.top-offset,innerBottom:r.bottom+offset}));
     const scope=el.closest('p,td,figcaption,.site-footer,.d-md-none');const collisions=[];
     if(scope) {
      const walker=document.createTreeWalker(scope,NodeFilter.SHOW_TEXT);
      for(let node;node=walker.nextNode();) {
       if(el.contains(node)||node.parentElement.closest('.sr-only,[hidden]'))continue;
       const range=document.createRange();
       for(const word of node.textContent.matchAll(/\S+/g)) {
        range.setStart(node,word.index);range.setEnd(node,word.index+word[0].length);
        for(const r of range.getClientRects())for(const f of frames) {
         const intersects=r.right>f.left+.5&&r.left<f.right-.5&&r.bottom>f.top+.5&&r.top<f.bottom-.5;
         const inside=r.left>=f.innerLeft&&r.right<=f.innerRight&&r.top>=f.innerTop&&r.bottom<=f.innerBottom;
         if(intersects&&!inside)collisions.push(word[0]);
        }
       }
      }
     }
     return {focused:el===document.activeElement&&el.matches(':focus-visible'),visible:style.outlineStyle==='solid'&&width>=2&&contrast>=3,textLink,background:style.backgroundColor,compact:!textLink||(['paddingRight','paddingLeft'].every(p=>parseFloat(style[p])<=2)&&style.lineHeight===getComputedStyle(el.parentElement).lineHeight),collisions,inViewport:frames.every(f=>f.left>=-.6&&f.top>=-.6&&f.right<=innerWidth+.6&&f.bottom<=innerHeight+.6),top:el.getBoundingClientRect().top+scrollY,height:document.documentElement.scrollHeight};
    });
    assert(result.focused&&result.visible,`${selector} lost its keyboard focus indicator`);
    assert(result.compact,`${selector} adds space around inline text`);
    if(result.textLink)assert.equal(result.background,before.background,`${selector} fills the link instead of outlining it`);
    assert.equal(result.collisions.length,0,`${selector} covers neighboring words: ${result.collisions.join(', ')}`);
    assert(result.inViewport,`${selector} focus frame is clipped by the viewport`);
    assert(Math.abs(result.top-before.top)<1&&result.height===before.height,`${selector} moves content when focus appears`);
   }
  }
  console.log(`PASS ${width}px ${scheme}, forced colors ${forcedColors}, enlarged ${enlarged}: compact links and contrasting outlines avoid adjacent text, clipping and layout shifts`);
  await context.close();
 }
 // Each sidebar row has one Tab stop, with keyboard and pointer submenu access.
 for(const width of [390,1280]) for(const scheme of ['light','dark']) {
  const context=await createContext({viewport:{width,height:900},colorScheme:scheme});
  const page=await context.newPage();await page.goto(pageUrl('docs/commands/country-finder.html'));
  if(width<800)await page.locator('#menu-button').click();
  const navigation=page.locator('#site-nav');
  const setup=navigation.getByRole('link',{name:'Setup',exact:true});
  const commands=navigation.getByRole('link',{name:'Commands',exact:true});
  const setupButton=navigation.getByRole('button',{name:'Setup submenu',exact:true});
  assert(await navigation.locator('.nav-list-expander').evaluateAll(buttons=>buttons.every(button=>button.tabIndex===-1)));
  assert(await navigation.locator('.nav-list-link').evaluateAll(links=>links.every(link=>link.hasAttribute('href'))),'A current-page row lost its Tab stop');
  await navigation.getByRole('link',{name:'Home',exact:true}).focus();
  await page.keyboard.press('Tab');assert(await setup.evaluate(el=>el===document.activeElement),'Tab stopped on the arrow before the row');
  assert(await setup.evaluate(el=>el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle==='solid'));
  const initial=page.url();await page.keyboard.press('ArrowRight');
  assert.equal(page.url(),initial);assert.equal(await setup.getAttribute('aria-expanded'),'true');
  assert.equal(await setupButton.getAttribute('aria-expanded'),'true');
  assert.equal(await setup.getAttribute('aria-controls'),await setupButton.getAttribute('aria-controls'));
  await page.keyboard.press('ArrowRight');assert.equal(await setup.getAttribute('aria-expanded'),'true');
  await page.keyboard.press('Tab');assert(await navigation.getByRole('link',{name:'Claude',exact:true}).evaluate(el=>el===document.activeElement));
  await page.keyboard.press('Shift+Tab');assert(await setup.evaluate(el=>el===document.activeElement));
  await page.keyboard.press('ArrowLeft');assert.equal(await setup.getAttribute('aria-expanded'),'false');
  assert.equal(await setupButton.getAttribute('aria-expanded'),'false');
  await page.keyboard.press('Tab');assert(await commands.evaluate(el=>el===document.activeElement),'Tab visited the collapsed submenu or a second row control');
  await page.keyboard.press('Shift+Tab');assert(await setup.evaluate(el=>el===document.activeElement));
  await setupButton.click();assert.equal(await setup.getAttribute('aria-expanded'),'true');
  await setupButton.click();assert.equal(await setup.getAttribute('aria-expanded'),'false');
  const country=navigation.getByRole('link',{name:'Country finder',exact:true});
  await country.focus();await page.keyboard.press('ArrowRight');
  assert.equal(await country.getAttribute('aria-expanded'),'true');
  await page.keyboard.press('Tab');assert(await navigation.getByRole('link',{name:'Step 1: Criteria intake',exact:true}).evaluate(el=>el===document.activeElement));
  await page.keyboard.press('Shift+Tab');await page.keyboard.press('ArrowLeft');
  assert.equal(await country.getAttribute('aria-expanded'),'false');
  await setup.focus();await page.keyboard.press('Enter');await page.waitForURL(pageUrl('docs/setup/'));
  if(width<800)await page.locator('#menu-button').click();
  const current=page.locator('#site-nav').getByRole('link',{name:'Setup',exact:true});
  assert.equal(await current.getAttribute('href'),'/agent-compass/docs/setup/');
  assert.equal(await current.getAttribute('aria-expanded'),'true');
  await current.focus();await page.keyboard.press('ArrowLeft');assert.equal(await current.getAttribute('aria-expanded'),'false');
  await page.goto(pageUrl('docs/commands/country-finder/detailed.html'));
  if(width<800)await page.locator('#menu-button').click();
  assert.equal(await page.locator('#site-nav').getByRole('link',{name:'Commands',exact:true}).getAttribute('aria-expanded'),'true');
  console.log(`PASS ${width}px ${scheme}: one sidebar Tab stop per row, arrows, nested menus, pointer toggles, Enter and current-page access`);
  await context.close();
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
  if(!blocked) {
   const direct=await context.newPage();const url=new URL(await page.locator('.diagram-viewer__image').getAttribute('src'),page.url());url.hash=`theme-${manual}`;
   await direct.goto(url.href);
   const colors=await direct.locator('svg').evaluate(el=>({background:getComputedStyle(el).backgroundColor,text:getComputedStyle(el.querySelector('foreignObject span, text')).color}));
   assert.equal(colors.background,manual==='dark'?'rgb(39, 38, 43)':'rgb(255, 255, 255)','Direct SVG ignored the selected theme');
   assert.equal(colors.text,manual==='dark'?'rgb(230, 225, 232)':'rgb(39, 38, 43)','Direct SVG labels ignored the selected theme');
   await direct.close();
  }
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
  assert(await fullSize.evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle==='solid'&&parseFloat(getComputedStyle(el).outlineWidth)>=2),'Full-size link has no keyboard focus outline');
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
  await context.route('**/search-data.json?v=*',async route=>{count++;await new Promise(resolve=>setTimeout(resolve,500));await route.continue();});
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
  await context.route('**/search-data.json?v=*',async route=>{
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
  await page.route(`**/just-the-docs-${target}.css?v=*`,async route=>{count++;await new Promise(resolve=>setTimeout(resolve,300));if(count===1)await route.abort();else await route.continue();});
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
  await page.route('**/just-the-docs-dark.css?v=*',route=>fail?route.abort():route.continue());
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
  const firstText=await first.locator('code').innerText();const secondText=await second.locator('code').innerText();
  assert(firstText.trim()&&secondText.trim(),'Clipboard fixtures need nonempty commands');
  assert.notEqual(firstText,secondText,'Clipboard fixtures need different commands to detect stale text');
  assert.equal(await button.evaluate(el=>getComputedStyle(el).opacity),'1','Touch copy control needs hover');
  await button.click();await button.evaluate(el=>el.click());
  assert.equal(await page.evaluate(()=>window.copyWrites.length),1,'Pending copies were duplicated');
  assert.equal(await page.evaluate(()=>window.copyWrites[0].text),firstText,'Copy sent the wrong first command');
  assert.equal(await first.locator('use').getAttribute('xlink:href'),'#svg-copy');
  await page.clock.runFor(2500);assert.equal(await status.textContent(),'Copying…');
  await page.evaluate(()=>window.copyWrites[0].resolve());assert.equal(await status.textContent(),'Copied');
  await second.locator('button').click();assert.equal(await status.textContent(),'Copied','A pending write cleared another success');
  assert.equal(await page.evaluate(()=>window.copyWrites[1].text),secondText,'Copy sent stale or incorrect second-command text');
  await page.evaluate(()=>window.copyWrites[1].reject(new Error('Clipboard denied')));
  assert.match(await other.textContent(),/Try again or select the code/);assert.equal(await status.textContent(),'Copied','A failed write cleared another success');
  await second.locator('button').click();assert.equal(await other.textContent(),'','A new attempt retained stale copy error');
  assert.equal(await page.evaluate(()=>window.copyWrites[2].text),secondText,'Retry sent the wrong command');
  await page.evaluate(()=>window.copyWrites[2].resolve());assert.equal(await status.textContent(),'');assert.equal(await other.textContent(),'Copied');
  await page.clock.runFor(1999);assert.equal(await other.textContent(),'Copied');
  await page.clock.runFor(1);assert.equal(await other.textContent(),'');assert.deepEqual(errors,[]);
  await second.locator('button').focus();await page.keyboard.press('Tab');await page.keyboard.press('Shift+Tab');
  assert(await second.locator('button').evaluate(el=>el===document.activeElement&&el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle!=='none'));
  console.log(`PASS ${scheme} touch clipboard: exact command text, visible control, pending deduplication, confirmed success, recoverable failure, latest confirmation and two-second timer`);await context.close();
 }
 // Enlarged feedback fits the viewport; attached theme feedback needs its control in view.
 for(const kind of ['copy','theme','search']) {
  const context=await createContext({viewport:{width:320,height:844},hasTouch:true,isMobile:true,colorScheme:'light'});const page=await context.newPage();
  if(kind==='copy')await page.addInitScript(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('Denied'))}}));
  if(kind==='search')await context.route('**/search-data.json?v=*',route=>route.abort());
  await page.goto(pageUrl(kind==='copy'?'docs/setup/claude.html#terminal':'docs/commands/country-finder.html'));
  await page.addStyleTag({content:'html{font-size:200%!important;}'});
  await page.waitForFunction(()=>document.documentElement.classList.contains('compass-compact'));
  if(kind==='copy')await page.locator('div.highlighter-rouge:visible > button').first().click();
  else {
   await page.locator('#menu-button').click();
   if(kind==='theme'){await page.route('**/just-the-docs-dark.css?v=*',route=>route.abort());await page.selectOption('#theme-mode','dark');}
   else await page.locator('#search-input').fill('country');
  }
  if(kind==='theme')await page.locator('#theme-mode').scrollIntoViewIfNeeded();
  const selector=kind==='copy'?'.copy-status:not(:empty)':`#${kind}-status`;
  await page.waitForFunction(selector=>{
   const el=document.querySelector(selector);if(!el?.textContent.trim())return false;
   const box=el.getBoundingClientRect();return box.width>0&&box.x>=0&&box.right<=innerWidth&&box.y>=0&&box.bottom<=innerHeight;
  },selector);
  const status=page.locator(selector);
  await page.setViewportSize({width:390,height:600});
  if(kind==='theme')await page.locator('#theme-mode').scrollIntoViewIfNeeded();
  await page.waitForFunction(selector=>{const box=document.querySelector(selector).getBoundingClientRect();return box.x>=0&&box.right<=innerWidth&&box.y>=0&&box.bottom<=innerHeight;},selector);
  assert(await status.isVisible());
  console.log(`PASS enlarged ${kind} feedback: viewport containment before and after resize`);await context.close();
 }
 for(const fault of ['no-js','storage-blocked','saved-light','saved-dark','dark-css-failed']) {
  const context=await createContext({javaScriptEnabled:fault!=='no-js',colorScheme:'dark'});const page=await context.newPage();
  if(fault==='storage-blocked')await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));
  if(fault.startsWith('saved-'))await page.addInitScript(mode=>localStorage.setItem('agent-compass-theme',mode),fault.slice(6));
  if(fault==='dark-css-failed')await page.route('**/just-the-docs-dark.css?v=*',route=>route.abort());
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
