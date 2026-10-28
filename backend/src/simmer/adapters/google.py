"""Google Calendar HTTP boundary. Token refresh is provided by encrypted owner credential service."""
from urllib.parse import quote
import httpx

class GoogleCalendar:
    def __init__(self,token): self.token=token
    def request(self,method,path,body=None,params=None):
        with httpx.Client(timeout=20) as client:
            r=client.request(method,'https://www.googleapis.com/calendar/v3'+path,headers={'Authorization':'Bearer '+self.token()},json=body,params=params)
            if r.status_code==404: return None
            r.raise_for_status(); return r.json()
    def list_calendars(self):
        return self._pages('/users/me/calendarList',{})
    def _pages(self,path,params):
        rows=[]
        for _ in range(100):
            response=self.request('GET',path,params=params)
            if response is None: raise ValueError('Calendar unavailable')
            rows.extend(response.get('items',[]))
            if not response.get('nextPageToken'): return rows
            params=dict(params,pageToken=response['nextPageToken'])
        raise ValueError('Calendar pagination limit reached')
    def events(self,calendar,start,end):
        return self._pages('/calendars/'+quote(calendar,safe='')+'/events',{'timeMin':start.isoformat(),'timeMax':end.isoformat(),'singleEvents':'true','maxResults':2500})
    def get_event(self,calendar,id): return self.request('GET',f'/calendars/{quote(calendar,safe="")}/events/{id}')
    def insert_event(self,calendar,event): return self.request('POST',f'/calendars/{quote(calendar,safe="")}/events',event,{'sendUpdates':'none'})
    def create_hosting_calendar(self): return self.request('POST','/calendars',{'summary':'Simmer and Gather','description':'Hosting prep blocks managed by Simmer and Gather'})
