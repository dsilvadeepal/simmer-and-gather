import pytest
from datetime import datetime,timezone
from simmer.domain import *
from simmer.profiles import HostingService
from simmer.agent import PlanningService
from simmer.approval import ApprovalService
from simmer.booking import BookingService
from simmer.db import Missing,Conflict

class Google:
    def __init__(self): self.remote={};self.inserts=0;self.timeout=False
    def list_calendars(self): return []
    def create_hosting_calendar(self,marker): return {'id':'dedicated','description':marker}
    def get_event(self,calendar,id): return self.remote.get(id)
    def insert_event(self,calendar,event):
        assert calendar=='dedicated' and event['transparency']=='opaque' and 'attendees' not in event
        self.inserts+=1; self.remote[event['id']]=event
        if self.timeout: raise TimeoutError()
        return event

def ready(store,owner):
    g=Gathering(arrival='2026-11-07T18:00:00-05:00',earliest_prep='2026-11-07',prep_days=['2026-11-07'],prep_windows=[Interval(start='2026-11-07T14:00:00-05:00',end='2026-11-07T17:00:00-05:00')],allergies=[],category_counts={'starters':0,'mains':1,'sides':0,'desserts':0,'drinks':0})
    HostingService(store).save_gathering(owner,g,None)
    r=RecipeSnapshot(title='Rice',source='fixture',servings=15,reviewed=True,tasks=[PrepTask(id='a',title='Cook rice',minutes=20,max_ahead_hours=4,evidence='Fixture')])
    service=PlanningService(store)
    service.apply_menu_changes(owner,g.id,[{'action':'add','selection':MenuSelection(title='Rice',recipe=r,servings=15).model_dump(mode='json')}],1)
    plan=service.generate_final_plan(owner,g.id,2,AvailabilitySnapshot(status='fresh',checked_at=datetime.now(timezone.utc)))
    assert plan.status=='feasible'
    return plan

def fresh(*args,**kwargs): return AvailabilitySnapshot(status='fresh',checked_at=datetime.now(timezone.utc))

def test_approval_hash_revision_owner_and_no_write_before_apply(store,owner):
    p=ready(store,owner); google=Google(); approvals=ApprovalService(store)
    with pytest.raises(Conflict): approvals.approve_plan(owner,p.id,p.revision,'wrong')
    with pytest.raises(Missing): approvals.approve_plan('other',p.id,p.revision,p.content_hash)
    a=approvals.approve_plan(owner,p.id,p.revision,p.content_hash)
    assert google.inserts==0
    result=BookingService(store,google,fresh).apply_booking(owner,a.id)
    assert all(x['status']=='confirmed' for x in result.outcomes)
    BookingService(store,google,fresh).apply_booking(owner,a.id)
    assert google.inserts==len(a.events)

def test_timeout_after_success_is_reconciled_without_duplicate(store,owner):
    p=ready(store,owner); a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash)
    google=Google();google.timeout=True
    result=BookingService(store,google,fresh).apply_booking(owner,a.id)
    assert all(x['status']=='confirmed' for x in result.outcomes)
    BookingService(store,google,fresh).apply_booking(owner,a.id)
    assert google.inserts==len(a.events)

def test_stale_revision_and_fresh_conflict_block_writes(store,owner):
    p=ready(store,owner); a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash); google=Google()
    def busy(*args,**kwargs): return AvailabilitySnapshot(status='fresh',checked_at=datetime.now(timezone.utc),busy=[Interval(start='2026-11-07T14:00:00-05:00',end='2026-11-07T17:00:00-05:00')])
    with pytest.raises(Conflict): BookingService(store,google,busy).apply_booking(owner,a.id)
    assert google.inserts==0
    g=HostingService(store).get_gathering(owner,p.gathering_id);HostingService(store).save_gathering(owner,g,g.revision)
    with pytest.raises(Conflict): BookingService(store,google,fresh).apply_booking(owner,a.id)

def test_changed_remote_event_is_reported_not_overwritten(store,owner):
    p=ready(store,owner); a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash);google=Google(); service=BookingService(store,google,fresh)
    service.apply_booking(owner,a.id)
    list(google.remote.values())[0]['summary']='Changed externally'
    result=service.apply_booking(owner,a.id)
    assert result.outcomes[0]['status']=='conflict'

def test_deleted_confirmed_event_is_not_recreated(store,owner):
    p=ready(store,owner);a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash);g=Google();service=BookingService(store,g,fresh)
    service.apply_booking(owner,a.id); before=g.inserts;g.remote.clear()
    result=service.apply_booking(owner,a.id)
    assert g.inserts==before and result.outcomes[0]['status']=='conflict'

def test_google_equivalent_timestamps_are_confirmed(store,owner):
    p=ready(store,owner);a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash);g=Google();service=BookingService(store,g,fresh)
    service.apply_booking(owner,a.id)
    for e in g.remote.values():
        for key in ['start','end']: e[key]={'dateTime':datetime.fromisoformat(e[key]['dateTime']).astimezone(timezone.utc).isoformat().replace('+00:00','Z'),'timeZone':'UTC'}
    result=service.apply_booking(owner,a.id)
    assert all(x['status']=='confirmed' for x in result.outcomes)

def test_repeated_retry_never_recreates_deleted_confirmed_event(store,owner):
    p=ready(store,owner);a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash);g=Google();service=BookingService(store,g,fresh)
    service.apply_booking(owner,a.id);before=g.inserts;g.remote.clear()
    service.apply_booking(owner,a.id);service.apply_booking(owner,a.id)
    assert g.inserts==before

def test_changed_remote_reservation_blocks_remaining_writes(store,owner):
    p=ready(store,owner);a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash);g=Google();service=BookingService(store,g,fresh)
    service.apply_booking(owner,a.id)
    # Any material remote change must stop the write phase before availability exclusions.
    list(g.remote.values())[0]['summary']='Changed externally'
    def inspect(owner,gathering,owned,force):
        assert owned==set(), 'Changed event must not be hidden from availability'
        return fresh()
    service.availability=inspect
    result=service.apply_booking(owner,a.id)
    assert result.outcomes[0]['status']=='conflict'

def test_second_gathering_cannot_overlap_hosting_reservations(store,owner):
    from simmer.availability import AvailabilityService
    p=ready(store,owner);a=ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash)
    google=Google();BookingService(store,google,fresh).apply_booking(owner,a.id)
    before=google.inserts
    second=ready(store,owner);approval=ApprovalService(store).approve_plan(owner,second.id,second.revision,second.content_hash)
    calls=[]
    def events(calendar,start,end):
        calls.append(calendar)
        return list(google.remote.values()) if calendar=='dedicated' else []
    availability=AvailabilityService(events).read_availability
    with pytest.raises(Conflict,match='Calendar changed'):
        BookingService(store,google,availability).apply_booking(owner,approval.id)
    assert 'dedicated' in calls and google.inserts==before
    # Retry of the first exact approval excludes only its verified reservations.
    BookingService(store,google,availability).apply_booking(owner,a.id)
    assert google.inserts==before
