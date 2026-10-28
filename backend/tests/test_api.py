from fastapi.testclient import TestClient
from simmer.api import create_app
class Auth:
    def require_owner(self,token):
        if token!='test': raise ValueError()
        return 'api-test-owner'

def test_api_requires_login_and_persists_edits(store):
    client=TestClient(create_app(store,Auth()))
    assert client.get('/api/recipes').status_code==401
    h={'Authorization':'Bearer test'}
    r=client.post('/api/gatherings',headers=h,json={'gathering':{'title':'Dinner'}})
    assert r.status_code==200
    id=r.json()['id']
    edit=client.post('/api/menu/'+id,headers=h,json={'expected_revision':1,'changes':[{'action':'add','selection':{'title':'Prepared dessert','mode':'buy'}}]})
    assert edit.status_code==200
    assert client.get('/api/workspace/'+id,headers=h).json()['inputs']['selections'][0]['mode']=='buy'
    assert client.post('/api/menu/'+id,headers=h,json={'expected_revision':1,'changes':[]}).status_code==409
