import {render,screen,fireEvent} from '@testing-library/react';
import {expect,test,vi} from 'vitest';
import {RecipeReview} from './RecipeReview';
test('unknown timings remain blank until explicitly entered',()=>{
 const change=vi.fn();render(<RecipeReview recipe={{id:'r',title:'Rice',source:'source',version:'1',category:'mains',source_text:'',reviewed:false,uncertainties:[],tasks:[{id:'t',title:'Cook rice',minutes:null,recipe_id:'r',dependencies:[],skill:'cook',capacity:1,ingredients:[],phase:'cooking',unattended:false}],ingredients:[]}} onChange={change}/>);
 const time=screen.getByLabelText('Elapsed minutes · Cook rice');expect(time).toHaveValue(null);
 fireEvent.change(time,{target:{value:'20'}});
 expect(change.mock.calls[0][0].tasks[0].minutes).toBe(20);
 expect(change.mock.calls[0][0].tasks[0].max_ahead_hours).toBeUndefined();
});
