import {useState} from 'react';
export function AllergyChoices({value,onChange}:{value:string[]|null|undefined;onChange:(v:string[]|null)=>void}){
 const known=['nuts','gluten'];const other=(value||[]).filter(v=>!known.includes(v));
 const [showOther,setShowOther]=useState(other.length>0);
 function toggle(name:string,checked:boolean){const next=checked?[...(value||[]).filter(x=>x!==name),name]:(value||[]).filter(x=>x!==name);onChange(next.length?next:null);}
 return <fieldset><legend>Guest allergies</legend>
 <label className="check"><input type="checkbox" checked={Array.isArray(value)&&value.length===0} onChange={e=>{onChange(e.target.checked?[]:null);setShowOther(false);}}/>No known allergies</label>
 {known.map(name=><label className="check" key={name}><input type="checkbox" checked={(value||[]).includes(name)} onChange={e=>toggle(name,e.target.checked)}/>Avoid {name}</label>)}
 <label className="check"><input type="checkbox" checked={showOther} onChange={e=>{setShowOther(e.target.checked);if(!e.target.checked){const rest=(value||[]).filter(x=>known.includes(x));onChange(rest.length?rest:null);}else if(value?.length===0)onChange(null);}}/>Other</label>
 {showOther&&<label>Other allergies<input value={other.join(', ')} placeholder="For example, milk or eggs" onChange={e=>{const next=[...(value||[]).filter(x=>known.includes(x)),...e.target.value.split(',').map(x=>x.trim()).filter(Boolean)];onChange(next.length?next:null);}}/></label>}
 {value==null&&<p className="meta">Confirm allergies, or choose “No known allergies”.</p>}
 </fieldset>;
}
