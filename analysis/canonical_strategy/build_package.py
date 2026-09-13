"""Serialize reviewed interpretations and deterministic facts; never modify inputs."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

from editorial_decisions import DECISIONS
from card_copy import CARDS

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
CORPUS = OUT.parent / 'prepared_corpus'
DATE = '2026-09-13'
UNKNOWN = 'unknown'
ABBREV = {'Shadow Priest': 'SP', 'Subtlety Rogue': 'Sub', 'Arms Warrior': 'Arms',
          'Holy Paladin': 'HPal', 'Discipline Priest': 'Disc', 'Feral Druid': 'Feral',
          'Balance Druid': 'Balance', 'Restoration Druid': 'RDruid', 'Marksmanship Hunter': 'MM',
          'Retribution Paladin': 'Ret', 'Destruction Warlock': 'Destro', 'Unholy Death Knight': 'Unholy',
          'Frost Mage': 'Frost', 'Elemental Shaman': 'Ele', 'Enhancement Shaman': 'Enh',
          'Restoration Shaman': 'RSham', 'Fire Mage': 'Fire', 'Assassination Rogue': 'Assa',
          'Arcane Mage': 'Arcane', 'Fury Warrior': 'Fury', 'Protection Paladin': 'ProtPal',
          'Protection Warrior': 'ProtWar', 'Affliction Warlock': 'Aff'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


ROWS = [json.loads(x) for x in (CORPUS / 'normalized_matches.jsonl').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
STATS = read(CORPUS / 'matchup_stats.json')
OVERVIEW = read(OUT / 'evidence_review/overview.json')
REFS = {f'M{i:03}': r for i, r in enumerate(ROWS, 1)}
REVERSE = {r['match_id']: k for k, r in REFS.items()}
SNAPSHOT = hashlib.sha256((CORPUS / 'normalized_matches.jsonl').read_bytes()).hexdigest()
CORPUS_VERSION = 'sha256:' + SNAPSHOT


def ids(refs):
    return [REFS[r]['match_id'] for r in refs]


def claim(text=UNKNOWN, refs=(), confidence='low', basis='inferred', counter=()):
    if text == UNKNOWN:
        confidence, basis = 'insufficient', 'unknown'
    return dict(text=text, basis=basis, confidence=confidence,
                supporting_match_ids=ids(refs), contradicting_match_ids=ids(counter),
                evidence_scope='cited_examples_not_exhaustive_frequency' if refs else 'none')


def target(row, field):
    """Analysis-only reconciliation to a unique enemy member; preserve raw input."""
    value = row[field]['normalized']
    if not value:
        return None, 'unknown'
    low = value.lower()
    if low.startswith(('none', 'no enemy')):
        return None, 'explicit_no_enemy_kill'
    if 'pet' in low or 'crab' in low:
        return value, 'pet'
    members = [m['normalized'] for m in row['enemy_comp']['members']]
    if value in members:
        return value, 'exact'
    matches = [m for m in members if re.search(r'\b' + re.escape(m.split()[-1]) + r'\b', low, re.I)]
    if len(matches) == 1:
        return matches[0], 'unique_enemy_class_in_label'
    return None, 'unmapped'


def facts(group):
    by_result = {}
    for result in ['win', 'loss', 'unknown']:
        subset = [r for r in group if (r['result']['value'] or 'unknown') == result]
        by_result[result] = dict(total=len(subset), opening_targets=dict(collections.Counter(target(r, 'opening_target')[0] or 'unknown' for r in subset)),
            enemy_kill_targets=dict(collections.Counter(target(r, 'kill_target')[0] or 'unknown_or_no_enemy_kill' for r in subset)))
    source_resources = collections.Counter()
    cc_mentions = collections.Counter()
    for r in group:
        # Each exact source label counted once per record, even if copied into two fields.
        for item in sorted(set(r['important_resources_observed'])):
            source_resources[item] += 1
        text = ' '.join(r['evidence_notes']['observed'])
        for cc in ['Sap', 'Blind', 'Fear', 'Silence', 'Gouge', 'Kidney Shot', 'Cyclone']:
            if re.search(r'\b' + re.escape(cc) + r'\b', text, re.I):
                cc_mentions[cc] += 1
    seq = collections.defaultdict(list)
    for r in group:
        a, b = target(r, 'opening_target')[0], target(r, 'kill_target')[0]
        seq[(a or 'unknown', b or 'unknown_or_no_enemy_kill', r['result']['value'] or 'unknown')].append(r['match_id'])
    return dict(by_result=by_result,
        opening_targets=dict(collections.Counter(target(r, 'opening_target')[0] or 'unknown' for r in group)),
        kill_targets=dict(collections.Counter(target(r, 'kill_target')[0] or 'unknown_or_no_enemy_kill' for r in group)),
        opening_to_reported_enemy_kill=[dict(opening_target=k[0], reported_enemy_kill=k[1], result=k[2], count=len(v), match_ids=v) for k, v in sorted(seq.items())],
        sequence_limit='Endpoints only. No intermediate swap timing, causal sequence, or survival at the enemy death is inferred by this computation.',
        source_resource_labels=[dict(label=k, records=n) for k, n in sorted(source_resources.items(), key=lambda pair: (-pair[1], pair[0]))],
        resource_count_limit='Exact source-listed labels, deduplicated within each match. They include uncertain or offensive entries and are not verified forced-resource frequencies.',
        cc_lexical_mentions=dict(cc_mentions),
        cc_count_limit='Literal mentions in observed notes, including negated/uncertain/post-death mentions. These are search aids, not counts of landed CC.',
        recovery_text_present=sum(bool(r['reset_or_recovery_observed']) for r in group),
        recovery_count_limit='Field coverage only: texts may explicitly say no reset. Not a reset-event rate.',
        missing_fields=dict(priest_role=sum(not r['priest_actions_or_role_evidence'] for r in group),
            rogue_role=sum(not r['rogue_actions_or_role_evidence'] for r in group),
            recovery_text=sum(not r['reset_or_recovery_observed'] for r in group),
            result=sum(r['result']['value'] is None for r in group),
            opening_target=sum(target(r, 'opening_target')[0] is None for r in group),
            enemy_kill_target=sum(target(r, 'kill_target')[0] is None for r in group)),
        quality_flags=dict(collections.Counter(f for r in group for f in r['quality_flags'])),
        extraction_confidence=dict(collections.Counter(r['confidence_from_source'] for r in group)))


def build(g):
    stat, ov = STATS[g], OVERVIEW[g]
    group = [r for r in ROWS if r['matchup_key'] == stat['matchup_key']]
    our, enemy = stat['matchup_key'].split('__vs__')
    base = 'SPR_vs_' + '_'.join(ABBREV[p] for p in enemy.split(' / '))
    sid = base + '_v1'
    f = facts(group)
    d = DECISIONS.get(g)
    insufficient = not d or d['confidence'] == 'insufficient'
    confidence = d['confidence'] if d else 'insufficient'
    refs = d['refs'] if d else [REVERSE[r['match_id']] for r in group]
    counters = d['challenge_refs'] if d else []
    opening = collections.Counter(target(r, 'opening_target')[0] for r in group if target(r, 'opening_target')[1] not in ['pet', 'unknown', 'unmapped'])
    modal, modal_n = opening.most_common(1)[0] if opening else (None, 0)
    tied = len([k for k, v in opening.items() if v == modal_n]) > 1
    if insufficient or not modal or tied or modal_n / len(group) < .60:
        start = claim()
    else:
        start_refs = [REVERSE[r['match_id']] for r in group if target(r, 'opening_target')[0] == modal]
        start = claim(f'{modal}; recorded in {modal_n}/{len(group)} games. This is the labeled opening target, not necessarily the first sustained coordinated damage.',
                      start_refs, 'medium' if len(group) >= 8 else 'low', 'pattern')
        start['evidence_scope'] = 'all_labeled_openers_in_this_matchup'
    default = {'opening_target': start}
    for key, field in [('initial_objective', 'objective'), ('win_condition', 'condition'), ('manufacture', 'manufacture'), ('conversion', 'conversion'), ('reset', 'reset')]:
        default[key] = claim(d[field] if d else UNKNOWN, refs if d and not insufficient else [], confidence)
    default['important_resources'] = []
    for res in d.get('resources', []) if d else []:
        entry = dict(name=res['name'], relevance='unknown' if res['role'].startswith('unknown:') else 'conditional',
            assessment=claim(res['role'], res['refs'], 'low' if res['name'] != 'Divine Shield' else confidence, 'inferred', res['counter']),
            requirement='not_established_as_universal_prerequisite',
            relevance_test={
                'repeated_forcing': 'Not computed from copied source hypotheses; cited observations reviewed individually.',
                'before_successful_conversion': 'See cited match chronology; a spend elsewhere in the round is insufficient.',
                'different_behavior_after_spend': 'Supported only for the cited control/immunity sequences; no complete frequency estimate.',
                'wins_with_resource_available': ids(res['counter']),
                'sufficiency_in_losses': 'Not established; compare the matchup failure examples.',
                'pressure_side_effect': 'Cannot be excluded from a spend alone.',
                'control_interaction': res['role']})
        default['important_resources'].append(entry)
    states = []
    state_fields = [('opening','manufacture'), ('pressure','initial_objective'), ('conversion','conversion'), ('recovery','reset')]
    for state, field in state_fields:
        obj = default[field]
        role = d.get('roles', {}).get(state, {}) if d else {}
        states.append(dict(state_id=state, description=obj['text'], team_objective=obj,
            priest_instruction=claim(),
            rogue_instruction=claim(),
            entry_conditions=[claim('An actual pressure commitment has begun.' if state == 'opening' and not insufficient else
                'The preceding attempt is healed, protected, or interrupted.' if state == 'recovery' and not insufficient else
                default['win_condition']['text'] if state == 'conversion' else UNKNOWN,
                refs if not insufficient and state in ['opening','recovery','conversion'] else [], confidence)],
            exit_conditions=[claim()], evidence=ids(refs) if not insufficient else [], confidence=confidence))
        for player in ['priest', 'rogue']:
            if player in role:
                text, rr = role[player]
                states[-1][player + '_instruction'] = claim(text, rr.split(), 'low')
    branches = []
    for i, b in enumerate(d.get('branches', []) if d else [], 1):
        branches.append(dict(branch_id=f'branch_{i}', from_state='pressure', next_state='conversion',
            trigger=claim(b['trigger'], b['refs'], 'low'), response=claim(b['response'], b['refs'], 'low'),
            classification=b['classification'], team_objective=claim(b['response'], b['refs'], 'low'),
            priest_instruction=claim(), rogue_instruction=claim(), evidence=ids(b['refs']), confidence='low'))
    failures = [claim(x['text'], x['refs'], 'low', 'inferred') for x in (d.get('failures', []) if d else [])]
    paired_wins = [r for r in group if r['result']['value'] == 'win' and target(r, 'kill_target')[0] is not None]
    same = [r for r in paired_wins if target(r, 'kill_target')[0] == modal]
    different = [r for r in paired_wins if target(r, 'kill_target')[0] != modal]
    hypotheses = [dict(hypothesis_id='H1', statement='One opening target also explains every reported enemy kill in wins.',
        tested_target=modal if not tied else None,
        disposition='not_testable_as_unique_default' if tied or not modal else 'rejected_as_exhaustive' if different else 'consistent_with_small_sample_not_proven',
        supporting_match_ids=[r['match_id'] for r in same] if not tied else [],
        contradicting_match_ids=[r['match_id'] for r in different] if not tied else [],
        unknown_kill_wins=stat['wins'] - len(paired_wins),
        limitation='Descriptive endpoint comparison. Does not establish intended kill target, causes, or conditional win probability.'),
        dict(hypothesis_id='H2', statement=d['condition'] if d and not insufficient else 'A repeatable default can be inferred from this sparse sample.',
             disposition='insufficient' if insufficient else 'provisional_interpretation',
             supporting_match_ids=ids(refs), contradicting_match_ids=[],
             limitation=d['challenge'] if d else 'Too few independent examples; preserve observations without asserting a default.'),
        dict(hypothesis_id='H3', statement='A stronger fixed resource/target/control prerequisite is necessary.',
             disposition='not_established', supporting_match_ids=[], contradicting_match_ids=ids(counters),
             limitation=d['challenge'] if d else 'No prerequisite is established from the small sample.')]
    quality = ['Source extractions reviewed; original videos were not reopened during synthesis.',
               'Both dedicated player-role fields are empty in all input records; roles remain unknown except where explicit narrative evidence is cited.',
               'Sample win rate is a property of selected footage, not expected ladder performance.',
               'Absent events are unknown unless the record explicitly establishes availability or absence.',
               'A reported enemy kill can occur after a friendly death; the round result is stored separately.']
    if stat['losses'] == 0: quality.append('No losses in this matchup; outcome discrimination and loss-derived failure modes cannot be established.')
    if stat['records_with_quality_flags']: quality.append(f"{stat['records_with_quality_flags']} records carry source quality flags; consult evidence and exceptions before treating a claim as footage-verified.")
    questions = [d['challenge'] if d else 'Collect more wins and losses before assigning a default, meaningful branches, resources or responsibilities.',
                 'Precise Priest/Rogue division of labour by phase is mostly unknown.',
                 'Exact runtime detection reliability on Warmane 3.3.5 is untested.']
    if start['basis'] == 'unknown': questions.append('A reliable default opener is not established; the factual distribution remains available.')
    if not failures: questions.append('No robust failure mode is established from this sample; absence of a failure entry is not evidence of safety.')
    assessments = []
    for r in group:
        ref = REVERSE[r['match_id']]
        matched = [b['classification'] for b in (d.get('branches', []) if d else []) if ref in b['refs']]
        a, k = target(r, 'opening_target')[0], target(r, 'kill_target')[0]
        deviation = (a != modal or k != modal or r['result']['value'] != 'win')
        assessments.append(dict(match_id=r['match_id'], review_id=ref,
            result=r['result']['value'] or 'unknown', observed_opening_target=a, reported_enemy_kill_target=k,
            assessment='cited_branch_example' if matched else 'candidate_endpoint_deviation' if deviation else 'consistent_endpoint_example',
            deviation_classification=matched[0] if matched else 'unknown' if deviation else 'not_applicable',
            limitation='Descriptive review classification; no unobserved intent, positioning trigger or player error assigned.',
            evidence_fields=['evidence_notes.observed', 'conversion_from_source', 'reset_or_recovery_observed', 'failure_or_turning_point_from_source', 'exception_notes']))
    return dict(strategy_id=sid, strategy_key=base, version=1, schema_version='1.0.0',
        status='insufficient_evidence' if insufficient else 'provisional', created_date=DATE,
        our_comp=our, enemy_comp=enemy,
        evidence=dict(total_games=len(group), wins=stat['wins'], losses=stat['losses'], unknown_result=stat['unknown_result'],
            confidence=confidence, supporting_match_ids=ids(refs), contradicting_match_ids=ids(counters),
            contradiction_scope='Challenges to candidate or stronger universal rules, not necessarily to the final qualified wording.',
            representative_match_ids=ids(refs[:3]), all_match_ids=[r['match_id'] for r in group],
            data_quality_notes=quality, source_batches=stat['source_batch_distribution']),
        facts=f, hypotheses=hypotheses, default_line=default, states=states, branches=branches,
        match_assessments=assessments,
        failure_modes=failures,
        runtime_observability=dict(
            automatic=[],
            automatic_candidates=[dict(signal='Verified cast/aura, present health, or an observed control start/end',
                status='unvalidated_candidate', scope='Raw events only; not strategic intent or reliable absence of an enemy cooldown.',
                limitation='No addon implementation or API testing was performed; no automatic transition is certified.')],
            manual_possible=[dict(transition='pressure_to_conversion', confirmation='A meaningful enemy health window, current partner control and friendly readiness overlap.'),
                             dict(transition='conversion_to_recovery', confirmation='Target recovered or became protected; team needs a new usable attempt.')],
            web_only=['Strategic intent', 'Reasons for a target-selection branch', 'Causal counterfactuals', 'Full comparison with losses and unresolved evidence']),
        uncertainties=questions, mechanics_context=[],
        provenance=dict(prepared_corpus_version=CORPUS_VERSION, matchup_file=ov['matchup_file'],
            review_file=f'evidence_review/group_{g:02}.txt', prepared_stats=stat,
            review_group=g, date=DATE),
        version_history=[dict(version=1, date=DATE, corpus=CORPUS_VERSION,
            change='Initial evidence-constrained synthesis; no prior approved strategy replaced.', reason='First canonical package for review.')])


def render_card(s, review_prefix='../'):
    e, line = s['evidence'], s['default_line']
    opening = line['opening_target']['text']
    if opening == UNKNOWN:
        opening += '; observed opening labels: ' + ', '.join(f'{k} {v}' for k,v in s['facts']['opening_targets'].items())
    copy = CARDS.get(s['provenance']['review_group'])
    if copy:
        rows = [f'**{label}:** {value}' for label, value in zip(
            ['Objective','Win condition','Create it','Convert','Alternative','Failure mode','Reset'], copy)]
    else:
        kill_labels = ', '.join(f"{'Unconfirmed enemy kill' if k == 'unknown_or_no_enemy_kill' else k}: {v}" for k,v in s['facts']['by_result']['win']['enemy_kill_targets'].items()) or 'no recorded wins'
        rows = [f'**Observed wins:** {kill_labels}.',
                '**Objective / win condition / conversion:** unknown; this sample does not justify a default.',
                '**Alternative / failure / reset:** unknown; inspect the individual records before generalising.']
    return '\n'.join([
        f"# {s['our_comp']} vs {s['enemy_comp']}", '',
        f"Evidence: {e['total_games']} games · {e['wins']}W/{e['losses']}L/{e['unknown_result']} unknown result · {e['confidence']} confidence · {s['status']} · v1", '',
        f"**Start:** {opening}  ", '  \n'.join(rows), '',
        'Priest/Rogue responsibilities: see the strategy object; unknown unless explicitly supported.', '',
        f"[Full evidence and hypotheses](../strategies/{s['strategy_id']}.json)",
        f"[Source review]({review_prefix}{s['provenance']['review_file']})", ''])


def emit(strategies, dest):
    dest.mkdir(parents=True, exist_ok=True)
    write(dest/'strategies.json', dict(schema_version='1.0.0', package_version='1.0.0', created_date=DATE,
        prepared_corpus_version=CORPUS_VERSION, strategies=strategies))
    for s in strategies:
        write(dest/'strategies'/f"{s['strategy_id']}.json", s)
        cards = dest/'cards'
        cards.mkdir(exist_ok=True)
        (cards/f"{s['strategy_id']}.md").write_text(render_card(s, '../../' if dest.name == 'schema_validation' else '../'), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--validation-only', action='store_true')
    args = parser.parse_args()
    groups = [1,13,35] if args.validation_only else range(len(STATS))
    strategies = [build(g) for g in groups]
    dest = OUT/'schema_validation' if args.validation_only else OUT
    emit(strategies, dest)
    if args.validation_only:
        print(json.dumps({'validation_examples': [s['strategy_id'] for s in strategies], 'written': str(dest)}))
        return
    write(OUT/'matchup_index.json', dict(schema_version='1.0.0',
        friendly_compositions=[dict(name='Shadow Priest / Subtlety Rogue', status='evidence_available', matchup_count=49),
                               dict(name='Discipline Priest / Subtlety Rogue', status='no_evidence', matchup_count=0)],
        strategies=[dict(strategy_id=s['strategy_id'], our_comp=s['our_comp'], enemy_comp=s['enemy_comp'],
            status=s['status'], confidence=s['evidence']['confidence'], games=s['evidence']['total_games'],
            version=s['version'], strategy_file=f"strategies/{s['strategy_id']}.json", card_file=f"cards/{s['strategy_id']}.md") for s in strategies]))
    write(OUT/'contradiction_index.json', dict(scope='Candidate rules and stronger universal claims; consult each hypothesis, not just the match ID.',
        entries=[dict(strategy_id=s['strategy_id'], hypothesis_id=h['hypothesis_id'], rule=h['statement'],
            disposition=h['disposition'], explanation=h['limitation'], contradicting_match_ids=h['contradicting_match_ids'])
            for s in strategies for h in s['hypotheses'] if h['contradicting_match_ids']]))
    write(OUT/'unresolved_matches.json', dict(status='excluded_from_strategy_groups', records=[r for r in ROWS if not r['matchup_key']]))
    # Self-contained evidence registry preserves observations separately from source inference.
    write(OUT/'evidence_matches.json', dict(prepared_corpus_version=CORPUS_VERSION, matches={r['match_id']: r for r in ROWS}))
    adjustments = []
    for r in ROWS:
        if not r['matchup_key']: continue
        for field in ['opening_target','kill_target']:
            mapped, method = target(r, field)
            if method not in ['exact','unknown','pet']:
                adjustments.append(dict(match_id=r['match_id'], field=field, raw=r[field]['normalized'], analysis_value=mapped, method=method))
    write(OUT/'evidence_review/target_reconciliation.json', dict(scope='Read-only analysis view; prepared corpus unchanged.', mappings=adjustments))
    counts = collections.Counter(s['evidence']['confidence'] for s in strategies)
    write(OUT/'package_counts.json', dict(valid_games=len(ROWS), assigned_games=sum(s['evidence']['total_games'] for s in strategies),
        unresolved_games=sum(r['matchup_key'] is None for r in ROWS), matchup_groups=len(strategies), confidence=dict(counts),
        prepared_corpus_version=CORPUS_VERSION))
    print(json.dumps(dict(groups=len(strategies), games=sum(s['evidence']['total_games'] for s in strategies), confidence=dict(counts))))


if __name__ == '__main__':
    main()
