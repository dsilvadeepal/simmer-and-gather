import {render,screen,fireEvent} from '@testing-library/react';
import {test,expect,vi} from 'vitest';
import {StepNavigation} from './StepNavigation';
test('marks current step and preserves back navigation',()=>{
 const choose=vi.fn();render(<StepNavigation step={2} onSelect={choose}/>);
 expect(screen.getByRole('button',{name:'3 Prep plan'})).toHaveAttribute('aria-current','step');
 fireEvent.click(screen.getByRole('button',{name:'1 Gathering'}));
 expect(choose).toHaveBeenCalledWith(0);
 expect(screen.getByRole('navigation',{name:'Planning steps'})).toBeVisible();
});
