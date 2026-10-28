"""Bounded OpenAI-compatible calls; caller must reserve verified spend first."""
import httpx
class ModelClient:
    def __init__(self,url,key,model,reserve,settle):
        if url not in ('https://api.tokenfactory.nebius.com/v1','https://api.fireworks.ai/inference/v1'): raise ValueError('Unapproved provider')
        self.url,self.key,self.model,self.reserve,self.settle=url,key,model,reserve,settle
    def complete(self,messages,request_id,max_tokens=2000):
        if max_tokens>4000: raise ValueError('Output cap exceeded')
        if len(str(messages))>120_000: raise ValueError('Input cap exceeded')
        if not self.reserve(request_id): raise ValueError('Model budget unavailable')
        with httpx.Client(timeout=60) as client:
            r=client.post(self.url+'/chat/completions',headers={'Authorization':'Bearer '+self.key},json={'model':self.model,'messages':messages,'max_tokens':max_tokens,'temperature':0})
            r.raise_for_status(); data=r.json()
        self.settle(request_id,data.get('usage'))
        return data['choices'][0]['message']['content']
