"""Offline hard-constraint regression evals, separate from live model quality."""
import argparse,json,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['fixtures','live'],required=True);ap.add_argument('--split',choices=['all','development','heldout'],default='all');ap.add_argument('--max-usd',type=float);args=ap.parse_args()
    if args.mode=='live': raise SystemExit('Live semantic planning evaluation not yet configured. Use vision_benchmark.py for the bounded image experiment; do not relabel fixtures as live.')
    cases=[json.loads(x) for x in (ROOT/'evals/cases.jsonl').read_text().splitlines()]
    cases=[x for x in cases if args.split=='all' or x['split']==args.split]
    report=ROOT/'.superpowers/eval-results.xml';report.parent.mkdir(exist_ok=True)
    proc=subprocess.run([sys.executable,'-m','pytest','-q',*[x['test'] for x in cases],f'--junitxml={report}'],cwd=ROOT,capture_output=True,text=True)
    tests={x.attrib['name']:x for x in ET.parse(report).iter('testcase')}
    results=[]
    for case in cases:
        test=tests.get(case['test'].split('::')[-1]);passed=test is not None and test.find('failure') is None and test.find('error') is None and test.find('skipped') is None
        results.append({**case,'passed':passed,'evidence':'Local code evaluation with external service fakes; not live AI or Google acceptance'})
    output={'mode':'fixtures','passed':sum(x['passed'] for x in results),'total':len(results),'human_review':'pending','results':results}
    (ROOT/'evals/fixture-results.json').write_text(json.dumps(output,indent=2));print(json.dumps({k:v for k,v in output.items() if k!='results'}));raise SystemExit(proc.returncode)
if __name__=='__main__': main()
