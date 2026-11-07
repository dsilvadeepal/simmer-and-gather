from datetime import datetime, time, timezone, timedelta
from threading import Lock
from zoneinfo import ZoneInfo
from .domain import AvailabilitySnapshot, Interval

def overlaps(a,b): return a.start < b.end and b.start < a.end

def event_interval(event,zone):
    def parse(value):
        if 'dateTime' in value: return datetime.fromisoformat(value['dateTime'].replace('Z','+00:00'))
        return datetime.combine(datetime.fromisoformat(value['date']).date(),time.min,ZoneInfo(value.get('timeZone',zone)))
    return Interval(start=parse(event['start']),end=parse(event['end']))

class AvailabilityService:
    def __init__(self,events,clock=None,hosting_calendar=None):
        self.hosting_calendar=hosting_calendar or (lambda owner:None)
        self.events=events; self.clock=clock or (lambda:datetime.now(timezone.utc)); self.cache={}; self.lock=Lock()
    def read_availability(self,owner,gathering,owned=None,force=False):
        owned=owned or set(); now=self.clock()
        hosting=self.hosting_calendar(owner)
        calendars=list(dict.fromkeys([*gathering.selected_calendars,*([hosting] if hosting else [])]))
        key=(owner,gathering.id,gathering.revision,tuple(sorted(owned)),tuple(calendars),gathering.model_dump_json())
        with self.lock:
            old=self.cache.get(key)
            if not force and old and now-old.checked_at<timedelta(seconds=5): return old.model_copy(deep=True)
            if not gathering.arrival or not gathering.earliest_prep or not gathering.selected_calendars:
                return AvailabilitySnapshot(errors=['Choose calendars, prep start and arrival time'])
            start=datetime.combine(gathering.earliest_prep,time.min,ZoneInfo(gathering.profile.timezone))
            busy=list(gathering.profile.protected)
            try:
                for calendar in calendars:
                    for event in self.events(calendar,start,gathering.arrival):
                        if (calendar,event['id']) in owned or event.get('status')=='cancelled' or event.get('transparency')=='transparent': continue
                        if any(a.get('self') and a.get('responseStatus')=='declined' for a in event.get('attendees',[])): continue
                        busy.append(event_interval(event,gathering.profile.timezone))
                result=AvailabilitySnapshot(busy=busy,checked_at=now,status='fresh')
                self.cache[key]=result
                return result.model_copy(deep=True)
            except Exception:
                if old: return old.model_copy(update={'status':'stale','errors':['Calendar unavailable; last successful snapshot shown']},deep=True)
                return AvailabilitySnapshot(status='unavailable',errors=['Reconnect calendar and recheck'])
