import type {Recipe, Task} from './api';
const numberOrNull=(s:string)=>s===''?null:Number(s);
export function RecipeReview({recipe:r,onChange}:{recipe:Recipe;onChange:(r:Recipe)=>void}) {
 const update=(v:Partial<Recipe>)=>onChange({...r,...v});
 const task=(i:number,v:Partial<Task>)=>update({tasks:(r.tasks||[]).map((t,j)=>j===i?{...t,...v}:t)});
 return <div className="recipe-review">
  <p className="meta">Review what the source supports. Leave unknown values blank; missing timing or storage evidence will prevent an unsupported prep plan.</p>
  <div className="grid">
   <label>Recipe name<input value={r.title} onChange={e=>update({title:e.target.value})}/></label>
   <label>Servings<input type="number" min="1" value={r.servings??''} onChange={e=>update({servings:numberOrNull(e.target.value)})}/></label>
   <label>Category<select value={r.category||'mains'} onChange={e=>update({category:e.target.value as Recipe['category']})}>{['starters','mains','sides','desserts','drinks'].map(c=><option key={c}>{c}</option>)}</select></label>
   <label>Vegetarian<select value={r.vegetarian===null||r.vegetarian===undefined?'unknown':String(r.vegetarian)} onChange={e=>update({vegetarian:e.target.value==='unknown'?null:e.target.value==='true'})}><option value="unknown">Not verified</option><option value="true">Yes</option><option value="false">No</option></select></label>
  </div>
  <label>Known allergens (comma separated; blank means not verified)<input value={r.allergens?.join(', ')||''} onChange={e=>update({allergens:e.target.value.trim()?e.target.value.split(',').map(s=>s.trim()):null})}/></label>
  <label className="check"><input type="checkbox" checked={Array.isArray(r.allergens)&&r.allergens.length===0} onChange={e=>update({allergens:e.target.checked?[]:null})}/>I checked the source: no declared allergens</label>
  <h3>Ingredients</h3>
  {(r.ingredients||[]).map((item,i)=><div className="grid" key={i}>
   <label>Ingredient {i+1}<input value={item.name} onChange={e=>update({ingredients:r.ingredients!.map((x,j)=>j===i?{...x,name:e.target.value}:x)})}/></label>
   <label>Quantity {i+1}<input type="number" min="0" step="any" value={item.quantity??''} onChange={e=>update({ingredients:r.ingredients!.map((x,j)=>j===i?{...x,quantity:numberOrNull(e.target.value)}:x)})}/></label>
   <label>Unit {i+1}<input value={item.unit||''} onChange={e=>update({ingredients:r.ingredients!.map((x,j)=>j===i?{...x,unit:e.target.value||null}:x)})}/></label>
  </div>)}
  <button className="secondary" onClick={()=>update({ingredients:[...(r.ingredients||[]),{name:'',quantity:null,unit:null}]})}>Add ingredient</button>
  <h3>Preparation steps</h3>
  {(r.tasks||[]).map((t,i)=><details key={t.id} open={i===0}>
   <summary>{t.title||`Step ${i+1}`}</summary>
   <label>Step name<input value={t.title} onChange={e=>task(i,{title:e.target.value})}/></label>
   <div className="grid">
    {(['minutes','active_minutes','presence_minutes','max_ahead_hours'] as const).map((key,k)=><label key={key}>{['Elapsed minutes','Hands-on minutes','Minutes someone must be present','Maximum hours ahead supported by source'][k]}<input aria-label={`${['Elapsed minutes','Hands-on minutes','Presence minutes','Make-ahead hours'][k]} · ${t.title}`} type="number" min={key==='minutes'?1:0} value={t[key]??''} onChange={e=>task(i,{[key]:numberOrNull(e.target.value)})}/></label>)}
   </div>
   <label>Source evidence<textarea value={t.evidence||''} onChange={e=>task(i,{evidence:e.target.value||null})}/></label>
   <label>Storage / preparation notes<textarea value={t.guidance||''} onChange={e=>task(i,{guidance:e.target.value||null})}/></label>
   <label>Equipment<select value={t.resource||''} onChange={e=>task(i,{resource:e.target.value||null})}><option value="">None</option>{['oven','stovetop','air_fryer','instant_pot'].map(x=><option key={x}>{x}</option>)}</select></label>
   <label>Depends on completed steps<select multiple value={t.dependencies||[]} onChange={e=>task(i,{dependencies:Array.from(e.target.selectedOptions,x=>x.value)})}>{(r.tasks||[]).filter(x=>x.id!==t.id).map(x=><option key={x.id} value={x.id}>{x.title}</option>)}</select></label>
   <p className="meta">Ingredient amounts for this step</p>
   {(r.ingredients||[]).map((item,j)=><label key={j} className="check"><input type="checkbox" checked={(t.ingredients||[]).some(x=>x.name===item.name)} onChange={e=>task(i,{ingredients:e.target.checked?[...(t.ingredients||[]),item]:(t.ingredients||[]).filter(x=>x.name!==item.name)})}/>{item.name}</label>)}
  </details>)}
  <button className="secondary" onClick={()=>update({tasks:[...(r.tasks||[]),{id:crypto.randomUUID(),title:'New step',recipe_id:r.id||'',dependencies:[],skill:'cook',capacity:1,ingredients:[],phase:'cooking',unattended:false}]})}>Add step</button>
  <details><summary>Original source</summary><p style={{whiteSpace:'pre-wrap',overflowWrap:'anywhere'}}>{r.source_text}</p><p>{r.source}</p></details>
 </div>;
}
