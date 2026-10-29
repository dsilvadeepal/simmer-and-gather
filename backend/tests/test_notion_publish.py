import pytest
from simmer.db import Conflict
from simmer.recipes import RecipeService, preview_text
from simmer.notion_publish import NotionPublisher

class Notion:
    def __init__(self): self.pages=[]; self.fail=False
    def page(self,id,key): return next(p for p in self.pages if p['id']==id)
    def find_projection(self,key,title): return [p for p in self.pages if p['title']==title]
    def create_projection(self,key,title,lines,properties=None):
        page={'id':str(len(self.pages)+1),'url':'https://notion.so/example','title':title}
        self.pages.append(page)
        if self.fail: raise TimeoutError()
        return page

def recipe(store,owner):
    r=preview_text('Test recipe');r.reviewed=True
    return RecipeService(store).save_reviewed_recipe(owner,r,None)

def test_publishing_exact_reviewed_recipe_is_idempotent(store,owner):
    n=Notion();p=NotionPublisher(store,n);r=recipe(store,owner)
    a=p.recipe(owner,r.id,r.version);b=p.recipe(owner,r.id,r.version)
    assert a==b and a['status']=='saved' and len(n.pages)==1
    with pytest.raises(Conflict):p.recipe(owner,r.id,'wrong-version')

def test_timeout_after_remote_write_reconciles_without_duplicate(store,owner):
    n=Notion();n.fail=True;p=NotionPublisher(store,n);r=recipe(store,owner)
    assert p.recipe(owner,r.id,r.version)['status']=='uncertain'
    assert p.recipe(owner,r.id,r.version)['status']=='saved'
    assert len(n.pages)==1

def test_uncertain_missing_page_does_not_repeat_create(store,owner):
    n=Notion();n.fail=True;p=NotionPublisher(store,n);r=recipe(store,owner)
    assert p.recipe(owner,r.id,r.version)['status']=='uncertain'
    n.pages=[];n.fail=False
    assert p.recipe(owner,r.id,r.version)['status']=='uncertain'
    assert n.pages==[]

def test_plan_export_retries_sessions_and_rejects_stale_revision(store,owner):
    from test_booking import ready
    from simmer.profiles import HostingService
    p=ready(store,owner);n=Notion();publisher=NotionPublisher(store,n)
    a=publisher.plan(owner,p.id,p.revision,p.content_hash)
    assert a['status']=='saved' and len(a['sessions'])==len(p.assignments)
    assert store.list(owner,'approval')==[]
    publisher.plan(owner,p.id,p.revision,p.content_hash)
    assert len(n.pages)==1+len(p.assignments)
    g=HostingService(store).get_gathering(owner,p.gathering_id)
    HostingService(store).save_gathering(owner,g,g.revision)
    with pytest.raises(Conflict): publisher.plan(owner,p.id,p.revision,p.content_hash)

def test_failed_preflight_can_retry_after_connection_repair(store,owner):
    from simmer.adapters.notion import BeforeWriteError
    n=Notion();original=n.create_projection
    n.create_projection=lambda *args: (_ for _ in ()).throw(BeforeWriteError('schema unavailable'))
    r=recipe(store,owner);p=NotionPublisher(store,n)
    assert p.recipe(owner,r.id,r.version)['status']=='retryable'
    n.create_projection=original
    assert p.recipe(owner,r.id,r.version)['status']=='saved'
    assert len(n.pages)==1


def test_deleted_saved_page_is_not_claimed_saved_or_recreated(store,owner):
    n=Notion();p=NotionPublisher(store,n);r=recipe(store,owner)
    assert p.recipe(owner,r.id,r.version)['status']=='saved'
    n.pages=[]
    assert p.recipe(owner,r.id,r.version)['status']=='unavailable'
    assert n.pages==[]

def test_changed_recipe_blocks_plan_export(store,owner):
    from test_booking import ready
    from simmer.domain import PlanInputs
    p=ready(store,owner)
    inputs=PlanInputs.model_validate(store.get(owner,'plan',p.id)[0]['inputs'])
    r=next(s.recipe for s in inputs.selections if s.recipe)
    r=r.model_copy(update={'version':'newer'})
    store.put(owner,'recipe',r.id,r.model_dump(mode='json'))
    n=Notion()
    with pytest.raises(Conflict,match='Recipe collection changed'):
        NotionPublisher(store,n).plan(owner,p.id,p.revision,p.content_hash)
    assert not n.pages
