import type {Gathering} from './api';
export function SchedulingChoices({gathering:g,days,change}:{gathering:Gathering;days:string[];change:(values:Partial<Gathering>)=>void}){
 const selected=g.prep_days||[];
 const limit=(d:string)=>g.daily_limits?.[d]??(new Date(d+'T12:00:00').getDay()%6===0?(g.profile?.weekend_minutes??120):(g.profile?.weekday_minutes??120));
 const limits=selected.map(limit); const uniform=limits.length>0&&limits.every(x=>x===limits[0]);
 const deadline=g.arrival?new Date(Date.parse(g.arrival)-(g.relax_minutes??60)*60000).toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',timeZone:g.profile?.timezone||'America/New_York'}):null;
 return <section className="card scheduling-choices"><h2>When can you prep?</h2>
 <div className="prep-day-chips">{days.map(day=><label key={day} className={selected.includes(day)?'chosen':''}><input type="checkbox" checked={selected.includes(day)} onChange={e=>change({prep_days:e.target.checked?[...selected,day]:selected.filter(d=>d!==day)})}/>{new Date(day+'T12:00:00').toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})}</label>)}</div>
 <details><summary>{uniform?`Up to ${limits[0]/60} hours per day`:limits.length?'Custom daily time':'Up to 2 hours per day'} · Adjust</summary><p className="meta">Includes cooking, supervision and cleanup.</p>{selected.map(day=><label key={day}>{day}<input aria-label={'Daily minutes '+day} type="number" min="0" max="1440" value={limit(day)} onChange={e=>change({daily_limits:{...g.daily_limits,[day]:+e.target.value}})}/></label>)}</details>
 <details><summary>Start prepping earlier</summary><label>I can start preparing on<input type="date" value={g.earliest_prep||''} onChange={e=>change({earliest_prep:e.target.value})}/></label></details>
 <h2>Cooking finished by</h2><p className="cooking-deadline"><strong>{deadline||'Set guest arrival first'}</strong> · {g.relax_minutes??60} minutes before guests arrive</p><p className="meta">Only light finishing after this.</p>
 <details><summary>Change cooking deadline</summary><label>Minutes before guests arrive<input type="number" min="0" max="240" value={g.relax_minutes??60} onChange={e=>change({relax_minutes:+e.target.value})}/></label></details>
 <p className="meta">{g.prep_windows?.length?`${g.prep_windows.length} custom prep windows · edit under More scheduling options.`:'We find free time on your selected calendar between 9 am and 9 pm, respecting protected time and your cooking deadline.'}</p>
 </section>;
}
