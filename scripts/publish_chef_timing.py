"""Publish reviewed timing estimates to the scoped Simmer and Gather Notion recipe pages."""
import json
from pathlib import Path
from simmer.adapters.notion import ScopedNotion,NotionAPITransport
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'docs/recipe-chef-timing.json').read_text())
c=dict(x.split('=',1) for x in (ROOT/'.env.notion').read_text().splitlines() if '=' in x)
a=ScopedNotion(NotionAPITransport(c['NOTION_TOKEN']),json.loads(c['NOTION_COLLECTIONS']))
pages={p['properties'].get('Source URL',{}).get('url'):p for p in a.query('recipes')}
assert len(pages)==len(rows)==40

def rich(s): return [{'type':'text','text':{'content':s[:1900]}}]

def plain(block):
    q=block.get(block.get('type',''),{})
    return ''.join(z.get('plain_text',z.get('text',{}).get('content','')) for z in q.get('rich_text',[]))

for row in rows:
    p=pages[row['url']]
    if row['active_minutes'] is None:
        print('SOURCE NEEDED',row['title'],flush=True)
        continue
    properties={
        'Active Minutes':{'number':row['active_minutes']},
        'Unattended Minutes':{'number':row['unattended_minutes']},
        'Total Elapsed Minutes':{'number':row['elapsed_minutes']},
        'Timing Basis':{'select':{'name':'Estimated - review needed'}},
        'Planning Ready':{'checkbox':False},
    }
    a.transport('PATCH','/pages/'+p['id'],{'properties':properties})
    existing=a.transport('GET','/blocks/'+p['id']+'/children?page_size=100')
    if not any('Home-cook timing draft (untested)' in plain(b) for b in existing.get('results',[])):
        children=[{'object':'block','type':'heading_3','heading_3':{'rich_text':rich('Home-cook timing draft (untested)')}}]
        for phase in row['phases']:
            detail=f"{phase['task']}: {phase['active_minutes']} min hands-on"
            if phase['unattended_minutes']:detail+=f" + {phase['unattended_minutes']} min waiting/cooking"
            children.append({'object':'block','type':'bulleted_list_item','bulleted_list_item':{'rich_text':rich(detail)}})
        children.append({'object':'block','type':'paragraph','paragraph':{'rich_text':rich(f"Cleanup: {row['cleanup_minutes']} min. Active total including cleanup: {row['active_minutes']} min; unattended: {row['unattended_minutes']} min. {row['review']}")}})
        a.transport('PATCH','/blocks/'+p['id']+'/children',{'children':children})
    print('UPDATED',row['title'],flush=True)
