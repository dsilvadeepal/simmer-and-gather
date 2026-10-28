"""Explicit reviewed-revision exports. Notion never authorizes Calendar writes.

Immutable pages preserve manual Notion edits. A pending create is reconciled by
its unique title; an ambiguous/missing result never triggers another create.
"""
from hashlib import sha256
from .adapters.notion import BeforeWriteError
from .db import Conflict, Missing, serialized
from .domain import RecipeSnapshot, PlanCandidate, PlanInputs
from .scheduler import content_hash
from .menu import validate_menu
from .scheduler import validate_schedule

class NotionPublisher:
    def __init__(self,store,notion): self.store,self.notion=store,notion

    def publish(self,owner,key,identity,version,title,lines,properties=None):
        stamp=sha256(f'{owner}:{key}:{identity}:{version}'.encode()).hexdigest()[:24]
        remote_title=f'{title[:160]} · SG {stamp}'
        try: operation,revision=self.store.get(owner,'notion_export',stamp)
        except Missing: operation,revision=None,None
        if operation and operation['status']=='saved':
            try: page=self.notion.page(operation['page_id'],key)
            except Exception: return {'status':'unavailable','message':'Cannot verify the saved Notion page. Check access and retry.'}
            if page.get('in_trash') or page.get('archived'):
                return {'status':'changed','message':'This Notion page was archived. Restore it in Notion; it will not be recreated automatically.'}
            return operation
        if operation and operation['status']!='retryable':
            try: pages=self.notion.find_projection(key,remote_title)
            except Exception: return {'status':'uncertain','message':'Check Notion connection and retry to reconcile this save.'}
            if len(pages)!=1:
                return {'status':'uncertain','message':'Save outcome is uncertain. No second page was created. Check the connection and Notion before retrying.'}
            page=pages[0]
        else:
            operation={'status':'pending','collection':key,'title':remote_title}
            revision=self.store.put(owner,'notion_export',stamp,operation,revision)
            try: page=self.notion.create_projection(key,remote_title,lines,properties)
            except BeforeWriteError:
                self.store.put(owner,'notion_export',stamp,{**operation,'status':'retryable'},revision)
                return {'status':'retryable','message':'Notion rejected the save before writing. Check the connection or recipe size, then retry.'}
            except Exception:
                return {'status':'uncertain','message':'Notion did not confirm the save. Retry to check its result; your local version is safe.'}
        result={'status':'saved','page_id':page['id'],'url':page.get('url',''),'collection':key,'title':remote_title}
        self.store.put(owner,'notion_export',stamp,result,revision)
        return result

    @serialized
    def recipe(self,owner,id,version):
        body,_=self.store.get(owner,'recipe',id)
        r=RecipeSnapshot.model_validate(body)
        if not r.reviewed or r.version!=version: raise Conflict('Review and save the current recipe version first')
        lines=[r.title,f'Source: {r.source}',f'App recipe revision: {r.version}',f'Servings: {r.servings or "Unknown"}',f'Category: {r.category}',f'Vegetarian: {r.vegetarian}',f'Allergens: {r.allergens}', 'Ingredients']
        lines.extend(f'{x.name}: {x.quantity if x.quantity is not None else "Unknown"} {x.unit or ""}' for x in r.ingredients)
        lines.append('Preparation and cooking')
        for t in r.tasks:
            lines.extend([f'{t.id}: {t.title}',f'Duration: {t.minutes} min; active: {t.active_minutes}; presence: {t.presence_minutes}; skill: {t.skill}; phase: {t.phase}',f'Equipment: {t.resource or "None"}; capacity: {t.capacity}; temperature: {t.temperature}; unattended: {t.unattended}',f'Dependencies: {", ".join(t.dependencies) or "None"}; make-ahead hours: {t.max_ahead_hours if t.max_ahead_hours is not None else "Not established"}',f'Evidence: {t.evidence or "Not supplied"}',f'Guidance: {t.guidance or "None"}'])
            lines.extend(f'{i.name}: {i.quantity} {i.unit or ""}' for i in t.ingredients)
        lines.extend(['Review notes',*r.uncertainties])
        return self.publish(owner,'recipes',r.id,r.version,r.title,lines,{'Base Servings':{'number':r.servings},'Source URL':{'url':r.source if r.source.startswith('https://') else None}})

    @serialized
    def plan(self,owner,id,revision,hash):
        body,_=self.store.get(owner,'plan',id)
        p=PlanCandidate.model_validate(body['plan']);inputs=PlanInputs.model_validate(body['inputs'])
        current,_=self.store.get(owner,'gathering',p.gathering_id)
        if p.revision!=revision or current['revision']!=revision or p.content_hash!=hash or content_hash(p)!=hash:
            raise Conflict('Plan changed; review the current version before saving to Notion')
        if p.status!='feasible' or validate_schedule(inputs,p) or validate_menu(inputs):
            raise Conflict('Resolve plan issues before saving the final plan to Notion')
        g=inputs.gathering
        lines=[g.title,f'Plan revision: {revision}',f'Guests: {g.guests}; vegetarian guests: {g.vegetarian_guests}',f'Arrival: {g.arrival}; timezone: {g.profile.timezone}', 'This is a reviewed plan snapshot. Saving it does not approve or book calendar events.','Menu']
        lines.extend(f'{s.title} — {s.mode}, serves {s.servings}; must-have: {s.must_have}' for s in inputs.selections)
        lines.append('Shopping')
        lines.extend(f'{x.name}: {x.quantity} {x.unit or ""}' for x in p.shopping)
        lines.extend(['Final checklist',*p.checklist])
        gathering=self.publish(owner,'gatherings',p.id,p.content_hash,g.title,lines)
        sessions=[]
        for index,a in enumerate(p.assignments):
            t=a.task
            sessions.append(self.publish(owner,'prep_sessions',p.id+':'+str(index),p.content_hash,t.title,[f'Gathering: {g.title}; revision: {revision}',f'{a.interval.start.isoformat()} – {a.interval.end.isoformat()}; timezone: {g.profile.timezone}',f'Helper: {a.person}',f'Task: {t.title}',f'Duration: {t.minutes} min; phase: {t.phase}; equipment: {t.resource or "None"}',* [f'{i.name}: {i.quantity} {i.unit or ""}' for i in t.ingredients],f'Guidance: {t.guidance or "None"}',f'Evidence: {t.evidence or "Not supplied"}']))
        return {'status':'saved' if gathering['status']=='saved' and all(x['status']=='saved' for x in sessions) else 'uncertain','gathering':gathering,'sessions':sessions}
