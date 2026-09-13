"""Build only the staged candidate from the pinned v1 snapshot and reviewed sidecars.
Run from any directory. Original generators and baseline artifacts remain untouched.
"""
from review_work import *
from build_ledger import run as build_ledger, FAMILIES
from refined_content import CONTENT
from decision_context import FIRST_SWITCH
import copy, shutil
BASELINE_HASHES = {
 'strategies.json':'b57205f6a6f3cfba08cf8fabb6e8bd2206736f67677cf8f92c4991b8c1fd3440',
 'evidence_matches.json':'c6a7e9f67e9cc8bdf67293081116b34706dcd772eeeb6dc0fc5535ba2ac256ba',
 'matchup_index.json':'746208db06989f7d6073cb31317659dafdf10364f0c928214bca9faa6bb58fea',
 'contradiction_index.json':'83c7ae4c46128ec4fd04aec2f1e9bf43031f0671a4d855c669c15d669c0bd9e6',
 'package_counts.json':'972e37b555097a3cefa43403a1c868fb4eda0c64529d94da8c52b62fbea6e3a0',
 'unresolved_matches.json':'012fea10d2faa3a7b3d89aa6d01c3abd9c78123deaa52c366b103af187193880'}
def ids(aliases): return [ALIASES[a]['match_id'] for a in aliases.split()] if isinstance(aliases,str) else list(aliases)
def claim(text, aliases='', confidence='medium', basis='inferred', counters='', scope='Reviewed episodes, illustrative support; no estimated causal effect or complete opportunity frequency.'):
 return dict(text=text,basis=basis,confidence=confidence,supporting_match_ids=ids(aliases),contradicting_match_ids=ids(counters),evidence_scope=scope)
def unknown(): return claim('unknown',confidence='insufficient',basis='unknown',scope='Pre-choice discriminator not established; see claim review and precise review requests.')
def content_claim(entry): return claim(entry[0],entry[1],entry[2])
def getrefs(ledger, mids, include_solo=False):
 return [{'match_id':r['match_id'],'window_id':w['window_id'],'source_pointers':[e['source_pointer'] for e in w['evidence_refs']]} for r in ledger if r['match_id'] in mids for w in r['windows'] if include_solo or w['candidate_sequence_family'].split(':')[-1]!='D']
def cohort(ledger,key,predicate):
 rows=[r for r in ledger if r['strategy_key']==key and predicate(r)]
 return dict(distinct_matches=len(rows),denominator=STRATEGIES[key]['evidence']['total_games'],match_ids=[r['match_id'] for r in rows],source_batches=dict(collections.Counter(r['source_batch'] for r in rows)))
def stats(ledger):
 out={}
 for k in KEYS:
  def families(r): return {w['candidate_sequence_family'].split(':')[-1] for w in r['windows']}
  rows0=[r for r in ledger if r['strategy_key']==k]
  switches=[r for a,r in FIRST_SWITCH.items() if r['strategy_key']==k]
  cells={}
  for field in ['damage_opponent_trinket_at_first_healer_commitment','healer_trinket_at_first_healer_commitment','substantive_damage_opponent_pressure_healed_before_switch','partner_control_timing']:
   cells[field]={}
   for value in sorted({r[field] for r in switches}):
    aa=[a for a,r in FIRST_SWITCH.items() if r['strategy_key']==k and r[field]==value]
    cells[field][value]={'count':len(aa),'denominator':len(switches),'unit':'first healer commitment in an annotated damage-opening game with that branch','match_ids':ids(' '.join(aa))}
  out[k]={
   'opening_labels':{target:cohort(ledger,k,lambda r,t=target: REVERSE[r['match_id']] in opening_aliases(k,t)) for target in STRATEGIES[k]['facts']['opening_targets']},
   'damage_opening_with_healer_branch':cohort(ledger,k,lambda r:'W' in families(r) and 'P'in families(r)),
   'damage_line_without_healer_branch':cohort(ledger,k,lambda r:'W'in families(r) and not(families(r)&{'H','P','R','I','B'})),
   'first_switch_states':cells,
   'phase_coverage':dict(collections.Counter(w['phase'] for r in rows0 for w in r['windows'])),
   'all_reviewed_match_ids':[r['match_id'] for r in rows0],
   'round_results':dict(collections.Counter(r['round_result'] for r in rows0))}
 return out
