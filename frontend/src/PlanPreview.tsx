import type {Inputs,Plan} from './api';
import {PrepOverview} from './PrepOverview';
export function PlanPreview({inputs,plan}:{inputs:Inputs;plan:Plan}){
 return <div aria-label="Read-only schedule preview"><p className="meta">Preview only. Nothing is saved until you choose this option.</p><PrepOverview recipes={(inputs.selections||[]).flatMap(s=>s.recipe?[{...s.recipe,id:s.id}]:[])} assignments={plan.assignments||[]} timezone={inputs.gathering.profile?.timezone} fitDays={plan.fit_days}/></div>;
}
