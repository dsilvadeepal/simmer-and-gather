import {test,expect} from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
const fixture=JSON.parse(fs.readFileSync(path.resolve('../docs/reviews/2026-10-29-five-menu-rerun.json'),'utf8'))[0];
test('desktop and phone show library photos, no import control, and precise schedule outcome',async({page})=>{
 const inputs=fixture.inputs;
 const photo='https://ministryofcurry.com/wp-content/uploads/2017/02/Tandoori-Chicken-Wings_-6.jpg';
 const recipes=inputs.selections.filter((s:any)=>s.recipe).map((s:any)=>({...s.recipe,image_url:photo,image_credit:'Photo: Ministry of Curry'}));
 const workspace={inputs,recipes,fixture_mode:true,plan:{gathering_id:inputs.gathering.id,revision:inputs.gathering.revision,input_hash:'fixture',status:'conflict',assignments:[],shopping:[],violations:[],outcome:{code:'search_exhausted',message:'The search reached its limit without a complete plan. This does not mean you need more time.'}}};
 const writes:string[]=[];
 await page.route('**/api/**',async route=>{
  const req=route.request(),url=new URL(req.url());
  if(req.method()!=='GET'&&!url.pathname.endsWith('/dev-session'))writes.push(url.pathname);
  const body=url.pathname.endsWith('/dev-session')?{token:'synthetic'}:url.pathname.endsWith('/gatherings')?[inputs.gathering]:url.pathname.includes('/workspace/')?workspace:url.pathname.endsWith('/calendars')?[]:{};
  await route.fulfill({json:body});
 });
 await page.goto('/?view=menu');
 await expect(page.getByRole('heading',{name:'Add a dish'})).toBeVisible();
 await expect(page.getByText('Import a recipe',{exact:true})).toHaveCount(0);
 await expect(page.locator('.recipe img').first()).toHaveAttribute('src',photo);
 await expect(page.locator('.recipe img').first()).toBeVisible();
 await page.setViewportSize({width:390,height:844});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 await page.getByRole('button',{name:'3 Prep plan',exact:true}).click();
 await expect(page.getByText(workspace.plan.outcome.message,{exact:true})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 expect(writes).toEqual([]);
});
