from uuid import uuid5,NAMESPACE_URL
from .domain import *
from .db import Conflict,Missing,serialized
from .profiles import HostingService
from .scheduler import content_hash,validate_schedule,occupancy_windows,digest
from .menu import menu_blockers, MENU_ADVISORY_CODES, validate_menu

def event_proposals(owner,plan,inputs):
    windows=sorted([w for a in plan.assignments for w in occupancy_windows(a,inputs.gathering.profile.helpers)],key=lambda w:w.start)
    merged=[]
    for window in windows:
        if merged and window.start<=merged[-1].end:
            merged[-1]=Interval(start=merged[-1].start,end=max(merged[-1].end,window.end))
        else: merged.append(window.model_copy())
    return [{'id':uuid5(NAMESPACE_URL,owner+plan.id+str(i)).hex,'summary':'Prep · '+inputs.gathering.title,'start':{'dateTime':w.start.isoformat()},'end':{'dateTime':w.end.isoformat()},'transparency':'opaque','extendedProperties':{'private':{'app':'simmer-and-gather','plan':plan.id,'owner':digest(owner)}}} for i,w in enumerate(merged)]

class ApprovalService:
    def __init__(self,store): self.store=store
    def checked(self,owner,plan_id,revision,hash):
        body,_=self.store.get(owner,'plan',plan_id)
        p=PlanCandidate.model_validate(body['plan']); inputs=PlanInputs.model_validate(body['inputs'])
        current=HostingService(self.store).get_gathering(owner,p.gathering_id)
        if p.revision!=revision or current.revision!=revision or p.content_hash!=hash or content_hash(p)!=hash: raise Conflict('Plan changed; review and approve its current revision')
        from .recipe_readiness import changed_recipes
        from .recipes import RecipeService
        if changed_recipes(inputs,RecipeService(self.store).list_recipes(owner)): raise Conflict('Recipe collection changed; refresh selected recipes and regenerate before approval')
        if p.status!='feasible' or validate_schedule(inputs,p) or menu_blockers(validate_menu(inputs)): raise Conflict('Only a validated feasible plan can be approved')
        if inputs.availability.status!='fresh': raise Conflict('Live calendar verification required before approval')
        return p,inputs
    @serialized
    def approve_plan(self,owner,plan_id,revision,content_hash):
        p,inputs=self.checked(owner,plan_id,revision,content_hash)
        approval=Approval(id=str(uuid5(NAMESPACE_URL,owner+plan_id+content_hash)),plan_id=plan_id,revision=revision,content_hash=content_hash,events=event_proposals(owner,p,inputs))
        try:
            saved,_=self.store.get(owner,'approval',approval.id)
            return Approval.model_validate(saved)
        except Missing:
            self.store.put(owner,'approval',approval.id,approval.model_dump(mode='json'));return approval
