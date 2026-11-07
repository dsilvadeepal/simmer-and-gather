import {useId,useRef,useState} from 'react';
import type {Inputs,Plan} from './api';
import {PrepOverview} from './PrepOverview';
import {HostingSummary} from './HostingSummary';
import {ShoppingList} from './ShoppingList';
export function PlanViews({inputs,plan}:{inputs:Inputs;plan:Plan}){
 const [active,setActive]=useState(0);const refs=useRef<(HTMLButtonElement|null)[]>([]);const id=useId();
 const checklist=(plan.checklist||[]).filter(x=>!(/finish drinks/i.test(x)&&!(inputs.selections||[]).some(s=>s.category==='drinks'))&&!/^Keep dishes warm as directed$/i.test(x));
 const labels=['Schedule','Menu','Shopping','Finishing'];
 return <div className="plan-workspace"><div role="tablist" aria-label="Plan views" className="plan-tabs">{labels.map((label,i)=><button key={label} ref={el=>{refs.current[i]=el}} role="tab" id={`${id}-tab-${i}`} aria-controls={`${id}-panel-${i}`} aria-selected={active===i} tabIndex={active===i?0:-1} onClick={()=>setActive(i)} onKeyDown={e=>{const next=e.key==='ArrowRight'?(i+1)%4:e.key==='ArrowLeft'?(i+3)%4:e.key==='Home'?0:e.key==='End'?3:null;if(next!==null){e.preventDefault();setActive(next);refs.current[next]?.focus();}}}>{label}</button>)}</div>
 {labels.map((label,i)=><section key={label} role="tabpanel" id={`${id}-panel-${i}`} aria-labelledby={`${id}-tab-${i}`} hidden={active!==i} tabIndex={0}>
 {i===0&&<><HostingSummary inputs={inputs} plan={plan} view="fit"/>{!plan.assignments?.length&&<p>No cooking sessions are scheduled yet. Review the plan checks and update your plan.</p>}<PrepOverview recipes={(inputs.selections||[]).flatMap(s=>s.recipe?[{...s.recipe,id:s.id}]:[])} assignments={plan.assignments||[]} timezone={inputs.gathering.profile?.timezone} fitDays={plan.fit_days}/></>}
 {i===1&&<HostingSummary inputs={inputs} plan={plan} view="menu"/>}
 {i===2&&<section className="card"><h2>Shopping list</h2><ShoppingList key={inputs.gathering.id} gatheringId={inputs.gathering.id} items={plan.shopping||[]} selections={inputs.selections||[]}/></section>}
 {i===3&&<section className="card"><h2>Finishing touches</h2><ul>{checklist.map((x,n)=><li key={n}>{x}</li>)}</ul>{!checklist.length&&<p>No extra finishing tasks.</p>}</section>}
 </section>)}
 </div>;
}
