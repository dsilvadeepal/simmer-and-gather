import { useState } from 'react';
import { api, type Recipe } from './api';
export function NotionCollection({onSelect}:{onSelect:(source:string)=>void}) {
  const [recipes,setRecipes]=useState<Recipe[]|null>(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  async function refresh(){
    setLoading(true);setError('');
    try {setRecipes(await api<Recipe[]>('/notion/recipes'));}
    catch {setError('Your Notion collection is unavailable. You can still paste a recipe link below.');}
    finally {setLoading(false);}
  }
  return <section aria-label="Notion recipe collection">
    <button className="secondary" disabled={loading} onClick={refresh}>{loading?'Loading collection…':'Browse my Notion recipes'}</button>
    {error && <p role="alert">{error}</p>}
    {recipes?.length===0 && <p className="meta">Your Notion recipe library is connected and empty. Start by importing a recipe link below.</p>}
    {!!recipes?.length && <ul>{recipes.map(r=><li key={r.id}><button className="secondary" onClick={()=>onSelect(r.source)}>{r.title}</button></li>)}</ul>}
  </section>;
}
