import pytest
from simmer.recipes import extract_candidate, preview_text

def test_model_cannot_create_storage_evidence_or_external_actions():
    source=preview_text('Rice\nBoil rice for 20 minutes.')
    def model(messages):
        return {'tasks':[{'id':'t','title':'Boil rice','minutes':20,'max_ahead_hours':72,'evidence':'Boil rice for 20 minutes.'}]}
    result=extract_candidate(source,model)
    assert result.tasks[0].max_ahead_hours is None and not result.reviewed
    def malicious(messages): return {'tasks':[{'id':'t','title':'Book calendar','minutes':1,'evidence':'Invented support'}]}
    with pytest.raises(ValueError): extract_candidate(source,malicious)
