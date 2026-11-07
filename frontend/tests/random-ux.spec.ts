import {test,expect} from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
const report=path.resolve('../docs/reviews');
const rows=JSON.parse(fs.readFileSync(path.join(report,'2026-11-07-random-ux-results.json'),'utf8'));
const findings:any[]=[];
for(const width of [1440,390]){
 test(`${width}px: all 20 generated plans, build flow and controls`,async({page})=>{
  await page.setViewportSize({width,height:900});
  let current:any;const dialogs:string[]=[];const errors:string[]=[];
  page.on('dialog',async d=>{dialogs.push(d.message());await d.dismiss();});
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/api/**',async route=>{
   const p=new URL(route.request().url()).pathname;
   let body:any={};
   if(p.endsWith('/dev-session'))body={token:'synthetic-test'};
   else if(p==='/api/gatherings')body=[current.inputs.gathering];
   else if(p.includes('/workspace/'))body={inputs:current.inputs,plan:null,recipes:current.inputs.selections.filter((s:any)=>s.recipe).map((s:any)=>s.recipe),fixture_mode:true};
   else if(p.endsWith('/generate'))body=current.plan;
   else if(p.endsWith('/alternatives'))body=current.alternatives||{suggestions:[],message:'No alternatives for this test.'};
   else if(p==='/api/calendars')body=[];
   else if(p==='/api/profile')body={};
   else throw Error('Unexpected API request '+p);
   await route.fulfill({json:body});
  });
  for(const row of rows){
   current=row;await page.goto('/?view=menu');
   await expect(page.getByRole('button',{name:'Build my prep plan',exact:true})).toBeVisible();
   await page.getByRole('button',{name:'Build my prep plan',exact:true}).click();
   await expect(page.locator('.plan-status')).toBeVisible();
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
   const buttons=await page.getByRole('button').allTextContents();
   const nestedTabs=await page.getByRole('tablist').count();
   const checks=await page.locator('.plan-checks summary').allTextContents();
   findings.push({case:row.id,width,overflow,buttons:buttons.map(s=>s.trim()),tablistsInDOM:nestedTabs,checks,outcome:row.outcome});
   await page.getByRole('tab',{name:'Shopping',exact:true}).first().click();
   if(row.plan.shopping?.length){
    const group=page.locator('.shopping-list details').first();await group.locator('summary').first().click();
    const box=group.getByRole('checkbox').first();if(await box.count()){await box.check();await expect(box).toBeChecked();}
   }
   if(['random-ux-01','random-ux-16','random-ux-18','random-ux-20'].includes(row.id)){
    await page.getByRole('tab',{name:'Schedule',exact:true}).first().click();
    await page.screenshot({path:path.join(report,`random-ux-${row.id}-${width}.png`),fullPage:true});
   }
  }
  fs.writeFileSync(path.join(report,`2026-11-07-ui-${width}.json`),JSON.stringify({findings:findings.filter(x=>x.width===width),dialogs,errors},null,2));
  expect(dialogs).toEqual([]);expect(errors).toEqual([]);
 });
}
