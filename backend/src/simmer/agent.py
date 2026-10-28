"""One bounded planning workflow; all external writes stay outside the graph."""
from typing import TypedDict
from uuid import uuid5, NAMESPACE_URL
from sqlalchemy import select
from sqlalchemy.orm import Session
from langgraph.graph import StateGraph, START, END
from .domain import *
from .models import Document
from .profiles import HostingService
from .recipes import RecipeService
from .db import Missing, Conflict
from .scheduler import schedule, digest, content_hash
from .menu import propose_menu, validate_menu, rank_recipes

class State(TypedDict,total=False):
    inputs: PlanInputs
    recipes: list[RecipeSnapshot]
    proposal: list[MenuSelection]
    plan: PlanCandidate

class PlanningService:
    def __init__(self,store,model=None): self.store=store; self.host=HostingService(store); self.model=model
    def load(self,owner,id): return self.host.load_plan_inputs(owner,id)
    def apply_menu_changes(self,owner,gathering_id,changes,expected_revision):
        with Session(self.store.engine) as session, session.begin():
            row=session.scalar(select(Document).where(Document.owner==owner,Document.kind=='gathering',Document.id==gathering_id).with_for_update())
            if row is None: raise Missing('Gathering not found')
            if row.revision!=expected_revision: raise Conflict('Gathering changed; reload')
            saved=session.get(Document,(owner,'inputs',gathering_id))
            inputs=PlanInputs.model_validate(saved.body) if saved else PlanInputs(gathering=Gathering.model_validate(row.body))
            inputs.gathering=Gathering.model_validate(row.body)
            for change in changes:
                action=change.get('action')
                if action=='add': inputs.selections.append(MenuSelection.model_validate(change['selection']))
                elif action in ('update','remove'):
                    item=next((x for x in inputs.selections if x.id==change.get('id')),None)
                    if item is None: raise Missing('Menu item not found')
                    if action=='remove':
                        if item.must_have: raise ValueError('Unmark must-have explicitly before removing')
                        inputs.selections.remove(item)
                    else:
                        updated=MenuSelection.model_validate(item.model_dump()|change['values'])
                        inputs.selections=[updated if x.id==item.id else x for x in inputs.selections]
                elif action=='inventory':
                    from .inventory import confirm_items
                    inputs.inventory=confirm_items([InventoryItem.model_validate(x) for x in change['items']])
                else: raise ValueError('Unsupported edit')
            if len({x.id for x in inputs.selections})!=len(inputs.selections): raise ValueError('Duplicate menu item')
            inputs.gathering.revision+=1; row.revision+=1; row.body=inputs.gathering.model_dump(mode='json')
            if saved: saved.body=inputs.model_dump(mode='json'); saved.revision+=1
            else: session.add(Document(owner=owner,kind='inputs',id=gathering_id,revision=1,body=inputs.model_dump(mode='json')))
            return inputs
    def propose(self,owner,id):
        graph=StateGraph(State)
        graph.add_node('retrieve',lambda state:{'recipes':RecipeService(self.store).list_recipes(owner)})
        graph.add_node('propose',lambda state:{'proposal':propose_menu(state['inputs'],rank_recipes(state['inputs'].gathering,state['recipes'],self.model))})
        graph.add_edge(START,'retrieve'); graph.add_edge('retrieve','propose'); graph.add_edge('propose',END)
        return graph.compile().invoke({'inputs':self.load(owner,id)},{'recursion_limit':8})['proposal']
    def generate_final_plan(self,owner,gathering_id,expected_revision,availability=None):
        inputs=self.load(owner,gathering_id)
        if inputs.gathering.revision!=expected_revision: raise Conflict('Gathering changed; reload')
        if availability: inputs.availability=availability
        graph=StateGraph(State)
        graph.add_node('schedule',lambda state:{'plan':schedule(state['inputs'])})
        def validate(state):
            plan=state['plan']; issues=validate_menu(state['inputs'])
            plan.violations.extend(issues)
            if issues: plan.status='incomplete'
            plan.content_hash=content_hash(plan)
            return {'plan':plan}
        graph.add_node('validate',validate); graph.add_edge(START,'schedule'); graph.add_edge('schedule','validate'); graph.add_edge('validate',END)
        plan=graph.compile().invoke({'inputs':inputs},{'recursion_limit':8})['plan']
        plan.id=str(uuid5(NAMESPACE_URL,owner+gathering_id+plan.content_hash))
        # Guard against a concurrent edit while generation was running.
        with Session(self.store.engine) as s, s.begin():
            row=s.scalar(select(Document).where(Document.owner==owner,Document.kind=='gathering',Document.id==gathering_id).with_for_update())
            if not row or row.revision!=expected_revision: raise Conflict('Inputs changed during planning')
            existing=s.get(Document,(owner,'plan',plan.id))
            if not existing: s.add(Document(owner=owner,kind='plan',id=plan.id,body={'plan':plan.model_dump(mode='json'),'inputs':inputs.model_dump(mode='json')},revision=1))
        return plan
