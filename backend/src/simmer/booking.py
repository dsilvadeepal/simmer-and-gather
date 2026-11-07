from datetime import datetime,timezone,timedelta
from .domain import *
from .db import Conflict,Missing,serialized
from .approval import ApprovalService,event_proposals
from .scheduler import validate_schedule,digest

def remote_matches(remote,event):
    if remote.get('status')=='cancelled' or remote.get('attendees'): return False
    for key in ('id','summary','transparency'):
        if remote.get(key)!=event.get(key): return False
    if remote.get('extendedProperties',{}).get('private')!=event['extendedProperties']['private']: return False
    try:
        return all(datetime.fromisoformat(remote[key]['dateTime'].replace('Z','+00:00'))==datetime.fromisoformat(event[key]['dateTime']) for key in ('start','end'))
    except (KeyError,ValueError): return False

class BookingService:
    def __init__(self,store,google,availability,notion_sync=None): self.store,self.google,self.availability,self.notion_sync=store,google,availability,notion_sync
    def ensure_hosting_calendar(self,owner):
        try:
            saved,rev=self.store.get(owner,'calendar','hosting')
            if saved.get('id'): return saved['id']
        except Missing: saved={};rev=None
        marker='Simmer and Gather managed calendar '+digest(owner)
        matches=[c for c in self.google.list_calendars() if c.get('description')==marker]
        if len(matches)>1: raise Conflict('Multiple app calendars found; review the connection')
        if matches:
            self.store.put(owner,'calendar','hosting',{'id':matches[0]['id']},rev);return matches[0]['id']
        if saved.get('creation_attempted'): raise Conflict('Calendar creation outcome is uncertain; reconnect and reconcile before retrying')
        self.store.put(owner,'calendar','hosting',{'creation_attempted':True},rev)
        _,rev=self.store.get(owner,'calendar','hosting')
        result=self.google.create_hosting_calendar(marker)
        self.store.put(owner,'calendar','hosting',{'id':result['id']},rev)
        return result['id']
    @serialized
    def apply_booking(self,owner,approval_id):
        approval=Approval.model_validate(self.store.get(owner,'approval',approval_id)[0])
        plan,inputs=ApprovalService(self.store).checked(owner,approval.plan_id,approval.revision,approval.content_hash)
        if approval.events!=event_proposals(owner,plan,inputs): raise Conflict('Approved event proposal changed')
        # Already-owned IDs are excluded only by the availability implementation's verified ownership map.
        own=set()
        try:
            calendar=self.store.get(owner,'calendar','hosting')[0].get('id')
            if calendar:
                conflicts=[]
                for event in approval.events:
                    try: operation,_=self.store.get(owner,'operation',event['id'])
                    except Missing: operation={}
                    try: remote=self.google.get_event(calendar,event['id'])
                    except Exception: raise Conflict('Cannot verify existing reservations; retry without changing them')
                    if remote and remote_matches(remote,event): own.add((calendar,event['id']))
                    elif remote or operation.get('ever_confirmed') or operation.get('status')=='confirmed': conflicts.append(event['id'])
                if conflicts:
                    return BookingResult(approval_id=approval.id,outcomes=[{'id':e['id'],'title':e['summary'],'status':'conflict' if e['id'] in conflicts else 'not_attempted'} for e in approval.events],notion_status='not_attempted')
        except Missing: calendar=None
        # Include prior hosting reservations without modifying the approved inputs.
        gathering=inputs.gathering.model_copy(deep=True)
        if calendar and calendar not in gathering.selected_calendars:gathering.selected_calendars.append(calendar)
        fresh=self.availability(owner,gathering,owned=own,force=True)
        if fresh.status!='fresh' or not fresh.checked_at or datetime.now(timezone.utc)-fresh.checked_at>timedelta(seconds=60): raise Conflict('Fresh calendar availability is required')
        current=inputs.model_copy(update={'availability':fresh})
        if validate_schedule(current,plan): raise Conflict('Calendar changed; review a new plan before booking')
        calendar=calendar or self.ensure_hosting_calendar(owner)
        outcomes=[]
        for event in approval.events:
            id=event['id']
            try: operation,rev=self.store.get(owner,'operation',id)
            except Missing:
                operation={'event':event,'calendar':calendar,'status':'pending'}
                self.store.put(owner,'operation',id,operation);rev=1
            if operation['calendar']!=calendar or operation['event']!=event: raise Conflict('Operation payload changed')
            status='pending'
            try:
                remote=self.google.get_event(calendar,id)
                deleted=remote is None and (operation.get('ever_confirmed') or operation['status']=='confirmed')
                if remote is None and not deleted:
                    try: remote=self.google.insert_event(calendar,event)
                    except Exception: remote=self.google.get_event(calendar,id)
                status='confirmed' if remote and remote_matches(remote,event) else ('conflict' if remote or deleted else 'unknown')
            except Exception: status='unknown'
            self.store.put(owner,'operation',id,{**operation,'status':status,'ever_confirmed':operation.get('ever_confirmed',False) or status=='confirmed'},rev)
            outcomes.append({'id':id,'title':event['summary'],'status':status})
        notion='not_connected'
        if self.notion_sync:
            try: self.notion_sync(owner,plan.id);notion='synced'
            except Exception: notion='failed'
        return BookingResult(approval_id=approval.id,outcomes=outcomes,notion_status=notion)
