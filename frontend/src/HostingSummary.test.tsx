import {render,screen,cleanup} from '@testing-library/react';
import {expect,test,afterEach} from 'vitest';
import {HostingSummary} from './HostingSummary';
afterEach(cleanup);
test('shows source-linked menu, daily allowance and buffer without invented reason',()=>{
 render(<HostingSummary inputs={{gathering:{guests:15,arrival:'2026-11-01T18:00:00-05:00',relax_minutes:60,profile:{timezone:'America/New_York'},daily_limits:{}},selections:[{id:'one',title:'Butter chicken',category:'mains',mode:'cook',servings:10,must_have:true,recipe:{title:'Butter chicken',source:'https://example.com/chicken',servings:5,ingredients:[{name:'chicken',quantity:2,unit:'lb'}]}}]}} plan={{gathering_id:'g',revision:1,input_hash:'hash',assignments:[],fit_days:[{day:'2026-11-01',presence_minutes:90,cooking_minutes:75,limit_minutes:120,cleanup_allowance:15}],advisories:[]}}/>);
 expect(screen.getByRole('link',{name:'Butter chicken'})).toHaveAttribute('href','https://example.com/chicken');
 expect(screen.getByText(/4 lb chicken/)).toBeVisible();
 expect(screen.getByText(/90 min of 120 min/)).toBeVisible();
 expect(screen.getByText(/5:00 PM/)).toBeVisible();
});
