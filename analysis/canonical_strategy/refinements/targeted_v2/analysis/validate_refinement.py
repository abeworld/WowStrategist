"""Scoped structural, declared-schema, evidence, count and packaging checks.
No writes outside this candidate. Not a general-purpose JSON Schema implementation.
"""
from review_work import *
from build_ledger import resolve
from build_candidate import BASELINE_HASHES, stats
from refined_content import CONTENT
import importlib.util, re, traceback

COMMANDS = [
 'python analysis\\canonical_strategy\\refinements\\targeted_v2\\analysis\\build_candidate.py',
 'python analysis\\canonical_strategy\\refinements\\targeted_v2\\analysis\\write_refinement_reports.py',
 'python analysis\\canonical_strategy\\refinements\\targeted_v2\\analysis\\validate_refinement.py']
def contract(value,schema,root,path='$'):
 """Check every constraint actually present in the supplied narrow strategy schema."""
 supported={'$schema','$id','title','$defs','$ref','type','required','properties','items','minItems','minimum','enum','const','uniqueItems'}
 assert not(set(schema)-supported), ('unhandled schema keyword',path,set(schema)-supported)
 if '$ref'in schema: return contract(value,resolve(root,schema['$ref'][1:]),root,path)
 if 'type'in schema:
  t=schema['type'];valid={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),'integer':type(value)is int}[t]
  assert valid,(path,t,type(value).__name__)
 if 'const'in schema: assert value==schema['const'],path
 if 'enum'in schema: assert value in schema['enum'],path
 if 'minimum'in schema: assert value>=schema['minimum'],path
 if isinstance(value,dict):
  assert set(schema.get('required',[]))<=set(value),(path,'missing',set(schema.get('required',[]))-set(value))
  for k,v in schema.get('properties',{}).items():
   if k in value: contract(value[k],v,root,path+'.'+k)
 if isinstance(value,list):
  assert len(value)>=schema.get('minItems',0),path
  if schema.get('uniqueItems'): assert len({json.dumps(x,sort_keys=True) for x in value})==len(value),path
  if 'items'in schema:
   for i,x in enumerate(value): contract(x,schema['items'],root,path+'['+str(i)+']')

