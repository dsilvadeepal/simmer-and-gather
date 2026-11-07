import {render,screen,fireEvent,waitFor} from '@testing-library/react';
import {vi,test,expect} from 'vitest';
import App from './App';
import {api} from './api';
vi.mock('./api',()=>({api:vi.fn(),localLogin:vi.fn().mockResolvedValue(undefined)}));
vi.mock('./PlanViews',()=>({PlanViews:()=> <p>Built schedule</p>}));
test('save and continue then build opens the generated plan in one action',async()=>{
 history.replaceState(null,'','/');
 let g:any={id:'test',revision:1,title:'Dinner',arrival:'2027-04-24T18:00:00-04:00',earliest_prep:'2027-04-23',prep_days:['2027-04-23','2027-04-24'],guests:8,vegetarian_guests:0,allergies:null,relax_minutes:60,profile:{timezone:'America/New_York',helpers:[],weekday_minutes:120,weekend_minutes:120},daily_limits:{}};
 vi.mocked(api).mockImplementation(async(path,body:any)=>{
  if(path==='/gatherings'&&!body)return [g];
  if(path==='/gatherings'){g={...body.gathering,revision:2};return g;}
  if(path==='/workspace/test')return {inputs:{gathering:g,selections:[]},recipes:[],fixture_mode:true};
  if(path==='/calendars')return [];
  if(path==='/plans/test/generate')return {id:'new',status:'feasible',violations:[],fit_days:[],assignments:[]};
  throw Error('Unexpected '+path);
 });
 render(<App/>);
 fireEvent.click(await screen.findByLabelText('No known allergies'));
 fireEvent.click(screen.getByText('Save and continue'));
 await screen.findByText('What’s on the menu?');
 expect(screen.queryByText('Save menu preferences')).not.toBeInTheDocument();
 fireEvent.click(screen.getByText('Build my prep plan'));
 await screen.findByText('Built schedule');
 await waitFor(()=>expect(api).toHaveBeenCalledWith('/plans/test/generate',{expected_revision:2}));
 expect(vi.mocked(api).mock.calls.filter(([p])=>p.includes('/generate'))).toHaveLength(1);
});
