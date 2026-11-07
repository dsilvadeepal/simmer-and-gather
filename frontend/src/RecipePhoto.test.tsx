import {render,screen,fireEvent} from '@testing-library/react';
import {expect,it} from 'vitest';
import {RecipePhoto} from './RecipePhoto';
it('uses current library image without replacing saved recipe content, with a visible fallback',()=>{
 const recipe={id:'r',title:'Curry',source:'https://example.org/recipe'};
 render(<RecipePhoto title="Curry" recipe={recipe} library={[{...recipe,image_url:'https://example.org/curry.jpg'}]}/>);
 expect(screen.getByRole('img',{name:'Curry'}).getAttribute('src')).toBe('https://example.org/curry.jpg');
 fireEvent.error(screen.getByRole('img',{name:'Curry'}));
 expect(screen.getByLabelText('Recipe photo unavailable')).toBeTruthy();
});
