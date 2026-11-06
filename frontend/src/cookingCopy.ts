// Present cooking guidance separately from provenance; never infer cooking settings.
export function cookingCopy(text:string='') {
 const steps:string[]=[], storage:string[]=[], notes:string[]=[];
 for(const raw of text.split(/(?<=[.!?])\s+|\n+/)){
  let line=raw.trim();
  if(!line)continue;
  if(/^(Method reviewed|Estimated attention|Attention placement|hands-on and waiting|make-ahead window is)/i.test(line))continue;
  line=line.replace(/^The author cooks this (.+?) the night before entertaining\.?$/i,'Make this $1 the day before.')
   .replace(/^The page says /i,'');
  if(/^contains\b|allergen|allergies|nut.free|gluten.free/i.test(line)) notes.push(line.replace(/ in the listed recipe/i,''));
  else if(/^reheat/i.test(line)) storage.push(line.split(';')[0]+(line.includes(';')?'.':''));
  else if(/cook near serving|best hot and fresh/i.test(line)) notes.push('Cook close to serving for the best texture.');
  else if(/refrigerat|shallow containers|make.+ahead|day before|day ahead|leftovers|store|storage/i.test(line)) storage.push(line);
  else steps.push(line);
 }
 return {steps:[...new Set(steps)],storage:[...new Set(storage)],notes:[...new Set(notes)]};
}

export function taskInstructions(text:string, title:string, repeated=false) {
 const copy=cookingCopy(text);
 // Shared recipe-level guidance is not an instruction for every task.
 const steps=repeated?[]:copy.steps;
 if(/reheat/i.test(title)) return [...steps,...copy.storage.filter(s=>/^reheat/i.test(s))];
 return steps;
}
