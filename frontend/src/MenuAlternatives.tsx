import {useEffect,useState} from 'react';
import {api,type Inputs,type Plan} from './api';
import {PlanViews} from './PlanViews';
type Option={swaps:unknown[];changes:{from:string;to:string;servings:number}[];inputs:Inputs;plan:Plan};
export function MenuAlternatives({inputs,plan,disabled,onApproved}:{inputs:Inputs;plan:Plan;disabled:boolean;onApproved:()=>Promise<void>}){
 const [options,setOptions]=useState<Option[]>([]),[message,setMessage]=useState(''),[busy,setBusy]=useState(false);
 const relevant=(plan.violations||[]).some(v=>['allergy','allergy_unknown','vegetarian'].includes(v.code));
 const id=inputs.gathering.id,revision=inputs.gathering.revision;
 useEffect(()=>{
  if(!relevant||disabled)return;
  let cancelled=false;setBusy(true);setOptions([]);setMessage('Checking recipe alternatives and prep time…');
  api<{suggestions:Option[];message:string}>('/menu/'+id+'/alternatives',{expected_revision:revision}).then(r=>{if(!cancelled){setOptions(r.suggestions);setMessage(r.message);}}).catch(e=>{if(!cancelled)setMessage(e.message);}).finally(()=>{if(!cancelled)setBusy(false);});
  return()=>{cancelled=true;};
 },[id,revision,plan.id,relevant,disabled]);
 if(!relevant)return null;
 return <section className="card"><h2>Alternatives that fit</h2><p role="status">{message}</p>{options.map((option,index)=><div key={index}>
  <ul>{option.changes.map(c=><li key={c.from}>{c.from===c.to?<>Keep <strong>{c.to}</strong> · updated ingredient screening</>:<>{c.from} → <strong>{c.to}</strong></>} · {c.servings} servings</li>)}</ul>
  <p className="meta">Prep limits and buffer preserved. Ingredient labels still need checking.</p>
  <details><summary>Review checked prep schedule</summary><PlanViews inputs={option.inputs} plan={option.plan}/></details>
  <button disabled={busy||disabled} onClick={async()=>{setBusy(true);try{await api('/menu/'+id+'/alternatives/approve',{expected_revision:revision,swaps:option.swaps});await onApproved();}catch(e){setMessage(e instanceof Error?e.message:'Could not approve this swap.');}finally{setBusy(false);}}}>Approve these swaps</button>
 </div>)}<p className="meta">Previews are not saved. Approval rechecks availability and updates your menu only.</p></section>;
}
