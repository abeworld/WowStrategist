"""Scoped review utilities. No baseline writes and no automatic semantic classification."""
import json, pathlib, sys, hashlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT.parents[1]
KEYS = ['SPR_vs_Arms_HPal', 'SPR_vs_SP_Sub', 'SPR_vs_Disc_Feral']
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p, obj): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
PACKAGE = read(BASE/'strategies.json')
STRATEGIES = {s['strategy_key']:s for s in PACKAGE['strategies']}
EVIDENCE = read(BASE/'evidence_matches.json')['matches']
ALIASES = read(BASE/'evidence_review/match_references.json')
REVERSE = {v['match_id']:k for k,v in ALIASES.items()}
SCOPED = {key:sorted(REVERSE[i] for i in STRATEGIES[key]['evidence']['all_match_ids']) for key in KEYS}
def record(a): return EVIDENCE[ALIASES[a]['match_id']]
def projection(a):
    r=record(a)
    print('\n'+a+' '+r['result']['value']+' OPEN '+str(r['opening_target']['normalized'])+' KILL '+str(r['kill_target']['normalized'])+' BATCH '+r['provenance']['source_batch']+' CLIP '+str(r['provenance']['source_clip']))
    print('CC',r['opening_cc'])
    for i,t in enumerate(r['setup_actions_from_source']): print('S'+str(i),t)
    for i,t in enumerate(r['evidence_notes']['observed']): print('O'+str(i),t)
    print('RESOURCE LEADS',list(dict.fromkeys(r['important_resources_observed'])))
    for k,n in [('conversion_from_source','C'),('reset_or_recovery_observed','R'),('failure_or_turning_point_from_source','F')]:
        if r[k]: print(n,r[k])
    # Source interpretations remain verbatim in the ledger; do not repeat them as findings.
    print('GAPS',r['evidence_notes']['unknown'],r['exception_notes'],r['quality_flags'],r['field_conflicts'])
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1]=='scope': print(json.dumps(SCOPED))
    elif sys.argv[1]=='show':
        for a in sys.argv[2:]: projection(a)
    elif sys.argv[1]=='batch':
        key=KEYS[int(sys.argv[2])]; start=int(sys.argv[3]); count=int(sys.argv[4])
        for a in SCOPED[key][start:start+count]: projection(a)
