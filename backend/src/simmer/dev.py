"""Explicit loopback-only synthetic demo launcher. Not a production auth option."""
import os,secrets
from datetime import datetime, timezone, timedelta
from pathlib import Path
import jwt
from fastapi import Request, HTTPException
from .api import create_app
from .auth import Authenticator
from .db import Store, Missing
from .domain import *
from .profiles import HostingService
from .recipes import RecipeService
from .agent import PlanningService

OWNER='00000000-0000-4000-8000-000000000044'
KEY=secrets.token_urlsafe(48)
store=Store(os.getenv('DATABASE_URL','postgresql+psycopg://simmer:local-dev-only@localhost:55444/simmer'))
store.create_schema()
app=create_app(store,Authenticator(KEY,OWNER,'simmer-local','simmer-local'),fixture_mode=True)

@app.post('/api/dev-session')
def session(request:Request):
    if request.client.host not in ('127.0.0.1','::1'): raise HTTPException(403,'Local demo only')
    origin=request.headers.get('origin','')
    if origin and origin not in ('http://127.0.0.1:5173','http://localhost:5173','http://127.0.0.1:8000','http://127.0.0.1:5174'): raise HTTPException(403,'Local origin required')
    return {'token':jwt.encode({'sub':OWNER,'iss':'simmer-local','aud':'simmer-local','exp':datetime.now(timezone.utc)+timedelta(hours=4)},KEY,algorithm='HS256'),'fixture_mode':True}

def seed():
    g=Gathering(id='00000000-0000-4000-8000-000000000015',title='Diwali with friends & family',arrival='2026-11-07T18:00:00-05:00',earliest_prep='2026-11-05',prep_days=['2026-11-05','2026-11-06','2026-11-07'],vegetarian_guests=6,allergies=[],profile=HostProfile(equipment={'stovetop':2,'oven':1,'air fryer':1,'instant pot':1}),prep_windows=[Interval(start='2026-11-05T18:00:00-05:00',end='2026-11-05T19:00:00-05:00'),Interval(start='2026-11-06T18:00:00-05:00',end='2026-11-06T19:00:00-05:00'),Interval(start='2026-11-07T14:00:00-05:00',end='2026-11-07T17:00:00-05:00')])
    try: HostingService(store).get_gathering(OWNER,g.id); return
    except Missing: pass
    HostingService(store).save_gathering(OWNER,g,None)
    recipes=[]
    for id,title,category,veg,duration,ingredient,amount,unit in [('paneer','Palak paneer','mains',True,30,'Paneer',600,'g'),('chicken','Chicken curry','mains',False,40,'Chicken',1500,'g'),('rice','Jeera rice','sides',True,25,'Basmati rice',750,'g'),('raita','Cucumber raita','sides',True,10,'Yogurt',500,'g'),('lassi','Mango lassi','drinks',True,10,'Mango pulp',500,'g')]:
        item=Ingredient(name=ingredient,quantity=amount,unit=unit)
        r=RecipeSnapshot(id=id,title=title,source='fixture:illustrative-only',servings=15,category=category,vegetarian=veg,allergens=[],reviewed=True,ingredients=[item],tasks=[PrepTask(id='prepare',title='Prepare '+title.lower(),minutes=duration,skill='cook',max_ahead_hours=72,evidence='Synthetic demonstration only; not verified recipe guidance',ingredients=[item])])
        recipes.append(RecipeService(store).save_reviewed_recipe(OWNER,r,None))
    selections=[MenuSelection(id=r.id,title=r.title,category=r.category,recipe=r,servings=15,vegetarian=r.vegetarian) for r in recipes]
    selections += [MenuSelection(id='starter',title='Prepared samosas',category='starters',mode='buy',servings=15,vegetarian=True),MenuSelection(id='dessert',title='Gulab jamun',category='desserts',mode='buy',servings=15,vegetarian=True),MenuSelection(id='water',title='Sparkling water',category='drinks',mode='buy',servings=15,vegetarian=True)]
    PlanningService(store).apply_menu_changes(OWNER,g.id,[{'action':'add','selection':s.model_dump(mode='json')} for s in selections],1)
seed()
