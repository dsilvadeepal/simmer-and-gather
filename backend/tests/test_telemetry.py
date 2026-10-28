from simmer.telemetry import sanitized_run, configured_telemetry, Telemetry

def test_raw_photos_tokens_and_personal_content_never_enter_trace():
    data=sanitized_run({'model':'test','revision':3,'secret':'private','owner':'person'}, {'status':'feasible','task_count':5,'image':'raw','calendar_title':'doctor appointment','access_token':'secret'})
    assert data=={'metadata':{'model':'test','revision':3},'outputs':{'status':'feasible','task_count':5}}

def test_langsmith_is_opt_in_and_run_payload_is_redacted():
    assert configured_telemetry({'LANGSMITH_TRACING':'false','LANGSMITH_API_KEY':'unused'}) is None
    calls=[]
    class Client:
        def create_run(self,**kwargs): calls.append(kwargs)
    Telemetry(Client()).record_run({'revision':2,'owner':'private'}, {'status':'feasible','calendar_title':'private','task_count':3})
    assert calls[0]['inputs']=={}
    assert calls[0]['outputs']=={'status':'feasible','task_count':3}
    assert calls[0]['extra']['metadata']=={'revision':2}
