import { useState } from 'react';
import { api, type Recipe } from './api';
export function NotionCollection({onSelect}:{onSelect:(recipe:Recipe)=>void}) {
  const [recipes,setRecipes]=useState<Recipe[]|null>(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  async function select(recipe:Recipe){
    setLoading(true);setError('');
    try {
      if (!recipe.id) throw new Error('Missing Notion page ID');
      onSelect(await api<Recipe>(`/notion/recipes/${encodeURIComponent(recipe.id)}/preview`));
    }
    catch {setError('Could not read this Notion recipe. Open its source link or try again.');}
    finally {setLoading(false);}
  }
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
    {!!recipes?.length && <ul>{recipes.map(r=><li key={r.id}><button className="secondary" disabled={loading} onClick={()=>select(r)}>{r.title}</button></li>)}</ul>}
  </section>;
}
