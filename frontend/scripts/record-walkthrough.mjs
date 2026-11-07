// Isolated UI walkthrough: every API request is fulfilled locally with generic fixtures.
import {chromium} from '@playwright/test';
import fs from 'node:fs/promises';
const root=new URL('../../',import.meta.url);
const samples=JSON.parse(await fs.readFile(new URL('docs/reviews/2026-11-07-random-ux-results.json',root),'utf8'));
const sample=samples.find(x=>x.id==='random-ux-13');
sample.inputs.gathering.title='Weekend gathering';sample.inputs.gathering.occasion='Other';
const ws={inputs:sample.inputs,plan:sample.plan,recipes:sample.inputs.selections.map(s=>s.recipe),fixture_mode:true,previous_plan:null,recipe_updates:[],recipe_readiness:{}};
const out=process.env.WALKTHROUGH_OUTPUT||'/tmp/simmer-walkthrough-2026-11-07';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
const context=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:out,size:{width:1440,height:1000}},timezoneId:'America/New_York'});
const calls=[];
await context.route('**/api/**',async route=>{const req=route.request(),p=new URL(req.url()).pathname;calls.push({method:req.method(),path:p});let body={};
if(p==='/api/dev-session')body={token:'isolated-video-fixture'};
else if(p==='/api/gatherings'){if(req.method()==='POST'){const data=req.postDataJSON();Object.assign(sample.inputs.gathering,data.gathering);body=sample.inputs.gathering;}else body=[sample.inputs.gathering];}
else if(p.startsWith('/api/workspace/'))body=ws;
else if(p==='/api/calendars')body=[{id:'sample-personal',name:'Personal'}];
else if(p.endsWith('/generate'))body=sample.plan;
else if(p.startsWith('/api/menu/'))body=sample.inputs;
await route.fulfill({json:body});});
const page=await context.newPage();
await page.goto(process.env.WALKTHROUGH_URL||'http://127.0.0.1:5198/');await page.getByLabel('Gathering name').waitFor();await page.evaluate(()=>document.fonts.ready);
async function caption(text){await page.evaluate(text=>{let e=document.getElementById('walkthrough-caption');if(!e){e=document.createElement('div');e.id='walkthrough-caption';e.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:99999;background:#213c32;color:white;padding:15px 25px;border-radius:12px;font:600 22px system-ui;text-align:center;box-shadow:0 4px 24px #0003;max-width:88%;width:max-content;pointer-events:none';document.body.append(e);}e.textContent=text;},text);}
async function hold(ms=4500){await page.waitForTimeout(ms);}
async function show(locator){await locator.evaluate(el=>window.scrollTo({top:window.scrollY+el.getBoundingClientRect().top-120,behavior:'smooth'}));await hold(800);}
await caption('Simmer and Gather • Plan the food. Enjoy the gathering.');await hold();
await caption('A sample gathering for 12 guests — your plans stay untouched.');await show(page.getByLabel('Gathering name'));await hold();
await caption('Set your prep days, daily time and time to relax.');
await show(page.getByRole('button',{name:/Save and continue/}));await hold();
await page.getByRole('button',{name:/Save and continue/}).click();await page.getByRole('heading',{name:'What’s on the menu?'}).waitFor();await page.evaluate(()=>window.scrollTo(0,0));
await caption('Review your menu, portions and what to cook or buy.');await hold(6000);
await show(page.getByRole('button',{name:/Build my prep plan/}));await caption('Build the prep plan in one step.');await hold(3000);await page.getByRole('button',{name:/Build my prep plan/}).click();
await page.getByRole('tab',{name:'Schedule',exact:true}).waitFor();await page.evaluate(()=>window.scrollTo(0,0));await caption('A complete sample plan, grouped into useful prep sessions.');await hold();
await show(page.locator('.prep-day').first());await caption('See hands-on time separately from cooking and waiting.');await hold(6000);
const how=page.locator('.prep-day summary').filter({hasText:'How to'}).first();if(await how.count()){await how.click();await show(how);await caption('Expand a task only when you need the cooking details.');await hold(5500);await how.click();}
await show(page.getByRole('tab',{name:'Shopping',exact:true}));await page.getByRole('tab',{name:'Shopping',exact:true}).click();await caption('The shopping list is grouped by grocery category.');await hold();
const produce=page.locator('.shopping-list summary').filter({hasText:'Produce'}).first();await produce.click();await show(produce);await hold(2500);await page.locator('.shopping-list input[type=checkbox]').first().check();await caption('Tick ingredients you already have. They stay crossed out.');await hold();
await show(page.getByRole('button',{name:'Show only what I need',exact:true}));await page.getByRole('button',{name:'Show only what I need',exact:true}).click();await caption('Show only what you still need to buy.');await hold();
await show(page.getByRole('tab',{name:'Finishing',exact:true}));await page.getByRole('tab',{name:'Finishing',exact:true}).click();await caption('Keep the small finishing jobs in their own checklist.');await hold();
await page.getByRole('tab',{name:'Schedule',exact:true}).click();await page.setViewportSize({width:390,height:844});await show(page.locator('.prep-day').first());await caption('A clean prep view on your phone while cooking.');await hold(6500);
await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>window.scrollTo(0,0));await caption('Ready to host • Sample data only • Nothing added to a calendar');await hold(5000);
await page.screenshot({path:out+'/final-frame.png'});
const video=page.video();await context.close();await video.saveAs(out+'/simmer-and-gather-walkthrough.webm');await browser.close();await fs.writeFile(out+'/request-audit.json',JSON.stringify({all_api_requests_mocked:true,calls},null,2));console.log(out+'/simmer-and-gather-walkthrough.webm');
