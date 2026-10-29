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
