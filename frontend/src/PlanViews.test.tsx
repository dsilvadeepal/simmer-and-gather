import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {test,expect,afterEach} from 'vitest';
import {PlanViews} from './PlanViews';
afterEach(cleanup);
const inputs={gathering:{guests:15,arrival:'2026-11-01T18:00:00-05:00',profile:{timezone:'America/New_York'}},selections:[]};
const plan={gathering_id:'g',revision:1,input_hash:'h',assignments:[],shopping:[{name:'rice',quantity:2,unit:'cup'}],checklist:['Finish drinks']};
test('schedule is default and keyboard switches to secondary views',()=>{
 render(<PlanViews inputs={inputs} plan={plan}/>);
 expect(screen.getByRole('tab',{name:'Schedule'})).toHaveAttribute('aria-selected','true');
 expect(screen.queryByText('Finish drinks')).not.toBeVisible();
 fireEvent.keyDown(screen.getByRole('tab',{name:'Schedule'}),{key:'ArrowRight'});
 expect(screen.getByRole('tab',{name:'Menu'})).toHaveFocus();
 expect(screen.getByRole('tab',{name:'Menu'})).toHaveAttribute('aria-selected','true');
 fireEvent.click(screen.getByRole('tab',{name:'Finishing'}));
 expect(screen.getByText('Finish drinks')).toBeVisible();
});
