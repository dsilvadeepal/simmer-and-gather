import {render,screen,fireEvent,waitFor,cleanup} from '@testing-library/react';
import {test,expect,vi,afterEach} from 'vitest';
import {PantryEntry} from './PantryEntry';
afterEach(cleanup);
test('retains entry on failed save and clears after success',async()=>{
 const onAdd=vi.fn().mockResolvedValueOnce(false).mockResolvedValueOnce(true);
 render(<PantryEntry onAdd={onAdd}/>);
 fireEvent.change(screen.getByLabelText('Ingredient'),{target:{value:'Rice'}});
 fireEvent.change(screen.getByLabelText('Amount'),{target:{value:'500'}});
 fireEvent.click(screen.getByText('Add ingredient'));
 await waitFor(()=>expect(onAdd).toHaveBeenCalledTimes(1));
 expect(screen.getByLabelText('Ingredient')).toHaveValue('Rice');
 fireEvent.click(screen.getByText('Add ingredient'));
 await waitFor(()=>expect(screen.getByLabelText('Ingredient')).toHaveValue(''));
 expect(onAdd).toHaveBeenCalledWith({name:'Rice',quantity:500,unit:'g',source:'manual'});
});
