"""Google web OAuth with PKCE, browser binding, single-use state, owner allowlist."""
import base64,hashlib,json,os,secrets
from datetime import datetime,timedelta,timezone
from urllib.parse import urlencode
import httpx,jwt
from fastapi import Request,HTTPException
from fastapi.responses import RedirectResponse
from .db import Conflict,Missing,serialized
from .auth import encrypt_secret,decrypt_secret
from .scheduler import digest

SCOPES=['openid','email','https://www.googleapis.com/auth/calendar.calendarlist.readonly','https://www.googleapis.com/auth/calendar.events.readonly','https://www.googleapis.com/auth/calendar.app.created']

class OAuthState:
    def __init__(self,store): self.store=store
    def begin(self):
        state,binder,verifier=[secrets.token_urlsafe(40) for _ in range(3)]
        self.store.put('oauth','state',digest(state),{'binder':digest(binder),'verifier':verifier,'expires':(datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat(),'used':False})
        return state,binder,verifier
    def consume(self,state,binder):
        try: row,rev=self.store.get('oauth','state',digest(state))
        except Missing: raise Conflict('OAuth state missing; start again')
        if row['used'] or datetime.fromisoformat(row['expires'])<=datetime.now(timezone.utc) or not secrets.compare_digest(row['binder'],digest(binder)):
            raise Conflict('OAuth session expired or browser mismatch')
        self.store.put('oauth','state',digest(state),{**row,'used':True,'verifier':''},rev)
        return row['verifier']

class GoogleCredentials:
    def __init__(self,store,owner,config): self.store,self.owner,self.config=store,owner,config
    def access_token(self):
        raw,rev=self.store.get(self.owner,'credential','google')
        credentials=json.loads(decrypt_secret(raw['encrypted'],self.config['CREDENTIAL_ENCRYPTION_KEY']))
        if datetime.fromisoformat(credentials['expires'])>datetime.now(timezone.utc)+timedelta(seconds=60): return credentials['access_token']
        with httpx.Client(timeout=20) as client:
            r=client.post('https://oauth2.googleapis.com/token',data={'client_id':self.config['GOOGLE_CLIENT_ID'],'client_secret':self.config['GOOGLE_CLIENT_SECRET'],'refresh_token':credentials['refresh_token'],'grant_type':'refresh_token'})
            r.raise_for_status(); updated=r.json()
        credentials.update(updated,expires=(datetime.now(timezone.utc)+timedelta(seconds=updated['expires_in'])).isoformat())
        try:
            self.store.put(self.owner,'credential','google',{'encrypted':encrypt_secret(json.dumps(credentials),self.config['CREDENTIAL_ENCRYPTION_KEY'])},rev)
        except Conflict:
            # Another refresh or reconnect won. Never overwrite its newer credentials.
            saved,_=self.store.get(self.owner,'credential','google')
            winner=json.loads(decrypt_secret(saved['encrypted'],self.config['CREDENTIAL_ENCRYPTION_KEY']))
            if datetime.fromisoformat(winner['expires'])<=datetime.now(timezone.utc)+timedelta(seconds=60):
                raise Conflict('Google credentials changed; retry the connection')
            return winner['access_token']
        return credentials['access_token']

def install_oauth(app,store,config):
    states=OAuthState(store)
    @app.get('/api/google/start')
    def start():
        state,binder,verifier=states.begin()
        challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
        params={'client_id':config['GOOGLE_CLIENT_ID'],'redirect_uri':config['GOOGLE_REDIRECT_URI'],'response_type':'code','scope':' '.join(SCOPES),'access_type':'offline','prompt':'consent','state':state,'code_challenge':challenge,'code_challenge_method':'S256'}
        response=RedirectResponse('https://accounts.google.com/o/oauth2/v2/auth?'+urlencode(params))
        response.set_cookie('simmer_oauth',binder,max_age=600,httponly=True,secure=config['GOOGLE_REDIRECT_URI'].startswith('https:'),samesite='lax',path='/api/google')
        return response
    @app.get('/api/google/callback')
    def callback(request:Request,code:str,state:str):
        verifier=states.consume(state,request.cookies.get('simmer_oauth',''))
        with httpx.Client(timeout=20) as client:
            r=client.post('https://oauth2.googleapis.com/token',data={'client_id':config['GOOGLE_CLIENT_ID'],'client_secret':config['GOOGLE_CLIENT_SECRET'],'redirect_uri':config['GOOGLE_REDIRECT_URI'],'code':code,'code_verifier':verifier,'grant_type':'authorization_code'})
            if not r.is_success: raise HTTPException(400,'Google sign-in failed; start again')
            tokens=r.json()
        key=jwt.PyJWKClient('https://www.googleapis.com/oauth2/v3/certs').get_signing_key_from_jwt(tokens['id_token'])
        claims=jwt.decode(tokens['id_token'],key.key,algorithms=['RS256'],audience=config['GOOGLE_CLIENT_ID'],issuer=['https://accounts.google.com','accounts.google.com'],options={'require':['exp','sub','email']})
        if not claims.get('email_verified') or claims['email'].casefold()!=config['ALLOWED_EMAIL'].casefold(): raise HTTPException(403,'This demo is private to its owner')
        owner=config['ALLOWED_OWNER_ID']; tokens['expires']=(datetime.now(timezone.utc)+timedelta(seconds=tokens['expires_in'])).isoformat()
        tokens.pop('id_token',None)
        try:
            old,rev=store.get(owner,'credential','google')
            if not tokens.get('refresh_token'): tokens['refresh_token']=json.loads(decrypt_secret(old['encrypted'],config['CREDENTIAL_ENCRYPTION_KEY']))['refresh_token']
        except Missing: rev=None
        if not tokens.get('refresh_token'): raise HTTPException(400,'Offline access missing; reconnect Google')
        store.put(owner,'credential','google',{'encrypted':encrypt_secret(json.dumps(tokens),config['CREDENTIAL_ENCRYPTION_KEY'])},rev)
        token=jwt.encode({'sub':owner,'iss':'simmer','aud':'simmer','exp':datetime.now(timezone.utc)+timedelta(hours=4)},config['SESSION_SECRET'],algorithm='HS256')
        response=RedirectResponse(config['APP_URL']+'/#session='+token)
        response.delete_cookie('simmer_oauth',path='/api/google');response.headers['Referrer-Policy']='no-referrer'
        return response
