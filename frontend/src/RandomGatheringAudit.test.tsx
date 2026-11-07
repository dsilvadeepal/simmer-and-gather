import {render,screen,fireEvent,waitFor,cleanup} from '@testing-library/react';
import {vi,test,expect,afterEach} from 'vitest';
import fixture from '../../docs/reviews/2026-11-07-random-ux-results.json';
import App from './App';
import {api} from './api';
vi.mock('./api',()=>({api:vi.fn(),localLogin:vi.fn().mockResolvedValue(undefined)}));
const rows:any[]=fixture;
if(rows.length!==20)throw new Error("Expected all 20 completed evaluation outputs");
afterEach(()=>{cleanup();vi.mocked(api).mockReset();localStorage.clear();});
for(const row of rows){test(row.id+' renders and builds the actual evaluation output',async()=>{
 history.replaceState(null,'','/?view=menu');
 vi.mocked(api).mockImplementation(async(p)=>{
  if(p==='/gatherings')return [row.inputs.gathering];
  if(p.startsWith('/workspace/'))return {inputs:row.inputs,recipes:row.inputs.selections.filter((s:any)=>s.recipe).map((s:any)=>s.recipe),fixture_mode:true};
  if(p==='/calendars')return [];
  if(p.endsWith('/generate'))return row.plan;
  if(p.endsWith('/alternatives'))return row.alternatives||{suggestions:[],message:'No alternatives in this case'};
  throw Error('Unexpected request: '+p);
 });
 render(<App/>);
 fireEvent.click(await screen.findByRole('button',{name:'Build my prep plan'}));
 if(row.inputs.gathering.allergies==null){await screen.findByRole('heading',{name:'Confirm guest allergies first'});expect(screen.queryByRole('tab',{name:'Shopping'})).not.toBeInTheDocument();return;}
 await waitFor(()=>expect(document.querySelector('.plan-status')).not.toBeNull());
 expect(vi.mocked(api).mock.calls.filter(([p])=>p.endsWith('/generate'))).toHaveLength(1);
 if(row.alternatives?.suggestions.length){await screen.findAllByRole('button',{name:'Use this menu and plan'});}
 expect(vi.mocked(api).mock.calls.some(([p])=>p.endsWith('/approve')||p.includes('/apply'))).toBe(false);
 const shopping=screen.getAllByRole('tab',{name:'Shopping'});
 fireEvent.click(shopping[shopping.length-1]);
 expect(screen.getByRole('heading',{name:'Shopping list'})).toBeInTheDocument();
});}

test('alternative preview cannot alter the gathering checklist',async()=>{
 const {MenuAlternatives}=await import('./MenuAlternatives');
 const row=rows.find((r:any)=>r.alternatives?.suggestions.length);
 vi.mocked(api).mockResolvedValue(row.alternatives);
 const {container}=render(<MenuAlternatives inputs={row.inputs} plan={row.plan} disabled={false} onApproved={async()=>{}}/>);
 await screen.findAllByRole('button',{name:'Use this menu and plan'});
 const details=container.querySelector('details')!;details.open=true;
 expect(container.querySelector('input[type=checkbox]')).toBeNull();
 expect(screen.queryByRole('tab',{name:'Shopping'})).not.toBeInTheDocument();
 expect(localStorage.getItem('simmer:shopping:'+row.inputs.gathering.id)).toBeNull();
 expect(vi.mocked(api).mock.calls.some(([p])=>p.endsWith('/approve'))).toBe(false);
});
