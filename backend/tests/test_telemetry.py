from simmer.telemetry import sanitized_run

def test_raw_photos_tokens_and_personal_content_never_enter_trace():
    data=sanitized_run({'model':'test','revision':3,'secret':'private','owner':'person'}, {'status':'feasible','task_count':5,'image':'raw','calendar_title':'doctor appointment','access_token':'secret'})
    assert data=={'metadata':{'model':'test','revision':3},'outputs':{'status':'feasible','task_count':5}}
