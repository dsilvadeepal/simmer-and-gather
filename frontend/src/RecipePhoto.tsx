import {useState} from 'react';
import {Leaf} from 'lucide-react';
import type {Recipe} from './api';
import {recipeImages} from './recipeImages';
export function recipePhoto(recipe:Recipe|null|undefined,library:Recipe[]) {
 const current=library.find(r=>r.id===recipe?.id);
 return {
  url:current?.image_url||recipe?.image_url||recipeImages[recipe?.source||''],
  credit:current?.image_credit||recipe?.image_credit||(recipeImages[recipe?.source||'']?'Photo: Ministry of Curry':null)
 };
}
export function RecipePhoto({title,recipe,library}:{title:string;recipe?:Recipe|null;library:Recipe[]}) {
 const {url}=recipePhoto(recipe,library);
 const [failed,setFailed]=useState<string|null>(null);
 return <div className="food-icon">{url&&failed!==url?<img src={url} alt={title} loading="lazy" onError={()=>setFailed(url)}/>:<Leaf size={24} aria-label="Recipe photo unavailable"/>}</div>;
}