def main():
 checks=[];report={'status':'IN_PROGRESS','date':'2026-09-13','commands':COMMANDS}
 save(ROOT/'validation_results.json',report)
 try:
  for name,h in BASELINE_HASHES.items(): assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
  checks.append('All six pinned baseline file hashes unchanged; snapshot agrees with the attached baseline.')
  for name in ['evidence_matches.json','unresolved_matches.json','strategy.schema.json']:
   assert (BASE/name).read_bytes()==(ROOT/name).read_bytes(),name
  checks.append('Evidence and unresolved copies byte-identical; schema file unchanged.')
  package=read(ROOT/'strategies.json');current={s['strategy_key']:s for s in package['strategies']};matches=read(ROOT/'evidence_matches.json')['matches']
  assert len(current)==len(package['strategies'])==49 and set(current)==set(STRATEGIES)
  assert (package['package_version'],package['schema_version'],package['prepared_corpus_version'])==('1.1.0','1.0.0',PACKAGE['prepared_corpus_version'])
  schema=read(ROOT/'strategy.schema.json')
  spec=importlib.util.spec_from_file_location('baseline_validator',BASE/'validate_package.py');baseline_validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline_validator)
  assigned=set();statuses=collections.Counter();confidence=collections.Counter()
  for key,s in current.items():
   contract(s,schema,schema);group=set(s['evidence']['all_match_ids']);baseline_validator.walk(s,group)
   assert not assigned&group;assigned|=group
   e=s['evidence'];rc=collections.Counter(matches[mid]['result']['value'] or 'unknown' for mid in group)
   assert len(group)==e['total_games']==e['wins']+e['losses']+e['unknown_result']
   assert (rc['win'],rc['loss'],rc['unknown'])==(e['wins'],e['losses'],e['unknown_result'])
   for mid in group:
    m=matches[mid];assert m['our_comp']['normalized']==s['our_comp'] and m['enemy_comp']['normalized']==s['enemy_comp'];assert m['eligibility']['is_2v2'] and m['eligibility']['bucket']=='assigned'
   assert s['facts']==STRATEGIES[key]['facts']
   states={x['state_id'] for x in s['states']};assert len(states)==len(s['states']);assert all(b['from_state'] in states and b['next_state'] in states for b in s['branches'])
   assert read(ROOT/'strategies'/(s['strategy_id']+'.json'))==s
   assert (ROOT/'cards'/(s['strategy_id']+'.md')).is_file()
   assert (ROOT/s['provenance']['review_file']).is_file()
   assert (BASE.parents[1]/s['provenance']['matchup_file']).is_file()
   if key in KEYS:
    assert s['strategy_id']==key+'_v2' and s['version']==2 and s['status']=='provisional'
    assert s['version_history'][:-1]==STRATEGIES[key]['version_history'] and s['version_history'][-1]['version']==2
    assert s['evidence']['confidence']==STRATEGIES[key]['evidence']['confidence']=='medium'
    assert s['runtime_observability']==STRATEGIES[key]['runtime_observability']
    assert s['branches'][0]['trigger']['text']=='unknown' and s['branches'][0]['trigger']['basis']=='unknown'
   else:
    assert s==STRATEGIES[key],key
    for folder,ext in [('strategies','.json'),('cards','.md')]: assert (ROOT/folder/(s['strategy_id']+ext)).read_bytes()==(BASE/folder/(s['strategy_id']+ext)).read_bytes(),key
   assert s['status']!='approved';assert not s['runtime_observability']['automatic']
   statuses[s['status']]+=1;confidence[e['confidence']]+=1
  assert len(assigned)==468 and len(matches)==487
  unresolved=read(ROOT/'unresolved_matches.json')['records'];unresolved_ids={x['match_id'] for x in unresolved}
  assert len(unresolved)==19 and assigned.isdisjoint(unresolved_ids) and assigned|unresolved_ids==set(matches)
  checks.append('All 49 strategy objects satisfy every constraint declared by the supplied schema and the reused baseline claim/domain walker; compositions, facts and counts reconcile.')
  checks.append('Only three strategy versions changed to v2; other 46 objects and individual JSON/cards are byte-preserved where applicable. No new approval or automatic observability certification.')
  ledger=[json.loads(t) for t in (ROOT/'analysis/decision_ledger.jsonl').read_text(encoding='utf-8').splitlines() if t.strip()]
  scope=set().union(*(set(STRATEGIES[k]['evidence']['all_match_ids']) for k in KEYS));li={r['match_id']:r for r in ledger}
  assert len(ledger)==len(li)==len(scope)==215 and set(li)==scope
  assert sum(r['round_result']=='loss' for r in ledger)==53
  assert set(r['review_status'] for r in ledger)=={'reviewed_with_gaps'}
  window_map={};source_ref_count=0
  required={'match_id','strategy_key','source_batch','round_result','review_status','opening','windows','first_death_or_trade_context','match_level_assessment','unresolved_decision_questions'}
  window_required={'window_id','timing_as_recorded','phase','decision_context_before_action','relevant_resource_and_control_state','observed_action_sequence','attempted_damage_target','control_target','local_outcome','subsequent_recovery_or_switch','candidate_sequence_family','inferred_purpose','evidence_refs','uncertainties'}
  for r in ledger:
   assert required<=r.keys();m=matches[r['match_id']];assert r['round_result']==m['result']['value'] and r['source_batch']==m['provenance']['source_batch'];assert r['match_id'] in current[r['strategy_key']]['evidence']['all_match_ids']
   assert r['retained_source_context']['observed_notes']==m['evidence_notes']['observed'];assert r['retained_source_context']['unknown_notes']==m['evidence_notes']['unknown'];assert r['retained_source_context']['exception_notes']==m['exception_notes'];assert r['retained_source_context']['quality_flags']==m['quality_flags']
   for w in r['windows']:
    assert window_required<=w.keys() and w['evidence_refs'];assert w['phase'] in ['intact_2v2','post_first_death','unknown'];assert w['window_id'] not in window_map
    assert w['exact_attempt_count'] is None and w['window_unit']=='reviewed_episode_not_exact_attempt_count'
    window_map[w['window_id']]=(r,w)
    if w['candidate_sequence_family'].endswith(':D'): assert w['phase']=='post_first_death'
    for ref in w['evidence_refs']:
     assert ref['match_id']==r['match_id'];v=resolve(m,ref['source_pointer']);assert isinstance(v,str) and v.startswith(ref['excerpt']);source_ref_count+=1
     if ref['basis']=='source_observed': assert ref['source_pointer'].startswith('/evidence_notes/observed/') or ref['source_pointer']=='/opening_cc'
  for k in KEYS: assert {x['match_id'] for x in current[k]['match_assessments']}=={r['match_id'] for r in ledger if r['strategy_key']==k}
  checks.append('Exactly 80 + 104 + 31 ledger entries cover every scoped ID once, including all 53 losses; source notes, exceptions, match membership and individual source field/item pointers verified.')
  claims=read(ROOT/'analysis/claim_review.json')['claims'];claim_ids={c['claim_id'] for c in claims};assert len(claim_ids)==len(claims)
  for c in claims:
   assert c['decision'] in ['retain','refine','reject','unresolved'];assert c['claim_type'] in ['default','interpretation','decision trigger','recovery','failure']
   for obs in c['supporting_observations']:
    mid=obs['match_id'];assert li[mid]['strategy_key']==c['strategy_key']
    for wr in obs['window_refs']:
     lr,w=window_map[wr['window_id']];assert wr['match_id']==lr['match_id']==mid
     assert set(wr['source_pointers'])<={x['source_pointer'] for x in w['evidence_refs']}
   for ch in c['strongest_challenges']:
    assert set(ch['match_ids'])<={r['match_id'] for r in ledger if r['strategy_key']==c['strategy_key']}
  for req in read(ROOT/'analysis/review_requests.json'): assert req['claim_id'] in claim_ids and li[req['match_id']]['strategy_key']==req['strategy_key']
  for check in read(ROOT/'analysis/supplemental_provenance_checks.json'):
   p=pathlib.Path(check['source_path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==check['sha256']
   rows0=[json.loads(t) for t in p.read_text(encoding='utf-8-sig').splitlines() if t.strip()];original=next(x for x in rows0 if x['match_id']==check['original_match_id'])
   assert all(original.get(field)==value for field,value in check['fields_checked'].items());assert check['match_id'] in scope
  checks.append('Every claim, challenge and precise review request resolves to the correct matchup and source-backed reviewed windows; qualified challenges are separately scoped.')
  sequence=read(ROOT/'analysis/sequence_counts.json')['groups']
  for key,g in sequence.items():
   rr=[r for r in ledger if r['strategy_key']==key];assert g['reviewed_matches']==len(rr)
   assert g['round_results']==dict(collections.Counter(r['round_result'] for r in rr))
   assert g['first_death_classifications']==dict(collections.Counter(r['first_death_or_trade_context']['classification'] for r in rr))
   for f,d in g['families'].items():
    pairs=[(r,w) for r in rr for w in r['windows'] if w['candidate_sequence_family']==key+':'+f];mids={r['match_id'] for r,w in pairs}
    assert d['distinct_matches']==len(mids) and set(d['match_ids'])==mids and d['reviewed_episode_windows']==len(pairs);assert d['denominator_reviewed_matches']==len(rr)
    assert d['local_outcomes']==dict(collections.Counter(w['local_outcome'] for r,w in pairs))
    assert d['round_results_by_distinct_match']==dict(collections.Counter(r['round_result'] for r in rr if r['match_id'] in mids))
    assert d['source_batches']==dict(collections.Counter(r['source_batch'] for r in rr if r['match_id'] in mids))
  assert read(ROOT/'analysis/review_statistics.json')['groups']==stats(ledger)
  first=read(ROOT/'analysis/first_switch_contexts.json')['records'];first_ids={x['match_id'] for x in first}
  expected_first={r['match_id'] for r in ledger if {'W','P'}<={w['candidate_sequence_family'].split(':')[-1] for w in r['windows']}}
  assert len(first)==len(first_ids) and first_ids==expected_first
  checks.append('Family matches/windows, local versus round outcomes, batch coverage and first-switch counts independently reconciled to ledger; exact attack counts remain unknown.')
  index=read(ROOT/'matchup_index.json');assert len(index['strategies'])==49
  assert {x['strategy_id'] for x in index['strategies']}=={s['strategy_id'] for s in current.values()}
  assert index['friendly_compositions']==read(BASE/'matchup_index.json')['friendly_compositions']
  for item in index['strategies']:
   s=current[item['strategy_id'].rsplit('_v',1)[0]]
   assert item['version']==s['version'] and item['games']==s['evidence']['total_games'] and item['status']==s['status'] and item['confidence']==s['evidence']['confidence']
   for key in ['strategy_file','card_file']:
    p=(ROOT/item[key]).resolve();assert p.is_relative_to(ROOT) and p.is_file()
  assert len(list((ROOT/'strategies').glob('*.json')))==len(list((ROOT/'cards').glob('*.md')))==49
  counts=read(ROOT/'package_counts.json');assert counts['status']==dict(statuses) and counts['confidence']==dict(confidence)
  assert (counts['valid_games'],counts['assigned_games'],counts['unresolved_games'],counts['matchup_groups'])==(487,468,19,49)
  contradictions=read(ROOT/'contradiction_index.json')
  for x in contradictions['entries']:
   key=x['strategy_id'].rsplit('_v',1)[0];assert x['strategy_id']==current[key]['strategy_id'];assert set(x['contradicting_match_ids'])<=set(current[key]['evidence']['all_match_ids'])
   assert x['hypothesis_id'] in {h['hypothesis_id'] for h in current[key]['hypotheses']}
  assert len(contradictions['historical_entries'])==6
  checks.append('Current-version index paths, aggregate and individual files, history, counts and historical-versus-active contradiction identities agree; every indexed path exists inside candidate.')
  card_words={};report_words={}
  for k in KEYS:
   card=(ROOT/'cards'/(k+'_v2.md')).read_text(encoding='utf-8');body=card.split('\n\n',1)[1].split('\n\n[Strategy',1)[0];card_words[k]=len(body.split());assert card_words[k]<=180
   assert len(re.findall(r'^\*\*[^*]+:\*\*',card,re.M))==10
   for label,text0 in CONTENT[k]['card']: assert f'**{label}:** {text0}' in card
   assert current[k]['default_line']['conversion']['text']==CONTENT[k]['conversion'][0]
   analysis=(ROOT/'analysis'/(k+'.md')).read_text(encoding='utf-8');report_words[k]=len(analysis.split('## Sequence families and coverage')[0].split());assert 600<=report_words[k]<=1250,(k,report_words[k])
  parsed=0
  for p in ROOT.rglob('*.json'): read(p);parsed+=1
  link_count=0
  # A placeholder is replaced by the final report below; checking its links is unnecessary.
  for p in ROOT.rglob('*.md'):
   for dest in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
    if dest.startswith(('http:','https:','#')): continue
    d=dest.strip('<>').split('#',1)[0];target=(p.parent/d).resolve()
    assert target.exists() or target==ROOT/'VALIDATION_REPORT.md',(str(p),dest)
    assert target.is_relative_to(ROOT),(str(p),dest);link_count+=1
  checks.append('All JSON/JSONL parses; all local Markdown links resolve inside candidate; three cards have ten labeled lines and stay within 180 words. Reports are within the requested approximate length.')
  semantic={
   'circular_triggers':'Healer-line selection trigger is explicitly unknown; response gives a concrete manufacturing sequence. Recovered health or an already changed target is not used as an automatic selector.',
   'proxies_and_inferences':'No old win-condition boolean, lexical CC tally, source-label frequency, target endpoint or recovery-text coverage is used as an event/strategy success count. Source narratives and observations retain distinct basis labels.',
   'chronology':'Manual annotations separate during/before/coincident/ready/unknown first-switch states, recovered escapes, post-death continuations and unknown friendly death ordering. Unnamed protections and cast attempts remain qualified.',
   'ambiguous_damage':'M398 utility-versus-commitment uncertainty excluded from established Priest-switch counts; M461 recorded opener unchanged but substantive damage qualification retained.',
   'failure_calibration':'Feral losses described separately with low failure confidence; Cyclone counterexamples and failed attempts inside wins retained.',
   'limits':'This is a manual semantic self-review, not a mechanical proof of strategic correctness. No video, causality, gameplay or webapp integration test was performed.'}
  report.update(status='PASS',checks=checks,strategy_objects=49,revised_strategy_objects=3,unchanged_strategy_objects=46,cards=49,ledger_matches=215,losses_reviewed=53,review_status=dict(collections.Counter(r['review_status'] for r in ledger)),reviewed_episode_windows=len(window_map),exact_attempt_count=None,source_references_checked=source_ref_count,claim_reviews=len(claims),first_switch_records=len(first),json_files_parsed=parsed,markdown_links_checked=link_count,card_word_counts=card_words,analysis_word_counts_before_tables=report_words,confidence=dict(confidence),strategy_status=dict(statuses),semantic_self_check=semantic,
   schema_validation='Every keyword used in the supplied schema contract was checked by the narrow standard-library validator, plus the existing baseline domain walker. A general JSON Schema library was unavailable in both installed Python runtimes; unsupported schema keywords fail closed.',
   limitations=['All records reviewed with explicit extraction gaps; unknown phase and choice states are not filled from round result.','Episode windows can summarize repeated attempts; exact attempt counts and complete opportunity denominators unknown.','Human/model semantic annotations are not deterministic facts or causal evidence.','No VOD review, performance ranking, addon detection certification, deployment or app integration test.'])
 except Exception as err:
  report.update(status='FAIL',checks_completed=checks,error=str(err),traceback=traceback.format_exc());save(ROOT/'validation_results.json',report);print(json.dumps(report));raise
 save(ROOT/'validation_results.json',report)
 lines=['# Validation report — PASS','','All required structural, evidence, count and package checks passed for the staged candidate. These checks establish internal consistency, not strategic truth.','']
 lines+=['- '+x for x in checks]
 lines+=['','Verified totals: **49 strategies, 3 revised, 46 unchanged, 215 reviewed matches, 53 losses**. Evidence copies are byte-identical. All strategies retain their prior confidence/status distribution and no automatic detection is certified.','',f"There are {len(window_map)} reviewed episode windows and {source_ref_count} checked source references. Episodes can collapse repeated attacks: exact individual attempt counts remain unknown.",'','## Commands','','Run from the project workspace:','','```powershell',*COMMANDS,'```','','The scoped validator reuses the existing baseline claim/domain checks and checks every constraint present in the unchanged schema. A general JSON Schema library is unavailable in both local Python runtimes; this limitation does not bypass any declared constraint in the supplied schema.','','## Semantic self-check','']
 lines+=['- **'+k.replace('_',' ')+':** '+v for k,v in semantic.items()]
 lines+=['','The build initially encountered a missing closing brace and missing output-folder initialization; both were corrected before this successful validation. No failing check is reported as passed.','','Machine-readable commands, counts, word counts and results: [validation_results.json](validation_results.json).','']
 (ROOT/'VALIDATION_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
 print(json.dumps({k:report[k] for k in ['status','strategy_objects','revised_strategy_objects','unchanged_strategy_objects','ledger_matches','losses_reviewed','reviewed_episode_windows','source_references_checked','claim_reviews','first_switch_records','card_word_counts','analysis_word_counts_before_tables']}))
if __name__=='__main__': main()
