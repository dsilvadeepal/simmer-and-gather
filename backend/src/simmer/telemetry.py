"""Allowlisted trace metadata. Never serialize request/state objects to tracing."""
from datetime import datetime,timezone
from uuid import uuid4

META={'model','provider','revision','plan_id','prompt_version','dataset_version','mode','source_versions'}
OUTPUT={'status','task_count','violation_codes','input_tokens','output_tokens','estimated_usd','latency_seconds','booking_statuses','score'}
def sanitized_run(metadata,payload):
    return {'metadata':{k:v for k,v in metadata.items() if k in META},'outputs':{k:v for k,v in payload.items() if k in OUTPUT}}

class Telemetry:
    def __init__(self,client=None,project='simmer-and-gather-dev',limit=100): self.client,self.project,self.remaining=client,project,limit
    def record_run(self,metadata,redacted_payload,parent_id=None,name='hosting-plan'):
        id=str(uuid4())
        if not self.client or self.remaining<=0: return id
        self.remaining-=1
        safe=sanitized_run(metadata,redacted_payload);now=datetime.now(timezone.utc)
        self.client.create_run(name=name,id=id,run_type='chain',inputs={},outputs=safe['outputs'],extra={'metadata':safe['metadata']},start_time=now,end_time=now,project_name=self.project,**({'parent_run_id':parent_id} if parent_id else {}))
        return id
