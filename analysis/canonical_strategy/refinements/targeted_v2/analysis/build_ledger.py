"""Materialize individually authored annotations with exact source pointers; aggregate only."""
from review_work import *
from review_annotations import REVIEWS
from decision_context import enrich, FIRST_SWITCH
import re
FAMILIES = {
 KEYS[0]: {'W':('Warrior attack before a substantive Paladin commitment','Warrior','Paladin'),'P':('Paladin damage commitment following Warrior pressure','Paladin','Warrior'),'R':('Return to Warrior after a substantive Paladin commitment','Warrior','Paladin'),'H':('Paladin opening damage commitment','Paladin','Warrior'),'I':('Paladin recommit after a recorded protection response','Paladin','Warrior'),'B':('Renewed Paladin attack without a newly established protection interval','Paladin','Warrior')},
 KEYS[1]: {'W':('Enemy Rogue attack before a substantive Priest commitment','enemy Rogue','enemy Priest'),'P':('Enemy Priest commitment following Rogue pressure','enemy Priest','enemy Rogue'),'R':('Return to enemy Rogue after Priest damage commitment','enemy Rogue','enemy Priest'),'H':('Enemy Priest opening commitment','enemy Priest','enemy Rogue'),'B':('Renewed enemy Priest commitment','enemy Priest','enemy Rogue')},
 KEYS[2]: {'W':('Feral attack before a substantive Priest commitment','Feral','Discipline Priest'),'P':('Discipline Priest commitment following Feral pressure','Discipline Priest','Feral'),'R':('Return to Feral after Priest damage commitment','Feral','Discipline Priest'),'H':('Discipline Priest opening commitment','Discipline Priest','Feral'),'B':('Renewed Discipline Priest commitment','Discipline Priest','Feral')}
}
for fams in FAMILIES.values():
 fams.update(X=('Sequence not established','unknown','unknown'),D=('Post-first-death continuation','see source','see source'))
def pointer(sel):
 if sel[0] in 'SO': return ('/setup_actions_from_source/' if sel[0]=='S' else '/evidence_notes/observed/')+sel[1:]
 return {'C':'/conversion_from_source','R':'/reset_or_recovery_observed','F':'/failure_or_turning_point_from_source','CC':'/opening_cc'}[sel]
def resolve(obj, ptr):
 for part in ptr.strip('/').split('/'): obj=obj[int(part)] if isinstance(obj,list) else obj[part]
 return obj
