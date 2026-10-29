import {amount} from './ShoppingList';
import type {Inputs,Plan} from './api';
export function HostingSummary({inputs,plan,view='all'}:{inputs:Inputs;plan:Plan;view?:'all'|'menu'|'fit'}) {
 const g=inputs.gathering;
 const zone=g.profile?.timezone||'America/New_York';
 const deadline=g.arrival?new Date(Date.parse(g.arrival)-(g.relax_minutes??60)*60000):null;
 const fmt=amount;
 return <section className="card hosting-summary">
  {view!=='fit'&&<><h2>Your menu</h2>
  <p className="meta">{g.guests} people · quantities scale ingredients, not cooking batches</p>
  <div className="menu-summary" role="table" aria-label="Selected menu">
   <div role="row" className="menu-summary-head"><strong>Role / dish</strong><strong>Quantity to prepare</strong><strong>In your menu</strong></div>
   {(inputs.selections||[]).map(s=>{
    const r=s.recipe; const factor=r?.servings?(s.servings||1)/r.servings:null;
    const amounts=(r?.ingredients||[]).filter(i=>i.quantity!=null&&i.unit&&!/\b(butter|ghee|oil|spice|salt|pepper|paste)\b/i.test(i.name)&&i.name.toLowerCase().split(/\W+/).some(word=>word.length>3&&s.title.toLowerCase().includes(word))).slice(0,2);
    return <div role="row" key={s.id}>
     <div role="cell"><span className="meta">{s.category}</span><br/>{r?.source?.startsWith('https://')?<a href={r.source} target="_blank" rel="noreferrer">{s.title}</a>:s.title}</div>
     <div role="cell">{s.servings} portions{factor!=null&&<span className="meta"> · {fmt(factor)}× recipe</span>}{factor!=null&&amounts.map((i,n)=><div className="meta" key={n}>{fmt(i.quantity!*factor)} {i.unit} {i.name}</div>)}{!!r?.ingredients?.length&&<details><summary>All ingredient quantities</summary>{r.ingredients.map((i,n)=><p key={n}>{i.quantity==null||factor==null?'Check amount':fmt(i.quantity*factor)} {i.unit} {i.name}</p>)}</details>}</div>
     <div role="cell">{s.must_have?'Your must-have':s.mode==='buy'?'Bought prepared':s.mode==='guest'?'Guest contribution':s.vegetarian||r?.vegetarian?'Vegetarian option':'Your selected dish'}</div>
    </div>;
   })}
  </div>
  </>}{view!=='menu'&&<><h2>Your time</h2>
  {deadline&&<p>Major cooking ends by <strong>{deadline.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',timeZone:zone})}</strong> · {g.relax_minutes??60}-minute buffer before guests arrive.</p>}
  <p className="meta">Calendar: {inputs.availability?.status||'not checked'}{inputs.availability?.checked_at?' · checked '+new Date(inputs.availability.checked_at).toLocaleString('en-US',{timeZone:zone}):''}. Time below includes required presence and cleanup; waiting alone does not count.</p>
  {(plan.fit_days||[]).map((d:any)=><p className="fit-day" key={d.day}><strong>{d.day}</strong> · {d.presence_minutes} min of {d.limit_minutes} min{d.presence_minutes>d.limit_minutes?` + up to ${d.cleanup_allowance} min cleanup`:''}</p>)}
  {!!plan.advisories?.length&&<details><summary>Optional menu suggestions · {plan.advisories.length}</summary><ul>{plan.advisories.map((a,i)=><li key={i}>{a.explanation}</li>)}</ul></details>}
 </>}</section>;
}
