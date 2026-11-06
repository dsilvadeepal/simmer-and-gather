import {render,screen,cleanup} from '@testing-library/react';
import {afterEach,test,expect} from 'vitest';
import {PrepOverview} from './PrepOverview';
afterEach(cleanup);
test('separate morning and evening tasks remain separate rows and waiting is a note',()=>{
 const rows=[{task:{id:'a',title:'Paneer · Mix marinade',recipe_id:'p',minutes:10,active_minutes:10},interval:{start:'2026-11-01T10:00:00-05:00',end:'2026-11-01T10:10:00-05:00'}},{task:{id:'b',title:'Paneer · Marinate',recipe_id:'p',minutes:30,active_minutes:0,presence_minutes:0,unattended:true},interval:{start:'2026-11-01T10:10:00-05:00',end:'2026-11-01T10:40:00-05:00'}},{task:{id:'c',title:'Paneer · Cook paneer',recipe_id:'p',minutes:20,active_minutes:20},interval:{start:'2026-11-01T16:00:00-05:00',end:'2026-11-01T16:20:00-05:00'}}];
 render(<PrepOverview assignments={rows} timezone="America/New_York"/>);
 expect(screen.getAllByRole('row')).toHaveLength(3);
 expect(screen.getByText(/10:00 AM/)).toBeVisible();
 expect(screen.getByText(/4:00 PM/)).toBeVisible();
 expect(screen.getByText(/Marinate.*30 min waiting/)).toBeVisible();
});

test('date is a single day heading and ingredient quantities stay visible',()=>{
 render(<PrepOverview assignments={[{task:{id:'a',title:'Rice · Rinse rice',minutes:5,ingredients:[{name:'rice',quantity:2,unit:'cup'}]},interval:{start:'2026-11-01T10:00:00-05:00',end:'2026-11-01T10:05:00-05:00'}},{task:{id:'b',title:'Rice · Cook rice',minutes:20},interval:{start:'2026-11-01T16:00:00-05:00',end:'2026-11-01T16:20:00-05:00'}}]} timezone="America/New_York"/>);
 expect(screen.getAllByText('Sunday, Nov 1')).toHaveLength(1);
 expect(screen.getByText('2 cup')).toBeVisible();
});

test('waiting notes include their actual start and end times',()=>{
 render(<PrepOverview assignments={[{task:{id:'a',title:'Beans · Start',recipe_id:'b',minutes:5},interval:{start:'2026-10-30T18:00:00-04:00',end:'2026-10-30T18:05:00-04:00'}},{task:{id:'w',title:'Beans · Soak',recipe_id:'b',minutes:480,active_minutes:0,presence_minutes:0,unattended:true},interval:{start:'2026-10-30T18:05:00-04:00',end:'2026-10-31T02:05:00-04:00'}}]}/>);
 expect(screen.getByText(/Friday, Oct 30 at 6:05 PM.*Saturday, Oct 31 at 2:05 AM/)).toBeVisible();
});

test('overlapping and touching tasks share one block, with no individual time slots',()=>{
 const rows=[['a','15:20','15:50'],['b','15:40','16:05'],['c','16:05','16:20']].map(([id,start,end])=>({task:{id,title:`Recipe · Task ${id}`,minutes:20},interval:{start:`2026-11-01T${start}:00-05:00`,end:`2026-11-01T${end}:00-05:00`}}));
 render(<PrepOverview assignments={rows}/>);
 expect(screen.getAllByRole('row')).toHaveLength(2);
 expect(screen.getByText('3:20 PM–4:20 PM')).toBeVisible();
 expect(screen.queryByText(/3:40 PM/)).not.toBeInTheDocument();
 expect(screen.getAllByRole('listitem')).toHaveLength(3);
});

test('storage appears once per recipe and research commentary is absent',()=>{
 const rows=['a','b'].map((id)=>({task:{id,title:`Dal · Task ${id}`,recipe_id:'dal',minutes:5,guidance:'Refrigerate in shallow containers.',evidence:'Method reviewed against publisher'},interval:{start:'2026-11-01T10:00:00-05:00',end:'2026-11-01T10:05:00-05:00'}}));
 render(<PrepOverview assignments={rows} recipes={[{id:'dal',title:'Dal',source:'https://example.com/dal'}]}/>);
 expect(screen.getAllByText('Refrigerate in shallow containers.')).toHaveLength(1);
 expect(screen.queryByText(/Method reviewed/)).not.toBeInTheDocument();
 expect(screen.getByRole('link',{name:'Original recipe',hidden:true})).toHaveAttribute('href','https://example.com/dal');
});

test('does not show recipe-wide allergy or reheating notes under chopping tasks',()=>{
 render(<PrepOverview assignments={[
 {task:{id:'a',title:'Rice · Chop vegetables',recipe_id:'r',minutes:5,guidance:'Contains cashews in the listed recipe.'},interval:{start:'2026-11-01T10:00:00-05:00',end:'2026-11-01T10:05:00-05:00'}},
 {task:{id:'b',title:'Chicken · Chop onion',recipe_id:'c',minutes:5,guidance:'Reheat thoroughly before serving; sauce usually tolerates this better than last-minute cooking.'},interval:{start:'2026-11-01T10:05:00-05:00',end:'2026-11-01T10:10:00-05:00'}}
 ]} recipes={[{id:'r',title:'Rice',source:'https://example.com/r'},{id:'c',title:'Chicken',source:'https://example.com/c'}]}/>);
 expect(screen.queryByText('How to')).not.toBeInTheDocument();
 expect(screen.getByText('Contains cashews.')).toBeInTheDocument();
 expect(screen.getByText('Reheat thoroughly before serving.')).toBeInTheDocument();
});

test('combines adjacent reheating and paneer air-frying into two bullets',()=>{
 const specs=[['a','dal','Dal · Reheat curry thoroughly'],['b','chicken','Butter Chicken · Reheat curry thoroughly'],['c','paneer','Paneer · Thread skewers and preheat air fryer'],['d','paneer','Paneer · Air-fry a single layer, turning halfway']];
 render(<PrepOverview assignments={specs.map(([id,recipe_id,title])=>({task:{id,recipe_id,title,minutes:5},interval:{start:'2026-11-01T16:00:00-05:00',end:'2026-11-01T16:05:00-05:00'}}))}/>);
 expect(screen.getAllByRole('listitem')).toHaveLength(2);
 expect(screen.getByText('Reheat dal and butter chicken')).toBeVisible();
 expect(screen.getByText('Thread skewers, preheat and air-fry, turning halfway')).toBeVisible();
});

test('distinguishes counted time from elapsed blocks and passive cooking',()=>{
 render(<PrepOverview fitDays={[{day:'2026-12-25',presence_minutes:20,limit_minutes:180}]} assignments={[
 {task:{id:'a',title:'Cafreal · Cook chicken',minutes:45,active_minutes:20,presence_minutes:20,resource:'stovetop'},interval:{start:'2026-12-25T14:30:00-05:00',end:'2026-12-25T15:15:00-05:00'}}
 ]}/>);
 expect(screen.getByText(/20 min active · 3 hr daily allowance/)).toBeVisible();
 expect(screen.getByText('45 min start to finish')).toBeVisible();
 expect(screen.getByText(/20 min hands-on · 25 min cooking or waiting between check-ins/)).toBeVisible();
 expect(screen.getByText(/45 min start to finish across sessions/)).toBeVisible();
});
