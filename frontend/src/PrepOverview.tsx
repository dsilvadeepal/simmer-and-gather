import type {Plan} from './api';
import {amount} from './ShoppingList';
type Assignment=NonNullable<Plan['assignments']>[number];
export function PrepOverview({assignments,timezone='America/New_York',fitDays=[]}:{assignments:Assignment[];timezone?:string;fitDays?:Plan['fit_days']}) {
 const sorted=[...assignments].sort((a,b)=>Date.parse(a.interval.start)-Date.parse(b.interval.start));
 const passive=(a:Assignment)=>a.task.active_minutes===0&&a.task.presence_minutes===0&&a.task.unattended;
 const work=sorted.filter(a=>!passive(a));
 const waiting=sorted.filter(passive);
 const clock=(s:string)=>new Date(s).toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',timeZone:timezone});
 const day=(s:string)=>new Date(s).toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric',timeZone:timezone});
 const title=(a:Assignment)=>a.task.title.split(' · ').slice(1).join(' · ')||a.task.title;
 // Attach waits to the nearest preceding work for that recipe; unpaired waits remain notes.
 const notes=new Map<string,Assignment[]>(); const unattached:Assignment[]=[];
 for(const w of waiting){
  const previous=work.filter(a=>a.task.recipe_id===w.task.recipe_id&&Date.parse(a.interval.start)<=Date.parse(w.interval.start)).at(-1);
  if(previous)notes.set(previous.task.id,[...(notes.get(previous.task.id)||[]),w]);else unattached.push(w);
 }
 const days=[...new Set(work.map(a=>day(a.interval.start)))];
 return <div className="prep-overview">
 {days.map(label=>{const rows=work.filter(a=>day(a.interval.start)===label);const dateKey=new Intl.DateTimeFormat('en-CA',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(rows[0].interval.start));const fit=fitDays?.find((d:any)=>d.day===dateKey) as {presence_minutes:number;limit_minutes:number}|undefined;return <section className="prep-day" key={label}><div className="day-heading"><h2>{label}</h2>{fit&&<span className="meta">{fit.presence_minutes} min planned / {fit.limit_minutes} min available{fit.presence_minutes>fit.limit_minutes?` · ${fit.presence_minutes-fit.limit_minutes} min cleanup overrun`:""}</span>}</div><div role="table" aria-label={label+" prep"}>
  <div className="prep-overview-header" role="row"><span>When</span><span>What to do</span><span>Details / tips</span></div>
  {rows.map(a=><div className="prep-overview-row" role="row" key={a.task.id}>
   <div role="cell"><p className="task-time">{clock(a.interval.start)}–{clock(a.interval.end)}</p></div>
   <div role="cell"><strong>{title(a)}</strong>{a.task.recipe_id&&<p className="meta">{a.task.title.split(' · ')[0]}</p>}</div>
   <div role="cell"><p className="meta">{a.task.active_minutes??a.task.minutes} min hands-on{a.person&&a.person!=='host'?` · helper ${a.person}`:''}</p>
    {(notes.get(a.task.id)||[]).map(w=><p className="meta" key={w.task.id}>{title(w)} · {w.task.minutes} min waiting, no active work. {day(w.interval.start)} at {clock(w.interval.start)} – {day(w.interval.end)} at {clock(w.interval.end)}.{w.task.guidance?' '+w.task.guidance:''}</p>)}
    {a.task.phase!=='cleanup'&&<>{(a.task.ingredients||[]).map((i,n)=><div className="inline-ingredient" key={n}><span>{i.name}</span><strong>{i.quantity==null?'Check amount':`${amount(i.quantity)} ${i.unit||''}`}</strong></div>)}{(a.task.guidance||a.task.evidence)&&<details><summary>Instructions & source notes</summary>{a.task.guidance&&<p>{a.task.guidance}</p>}{a.task.evidence&&<p className="meta">{a.task.evidence}</p>}</details>}</>}
   </div>
  </div>)}
 </div></section>;})}
  {!!unattached.length&&<div className="card"><strong>Preparation notes</strong>{unattached.map(w=><p className="meta" key={w.task.id}>{w.task.title} · {w.task.minutes} min waiting · starts {day(w.interval.start)} at {clock(w.interval.start)}.{w.task.guidance?' '+w.task.guidance:''}</p>)}</div>}
 </div>;
}
