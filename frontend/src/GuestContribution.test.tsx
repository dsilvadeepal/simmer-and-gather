import {render,screen,fireEvent,waitFor} from '@testing-library/react';
import {test,expect,vi} from 'vitest';
import {GuestContribution} from './GuestContribution';
test('collects contribution details together without browser prompts',async()=>{
 const save=vi.fn().mockResolvedValue(undefined),prompt=vi.spyOn(window,'prompt');
 render(<GuestContribution item={{title:'Fruit platter',servings:8}} onSave={save}/>);
 fireEvent.change(screen.getByLabelText('Who’s bringing it?'),{target:{value:'Sample guest'}});
 fireEvent.click(screen.getByRole('button',{name:'Save contribution'}));
 await waitFor(()=>expect(save).toHaveBeenCalledWith(expect.objectContaining({servings:8,contribution:expect.objectContaining({person:'Sample guest',warming_minutes:0})})));
 expect(prompt).not.toHaveBeenCalled();prompt.mockRestore();
});
