"""Validate package domain invariants and links with Python's standard library.

This performs explicit contract and provenance checks. It is not a replacement
implementation of a general JSON Schema validator.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def walk(node, all_ids):
    if isinstance(node, dict):
        if 'basis' in node:
            assert set(['text','basis','confidence','supporting_match_ids','contradicting_match_ids','evidence_scope']) <= node.keys()
            assert node['basis'] in ['observed','inferred','pattern','unknown']
            assert node['confidence'] in ['high','medium','low','insufficient']
            assert isinstance(node['text'], str)
            if node['basis'] == 'unknown':
                assert node['text'] == 'unknown' and node['confidence'] == 'insufficient'
            elif node['text'] != 'unknown':
                assert node['supporting_match_ids'] or node['contradicting_match_ids'], node
        for key, value in node.items():
            if key.endswith('match_ids') or key == 'evidence' and isinstance(value, list):
                assert isinstance(value, list)
                assert len(value) == len(set(value)), key
                assert set(value) <= all_ids, (key, set(value) - all_ids)
            elif key == 'match_id':
                assert value in all_ids
            walk(value, all_ids)
    elif isinstance(node, list):
        for v in node: walk(v, all_ids)


def main():
    (OUT/'VALIDATION.json').write_text('{"status":"IN_PROGRESS"}\n', encoding='utf-8')
    package = read(OUT/'strategies.json')
    strategies = package['strategies']
    matches = read(OUT/'evidence_matches.json')['matches']
    schema = read(OUT/'strategy.schema.json')
    assert len(strategies) == 49
    assert len(matches) == 487
    seen = []
    for s in strategies:
        assert set(schema['required']) <= s.keys()
        assert s['version'] == 1 and s['schema_version'] == '1.0.0'
        e = s['evidence']
        group_ids = set(e['all_match_ids'])
        seen.extend(e['all_match_ids'])
        assert e['total_games'] == len(group_ids) == e['wins'] + e['losses'] + e['unknown_result']
        assert s['our_comp'] == 'Shadow Priest / Subtlety Rogue'
        for mid in group_ids:
            m = matches[mid]
            assert m['our_comp']['normalized'] == s['our_comp']
            assert m['enemy_comp']['normalized'] == s['enemy_comp']
        walk(s, group_ids)
        counts = collections.Counter(matches[mid]['result']['value'] or 'unknown' for mid in group_ids)
        assert (counts['win'],counts['loss'],counts['unknown']) == (e['wins'],e['losses'],e['unknown_result'])
        for key in ['win','loss','unknown']:
            f = s['facts']['by_result'][key]
            assert f['total'] == counts[key] == sum(f['opening_targets'].values()) == sum(f['enemy_kill_targets'].values())
        assert sum(x['count'] for x in s['facts']['opening_to_reported_enemy_kill']) == e['total_games']
        assert {x['match_id'] for x in s['match_assessments']} == group_ids
        state_ids = {x['state_id'] for x in s['states']}
        assert len(state_ids) == len(s['states'])
        assert all(b['from_state'] in state_ids and b['next_state'] in state_ids for b in s['branches'])
        if s['status'] == 'insufficient_evidence':
            assert all(s['default_line'][k]['basis'] == 'unknown' for k in ['opening_target','initial_objective','win_condition','manufacture','conversion','reset'])
        assert (ROOT/s['provenance']['matchup_file']).is_file()
        assert (OUT/s['provenance']['review_file']).is_file()
        assert read(OUT/'strategies'/f"{s['strategy_id']}.json") == s
        assert (OUT/'cards'/f"{s['strategy_id']}.md").is_file()
    assert len(seen) == len(set(seen)) == 468
    unresolved = read(OUT/'unresolved_matches.json')['records']
    assert len(unresolved) == 19
    assert set(seen).isdisjoint(r['match_id'] for r in unresolved)
    assert set(seen) | {r['match_id'] for r in unresolved} == set(matches)
    for path, expected in read(OUT/'evidence_review/input_fingerprints.json').items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    parsed_json = 0
    for path in OUT.rglob('*.json'):
        read(path)
        parsed_json += 1
    links = 0
    for path in OUT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if target.startswith(('http:', 'https:', '#')): continue
            target = target.strip('<>').split('#')[0]
            assert (path.parent/target).exists(), (str(path), target)
            links += 1
    index = read(OUT/'matchup_index.json')['strategies']
    assert {x['strategy_id'] for x in index} == {s['strategy_id'] for s in strategies}
    pilots = read(OUT/'schema_validation/strategies.json')['strategies']
    for p in pilots:
        assert p == next(s for s in strategies if s['strategy_id'] == p['strategy_id'])
    report = dict(status='PASS', date='2026-09-13', strategy_objects=len(strategies), cards=len(list((OUT/'cards').glob('*.md'))),
        assigned_games=len(seen), unresolved_games=len(unresolved), total_valid_games=len(matches),
        confidence=dict(collections.Counter(s['evidence']['confidence'] for s in strategies)),
        json_files_parsed=parsed_json, markdown_links_checked=links,
        checks=['Required contract fields and claim enums', 'Every cited match belongs to its strategy composition',
                'Round-result and target counts reconcile', '468 assigned records covered exactly once; 19 unresolved retained',
                'State/branch links resolve', 'Unknown guidance retained for insufficient samples',
                'Combined and individual objects agree; pilot objects agree with final serialization',
                'Local Markdown links resolve', 'Prepared corpus SHA-256 fingerprints unchanged'],
        limitations=['Domain/structural checks performed with standard library; a general JSON Schema validator was unavailable.',
                     'No original VOD, gameplay execution, causal inference or addon detection validation was performed.'])
    (OUT/'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__': main()
