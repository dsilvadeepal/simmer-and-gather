import {useState} from 'react';
import type {Selection} from './api';
export function GuestContribution({item,arrival,onSave}:{item:Selection;arrival?:string|null;onSave:(values:Partial<Selection>)=>Promise<void>}){
 const [person,setPerson]=useState(item.contribution?.person||''),[servings,setServings]=useState(item.contribution?.servings||item.servings||1),[warm,setWarm]=useState(item.contribution?.warming_minutes||0),[saving,setSaving]=useState(false);
 return <form onSubmit={async e=>{e.preventDefault();setSaving(true);try{await onSave({servings,contribution:{...item.contribution,name:item.title,person:person.trim(),servings,confirmed:true,warming_minutes:warm,arrival,equipment:warm?'oven':null}});}finally{setSaving(false);}}}><label>Who’s bringing it?<input required value={person} onChange={e=>setPerson(e.target.value)}/></label><label>Serves<input type="number" required min="1" value={servings} onChange={e=>setServings(+e.target.value)}/></label><label>Warming time (minutes; 0 if none)<input type="number" required min="0" value={warm} onChange={e=>setWarm(+e.target.value)}/></label><button disabled={saving||!person.trim()}>Save contribution</button></form>;
}
