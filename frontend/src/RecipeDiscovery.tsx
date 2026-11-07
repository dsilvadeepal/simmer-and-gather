import {useState} from 'react';
import {api} from './api';
export function RecipeDiscovery({onSelect}:{onSelect:(url:string)=>void}){
 const [query,setQuery]=useState(''),[results,setResults]=useState<{title:string;url:string}[]>([]),[busy,setBusy]=useState(false),[message,setMessage]=useState('');
 async function search(){setBusy(true);setMessage('');try{const rows=await api<{title:string;url:string}[]>('/recipes/discover',{query});setResults(rows);if(!rows.length)setMessage('No matches. Try a dish name or paste a recipe link.');}catch(e){setMessage(e instanceof Error?e.message:'Search unavailable');}finally{setBusy(false);}}
 return <div><label>Find a recipe online<input value={query} onChange={e=>setQuery(e.target.value)} placeholder="For example: make-ahead paneer starter" maxLength={300}/></label>
 <p className="meta">Only this search phrase is sent to the search service. Results need review before saving.</p>
 <button className="secondary" disabled={busy||!query.trim()} onClick={search}>{busy?'Searching…':'Find recipe links'}</button>
 {message&&<p role="status">{message}</p>}
 <ul>{results.map(r=><li key={r.url}><a href={r.url} target="_blank" rel="noreferrer">{r.title}</a> <button className="secondary" onClick={()=>onSelect(r.url)}>Use this link</button></li>)}</ul></div>;
}
