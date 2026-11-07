import {render,screen,fireEvent,cleanup} from '@testing-library/react';
import {test,expect,afterEach} from 'vitest';
import {ShoppingList,ingredientName,shoppingGroup,shoppingAmount} from './ShoppingList';
afterEach(cleanup);
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
test('separates source ranges and optional quantities from unresolved amounts',()=>{
 render(<ShoppingList items={[{name:'1 to 2 tsp spice (scaled range: 2–4 tsp)',quantity:null},{name:'salt, to taste',quantity:null},{name:'mystery ingredient',quantity:null}]} selections={[]}/>);
 expect(screen.getByText('Recipe ranges · 1')).toBeVisible();
 expect(screen.getByText('To taste & optional · 1')).toBeVisible();
 expect(screen.getByText('Amounts to confirm · 1')).toBeVisible();
});
test('pantry checks stay crossed out until filtered, persist and reset when amounts change',()=>{
 localStorage.clear();
 const props={gatheringId:'test-gathering',selections:[],items:[{name:'rice',quantity:2,unit:'cup'}]};
 const {unmount}=render(<ShoppingList {...props}/>);
 fireEvent.click(screen.getByText('Pantry & spices · 1'));
 fireEvent.click(screen.getByRole('checkbox',{name:'Have rice'}));
 expect(screen.getByRole('checkbox',{name:'Have rice'})).toBeChecked();
 expect(screen.getByText('rice').className).toBe('shopping-have');
 fireEvent.click(screen.getByRole('button',{name:'Show only what I need'}));
 expect(screen.queryByRole('checkbox')).toBeNull();
 expect(screen.getByText('You have everything on this list.')).toBeVisible();
 fireEvent.click(screen.getByRole('button',{name:'Show all ingredients'}));
 unmount();
 const second=render(<ShoppingList {...props}/>);
 expect(screen.getByRole('checkbox',{name:'Have rice',hidden:true})).toBeChecked();
 second.unmount();
 render(<ShoppingList {...props} items={[{name:'rice',quantity:3,unit:'cup'}]}/>);
 expect(screen.getByRole('checkbox',{name:'Have rice',hidden:true})).not.toBeChecked();
 expect(screen.getByText('Amount changed—check again.')).toBeInTheDocument();
 localStorage.clear();
});
