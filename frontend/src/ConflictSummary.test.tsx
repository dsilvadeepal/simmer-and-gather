import {render,screen} from '@testing-library/react';
import {expect,test,vi} from 'vitest';
import {ConflictSummary} from './ConflictSummary';
test('groups multiple dependent failures under one dish and highlights the long wait',()=>{
 const inputs:any={selections:[{id:'t',title:'Turkey',recipe:{tasks:[{title:'Dry brining',minutes:2160,unattended:true}]}}]};
 const plan:any={violations:[{code:'unscheduled',affected_ids:['t:1'],explanation:'Wait'},{code:'unscheduled',affected_ids:['t:2'],explanation:'Roast'}],advisories:[{code:'buy_prepared',affected_ids:['t']}]};
 render(<ConflictSummary inputs={inputs} plan={plan} onEditDiet={vi.fn()}/>);
 expect(screen.getAllByText('Turkey:')).toHaveLength(1);
 expect(screen.getByText(/36 hours for dry brining/)).toBeInTheDocument();
 expect(screen.getByText(/bought-prepared option fits/)).toBeInTheDocument();
});
