import {render,screen} from '@testing-library/react';
import {expect,test} from 'vitest';
import {TaskCard} from './TaskCard';
test('ingredients visible without opening details; cleanup stays concise',()=>{
 render(<TaskCard task={{title:'Prepare paneer',minutes:20,ingredients:[{name:'Paneer',quantity:500,unit:'g'}],phase:'cooking',guidance:null,evidence:'Reviewed source'}}/>);
 expect(screen.getByText('500 g')).toBeVisible();
 expect(screen.getByText('Paneer')).toBeVisible();
 expect(screen.getByText('Recipe details')).toHaveAttribute('aria-expanded','false');
});
