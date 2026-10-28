"""Production entrypoint; fails closed if required configuration is absent."""
import os
from fastapi import Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from .api import create_app
from .auth import Authenticator
from .db import Store
from .oauth import install_oauth,GoogleCredentials
from .adapters.google import GoogleCalendar
from .availability import AvailabilityService
from .approval import ApprovalService
from .booking import BookingService
from .domain import Approval,BookingResult

class SearchRequest(BaseModel):
    query:str

class RecipePublishRequest(BaseModel):
    version:str

class ApproveRequest(BaseModel):
    revision:int
    content_hash:str

def build_app(config=None):
    config=dict(os.environ) if config is None else config
    required=['DATABASE_URL','SESSION_SECRET','ALLOWED_OWNER_ID','ALLOWED_EMAIL','CREDENTIAL_ENCRYPTION_KEY','GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET','GOOGLE_REDIRECT_URI','APP_URL']
    if any(not config.get(k) for k in required): raise RuntimeError('Complete private app configuration before starting production')
    if len(config['SESSION_SECRET'])<32: raise RuntimeError('Session secret must be at least 32 characters')
    store=Store(config['DATABASE_URL'])
    google=GoogleCalendar(GoogleCredentials(store,config['ALLOWED_OWNER_ID'],config).access_token)
    availability=AvailabilityService(google.events)
    auth=Authenticator(config['SESSION_SECRET'],config['ALLOWED_OWNER_ID'],'simmer','simmer')
    from .runtime import build_text_model
    app=create_app(store,auth,availability=availability,model=build_text_model(store,config['ALLOWED_OWNER_ID'],config))
    install_oauth(app,store,config)
    owner=app.state.owner
    if config.get('NOTION_TOKEN') and config.get('NOTION_COLLECTIONS'):
        import json
        from .adapters.notion_client import NotionRecipes
        notion=NotionRecipes(config['NOTION_TOKEN'],json.loads(config['NOTION_COLLECTIONS']))
        from .adapters.notion import ScopedNotion,NotionAPITransport
        from .notion_publish import NotionPublisher
        publisher=NotionPublisher(store,ScopedNotion(NotionAPITransport(config['NOTION_TOKEN']),json.loads(config['NOTION_COLLECTIONS'])))
        @app.post('/api/notion/recipes/{id}')
        def publish_recipe(id:str,body:RecipePublishRequest,o=Depends(owner)):
            return publisher.recipe(o,id,body.version)
        @app.post('/api/notion/plans/{id}')
        def publish_plan(id:str,body:ApproveRequest,o=Depends(owner)):
            return publisher.plan(o,id,body.revision,body.content_hash)
        @app.get('/api/notion/recipes')
        def notion_recipes(o=Depends(owner)):
            try: return notion.list_candidates()
            except Exception: raise HTTPException(503,'Notion unavailable; saved local recipes remain available')
    @app.post('/api/recipes/discover')
    def discover(body:SearchRequest,o=Depends(owner)):
        if config.get('ENABLE_RECIPE_SEARCH')!='true' or not config.get('TAVILY_API_KEY'):
            raise HTTPException(503,'Online search is not configured. Paste a recipe link instead.')
        from .discovery import RecipeDiscovery
        from .adapters.search import TavilySearch
        search=TavilySearch(config['TAVILY_API_KEY'],lambda:True)
        try: return RecipeDiscovery(store,search.discover_recipes).search(o,body.query)
        except ValueError: raise
        except Exception: raise HTTPException(503,'Search unavailable. Paste a recipe link or try again later.')
    @app.get('/api/calendars')
    def calendars(o=Depends(owner)):
        return [{'id':c['id'],'name':c.get('summary','Calendar')} for c in google.list_calendars()]
    @app.post('/api/plans/{id}/approve',response_model=Approval)
    def approve(id:str,body:ApproveRequest,o=Depends(owner)):
        return ApprovalService(store).approve_plan(o,id,body.revision,body.content_hash)
    @app.post('/api/approvals/{id}/apply',response_model=BookingResult)
    def apply(id:str,o=Depends(owner)):
        return BookingService(store,google,availability.read_availability).apply_booking(o,id)
    dist=Path(__file__).resolve().parents[3]/'frontend'/'dist'
    if dist.exists(): app.mount('/',StaticFiles(directory=dist,html=True),name='frontend')
    return app
