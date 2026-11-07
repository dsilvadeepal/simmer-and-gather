from simmer.oauth import OAuthState
from simmer.db import Conflict
import pytest

def test_state_single_use_and_browser_binding(store):
    manager=OAuthState(store)
    state,binder,verifier=manager.begin()
    with pytest.raises(Conflict): manager.consume(state,'wrong')
    assert manager.consume(state,binder)==verifier
    with pytest.raises(Conflict): manager.consume(state,binder)

def test_concurrent_refresh_uses_persisted_winner(store,owner,monkeypatch):
    from simmer.oauth import GoogleCredentials
    from simmer.auth import encrypt_secret
    from cryptography.fernet import Fernet
    from datetime import datetime,timezone,timedelta
    import json
    import simmer.oauth as oauth
    key=Fernet.generate_key().decode()
    old={'access_token':'expired','refresh_token':'refresh','expires':(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()}
    store.put(owner,'credential','google',{'encrypted':encrypt_secret(json.dumps(old),key)})
    winner={**old,'access_token':'winner','expires':(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()}
    class Response:
        def raise_for_status(self): pass
        def json(self): return {'access_token':'loser','expires_in':3600}
    class Client:
        def __init__(self,**kw): pass
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def post(self,*args,**kw):
            store.put(owner,'credential','google',{'encrypted':encrypt_secret(json.dumps(winner),key)},1)
            return Response()
    monkeypatch.setattr(oauth.httpx,'Client',Client)
    c=GoogleCredentials(store,owner,{'CREDENTIAL_ENCRYPTION_KEY':key,'GOOGLE_CLIENT_ID':'id','GOOGLE_CLIENT_SECRET':'test'})
    assert c.access_token()=='winner'