def run():
 enrich()
 ledger=[]
 for key in KEYS:
  for alias in SCOPED[key]:
   if alias not in REVIEWS: continue
   r=record(alias); a=REVIEWS[alias]; windows=[]
   for j, spec in enumerate(a['episodes'].split(';'),1):
    fam,outcome,sels=spec.split(':'); refs=[]
    for sel in sels.split(','):
     ptr=pointer(sel); val=resolve(r,ptr)
     refs.append(dict(match_id=r['match_id'],source_pointer=ptr,excerpt=val[:360],recorded_timing=re.findall(r'(?:~|about |around |at |near |approximately )?\d+(?:\.\d+)?(?:[–-]\d+(?:\.\d+)?)?\s*(?:seconds|s)\b',val),basis='source_observed' if sel.startswith('O') or sel=='CC' else 'source_narrative_mixed_event_and_interpretation'))
    definition,target,control=FAMILIES[key][fam]
    ctx=a.get('context',{}).get(str(j),{})
    windows.append(dict(window_id=f'{alias}-w{j:02d}',timing_as_recorded={'time_expressions':[t for x in refs for t in x['recorded_timing']],'clock':'source clip/segment as stated in exact evidence; relative order only when no time is stated'},phase='post_first_death' if fam=='D' else ('unknown' if fam=='X' or (j>1 and a['death']=='enemy_death_confirmed_friendly_order_unknown') else 'intact_2v2'),
     decision_context_before_action=ctx.get('before', ('Opening conditions: '+str(r['opening_cc'])) if j==1 else 'Preceding reviewed episode '+windows[-1]['window_id']+' ended '+windows[-1]['local_outcome']+'. Exact choice-point readiness is unknown unless explicitly timed in the referenced evidence; see chronological match assessment.'),
     relevant_resource_and_control_state=ctx.get('resources',{'before_action':'unknown unless explicit in the referenced chronology','events_and_order':'See exact evidence excerpts and match-level chronological assessment. A spend during this episode is not asserted to precede it.','control_target_candidate':control,'effect_identity_and_application':'Retain separately as named in excerpts; no merged Blind/Sap or inferred application from a macro.'}),
     observed_action_sequence=[{'text':resolve(r,x['source_pointer']),'basis':x['basis'],'source_pointer':x['source_pointer']} for x in refs],
     attempted_damage_target=target,control_target=control if fam not in ('X','D') else 'unknown',local_outcome=outcome,
     subsequent_recovery_or_switch='see next reviewed episode' if j<len(a['episodes'].split(';')) else 'see first_death_or_trade_context and match_level_assessment',
     candidate_sequence_family=key+':'+fam,inferred_purpose={'text':definition,'basis':'reviewer_interpretation'},evidence_refs=refs,
     uncertainties=['Episode is a bounded analytical summary, sometimes a collapsed series; exact number of attempts is not established.','Control target denotes the partner whose actions are relevant, not an assertion that control landed or lasted throughout.']+r['evidence_notes']['unknown'],
     window_unit='reviewed_episode_not_exact_attempt_count',exact_attempt_count=None))
   ledger.append(dict(match_id=r['match_id'],review_alias=alias,strategy_key=key,source_batch=r['provenance']['source_batch'],round_result=r['result']['value'],review_status='reviewed_with_gaps',
    opening={'recorded_target':r['opening_target'],'first_substantive_commitment_if_established':{'target':windows[0]['attempted_damage_target'],'qualification':a['assessment'],'certainty':'reviewer interpretation; split/chip/absorbed cases explicitly qualified, unknown where first episode is X'},'control_target':{'recorded_control_sequence':r['opening_cc'],'qualification':'Each actor and application is retained as written; not a verified normalized landed-control count.'}},
    windows=windows,first_death_or_trade_context={'classification':a['death'],'detail':a['assessment'],'source_conversion':r['conversion_from_source'],'source_failure':r['failure_or_turning_point_from_source']},
    match_level_assessment={'text':a['assessment'],'basis':'reviewer_interpretation_of_extracted_events'},unresolved_decision_questions=['Exact selection between target lines and unseen friendly readiness remain unknown where not explicitly narrated.']+r['evidence_notes']['unknown'],
    retained_source_context={'provenance':r['provenance'],'observed_notes':r['evidence_notes']['observed'],'source_inferences_not_reendorsed':r['evidence_notes']['inferred'],'unknown_notes':r['evidence_notes']['unknown'],'exception_notes':r['exception_notes'],'quality_flags':r['quality_flags'],'field_conflicts':r['field_conflicts'],'resource_leads_not_event_counts':list(dict.fromkeys(r['important_resources_observed']))}))
 (ROOT/'analysis/decision_ledger.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger),encoding='utf-8')
 counts={}
 for key in KEYS:
  rows=[r for r in ledger if r['strategy_key']==key]; families={}
  for f,(definition,_,__) in FAMILIES[key].items():
   pairs=[(r,w) for r in rows for w in r['windows'] if w['candidate_sequence_family']==key+':'+f]
   ids=sorted(set(r['match_id'] for r,w in pairs));
   if not ids: continue
   families[f]={'definition':definition,'distinct_matches':len(ids),'denominator_reviewed_matches':len(rows),'match_ids':ids,'reviewed_episode_windows':len(pairs),'exact_attempt_count':None,'local_outcomes':dict(collections.Counter(w['local_outcome'] for r,w in pairs)),'round_results_by_distinct_match':dict(collections.Counter(r['round_result'] for r in rows if r['match_id'] in ids)),'source_batches':dict(collections.Counter(r['source_batch'] for r in rows if r['match_id'] in ids)),'window_refs':[{'match_id':r['match_id'],'window_id':w['window_id']} for r,w in pairs]}
  counts[key]={'reviewed_matches':len(rows),'round_results':dict(collections.Counter(r['round_result'] for r in rows)),'first_death_classifications':dict(collections.Counter(r['first_death_or_trade_context']['classification'] for r in rows)),'families':families}
 save(ROOT/'analysis/sequence_counts.json',{'unit_note':'Family match counts overlap. Windows are reviewed episodes, including collapsed series, not exact counts of attacks or independent games. Classifications are semantic review annotations; aggregation is deterministic.','groups':counts})
 save(ROOT/'analysis/first_switch_contexts.json',{'unit':'first healer commitment per damage-opening match with such a branch; no opportunity denominator for a causal trigger','records':[dict(review_alias=a,match_id=record(a)['match_id'],**r) for a,r in FIRST_SWITCH.items()]})
 print(json.dumps({k:{'reviewed':v['reviewed_matches'],'families':{f:[d['distinct_matches'],d['reviewed_episode_windows']] for f,d in v['families'].items()}} for k,v in counts.items()}))
 return ledger
if __name__=='__main__': run()
