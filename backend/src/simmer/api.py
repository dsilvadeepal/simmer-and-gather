import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .auth import Authenticator
from .db import Store, Conflict, Missing
from .domain import Gathering
from .profiles import HostingService

class SaveGathering(BaseModel):
    gathering: Gathering
    expected_revision: int | None = None

def create_app(store=None, auth=None):
    app=FastAPI(title='Simmer and Gather')
    store=store or Store(os.environ['DATABASE_URL'])
    service=HostingService(store)
    auth=auth or Authenticator(os.environ['AUTH_VERIFY_KEY'],os.environ['ALLOWED_OWNER_ID'],os.environ['AUTH_ISSUER'],os.environ['AUTH_AUDIENCE'],os.getenv('AUTH_ALGORITHMS','RS256').split(','))
    bearer=HTTPBearer(auto_error=False)
    def owner(credentials: HTTPAuthorizationCredentials | None=Depends(bearer)):
        if not credentials: raise HTTPException(401,'Login required')
        try: return auth.require_owner(credentials.credentials)
        except ValueError: raise HTTPException(401,'Login required')
    @app.exception_handler(Conflict)
    async def conflict_handler(request,exc): return JSONResponse(status_code=409,content={'detail':str(exc)})
    @app.exception_handler(Missing)
    async def missing_handler(request,exc): return JSONResponse(status_code=404,content={'detail':'Record not found'})
    @app.get('/health')
    def health(): return {'status':'ok'}
    @app.get('/api/profile')
    def profile(o=Depends(owner)): return service.get_profile(o)
    @app.get('/api/gatherings')
    def gatherings(o=Depends(owner)): return store.list(o,'gathering')
    @app.post('/api/gatherings')
    def save(body:SaveGathering,o=Depends(owner)): return service.save_gathering(o,body.gathering,body.expected_revision)
    @app.get('/api/gatherings/{id}')
    def get(id:str,o=Depends(owner)): return service.get_gathering(o,id)
    app.state.store=store; app.state.service=service; app.state.owner=owner
    return app
