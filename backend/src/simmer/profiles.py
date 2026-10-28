from .db import serialized
from .domain import Gathering, HostProfile, PlanInputs
from .db import Missing

class HostingService:
    def __init__(self,store): self.store=store
    @serialized
    def save_gathering(self,owner,gathering,expected_revision):
        value=gathering.model_copy(deep=True)
        value.revision=1 if expected_revision is None else expected_revision+1
        self.store.put(owner,'gathering',value.id,value.model_dump(mode='json'),expected_revision)
        return value
    def get_gathering(self,owner,id): return Gathering.model_validate(self.store.get(owner,'gathering',id)[0])
    def get_profile(self,owner):
        try: return HostProfile.model_validate(self.store.get(owner,'profile','default')[0])
        except Missing: return HostProfile()
    def load_plan_inputs(self,owner,gathering_id):
        g=self.get_gathering(owner,gathering_id)
        try:
            body,_=self.store.get(owner,'inputs',gathering_id)
            body['gathering']=g.model_dump(mode='json')
            return PlanInputs.model_validate(body)
        except Missing: return PlanInputs(gathering=g)
