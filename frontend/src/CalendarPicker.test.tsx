import {render,screen,fireEvent} from '@testing-library/react';
import {expect,test,vi} from 'vitest';
import {CalendarPicker} from './CalendarPicker';
test('shows only Personal and replaces other calendar selections',()=>{
 const change=vi.fn();render(<CalendarPicker calendars={[{id:'a',name:'Personal'},{id:'b',name:'Family'}]} selected={['primary','b']} onChange={change}/>);
 expect(screen.queryByText('Family')).not.toBeInTheDocument();
 fireEvent.click(screen.getByRole('button',{name:'Use Personal calendar'}));expect(change).toHaveBeenCalledWith(['a']);
});
test('does not substitute another calendar when Personal is missing',()=>{
 render(<CalendarPicker calendars={[{id:'b',name:'Family'}]} selected={['b']} onChange={vi.fn()}/>);
 expect(screen.getByRole('status')).toHaveTextContent('Personal calendar unavailable');
});
