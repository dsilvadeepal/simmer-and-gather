import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {afterEach,test,expect,vi} from 'vitest';
import {SchedulingChoices} from './SchedulingChoices';
afterEach(cleanup);
test('simple choices retain daily overrides and hide editing controls',()=>{
 const change=vi.fn();render(<SchedulingChoices gathering={{arrival:'2026-11-01T18:00:00-05:00',relax_minutes:60,prep_days:['2026-11-01'],daily_limits:{'2026-11-01':90},profile:{timezone:'America/New_York'}}} days={['2026-11-01']} change={change}/>);
 expect(screen.getByText(/5:00 PM/)).toBeVisible();
 expect(screen.getByLabelText('Daily minutes 2026-11-01')).not.toBeVisible();
 expect(screen.getByText(/Up to 1.5 hours per day/)).toBeVisible();
 fireEvent.click(screen.getByRole('checkbox',{name:/Sun/}));expect(change).toHaveBeenCalledWith({prep_days:[]});
});
