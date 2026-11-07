"""Publish labeled chef proposals to the scoped Notion Recipe Library."""
import json
from pathlib import Path
from simmer.adapters.notion import ScopedNotion,NotionAPITransport
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'docs/recipe-collection.json').read_text())
c=dict(x.split('=',1) for x in (ROOT/'.env.notion').read_text().splitlines() if '=' in x)
a=ScopedNotion(NotionAPITransport(c['NOTION_TOKEN']),json.loads(c['NOTION_COLLECTIONS']))
pages={p['properties'].get('Source URL',{}).get('url'):p for p in a.query('recipes')}
assert len(pages)==len(rows)==40 and set(pages)=={r['url'] for r in rows}
def rich(s):return {'rich_text':[{'type':'text','text':{'content':s[:1900]}}]}
for r in rows:
 p=pages[r['url']]
 props={
  'Base Servings':{'number':r['estimated_base_servings']},
  'Equipment':{'multi_select':[{'name':x} for x in r['equipment_assumption']]},
  'Planning Ready':{'checkbox':False},
 }
 if r['chef_make_ahead_proposal']:
  props['Make Ahead Notes']=rich('CHEF PROPOSAL — untested; not a publisher storage instruction. '+r['chef_make_ahead_proposal'])
 props['Missing Information']=rich('Serving basis: '+r['base_servings_basis']+'. '+r['equipment_review']+' Check actual package labels/cross-contact, food storage and reheat method. Task minutes are untested estimates. Confirm selected-menu quantities before scheduling.')
 a.transport('PATCH','/pages/'+p['id'],{'properties':props})
 print('UPDATED',r['title'],flush=True)
