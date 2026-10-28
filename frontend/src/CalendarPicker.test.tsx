import {render,screen,fireEvent} from '@testing-library/react';
import {expect,test,vi} from 'vitest';
import {CalendarPicker} from './CalendarPicker';
test('calendar choice preserves other selected calendars',()=>{
 const change=vi.fn();render(<CalendarPicker calendars={[{id:'a',name:'Personal'},{id:'b',name:'Family'}]} selected={['a']} onChange={change}/>);
 fireEvent.click(screen.getByLabelText('Family'));expect(change).toHaveBeenCalledWith(['a','b']);
 expect(screen.getByLabelText('Personal')).toBeChecked();
});
