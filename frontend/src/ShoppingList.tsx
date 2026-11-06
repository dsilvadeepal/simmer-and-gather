import type {Plan,Selection} from './api';
export function amount(n:number) {
 const whole=Math.floor(n), fraction=n-whole;
 for(const [value,symbol] of [[.25,'¼'],[.5,'½'],[.75,'¾'],[1/3,'⅓'],[2/3,'⅔']] as const)
  if(Math.abs(fraction-value)<.006)return (whole?String(whole):'')+symbol;
 return Number(n.toFixed(2)).toLocaleString();
}
export function ingredientName(name:string) {
 return name.replace(/\([^)]*\)/g,'').replace(/\*/g,'').replace(/^\s*\d+(?:[./]\d+)?(?:\s+to\s+\d+)?\s+/,'').replace(/\s+/g,' ').trim();
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
export function ShoppingList({items,selections}:{items:NonNullable<Plan['shopping']>;selections:Selection[]}) {
 const rows=items.filter(i=>! /^(water|tap water|warm water|cold water|hot water)$/i.test(ingredientName(i.name)));
 const combined=new Map<string,typeof items[number]>();
 for(const row of rows){const name=ingredientName(row.name),key=name.toLowerCase()+'|'+(row.unit||'');const previous=combined.get(key);combined.set(key,{...row,name,quantity:previous?(previous.quantity==null||row.quantity==null?null:previous.quantity+row.quantity):row.quantity});}
 const known=[...combined.values()].filter(i=>i.quantity!=null), unknown=[...combined.values()].filter(i=>i.quantity==null);
 const groups=new Map<string,typeof items>();
 for(const i of known){const group=shoppingGroup(ingredientName(i.name));groups.set(group,[...(groups.get(group)||[]),i]);}
 return <><p className="meta">Amounts cover the menu, minus confirmed ingredients on hand. “About” means rounded for shopping; use the recipe amounts when cooking.</p>
  {['Produce','Dairy & proteins','Pantry & spices','Frozen'].filter(name=>groups.has(name)).map(name=><details key={name}><summary>{name} · {groups.get(name)!.length}</summary><ul>{groups.get(name)!.map((i,n)=><li key={n}>{ingredientName(i.name)} <strong>{shoppingAmount(i.quantity!,i.unit)}</strong></li>)}</ul></details>)}
  {!!unknown.length&&<details><summary>Amounts to confirm · {unknown.length}</summary><p>The recipe quantity could not be scaled reliably. Check the original recipe for your guest count before buying.</p><ul>{unknown.map((i,n)=><li key={n}>{ingredientName(i.name)}</li>)}</ul></details>}
  {!rows.length&&<p>No shopping items in this proposal.</p>}
  <details><summary>Ingredients by recipe</summary>{selections.filter(s=>s.mode==='cook').map(s=><details key={s.id}><summary>{s.title}</summary>{s.recipe?.source&&/^https?:/.test(s.recipe.source)&&<a href={s.recipe.source} target="_blank" rel="noreferrer">Original recipe</a>}<ul>{s.recipe?.ingredients?.map((i,n)=><li key={n}>{i.name}</li>)}</ul></details>)}</details>
 </>;
}