def opening_aliases(key,target):
 # Reuse the existing documented target reconciliation, not a new strategy classifier.
 out=[]
 for alias in SCOPED[key]:
  raw=record(alias)['opening_target']['normalized']
  if target=='unknown': match=not raw
  elif 'Warrior' in target: match=raw and 'Warrior' in raw
  elif 'Paladin' in target: match=raw and 'Paladin' in raw
  elif 'Feral' in target: match=raw and ('Feral' in raw or 'Druid' in raw)
  elif 'Rogue' in target: match=raw and 'Rogue' in raw
  else: match=raw and 'Priest' in raw
  if match: out.append(alias)
 return out
CHALLENGES = {
 KEYS[0]: {
  'alternative':'M048 M091 M322 M431 M456',
  'failed_sequence':'M052 M090 M328 M475',
  'without_depletion':'M070 M087 M229 M472',
  'choice_counter':'M079 M090 M322',
  'explanation':'Warrior attacks may be intended as kills with opportunistic healer changes; the extraction rarely records advance player intent. Some first healer commitments precede escape use or the later Blind. A depleted/controlled state can coexist with continued Warrior damage.'},
 KEYS[1]: {
  'alternative':'M092 M196 M208 M337 M421',
  'failed_sequence':'M078 M190 M292 M417 M423',
  'without_depletion':'M203 M218 M257 M272 M337',
  'choice_counter':'M196 M203 M208 M292 M383',
  'explanation':'The opener may primarily threaten Rogue, with a Priest opportunity emerging from spread damage, control or unrecorded accessibility. Escape use, healing and later control do not uniquely predict the chosen target; some control starts after the switch.'},
 KEYS[2]: {
  'alternative':'M065 M307 M382 M438 M439 M454',
  'failed_sequence':'M308 M450',
  'without_depletion':'M065 M277 M392 M439 M448',
  'choice_counter':'M325 M326 M370 M392 M439 M448 M453',
  'explanation':'Feral may be a setup target for a Priest go in some games, but deep recovered Feral attacks are repeatedly renewed on Feral. Fast healer switches also follow nearly undamaged Feral openers; healing alone is not a discriminator.'}}
