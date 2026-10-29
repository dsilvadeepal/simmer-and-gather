"""Explicitly enabled, priced text inference. No implicit credential discovery."""
from decimal import Decimal
from uuid import uuid4
import json
from .adapters.models import ModelClient
from .budget import Budget

MODEL='accounts/fireworks/models/glm-5p3-flash'

def build_text_model(store,owner,config):
    if config.get('ENABLE_PAID_MODELS')!='true': return None
    if config.get('PLANNING_MODEL',MODEL)!=MODEL: raise ValueError('Planning model has no verified rate contract')
    if not config.get('FIREWORKS_API_KEY'): raise ValueError('Configure Fireworks credentials before enabling paid models')
    budget=Budget(store)
    def settle(request_id,usage):
        # Missing or malformed usage keeps the full conservative reservation.
        if not isinstance(usage,dict): return
        incoming,outgoing=usage.get('prompt_tokens'),usage.get('completion_tokens')
        if not all(type(x) is int and x>=0 for x in (incoming,outgoing)): return
        cost=(Decimal(incoming)*Decimal('.15')+Decimal(outgoing)*Decimal('.50'))/1_000_000
        budget.settle_spend(owner,request_id,cost)
    client=ModelClient('https://api.fireworks.ai/inference/v1',config['FIREWORKS_API_KEY'],MODEL,
                       lambda rid:budget.reserve_spend(owner,rid,Decimal('.05')),settle)
    def complete(messages):
        if any(not isinstance(m.get('content'),str) for m in messages): raise ValueError('Text model accepts text only')
        if len(json.dumps(messages,ensure_ascii=False).encode('utf-8'))>120_000: raise ValueError('Input cap exceeded')
        # Byte-bounded text and 2k output fit this reservation at the verified rates.
        return client.complete(messages,str(uuid4()),max_tokens=2000)
    complete.model_id=MODEL
    return complete
