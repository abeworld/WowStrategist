"""Read-only corpus audit and compact evidence views for strategic review."""
import collections
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
CORPUS = OUT.parent / 'prepared_corpus'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    rows = [json.loads(line) for line in (CORPUS / 'normalized_matches.jsonl').read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    stats = read_json(CORPUS / 'matchup_stats.json')
    review = OUT / 'evidence_review'
    review.mkdir(parents=True, exist_ok=True)
    short_ids = {r['match_id']: f'M{i:03}' for i, r in enumerate(rows, 1)}
    write_json(review / 'match_references.json', {
        short_ids[r['match_id']]: {'match_id': r['match_id'], 'provenance': r['provenance']}
        for r in rows
    })
    group_files = {}
    for path in (CORPUS / 'matchups').glob('*.jsonl'):
        group = [json.loads(x) for x in path.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
        keys = {r['matchup_key'] for r in group}
        assert len(keys) == 1, path
        group_files[next(iter(keys))] = path.relative_to(ROOT).as_posix()
        assert group == [r for r in rows if r['matchup_key'] == next(iter(keys))], path
    assert len({r['match_id'] for r in rows}) == len(rows)
    assert len(stats) == len(group_files)
    overview = []
    for i, stat in enumerate(stats):
        group = [r for r in rows if r['matchup_key'] == stat['matchup_key']]
        counts = collections.Counter(r['result']['value'] for r in group)
        assert len(group) == stat['total_games']
        assert counts['win'] == stat['wins'] and counts['loss'] == stat['losses']
        view = [f"GROUP {i:02}: {stat['matchup_key']}", json.dumps(stat, ensure_ascii=False)]
        for r in sorted(group, key=lambda r: (r['result']['value'] or 'unknown', r['match_id'])):
            view += ['', f"{short_ids[r['match_id']]} | {r['result']['value']} | open={r['opening_target']['normalized']} | kill={r['kill_target']['normalized']} | extraction={r['confidence_from_source']} | flags={','.join(r['quality_flags'])}"]
            for note in r['evidence_notes'].get('observed', []):
                view.append('OBS: ' + str(note))
            view.append('SOURCE CONVERSION: ' + str(r['conversion_from_source']))
            if r['reset_or_recovery_observed']:
                view.append('SOURCE RESET: ' + r['reset_or_recovery_observed'])
            if r['failure_or_turning_point_from_source']:
                view.append('SOURCE FAILURE: ' + r['failure_or_turning_point_from_source'])
            if r['evidence_notes'].get('unknown'):
                view.append('UNKNOWN: ' + json.dumps(r['evidence_notes']['unknown'], ensure_ascii=False))
            for note in r['exception_notes']:
                view.append('EXCEPTION: ' + note)
        (review / f'group_{i:02}.txt').write_text('\n'.join(view) + '\n', encoding='utf-8')
        overview.append({**stat, 'review_group': i, 'matchup_file': group_files[stat['matchup_key']],
                         'all_match_ids': [r['match_id'] for r in group],
                         'source_confidence': dict(collections.Counter(r['confidence_from_source'] for r in group)),
                         'missing_role_fields': sum(not r['priest_actions_or_role_evidence'] and not r['rogue_actions_or_role_evidence'] for r in group)})
    write_json(review / 'overview.json', overview)
    files = sorted(p for p in CORPUS.rglob('*') if p.is_file())
    fingerprints = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write_json(review / 'input_fingerprints.json', fingerprints)
    print(json.dumps({'valid_games': len(rows), 'assigned_games': sum(s['total_games'] for s in stats),
                      'groups': len(stats), 'unresolved_games': sum(r['matchup_key'] is None for r in rows),
                      'prepared_snapshot_sha256': hashlib.sha256((CORPUS / 'normalized_matches.jsonl').read_bytes()).hexdigest(),
                      'group_file_consistency': True, 'results_reconcile': True}))


if __name__ == '__main__':
    main()