def main():
 for name,h in BASELINE_HASHES.items(): assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h, f'Baseline changed: {name}'
 ledger=build_ledger(); assert len(ledger)==215
 lookup={r['match_id']:r for r in ledger}; st=stats(ledger)
 save(ROOT/'analysis/review_statistics.json',{'scope':'Semantic annotations counted after review; overlapping families and selected source footage. No ladder performance or causal ranking.','groups':st})
 manifest={'baseline_root':str(BASE),'output_root':str(ROOT),'baseline_package_version':PACKAGE['package_version'],'candidate_package_version':'1.1.0','schema_version':'1.0.0','prepared_corpus_version':PACKAGE['prepared_corpus_version'],'input_files':{n:{'path':str(BASE/n),'sha256':h} for n,h in BASELINE_HASHES.items()},'instruction_brief':{'path':r'C:\Users\Gary Goldman\Downloads\03_ASTRA_TARGETED_STRATEGY_REFINEMENT.md'},'source_review':'All 215 normalized records reviewed; six original extraction records checked for material ambiguities. No footage viewed.'}
 brief=pathlib.Path(manifest['instruction_brief']['path']);manifest['instruction_brief']['sha256']=hashlib.sha256(brief.read_bytes()).hexdigest()
 save(ROOT/'analysis/input_manifest.json',manifest)
 for name in ['evidence_matches.json','unresolved_matches.json','strategy.schema.json']:
  shutil.copyfile(BASE/name,ROOT/name)
 # These are link dependencies for unchanged cards and provenance, mechanically copied.
 for f in (BASE/'evidence_review').iterdir():
  if f.is_file(): (ROOT/'evidence_review').mkdir(exist_ok=True);shutil.copyfile(f,ROOT/'evidence_review'/f.name)
 for folder in ['cards','strategies']: (ROOT/folder).mkdir(exist_ok=True)
 reviews=[]; result=copy.deepcopy(PACKAGE); result['package_version']='1.1.0'
 for s in result['strategies']:
  key=s['strategy_key']
  if key not in KEYS:
   for folder,suffix in [('strategies','.json'),('cards','.md')]:
    (ROOT/folder).mkdir(exist_ok=True);shutil.copyfile(BASE/folder/(s['strategy_id']+suffix),ROOT/folder/(s['strategy_id']+suffix))
   continue
  cfg=CONTENT[key]; c={name:content_claim(cfg[name]) for name in ['opening','objective','win_condition','manufacture','conversion','reset','alternative','failure']}
  c['opening']['basis']='pattern';c['opening']['supporting_match_ids']=ids(' '.join(opening_aliases(key,{'SPR_vs_Arms_HPal':'Arms Warrior','SPR_vs_SP_Sub':'Subtlety Rogue','SPR_vs_Disc_Feral':'Feral Druid'}[key])))
  c['opening']['evidence_scope']='Complete recorded-opening distribution, qualified against first substantive commitment in all reviewed narratives. analysis/review_statistics.json'
  for name in ['objective','manufacture','reset','alternative']: c[name]['basis']='pattern' if name!='objective' else 'inferred'
  roles={role:content_claim(cfg['roles'][role]) for role in ['priest','rogue']}
  s['version']+=1;s['strategy_id']=key+'_v'+str(s['version']);s['status']='provisional'
  s['version_history'].append({'version':s['version'],'date':'2026-09-13','corpus':PACKAGE['prepared_corpus_version'],'change':'Targeted decision-window review of every match; revised default, competing conversions, resource chronology, unresolved choice triggers and recovery guidance.','reason':'Separate an observed default and conditional setup advantages from universal prerequisites; replace circular target-selection guidance.'})
  resources=[]
  for name,support,text0,challenge in cfg['resources']:
   resources.append({'name':name,'relevance':'conditional','assessment':claim(text0,support),
    'requirement':'Conditional strategic relevance; not an automatic transition or universal pre-attack gate.',
    'relevance_test':{'reviewed_support_match_ids':ids(support),'comparison_match_ids':ids(challenge),'chronology_review':'analysis/first_switch_contexts.json and decision_ledger.jsonl; each enemy and current window tracked separately.','frequency_limit':'Examples and first-switch state coverage; no raw source-label use count, exact repeated-event count or complete opportunity denominator.','different_behavior_after_spend':'See individual annotated windows and claim review; continued same-target attacks are explicitly compared.','pressure_side_effect':'A resource use alone may be a response to pressure; it does not establish intended extraction or branch preference.'}})
  s['default_line']={'opening_target':c['opening'],'initial_objective':c['objective'],'important_resources':resources,'win_condition':c['win_condition'],'manufacture':c['manufacture'],'conversion':c['conversion'],'reset':c['reset']}
  s['states']=[]
  for sid,desc,obj,entry,exitc in [('opening','Observed opening; exact tactical intent remains interpreted',c['opening'],c['opening'],c['objective']),('pressure','Build an actual attack and assess current control/resource responses',c['objective'],c['manufacture'],c['win_condition']),('conversion','Execute a documented damage line; target preference unresolved',c['win_condition'],c['conversion'],c['reset']),('recovery','Recover or leave the intact-team plan after a nonlethal attempt or friendly death',c['reset'],c['reset'],c['manufacture'])]:
   s['states'].append({'state_id':sid,'description':desc,'team_objective':copy.deepcopy(obj),'priest_instruction':copy.deepcopy(roles['priest']),'rogue_instruction':copy.deepcopy(roles['rogue']),'entry_conditions':[copy.deepcopy(entry)],'exit_conditions':[copy.deepcopy(exitc)],'evidence':sorted(set(obj['supporting_match_ids']+entry['supporting_match_ids'])),'confidence':'medium'})
  def branch(bid,trigger,response,classification,frm='pressure',nxt='conversion'):
   return {'branch_id':bid,'from_state':frm,'next_state':nxt,'trigger':trigger,'response':copy.deepcopy(response),'classification':classification,'team_objective':copy.deepcopy(response),'priest_instruction':copy.deepcopy(roles['priest']),'rogue_instruction':copy.deepcopy(roles['rogue']),'evidence':sorted(set(trigger['supporting_match_ids']+response['supporting_match_ids'])),'confidence':response['confidence']}
  repeat_alias={KEYS[0]:'M123 M322 M403 M456',KEYS[1]:'M071 M196 M208 M253 M435',KEYS[2]:'M325 M370 M448 M453'}[key]
  s['branches']=[
   branch('healer_line_selection_unresolved',unknown(),c['conversion'],'recurrent_observed_line_selection_trigger_unknown'),
   branch('renew_damage_target',claim('The previous damage-target attempt has been partially healed; a new same-target attack with renewed partner disruption is the observed continuation in these examples. Exact readiness and priority over switching are not established.',repeat_alias),c['alternative'],'observed_continuation_not_exclusive_choice_rule'),
   branch('rebuild_after_nonlethal_attempt',claim('The attempted target has recovered or a confirmed protection has interrupted its low-health window; the current attempt has not finished it.',cfg['reset'][1]),c['reset'],'conditional_recovery_options',frm='conversion',nxt='recovery')]
  for field,cl in c.items():
   ch=CHALLENGES[key];typ={'opening':'default','objective':'interpretation','win_condition':'interpretation','manufacture':'interpretation','conversion':'decision trigger','reset':'recovery','alternative':'interpretation','failure':'failure'}[field]
   rev={'claim_id':key+'-'+field,'strategy_key':key,'exact_qualified_statement':cl['text'],'claim_type':typ,'applicable_context':'Observed extracted 2v2 episodes; no unobserved player intent, universal priority, or guaranteed success. Solo/trade outcomes are separately identified.',
    'supporting_observations':[{'match_id':mid,'assessment':lookup[mid]['match_level_assessment']['text'],'window_refs':getrefs(ledger,[mid],field=='failure')} for mid in cl['supporting_match_ids']],
    'frequency_and_coverage':{'unit':'selected supporting matches unless explicitly complete recorded-opener distribution','support_count':len(cl['supporting_match_ids']),'group_denominator':s['evidence']['total_games'],'complete_strategy_frequency_estimated':field=='opening','complete_family_counts':'analysis/sequence_counts.json','first_choice_state_coverage':'analysis/review_statistics.json'},
    'strongest_challenges':[{'classification':'alternative_observed_line_not_a_contradiction_to_a_qualified_default','match_ids':ids(ch['alternative'])},{'classification':'nonconversion_or_survival_failure_despite_some_setup_progress_not_a_disproof_of_useful_setup','match_ids':ids(ch['failed_sequence'])},{'classification':'different_resource_path_challenges_a_stronger_mandatory_depletion_interpretation','match_ids':ids(ch['without_depletion'])}],
    'alternative_explanation':ch['explanation'],'decision':'unresolved' if field=='conversion' else 'refine','confidence':cl['confidence'],'confidence_reason':'Repeated described actions support this qualified sequence; pre-choice discrimination, independent opponent sampling and unseen readiness remain limited. Overall strategy confidence remains medium.','actionability_check':'Guidance names an attack/control/recovery action. The healer choice trigger remains unknown and is not implemented as a deterministic if/then.'}
   reviews.append(rev)
  for resource in resources:
   cl=resource['assessment'];support=cl['supporting_match_ids'];reviews.append({'claim_id':key+'-resource-'+str(resources.index(resource)+1),'strategy_key':key,'exact_qualified_statement':cl['text'],'claim_type':'interpretation','applicable_context':resource['name'],'supporting_observations':[{'match_id':mid,'window_refs':getrefs(ledger,[mid]),'assessment':lookup[mid]['match_level_assessment']['text']} for mid in support],'frequency_and_coverage':{'unit':'illustrative reviewed matches, not exact resource-event count','support_count':len(support),'group_denominator':s['evidence']['total_games'],'first_switch_counts':'analysis/review_statistics.json'},'strongest_challenges':[{'classification':'resource-state and alternate-sequence comparisons; not all contradict qualified relevance','match_ids':resource['relevance_test']['comparison_match_ids']}],'alternative_explanation':'Spend may be a pressure response; unseen availability, timing or friendly readiness may determine the choice.','decision':'refine','confidence':'medium','confidence_reason':'Concrete chronological examples; no complete opportunity comparison or causal effect estimate.'})
  for role,cl in roles.items():
   reviews.append({'claim_id':key+'-role-'+role,'strategy_key':key,'exact_qualified_statement':cl['text'],'claim_type':'interpretation','applicable_context':'Narratives with explicit friendly actor ownership only.','supporting_observations':[{'match_id':mid,'window_refs':getrefs(ledger,[mid]),'assessment':lookup[mid]['match_level_assessment']['text']} for mid in cl['supporting_match_ids']],'frequency_and_coverage':{'unit':'illustrative actor-explicit narratives','support_count':len(cl['supporting_match_ids']),'group_denominator':s['evidence']['total_games']},'strongest_challenges':[{'classification':'Dedicated role fields empty; no fixed rotation or universal role attribution inferred.','match_ids':[]}],'alternative_explanation':'These may be situational responsibilities rather than a fixed assignment.','decision':'refine','confidence':cl['confidence'],'confidence_reason':'Actor-explicit examples used; broader role coverage remains incomplete.'})
  reject=key+'-automatic_switch'
  reviews.append({'claim_id':reject,'strategy_key':key,'exact_qualified_statement':'A healed opening damage-target attempt or its Trinket expenditure selects the healer switch over continued damage-target pressure.','claim_type':'decision trigger','applicable_context':'Proposed deterministic target-choice rule, evaluated against actual alternate responses.','supporting_observations':[{'match_id':mid,'window_refs':getrefs(ledger,[mid])} for mid in ids(cfg['conversion'][1])],
   'frequency_and_coverage':{'unit':'first healer branches in damage-opening games; actual comparable no-switch cases additionally reviewed','complete_first_switch_classification':'analysis/first_switch_contexts.json','counterexample_match_ids':ids(CHALLENGES[key]['choice_counter']),'opportunity_denominator':'unknown; recordings do not enumerate every accessible/ready choice point'},
   'strongest_challenges':[{'classification':'state does not select branch; alternate action and branch without that prerequisite both occur','match_ids':ids(CHALLENGES[key]['choice_counter'])}],
   'alternative_explanation':CHALLENGES[key]['explanation'],'decision':'reject','confidence':'medium','confidence_reason':'Observed alternative responses refute a deterministic selector. A probabilistic preference or an additional readiness/accessibility discriminator remains unresolved.'})
  s['hypotheses']=[{'hypothesis_id':r['claim_id'],'statement':r['exact_qualified_statement'],'disposition':r['decision'],'supporting_match_ids':sorted(set(x['match_id'] for x in r['supporting_observations'])),'contradicting_match_ids':ids(CHALLENGES[key]['choice_counter']) if r['claim_id']==reject else [],'limitation':r['alternative_explanation'],'claim_review_file':'analysis/claim_review.json'} for r in reviews if r['strategy_key']==key and r['claim_type'] in ('default','interpretation','decision trigger')]
  s['match_assessments']=[{'match_id':r['match_id'],'review_id':r['review_alias'],'result':r['round_result'],'observed_opening_target':EVIDENCE[r['match_id']]['opening_target']['normalized'],'reported_enemy_kill_target':EVIDENCE[r['match_id']]['kill_target']['normalized'],'assessment':r['match_level_assessment']['text'],'deviation_classification':r['first_death_or_trade_context']['classification'],'review_status':r['review_status'],'reviewed_window_ids':[w['window_id'] for w in r['windows']],'decision_ledger_file':'analysis/decision_ledger.jsonl','limitation':'Semantic record review, including source-observed events and separated interpretations; no independent footage verification or unobserved choice-state inference.'} for r in ledger if r['strategy_key']==key]
  s['failure_modes']=[c['failure']]
  s['uncertainties']=[cfg['unknown'],'Episode counts summarize reviewed attacks or series; exact repeated-attempt counts and complete assessable opportunity denominators are unavailable.','First friendly-death ordering is unknown where the extraction confirms an enemy death without establishing friendly survival; such later episodes have unknown phase.','Dedicated role fields are empty; explicit narrative ownership supports only the qualified role options above.','Raw source-resource labels and lexical CC mentions are unchanged retrieval aids, not landed/forced event frequencies.','No new video review or automatic addon detection validation. Source batches and repeated opponents do not establish independent samples.']
  s['provenance']['review_file']='analysis/'+key+'.md';s['provenance']['refinement_ledger']='analysis/decision_ledger.jsonl';s['provenance']['claim_review']='analysis/claim_review.json'
  s['evidence']['supporting_match_ids']=sorted(set(mid for cl in c.values() for mid in cl['supporting_match_ids']))
  s['evidence']['contradicting_match_ids']=ids(CHALLENGES[key]['choice_counter'])
  s['evidence']['contradiction_scope']='Only challenges to the explicitly rejected automatic-switch hypothesis, not a union of v1 universal-claim exceptions. Qualified defaults have separate alternative and failure evidence in claim_review.json.'
  s['evidence']['data_quality_notes'].append('All scoped matches have individually authored decision episodes; unresolved timing, phase and pre-choice states remain explicit. Review status reviewed_with_gaps reflects extraction limits, not skipped records.')
  save(ROOT/'strategies'/(s['strategy_id']+'.json'),s)
  e=s['evidence']; lines=[f"# {s['our_comp']} vs {s['enemy_comp']}",'',f"**Evidence:** {e['total_games']} games · {e['wins']}W/{e['losses']}L/0 unknown · medium confidence · provisional · v{s['version']}  "]
  lines += [f'**{label}:** {txt}  ' for label,txt in cfg['card']]
  lines += ['',f"[Strategy and claims](../strategies/{s['strategy_id']}.json) · [Decision analysis](../analysis/{key}.md)",'']
  (ROOT/'cards'/(s['strategy_id']+'.md')).write_text('\n'.join(lines),encoding='utf-8')
 save(ROOT/'strategies.json',result)
 save(ROOT/'analysis/claim_review.json',{'review_scope':'Three target strategies only; all 215 source records reviewed. References describe extracted events, not independently watched footage.','claims':reviews})
 index=copy.deepcopy(read(BASE/'matchup_index.json'));index['package_version']='1.1.0'
 for item in index['strategies']:
  key=item['strategy_id'].rsplit('_v',1)[0]
  if key in KEYS:
   item.update(strategy_id=key+'_v2',version=2,strategy_file='strategies/'+key+'_v2.json',card_file='cards/'+key+'_v2.md')
 save(ROOT/'matchup_index.json',index)
 contradictions=copy.deepcopy(read(BASE/'contradiction_index.json'))
 historical=[x for x in contradictions['entries'] if x['strategy_id'].rsplit('_v',1)[0] in KEYS]
 contradictions['entries']=[x for x in contradictions['entries'] if x not in historical]
 for key in KEYS:
  contradictions['entries'].append({'strategy_id':key+'_v2','hypothesis_id':key+'-automatic_switch','rule':'Healed damage-target pressure or its escape spend selects the healer switch over continued damage-target pressure.','disposition':'rejected_as_deterministic_selector','explanation':CHALLENGES[key]['explanation'],'contradicting_match_ids':ids(CHALLENGES[key]['choice_counter']),'claim_review_file':'analysis/claim_review.json'})
 contradictions['historical_entries']=[dict(x,scope='Historical v1 universal/endpoint challenge only; not an active contradiction to the v2 qualified default.') for x in historical]
 contradictions['scope']='Active entries identify the exact challenged rule. Historical v1 target entries are separately scoped; alternative winning lines do not automatically contradict a qualified default.'
 contradictions['package_version']='1.1.0';save(ROOT/'contradiction_index.json',contradictions)
 counts=copy.deepcopy(read(BASE/'package_counts.json'));counts.update(package_version='1.1.0',schema_version='1.0.0',status=dict(collections.Counter(s['status'] for s in result['strategies'])))
 save(ROOT/'package_counts.json',counts)
 print('Candidate written: 49 current strategies; 3 revised v2; 46 copied unchanged; package 1.1.0.')
if __name__=='__main__': main()
