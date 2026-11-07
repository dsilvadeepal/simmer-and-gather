from datetime import datetime, timezone
from fastapi import Depends, HTTPException, UploadFile
from pydantic import BaseModel
from .domain import *
from .agent import PlanningService
from .recipes import RecipeService, extract_candidate
from .availability import AvailabilityService
from .adapters.storage import UploadStore
from .db import Missing

class MenuEdit(BaseModel):
    expected_revision: int
    changes: list[dict]
class Generate(BaseModel): expected_revision: int
class Preview(BaseModel): source: str
class SaveRecipe(BaseModel):
    recipe: RecipeSnapshot
    expected_source_version: str | None = None
class Workspace(BaseModel):
    inputs: PlanInputs
    recipes: list[RecipeSnapshot]
    plan: PlanCandidate | None = None
    previous_plan: PlanCandidate | None = None
    recipe_updates: list[str] = []
    recipe_readiness: dict[str, dict[str, bool]] = {}
    fixture_mode: bool

def install_routes(app,owner,store,availability=None,fixture_mode=False,model=None,telemetry=None):
    planning=PlanningService(store,model,telemetry); recipes=RecipeService(store)
    def unavailable(*args): raise ValueError('Calendar disconnected')
    calendar=availability or AvailabilityService(unavailable)
    def snapshot(o,g,force=False):
        if fixture_mode: return AvailabilitySnapshot(status='fixture',checked_at=datetime.now(timezone.utc))
        return calendar.read_availability(o,g,force=force)
    @app.exception_handler(ValueError)
    async def invalid_handler(request,exc):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=422,content={'detail':str(exc)})
    @app.get('/api/workspace/{id}',response_model=Workspace)
    def workspace(id:str,o=Depends(owner)):
        inputs=planning.load(o,id)
        # Calendar on open, no background checks. Saved plans retain exact original snapshot.
        inputs.availability=snapshot(o,inputs.gathering)
        records=[x for x in store.list(o,'plan') if x['plan']['gathering_id']==id]
        records.sort(key=lambda x: x['plan'].get('generated_at') or x.get('inputs',{}).get('availability',{}).get('checked_at') or '')
        all_plans=[PlanCandidate.model_validate(x['plan']) for x in records]
        plans=[p for p in all_plans if p.revision==inputs.gathering.revision]
        plan=plans[-1] if plans else None
        previous=next((p for p in reversed(all_plans) if (not plan or p.id!=plan.id) and p.assignments),None)
        if plan and plan.status=='feasible':
            from .scheduler import validate_schedule
            current_issues=validate_schedule(inputs,plan)
            if current_issues:
                plan=plan.model_copy(deep=True)
                plan.status='conflict'
                plan.outcome=SchedulingOutcome(code='validation_failed',message='This saved schedule no longer passes the current checks. Generate a new proposal before using it.')
                plan.violations=current_issues
        library=recipes.list_recipes(o)
        from .recipe_readiness import changed_recipes,readiness
        updates=changed_recipes(inputs,library)
        return Workspace(inputs=inputs,recipes=library,plan=plan,previous_plan=previous,recipe_updates=updates,recipe_readiness={r.id:readiness(r) for r in library},fixture_mode=fixture_mode)
    @app.get('/api/recipes',response_model=list[RecipeSnapshot])
    def recipe_list(o=Depends(owner)): return recipes.list_recipes(o)
    @app.post('/api/recipes/preview',response_model=RecipeSnapshot)
    def preview(body:Preview,o=Depends(owner)):
        candidate=recipes.preview_recipe(o,body.source)
        if model:
            try:
                from .hosting_recipe import HostingRecipeTool
                candidate=HostingRecipeTool(store,model,telemetry).prepare_recipe_for_hosting(o,candidate)
            except Exception:
                # Provider or parsing failures preserve usable source preview/manual review.
                candidate.uncertainties.append('Automatic step extraction unavailable; review the original source manually')
        return candidate
    @app.post('/api/recipes',response_model=RecipeSnapshot)
    def recipe_save(body:SaveRecipe,o=Depends(owner)): return recipes.save_reviewed_recipe(o,body.recipe,body.expected_source_version)
    @app.post('/api/menu/{id}',response_model=PlanInputs)
    def edit(id:str,body:MenuEdit,o=Depends(owner)): return planning.apply_menu_changes(o,id,body.changes,body.expected_revision)
    @app.post('/api/menu/{id}/propose',response_model=list[MenuSelection])
    def propose(id:str,o=Depends(owner)): return planning.propose(o,id)
    @app.post('/api/availability/{id}',response_model=AvailabilitySnapshot)
    def recheck(id:str,o=Depends(owner)): return snapshot(o,planning.load(o,id).gathering,True)
    @app.post('/api/plans/{id}/generate',response_model=PlanCandidate)
    def generate(id:str,body:Generate,o=Depends(owner)):
        g=planning.load(o,id).gathering
        return planning.generate_final_plan(o,id,body.expected_revision,snapshot(o,g,True))
    @app.post('/api/inventory/{id}/upload')
    async def upload(id:str,file:UploadFile,o=Depends(owner)):
        planning.load(o,id)
        if not fixture_mode and not getattr(app.state,'retention_verified',False): raise HTTPException(503,'Upload retention must be configured before uploads are enabled')
        data=await file.read(10*1024*1024+1)
        return {'upload_id':UploadStore(store).upload(o,data,file.content_type,datetime.now(timezone.utc))}
    @app.delete('/api/inventory/uploads/{id}')
    def delete_upload(id:str,o=Depends(owner)):
        UploadStore(store).delete(o,id); return {'deleted':True}
