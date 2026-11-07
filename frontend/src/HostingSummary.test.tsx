import {render,screen,cleanup} from '@testing-library/react';
import {expect,test,afterEach} from 'vitest';
import {HostingSummary} from './HostingSummary';
afterEach(cleanup);
test('shows source-linked menu, daily allowance and buffer without invented reason',()=>{
 render(<HostingSummary inputs={{gathering:{guests:15,arrival:'2026-11-01T18:00:00-05:00',relax_minutes:60,profile:{timezone:'America/New_York'},daily_limits:{}},selections:[{id:'one',title:'Butter chicken',category:'mains',mode:'cook',servings:10,must_have:true,recipe:{title:'Butter chicken',source:'https://example.com/chicken',servings:5,ingredients:[{name:'chicken',quantity:2,unit:'lb'}]}}]}} plan={{gathering_id:'g',revision:1,input_hash:'hash',assignments:[],fit_days:[{day:'2026-11-01',presence_minutes:90,cooking_minutes:75,limit_minutes:120,cleanup_allowance:15}],advisories:[]}}/>);
 expect(screen.getByRole('link',{name:'Butter chicken'})).toHaveAttribute('href','https://example.com/chicken');
 expect(screen.getByText(/4 lb chicken/,{selector:'.meta'})).toBeVisible();
 expect(screen.getByText(/90 min of 120 min/)).toBeVisible();
 expect(screen.getByText(/5:00 PM/)).toBeVisible();
});

test('menu prioritizes chicken over butter and retains full quantities',()=>{
 render(<HostingSummary view="menu" inputs={{gathering:{guests:15},selections:[{id:'a',title:'Butter Chicken',servings:10,recipe:{title:'Butter Chicken',source:'https://example.com',servings:5,ingredients:[{name:'butter',quantity:2,unit:'tbsp'},{name:'chicken',quantity:2,unit:'lb'}]}}]}} plan={{gathering_id:'g',revision:1,input_hash:'h'}}/>);
 expect(screen.getByText('4 tbsp butter')).not.toBeVisible();
 expect(screen.getByText('4 lb chicken',{selector:'.meta'})).toBeVisible();
 expect(screen.getByText('All ingredient quantities')).toBeVisible();
});

test('ingredient checks are not presented as optional menu suggestions',()=>{
 render(<HostingSummary view="fit" inputs={{gathering:{guests:15},selections:[]}} plan={{gathering_id:'g',revision:1,input_hash:'h',advisories:[{code:'allergy_label_check',explanation:'Check packaged ingredients before serving.'}]}}/>);
 expect(screen.getByRole('heading',{name:'Before serving: check ingredient labels'})).toBeVisible();
 expect(screen.queryByText(/Optional menu suggestions/)).not.toBeInTheDocument();
});
