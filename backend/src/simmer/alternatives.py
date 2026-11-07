"""Bounded recipe-library search. Previews never write plans or calendar events."""
from itertools import product
from .domain import MenuSelection
from .menu import validate_menu,menu_blockers
from .scheduler import schedule,validate_schedule
from .agent import apply_menu_validation
from .db import Conflict

def trial_for(inputs,recipes,swaps):
    trial=inputs.model_copy(deep=True);library={r.id:r for r in recipes}
    if not swaps or len({s['selection_id'] for s in swaps})!=len(swaps):raise ValueError('Choose distinct dishes to swap')
    for swap in swaps:
        item=next((s for s in trial.selections if s.id==swap['selection_id']),None)
        r=library.get(swap['recipe_id'])
        if not item or item.must_have or item.mode!='cook':raise ValueError('Keep must-have and contributed dishes unchanged')
        if not r or not r.reviewed or r.version!=swap['version']:raise Conflict('Recipe changed; find alternatives again')
        servings=swap['servings']
        if not 0<servings<=max(inputs.gathering.guests,item.servings):raise ValueError('Invalid portions')
        item.title=r.title;item.recipe=r.model_copy(deep=True);item.vegetarian=r.vegetarian;item.category=r.category;item.servings=servings
    return trial

def checked(inputs):
    if menu_blockers(validate_menu(inputs)):return None
    plan=apply_menu_validation(inputs,schedule(inputs))
    return plan if plan.status=='feasible' and not validate_schedule(inputs,plan) else None

def suggest_alternatives(inputs,recipes,max_attempts=12):
    issues=menu_blockers(validate_menu(inputs))
    targets={id for v in issues if v.code in ('allergy','allergy_unknown') for id in v.affected_ids}
    veg=any(v.code=='vegetarian' for v in issues)
    groups=[]
    veg_covered=sum(s.servings for s in inputs.selections if s.category=='mains' and (s.vegetarian is True or s.recipe and s.recipe.vegetarian is True))
    missing_veg=max(0,inputs.gathering.vegetarian_guests-veg_covered)
    for item in inputs.selections:
        if item.must_have or item.mode!='cook':continue
        if item.id not in targets and not (veg and (item.vegetarian is False or item.recipe and item.recipe.vegetarian is False)):continue
        options=[]
        for r in sorted(recipes,key=lambda r:(not (item.recipe and r.id==item.recipe.id),r.title)):
            if not r.reviewed or not r.ingredients or not r.tasks:continue
            if any(s.recipe and s.recipe.id==r.id for s in inputs.selections if s.id!=item.id):continue
            if veg and item.id not in targets and not (r.category=='mains' and r.vegetarian is True):continue
            if r.category!=item.category and not (veg and r.category=='mains' and r.vegetarian):continue
            if (inputs.gathering.vegetarian_guests==inputs.gathering.guests or veg) and r.vegetarian is not True and r.category=='mains':continue
            portions=missing_veg if veg and item.id not in targets else max(item.servings,inputs.gathering.vegetarian_guests) if r.vegetarian and r.category=='mains' else item.servings
            swap={'selection_id':item.id,'recipe_id':r.id,'version':r.version,'servings':portions}
            t=trial_for(inputs,recipes,[swap])
            if any(v.code.startswith('allergy') and item.id in v.affected_ids for v in menu_blockers(validate_menu(t))):continue
            options.append(swap)
        if item.id in targets:groups.append(options[:5])
        elif veg and options:groups.append([None]+options[:5])
    results=[];attempts=0
    if groups and all(groups):
        combinations=product(*groups)
        # Prefer fewer changed dishes; metadata refresh of the same recipe is free.
        from itertools import islice
        combinations=sorted(islice(combinations,256),key=lambda combo:sum(bool(s) and not any(x.id==s['selection_id'] and x.recipe and x.recipe.id==s['recipe_id'] for x in inputs.selections) for s in combo))
        for combo in combinations:
            swaps=[s for s in combo if s]
            if not swaps:continue
            trial=trial_for(inputs,recipes,swaps)
            if menu_blockers(validate_menu(trial)):continue
            attempts+=1;plan=checked(trial)
            if plan:
                results.append({'swaps':swaps,'changes':[{'from':next(x.title for x in inputs.selections if x.id==s['selection_id']),'to':next(x.title for x in trial.selections if x.id==s['selection_id']),'servings':s['servings']} for s in swaps],'inputs':trial,'plan':plan})
            if len(results)>=3 or attempts>=max_attempts:break
    return {'suggestions':results,'checked_candidates':attempts,'message':'Review a checked alternative below.' if results else 'No checked alternative found in this limited search. Review must-have dishes, recipe screening or menu choices; this does not mean you need more time.'}
