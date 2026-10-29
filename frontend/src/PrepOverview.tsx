import type {Plan} from './api';
import {TaskCard} from './TaskCard';
type Assignment=NonNullable<Plan['assignments']>[number];
export function PrepOverview({assignments,timezone='America/New_York'}:{assignments:Assignment[];timezone?:string}) {
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
 return <div className="prep-overview" role="table" aria-label="Prep overview">
  <div className="prep-overview-header" role="row"><span>When</span><span>What to do</span><span>Details / tips</span></div>
  {work.map(a=><div className="prep-overview-row" role="row" key={a.task.id}>
   <div role="cell"><strong>{day(a.interval.start)}</strong><p className="meta">{clock(a.interval.start)}–{clock(a.interval.end)}</p></div>
   <div role="cell"><strong>{title(a)}</strong>{a.task.recipe_id&&<p className="meta">{a.task.title.split(' · ')[0]}</p>}</div>
   <div role="cell"><p className="meta">{a.task.active_minutes??a.task.minutes} min hands-on{a.person&&a.person!=='host'?` · helper ${a.person}`:''}</p>
    {(notes.get(a.task.id)||[]).map(w=><p className="meta" key={w.task.id}>{title(w)} · {w.task.minutes} min waiting, no active work.{w.task.guidance?' '+w.task.guidance:''}</p>)}
    {a.task.phase!=='cleanup'&&<details><summary>Task details</summary><TaskCard task={a.task}/></details>}
   </div>
  </div>)}
  {!!unattached.length&&<div className="card"><strong>Preparation notes</strong>{unattached.map(w=><p className="meta" key={w.task.id}>{w.task.title} · {w.task.minutes} min waiting · starts {day(w.interval.start)} at {clock(w.interval.start)}.{w.task.guidance?' '+w.task.guidance:''}</p>)}</div>}
 </div>;
}
