import {expect,test} from 'vitest';
import {cookingCopy} from './cookingCopy';
test('separates storage and removes internal scheduling commentary',()=>{
 const result=cookingCopy('The author cooks this dal the night before entertaining. The page says leftovers keep refrigerated for up to five days. Estimated attention is reserved at the start and return-to-task points; adjust to actual cooking progress.');
 expect(result.steps).toEqual([]);
 expect(result.storage).toEqual(['Make this dal the day before.','leftovers keep refrigerated for up to five days.']);
});
test('preserves concrete cooking settings and checks without inferring any',()=>{
 expect(cookingCopy('Cook on high pressure for 20 minutes. Allow pressure to release naturally. Check beans are tender.').steps).toEqual(['Cook on high pressure for 20 minutes.','Allow pressure to release naturally.','Check beans are tender.']);
 expect(cookingCopy('').steps).toEqual([]);
});

test('allergy notes are recipe information, not cooking instructions',()=>{
 expect(cookingCopy('Contains cashews in the listed recipe.')).toEqual({steps:[],storage:[],notes:['Contains cashews.']});
});
