import {useState} from 'react';
import type {Plan,Selection} from './api';
export function amount(n:number) {
 const whole=Math.floor(n), fraction=n-whole;
 for(const [value,symbol] of [[.25,'¼'],[.5,'½'],[.75,'¾'],[1/3,'⅓'],[2/3,'⅔']] as const)
  if(Math.abs(fraction-value)<.006)return (whole?String(whole):'')+symbol;
 return Number(n.toFixed(2)).toLocaleString();
}
export function ingredientName(name:string) {
 return name.replace(/\(([^)]*)\)/g,(whole,content)=>/^\d+(?:[.-]\d+)?[- ](?:ounce|oz|pound|lb)$/i.test(content)?whole:'').replace(/\*/g,'').replace(/^\s*\d+(?:[./]\d+)?(?:\s+to\s+\d+)?\s+/,'').replace(/\s+/g,' ').trim();
}
export function shoppingGroup(name:string) {
 if(/\bfrozen\b/i.test(name))return 'Frozen';
 if(/\b(chicken|paneer|cream|milk|yogurt|butter|eggs?|pork|turkey|fish)\b/i.test(name))return 'Dairy & proteins';
 if(/\b(onions?|tomatoes?|cilantro|cucumbers?|lemons?|limes?|peppers?|carrots?|potatoes?|sprouts?|mint|spinach|cauliflower|green beans|garlic|ginger|chili)\b/i.test(name)&&! /powder|paste|seeds|dried/i.test(name))return 'Produce';
 return 'Pantry & spices';
}
export function shoppingAmount(q:number,u?:string|null) {
 let n=q, unit=u||'';
 if(unit==='tsp'&&n>=3){n/=3;unit='tbsp';}
 if(unit==='tbsp'&&n>=16){n/=16;unit='cup';}
 const rounded=n>=.25?Math.round(n*4)/4:n;
 return `${Math.abs(rounded-n)>.006?'About ':''}${amount(rounded)} ${unit}`.trim();
}
export function ShoppingList({items,selections,gatheringId}:{items:NonNullable<Plan['shopping']>;selections:Selection[];gatheringId?:string}) {
 const storageKey=gatheringId?'simmer:shopping:'+gatheringId:null;
 const [checked,setChecked]=useState<Record<string,string>>(()=>{
  try {const value=JSON.parse(storageKey?localStorage.getItem(storageKey)||'{}':'{}');return value&&typeof value==='object'&&!Array.isArray(value)?value:{};}catch{return {};}
 });
 const [onlyNeeded,setOnlyNeeded]=useState(false);
 const [saveError,setSaveError]=useState(false);
 type Row=NonNullable<Plan['shopping']>[number];
 const identity=(i:Row)=>i.name.trim().toLowerCase()+'|'+(i.unit||'');
 const signature=(i:Row)=>JSON.stringify([i.quantity??null,i.amount_detail?.minimum??null,i.amount_detail?.maximum??null]);
 const have=(i:Row)=>checked[identity(i)]===signature(i);
 function toggle(i:Row){
  const next={...checked};
  if(have(i))delete next[identity(i)];else next[identity(i)]=signature(i);
  setChecked(next);
  try{if(storageKey)localStorage.setItem(storageKey,JSON.stringify(next));setSaveError(false);}catch{setSaveError(true);}
 }
 const visible=(list:Row[])=>onlyNeeded?list.filter(i=>!have(i)):list;
 function row(i:Row,n:number){
  const detail=i.quantity!=null?shoppingAmount(i.quantity,i.unit):i.amount_detail?.kind==='range'?amount(i.amount_detail.minimum!)+'–'+amount(i.amount_detail.maximum!)+' '+(i.unit||''):'';
  return <li key={identity(i)+n} className="shopping-check-row"><label><input type="checkbox" aria-label={'Have '+i.name} checked={have(i)} onChange={()=>toggle(i)}/><span className={have(i)?'shopping-have':''}>{i.name}</span>{detail&&<strong className={have(i)?'shopping-have shopping-quantity':'shopping-quantity'}>{detail}</strong>}</label>{checked[identity(i)]&&!have(i)&&<small>Amount changed—check again.</small>}</li>;
 }
 const rows=items.filter(i=>! /^(water|tap water|warm water|cold water|hot water)$/i.test(ingredientName(i.name)));
 const combined=new Map<string,typeof items[number]>();
 for(const row of rows){const name=row.quantity==null?row.name.trim():ingredientName(row.name),key=name.toLowerCase()+'|'+(row.unit||'')+(row.amount_detail?.kind==='range'?'|'+combined.size:'');const previous=combined.get(key);combined.set(key,{...row,name,quantity:previous?(previous.quantity==null||row.quantity==null?null:previous.quantity+row.quantity):row.quantity});}
 const known=[...combined.values()].filter(i=>i.quantity!=null), unknown=[...combined.values()].filter(i=>i.quantity==null);
 const flexible=unknown.filter(i=>i.amount_detail?.kind==='to_taste'||i.amount_detail?.optional||/to taste|as required|as needed|for greasing|for molds|oil for|pinch|optional|for serving/i.test(i.name));
 const ranges=unknown.filter(i=>!flexible.includes(i)&&(i.amount_detail?.kind==='range'||/scaled range:/i.test(i.name)));
 const review=unknown.filter(i=>!flexible.includes(i)&&!ranges.includes(i));
 const groups=new Map<string,typeof items>();
 for(const i of [...known,...ranges]){const group=shoppingGroup(ingredientName(i.name));groups.set(group,[...(groups.get(group)||[]),i]);}
 const all=[...combined.values()], haveCount=all.filter(have).length;
 return <div className="shopping-list"><p className="meta">Tick what you have at home. “About” means rounded for shopping; use the recipe amounts when cooking.</p>
 <div className="row"><button className="secondary" aria-pressed={onlyNeeded} onClick={()=>setOnlyNeeded(!onlyNeeded)}>{onlyNeeded?'Show all ingredients':'Show only what I need'}</button><span role="status">{all.length-haveCount} to buy · {haveCount} already have</span></div>
 {storageKey&&<p className="meta">{saveError?'Checks could not be saved. Keep this tab open.':'Checks saved for this gathering on this device.'}</p>}
 {onlyNeeded&&all.length>0&&haveCount===all.length&&<p>You have everything on this list.</p>}
  {['Produce','Dairy & proteins','Pantry & spices','Frozen'].filter(name=>groups.has(name)&&visible(groups.get(name)!).length>0).map(name=><details key={name}><summary>{name} · {visible(groups.get(name)!).length}</summary><ul>{visible(groups.get(name)!).map(row)}</ul></details>)}

  {!!visible(flexible).length&&<details><summary>To taste & optional · {visible(flexible).length}</summary><p>The source leaves the amount to your preference or use.</p><ul>{visible(flexible).map(row)}</ul></details>}
  {!!visible(review).length&&<details><summary>Amounts to confirm · {visible(review).length}</summary><p>Check the original recipe for your guest count before buying.</p><ul>{visible(review).map(row)}</ul></details>}
  {!rows.length&&<p>No shopping items in this proposal.</p>}
  {!onlyNeeded&&<details><summary>Ingredients by recipe</summary>{selections.filter(s=>s.mode==='cook').map(s=><details key={s.id}><summary>{s.title}</summary>{s.recipe?.source&&/^https?:/.test(s.recipe.source)&&<a href={s.recipe.source} target="_blank" rel="noreferrer">Original recipe</a>}<ul>{s.recipe?.ingredients?.map((i,n)=><li key={n}>{i.name}</li>)}</ul></details>)}</details>}
 </div>;
}
