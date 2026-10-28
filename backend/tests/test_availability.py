from datetime import datetime,timezone
from simmer.domain import Gathering,Interval
from simmer.availability import AvailabilityService

NOW=datetime(2026,11,5,12,tzinfo=timezone.utc)
def test_selected_calendars_protected_and_owned_exclusion():
    calls=[]
    def events(calendar,start,end):
        calls.append(calendar)
        return [{'id':'own','start':{'dateTime':'2026-11-05T18:00:00-05:00'},'end':{'dateTime':'2026-11-05T19:00:00-05:00'}}, {'id':'other','start':{'dateTime':'2026-11-05T19:00:00-05:00'},'end':{'dateTime':'2026-11-05T20:00:00-05:00'}}]
    g=Gathering(arrival='2026-11-07T18:00:00-05:00',earliest_prep='2026-11-05',selected_calendars=['work'])
    g.profile.protected=[Interval(start='2026-11-06T09:00:00-05:00',end='2026-11-06T17:00:00-05:00')]
    s=AvailabilityService(events,clock=lambda:NOW)
    result=s.read_availability('o',g,{('work','own')})
    assert len(result.busy)==2 and result.status=='fresh'
    s.read_availability('o',g,{('work','own')})
    assert calls==['work']

def test_disconnect_never_means_free():
    def unavailable(*args): raise RuntimeError('disconnected')
    g=Gathering(arrival='2026-11-07T18:00:00-05:00',earliest_prep='2026-11-05',selected_calendars=['work'])
    result=AvailabilityService(unavailable).read_availability('o',g)
    assert result.status=='unavailable' and result.errors
