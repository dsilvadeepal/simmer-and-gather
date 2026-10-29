import type {Plan,Selection} from './api';
export function amount(n:number) {
 const whole=Math.floor(n), fraction=n-whole;
 for(const [value,symbol] of [[.25,'¼'],[.5,'½'],[.75,'¾'],[1/3,'⅓'],[2/3,'⅔']] as const)
  if(Math.abs(fraction-value)<.006)return (whole?String(whole):'')+symbol;
 return Number(n.toFixed(2)).toLocaleString();
}
export function ShoppingList({items,selections}:{items:NonNullable<Plan['shopping']>;selections:Selection[]}) {
 const group=(name:string)=>/\b(chicken|paneer|cream|milk|yogurt|butter|egg|pork|turkey|fish)\b/i.test(name)?'Chilled & proteins':/\b(onion|tomato|cilantro|cucumber|lemon|lime|pepper|carrot|potato|sprout|mint)\b/i.test(name)?'Produce':'Pantry & other';
 const groups=new Map<string,typeof items>();
 for(const i of items)groups.set(group(i.name),[...(groups.get(group(i.name))||[]),i]);
 return <><p className="meta">Combined amounts after confirmed pantry deductions. Open a group or recipe as needed.</p>
  {[...groups].map(([name,rows])=><details key={name}><summary>{name} · {rows.length}</summary><ul>{rows.map((i,n)=><li key={n}>{i.name} <strong>{i.quantity==null?'— Check amount':`${amount(i.quantity)} ${i.unit||''}`}</strong></li>)}</ul></details>)}
  {!items.length&&<p>No shopping items in this proposal.</p>}
  <details><summary>Ingredients by recipe</summary>{selections.filter(s=>s.mode==='cook').map(s=><details key={s.id}><summary>{s.title}</summary><ul>{s.recipe?.ingredients?.map((i,n)=><li key={n}>{i.name}</li>)}</ul></details>)}</details>
 </>;
}
