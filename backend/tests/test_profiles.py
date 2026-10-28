import pytest
from simmer.domain import Gathering, HostProfile, Helper
from simmer.profiles import HostingService
from simmer.db import Conflict, Missing

def test_defaults_overrides_and_revision_guard(store, owner):
    service = HostingService(store)
    g = Gathering(title='Diwali')
    saved = service.save_gathering(owner,g,None)
    assert saved.profile.weekday_minutes == 60
    assert saved.profile.weekend_minutes == 120
    assert saved.relax_minutes == 60 and saved.finishing_minutes == 20
    assert saved.allergies is None and saved.profile.equipment == {}
    changed = saved.model_copy(deep=True)
    changed.daily_limits['2026-11-05'] = 90
    new = service.save_gathering(owner,changed,1)
    assert new.revision == 2 and new.profile.weekday_minutes == 60
    with pytest.raises(Conflict): service.save_gathering(owner,saved,1)
    with pytest.raises(Missing): service.get_gathering('other',saved.id)
    assert HostingService(store).get_gathering(owner,saved.id).daily_limits['2026-11-05'] == 90

def test_helper_windows_remain_explicit():
    p = HostProfile(helpers=[Helper(id='h', name='Helper', skills=['measure'])])
    assert p.helpers[0].available == []
