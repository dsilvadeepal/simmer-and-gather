import {useState} from 'react';
import {api,type Inputs,type Plan} from './api';
import {PlanPreview} from './PlanPreview';
type Result={inputs:Inputs;plan:Plan};
export function PreparedAlternative({inputs,selectionId,disabled,onApproved}:{inputs:Inputs;selectionId:string;disabled:boolean;onApproved:(r:Result)=>Promise<void>}){
 const [preview,setPreview]=useState<Result|null>(null),[busy,setBusy]=useState(false),[error,setError]=useState('');
 const item=(inputs.selections||[]).find(s=>s.id===selectionId);
 async function request(approve=false){setBusy(true);setError('');try{const r=await api<Result>('/menu/'+inputs.gathering.id+(approve?'/prepared-approve':'/prepared-preview'),{expected_revision:inputs.gathering.revision,selection_id:selectionId});if(approve)await onApproved(r);else setPreview(r);}catch(e){setError(e instanceof Error?e.message:'Could not check this option');}finally{setBusy(false);}}
 return <section className="card"><h2>Buy {item?.title} prepared</h2><p>Keep the dish and reduce cooking. Check the supplier’s ingredients and preparation instructions.</p>{error&&<p role="alert">{error}</p>}{preview?<><details><summary>Review checked prep schedule</summary><PlanPreview {...preview}/></details><button disabled={busy||disabled} onClick={()=>request(true)}>Use this option and plan</button></>:<button disabled={busy||disabled} onClick={()=>request()}>Review bought option</button>}</section>;
}
