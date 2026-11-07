"""Update existing scoped Notion recipes; never create recipes or touch plans."""
import json,os
from pathlib import Path
from simmer.db import Store
from simmer.domain import RecipeSnapshot
from simmer.adapters.notion import ScopedNotion,NotionAPITransport
from simmer.adapters.notion_recipe_details import block_text,from_notion_details
ROOT=Path(__file__).resolve().parents[1]
def rich(text):return [{'type':'text','text':{'content':text[i:i+1800]}} for i in range(0,len(text),1800)]
def block(kind,text):return {'object':'block','type':kind,kind:{'rich_text':rich(text)}}
def main():
 cfg=dict(os.environ)
 for name in ('.env.google','.env.notion','.env.services'):
  for line in (ROOT/name).read_text().splitlines():
   if '=' in line and not line.startswith('#'):
    k,v=line.split('=',1);cfg[k]=v.strip().strip('"').strip("'")
 store=Store(cfg['DATABASE_URL']);a=ScopedNotion(NotionAPITransport(cfg['NOTION_TOKEN']),json.loads(cfg['NOTION_COLLECTIONS']))
 titles=json.loads((ROOT/'docs/reviews/2026-11-07-realistic-library-updates.json').read_text())['updated_recipes']
 pages=a.query('recipes');results=[]
 for raw in store.list(cfg['ALLOWED_OWNER_ID'],'recipe'):
  r=RecipeSnapshot.model_validate(raw)
  if r.title not in titles:continue
  matches=[p for p in pages if (p['properties'].get('Source URL',{}).get('url') or '').rstrip('/')==r.source.rstrip('/')]
  if len(matches)!=1:raise ValueError('Expected one existing source page for '+r.title)
  p=matches[0];pageid=p['id']
  existing=a.transport('GET','/blocks/'+pageid+'/children?page_size=100')
  if existing.get('has_more'):raise ValueError('Paginated page requires explicit handling')
  marker='Current hosting preparation · 2026-11-07'
  if not any(block_text(b)==marker for b in existing['results']):
   children=[block('heading_3',marker)]
   for t in r.tasks:
    text=f'{t.title} — {t.minutes} min elapsed; {t.presence_minutes if t.presence_minutes is not None else t.minutes} min attention.'
    if t.dependencies:text+=' After: '+', '.join(t.dependencies)+'.'
    if t.guidance:text+=' '+t.guidance
    children.append(block('bulleted_list_item',text))
   children.append(block('paragraph','Current app planning data follows. Times and attention placement are estimates; use recipe doneness cues. Earlier timing sections below or above are superseded.'))
   payload=r.model_dump(mode='json');payload['source_text']=''
   children.append({'object':'block','type':'code','code':{'language':'json','caption':rich('Simmer and Gather recipe data v1'),'rich_text':rich(json.dumps(payload))}})
   a.transport('PATCH','/blocks/'+pageid+'/children',{'children':children})
  props={'Active Minutes':{'number':sum(t.active_minutes or 0 for t in r.tasks)},'Unattended Minutes':{'number':sum(max(0,(t.minutes or 0)-(t.presence_minutes if t.presence_minutes is not None else t.minutes or 0)) for t in r.tasks)},'Total Elapsed Minutes':{'number':sum(t.minutes or 0 for t in r.tasks)},'Last Reviewed':{'date':{'start':'2026-11-07'}}}
  if r.vegetarian:
   old=''.join(x.get('plain_text',x.get('text',{}).get('content','')) for x in p['properties'].get('Dietary Notes',{}).get('rich_text',[]))
   props['Dietary Notes']={'rich_text':rich('Vegetarian: yes (reviewed ingredients; dairy may be present). '+old) if not old.startswith('Vegetarian: yes') else rich(old)}
  if r.preparation_provenance.get('realistic_review'):props['Make Ahead Notes']={'rich_text':rich(r.preparation_provenance['realistic_review'])}
  a.transport('PATCH','/pages/'+pageid,{'properties':props})
  blocks=a.transport('GET','/blocks/'+pageid+'/children?page_size=100')['results']
  page=a.transport('GET','/pages/'+pageid)
  back=from_notion_details(page,blocks)
  assert back.tasks==r.tasks and back.ingredients==r.ingredients and back.vegetarian==r.vegetarian
  results.append({'title':r.title,'url':page.get('url'),'verified':True});print('Verified',r.title,flush=True)
 (ROOT/'docs/reviews/2026-11-07-notion-recipe-sync.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
