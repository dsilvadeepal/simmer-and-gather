from simmer.adapters.notion_client import candidate_from_page

def test_notion_planning_ready_never_bypasses_app_review():
    page={'id':'r','last_edited_time':'v2','properties':{'Recipe':{'type':'title','title':[{'plain_text':'Rice'}]},'Planning Ready':{'checkbox':True},'Source URL':{'url':'https://example.com/rice'},'Base Servings':{'number':4}}}
    r=candidate_from_page(page)
    assert r.title=='Rice' and r.servings==4
    assert r.reviewed is False and not r.tasks and r.uncertainties
