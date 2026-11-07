import type {Plan,Recipe} from './api';
import {cookingCopy,taskInstructions,shortDishName} from './cookingCopy';
import {amount} from './ShoppingList';
export function durationLabel(minutes:number) {
 const h=Math.floor(minutes/60), m=minutes%60;
 return h ? `${h} hr${m?` ${m} min`:''}` : `${m} min`;
}
type Assignment=NonNullable<Plan['assignments']>[number];
export function continuousBlocks(rows:Assignment[]) {
 const blocks:{start:string;end:string;tasks:Assignment[]}[]=[];
 for(const row of rows){
  const last=blocks.at(-1);
  if(last && Date.parse(row.interval.start)<=Date.parse(last.end)){
   last.tasks.push(row);
   if(Date.parse(row.interval.end)>Date.parse(last.end))last.end=row.interval.end;
  }else blocks.push({start:row.interval.start,end:row.interval.end,tasks:[row]});
 }
 return blocks;
}
export function taskGroups(tasks:Assignment[]) {
 const groups:{label:string;tasks:Assignment[]}[]=[];
 const action=(a:Assignment)=>a.task.title.split(' · ').slice(1).join(' · ')||a.task.title;
 for(const a of tasks){
  const last=groups.at(-1), previous=last?.tasks.at(-1);
  const reheat=previous&&/^reheat\b/i.test(action(a))&&/^reheat\b/i.test(action(previous));
  const airfry=previous&&a.task.recipe_id&&a.task.recipe_id===previous.task.recipe_id&&/preheat air fryer/i.test(action(previous))&&/^air.fry/i.test(action(a));
  if(last&&(reheat||airfry)&&previous?.person===a.person){
   last.tasks.push(a);
   const names=[...new Set(last.tasks.map(t=>t.task.title.split(' · ')[0]))];
   last.label=reheat?'Reheat dishes thoroughly':'Thread skewers, preheat and air-fry, turning halfway';
   if(reheat&&names.some(n=>/dal/i.test(n))&&names.some(n=>/butter chicken/i.test(n))&&names.length===2)last.label='Reheat dal and butter chicken';
  }else groups.push({label:action(a),tasks:[a]});
 }
 return groups;
}
export function PrepOverview({assignments,timezone='America/New_York',fitDays=[],recipes=[]}:{recipes?:Recipe[];assignments:Assignment[];timezone?:string;fitDays?:Plan['fit_days']}) {
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
 const recipeNotes=recipes.filter(r=>work.some(a=>a.task.recipe_id===r.id));
 const storageFor=(id:string|undefined)=>[...new Set(work.filter(a=>a.task.recipe_id===id).flatMap(a=>cookingCopy(a.task.guidance||'').storage))];
 const instructions=(a:Assignment)=>taskInstructions(a.task.guidance||'',title(a),work.filter(b=>b.task.recipe_id===a.task.recipe_id&&b.task.guidance===a.task.guidance).length>1);
 const otherNotes=(id:string|undefined)=>[...new Set(work.filter(a=>a.task.recipe_id===id).flatMap(a=>{
  const copy=cookingCopy(a.task.guidance||'');
  return [...copy.notes,...(work.filter(b=>b.task.recipe_id===id&&b.task.guidance===a.task.guidance).length>1?copy.steps:[])];
 }))];
 const days=[...new Set(work.map(a=>day(a.interval.start)))];
 return <div className="prep-overview"><p className="meta">Times are estimates. Active time includes cooking, supervision and cleanup; start-to-finish time also includes waiting.</p>
 {days.map(label=>{const rows=work.filter(a=>day(a.interval.start)===label);const dateKey=new Intl.DateTimeFormat('en-CA',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(rows[0].interval.start));const fit=fitDays?.find((d:any)=>d.day===dateKey) as {presence_minutes:number;limit_minutes:number}|undefined;return <section className="prep-day" key={label}><div className="day-heading"><h2>{label}</h2>{fit&&<span className="meta">{durationLabel(fit.presence_minutes)} active · {durationLabel(fit.limit_minutes)} daily allowance{fit.presence_minutes>fit.limit_minutes?` · ${fit.presence_minutes-fit.limit_minutes} extra min beyond allowance`:""}</span>}</div><p className="meta">{durationLabel(continuousBlocks(rows).reduce((total,b)=>total+(Date.parse(b.end)-Date.parse(b.start))/60000,0))} start to finish across sessions, including cooking and waiting.</p><div role="table" aria-label={label+" prep"}>
  <div className="prep-overview-header" role="row"><span>When</span><span>What to do</span></div>
  {continuousBlocks(rows).map(block=><div className="prep-overview-row prep-session" role="row" key={block.start}>
   <div role="cell"><p className="task-time">{clock(block.start)}–{clock(block.end)}</p><p className="meta">{durationLabel((Date.parse(block.end)-Date.parse(block.start))/60000)} start to finish</p></div>
   <div role="cell"><ul className="session-tasks">{taskGroups(block.tasks).map(group=><li key={group.tasks[0].task.id}><strong>{group.label}</strong><p className="meta">{[...new Set(group.tasks.filter(a=>a.task.recipe_id).map(a=>shortDishName(a.task.title.split(' · ')[0])))].join(' · ')}</p>{group.tasks.map(a=><div key={a.task.id}>{a.person&&a.person!=='host'&&<p className="meta">Helper: {a.person}</p>}
    {(notes.get(a.task.id)||[]).map(w=><p className="meta" key={w.task.id}>{title(w)} · {durationLabel(w.task.minutes||0)} waiting, no active work. {day(w.interval.start)} at {clock(w.interval.start)} – {day(w.interval.end)} at {clock(w.interval.end)}.</p>)}
    {a.task.phase!=='cleanup'&&<>{a.task.active_minutes!=null&&a.task.minutes!=null&&a.task.minutes>a.task.active_minutes&&<p className="meta">{durationLabel(a.task.active_minutes)} hands-on · {durationLabel(a.task.minutes-a.task.active_minutes)} cooking or waiting{(a.task.presence_minutes??0)>a.task.active_minutes?' with supervision':' between check-ins'}.</p>}{(a.task.ingredients||[]).map((i,n)=><div className="inline-ingredient" key={n}><span>{i.name}</span><strong>{i.quantity==null?'Check amount':`${amount(i.quantity)} ${i.unit||''}`}</strong></div>)}{instructions(a).length>0&&<details><summary>How to</summary><ul>{instructions(a).map(line=><li key={line}>{line}</li>)}</ul></details>}</>}
   </div>)}</li>)}</ul></div>
  </div>)}
 </div></section>;})}
  {!!unattached.length&&<div className="card"><strong>Preparation notes</strong>{unattached.map(w=><p className="meta" key={w.task.id}>{w.task.title} · {durationLabel(w.task.minutes||0)} waiting · starts {day(w.interval.start)} at {clock(w.interval.start)}.</p>)}</div>}
 {!!recipeNotes.length&&<details className="recipe-notes"><summary>Recipe notes & links</summary>{recipeNotes.map(r=><section key={r.id}><h3>{shortDishName(r.title)}</h3>{otherNotes(r.id).map(note=><p key={note}>{note}</p>)}{storageFor(r.id).length>0&&<><strong>Make ahead & store</strong><ul>{storageFor(r.id).map(note=><li key={note}>{note}</li>)}</ul></>}{/^https?:\/\//.test(r.source)&&<a href={r.source} target="_blank" rel="noreferrer">Original recipe</a>}</section>)}</details>}
 </div>;
}
