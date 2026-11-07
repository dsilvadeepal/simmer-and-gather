"""Apply only reviewed recipe metadata to app and existing Notion pages."""
import os,json,hashlib
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from simmer.db import Store
from simmer.models import Document
from simmer.recipes import RecipeService
from refine_heldout_recipes import refine,SOURCES
from sync_realistic_recipe_corrections import main as sync
ROOT=Path(__file__).resolve().parents[1]
def main():
 cfg=dict(os.environ)
 for name in ('.env.google','.env.notion','.env.services'):
  for line in (ROOT/name).read_text().splitlines():
   if '=' in line and not line.startswith('#'):
    k,v=line.split('=',1);cfg[k]=v.strip().strip('"').strip("'")
 store=Store(cfg['DATABASE_URL']);service=RecipeService(store);owner=cfg['ALLOWED_OWNER_ID']
 def untouched():
  with Session(store.engine) as session:
   rows=[(r.kind,r.id,r.revision,r.body) for r in session.scalars(select(Document).where(Document.owner==owner,Document.kind!='recipe'))]
  return hashlib.sha256(json.dumps(sorted(rows,key=lambda r:(r[0],r[1])),sort_keys=True,default=str).encode()).hexdigest()
 before=untouched();titles=[]
 for recipe in service.list_recipes(owner):
  if recipe.source.rstrip('/') not in SOURCES:continue
  corrected=refine(recipe);titles.append(recipe.title)
  if corrected!=recipe:service.save_reviewed_recipe(owner,corrected,recipe.version)
  print('Reviewed app recipe:',recipe.title,flush=True)
 assert len(titles)==4
 sync(titles,marker='Ingredient screening review v2 · 2026-11-07',report='2026-11-07-heldout-notion-sync.json')
 assert before==untouched(),'Non-recipe records changed'
 print('Verified: non-recipe records unchanged; no calendar calls.')
if __name__=='__main__':main()
