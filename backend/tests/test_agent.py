import pytest
from simmer.agent import PlanningService
from simmer.profiles import HostingService
from simmer.db import Conflict
from simmer.domain import Gathering, MenuSelection

def test_menu_edit_invalidates_revision_and_survives_service_restart(store,owner):
    g=HostingService(store).save_gathering(owner,Gathering(),None)
    s=PlanningService(store)
    updated=s.apply_menu_changes(owner,g.id,[{'action':'add','selection':MenuSelection(id='dessert',title='Cake',mode='cook').model_dump(mode='json')}],1)
    assert updated.gathering.revision==2
    changed=s.apply_menu_changes(owner,g.id,[{'action':'update','id':'dessert','values':{'mode':'buy'}}],2)
    assert PlanningService(store).load(owner,g.id).selections[0].mode=='buy'
    with pytest.raises(Conflict): s.apply_menu_changes(owner,g.id,[],2)

def test_must_have_cannot_be_silently_removed(store,owner):
    g=HostingService(store).save_gathering(owner,Gathering(),None); s=PlanningService(store)
    s.apply_menu_changes(owner,g.id,[{'action':'add','selection':MenuSelection(id='x',title='Must',must_have=True).model_dump(mode='json')}],1)
    with pytest.raises(ValueError): s.apply_menu_changes(owner,g.id,[{'action':'remove','id':'x'}],2)
