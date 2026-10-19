"""Search review cards; no AI authorship classification."""
from pathlib import Path
import argparse
import json

def load_cases():
    return json.loads(Path(__file__).with_name('cases.json').read_text('utf-8'))['cases']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query', nargs='?', default='')
    p.add_argument('--check', action='store_true')
    args=p.parse_args()
    cards=load_cases()
    if args.check:
        assert len(cards)==30 and len({c['id'] for c in cards})==30
        for c in cards:
            assert all(c[k] for k in ['id','title','evidence_type','version_status','problem','preserve_boundary','source_document','source_sha256'])
            assert len(c['source_sha256'])==64
        assert '否定' in next(c for c in cards if c['id']=='H02')['version_status']
        assert all('未获用户逐条审定' in c['evidence_type'] for c in cards if c['id'].startswith('F'))
        print('PASS: 30 unique cards, required fields, provenance and evidence boundaries')
        return
    for c in cards:
        if args.query.casefold() in json.dumps(c,ensure_ascii=False).casefold():
            print(json.dumps(c,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
