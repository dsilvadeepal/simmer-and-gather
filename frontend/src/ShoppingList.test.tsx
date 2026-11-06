import {render,screen,fireEvent} from '@testing-library/react';
import {test,expect} from 'vitest';
import {ShoppingList,ingredientName,shoppingGroup,shoppingAmount} from './ShoppingList';
test('separates unresolved quantities and excludes water',()=>{
 render(<ShoppingList items={[{name:'rice',quantity:2.5,unit:'cup'},{name:'mint',quantity:null},{name:'water',quantity:3,unit:'cup'}]} selections={[]}/>);
 fireEvent.click(screen.getByText(/Pantry & spices/));
 fireEvent.click(screen.getByText(/Amounts to confirm/));
 expect(screen.getByText(/2½ cup/)).toBeVisible();
 expect(screen.getByText('mint')).toBeVisible();
 expect(screen.queryByText('water')).toBeNull();
});
test('cleans import artifacts, categorizes produce and frozen, labels rounding',()=>{
 expect(ingredientName('6 cloves')).toBe('cloves');
 expect(ingredientName('spinach (baby spinach works best)')).toBe('spinach');
 expect(shoppingGroup('spinach')).toBe('Produce');
 expect(shoppingGroup('frozen green peas')).toBe('Frozen');
 expect(shoppingAmount(.94,'tbsp')).toBe('About 1 tbsp');
 expect(shoppingAmount(17.81,'tsp')).toBe('About 6 tbsp');
});
