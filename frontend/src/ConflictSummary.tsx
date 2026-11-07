import type {Inputs,Plan} from './api';
export function ConflictSummary({inputs,plan,onEditDiet}:{inputs:Inputs;plan:Plan;onEditDiet:()=>void}){
 const issues=plan.violations||[];
 const allergy=issues.filter(v=>v.code==='allergy'),unknown=issues.filter(v=>v.code==='allergy_unknown');
 const vegetarian=issues.some(v=>v.code==='vegetarian');
 const unscheduled=issues.filter(v=>v.code==='unscheduled');
 const dishes=(inputs.selections||[]).filter(s=>unscheduled.some(v=>v.affected_ids?.some(id=>id.startsWith(s.id+':'))));
 if(!issues.length)return null;
 return <section className="card" aria-label="What needs attention"><h2>What needs attention</h2>
 {!!allergy.length&&<p>{allergy.length===1?'A selected dish conflicts':'Selected dishes conflict'} with your guests’ dietary restrictions. Choose a checked alternative below.</p>}
 {!!unknown.length&&<p>Ingredient screening is incomplete for {unknown.length} {unknown.length===1?'dish':'dishes'}. Choose a reviewed alternative, or review the recipe and product labels. We haven’t assumed these dishes are suitable.</p>}
 {vegetarian&&<p>Your vegetarian guests need more main-dish portions. The alternatives below are checked for portions and prep time{unscheduled.length?' and can address both issues':''}.</p>}
 {!vegetarian&&dishes.map(s=>{
  const waiting=(s.recipe?.tasks||[]).filter(t=>t.unattended&&(t.minutes||0)>=720);
  return <p key={s.id}><strong>{s.title}:</strong> its preparation sequence doesn’t fit the selected windows.{waiting.length?` The recipe includes ${waiting.map(t=>`${Math.round((t.minutes||0)/60)} hours for ${t.title.toLowerCase()}`).join('; ')}.`:''} {plan.advisories?.some(a=>a.code==='buy_prepared'&&a.affected_ids?.includes(s.id!))?'A bought-prepared option fits; review it below.':'Review the task details or try a different recipe before adding more time.'}</p>;
 })}
 {(allergy.length>0||unknown.length>0||vegetarian)&&<button className="secondary" onClick={onEditDiet}>Review guest needs</button>}
 {!allergy.length&&!unknown.length&&!vegetarian&&!dishes.length&&<p>{plan.outcome?.message||"Review the details below before using this plan."}</p>}
 <details><summary>Task details · {issues.length}</summary><ul>{[...new Set(issues.map(v=>v.explanation))].map(text=><li key={text}>{text}</li>)}</ul></details>
 </section>;
}
