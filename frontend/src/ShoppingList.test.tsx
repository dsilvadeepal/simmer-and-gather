import {render,screen,fireEvent} from '@testing-library/react';
import {test,expect} from 'vitest';
import {ShoppingList} from './ShoppingList';
test('displays calculated shopping amounts and unknown quantities',()=>{
 render(<ShoppingList items={[{name:'rice',quantity:2.5,unit:'cup'},{name:'mint',quantity:null}]} selections={[]}/>);
 fireEvent.click(screen.getByText(/Pantry & other/));
 fireEvent.click(screen.getByText(/Produce/));
 expect(screen.getByText(/2½ cup/)).toBeVisible();
 expect(screen.getByText(/Check amount/)).toBeVisible();
});
