"""Upload only aggregate synthetic evaluation metrics to configured LangSmith."""
import json,os
from pathlib import Path
from simmer.telemetry import Telemetry

def export(client,report,project):
    telemetry=Telemetry(client,project=project,limit=20)
    ids=[]
    for case in report['results']:
        ids.append(telemetry.record_run(
            {'dataset_version':'architecture-controlled-v1','mode':'fixture'},
            {'status':case['outcome']['code'],'score':int(case['validation_passed']),
             'violation_codes':sorted({v['code'] for v in case['violations']}),
             'latency_seconds':case['seconds']},
            name='controlled-hosting-evaluation'))
    return ids

if __name__=='__main__':
    key=os.getenv('LANGSMITH_API_KEY')
    if not key:raise SystemExit('Set LANGSMITH_API_KEY privately before exporting. No upload attempted.')
    from langsmith import Client
    root=Path(__file__).resolve().parents[1]
    report=json.loads((root/'docs/reviews/2026-11-07-architecture-evals.json').read_text())
    client=Client(api_key=key)
    ids=export(client,report,os.getenv('LANGSMITH_PROJECT','simmer-and-gather-dev'))
    print(f'Submitted {len(ids)} synthetic metric records; check LangSmith for persistence.')
