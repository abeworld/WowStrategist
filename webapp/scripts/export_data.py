"""Export factual match evidence only.

Never writes canonical-package.json or any strategy text, branches, roles,
approval state, strategic confidence, or supporting/counterexample labels.
Those belong to the canonical-strategy track.

Usage:
  python scripts/export_data.py --corpus "C:\\path\\to\\prepared_corpus"
  set WAS_CORPUS=... && python scripts/export_data.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public" / "data"
CANONICAL_NAME = "canonical-package.json"


def coverage_band(games: int) -> str:
    if games >= 30:
        return "high"
    if games >= 10:
        return "medium"
    return "low"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def field_value(row: dict, name: str) -> str | None:
    value = row.get(name)
    if isinstance(value, dict):
        return value.get("normalized") or value.get("value")
    return value


def resolve_corpus(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    env = os.environ.get("WAS_CORPUS")
    if env:
        return Path(env)
    raise SystemExit(
        "prepared_corpus path required. Pass --corpus PATH or set WAS_CORPUS. "
        "This exporter does not hardcode a machine-specific directory."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export slim match evidence; never overwrite canonical strategy.")
    parser.add_argument("--corpus", help="Path to prepared_corpus directory")
    parser.add_argument("--out", default=str(OUT), help="Output directory (default: public/data)")
    args = parser.parse_args(argv)

    corpus = resolve_corpus(args.corpus)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if not corpus.is_dir():
        raise SystemExit(f"corpus not found: {corpus}")

    before_canonical = None
    canonical_path = out / CANONICAL_NAME
    if canonical_path.exists():
        before_canonical = canonical_path.read_bytes()

    stats = json.loads((corpus / "matchup_stats.json").read_text(encoding="utf-8"))
    matches = load_jsonl(corpus / "normalized_matches.jsonl")
    unresolved = load_jsonl(corpus / "unresolved_matches.jsonl") if (corpus / "unresolved_matches.jsonl").exists() else []
    excluded = load_jsonl(corpus / "excluded_records.jsonl") if (corpus / "excluded_records.jsonl").exists() else []

    slim = []
    friendly_games: Counter[str] = Counter()
    friendly_matchups: dict[str, set[str]] = defaultdict(set)
    for m in matches:
        our = field_value(m, "our_comp")
        enemy = field_value(m, "enemy_comp")
        result = field_value(m, "result")
        if our:
            friendly_games[our] += 1
            if enemy:
                friendly_matchups[our].add(enemy)
        slim.append(
            {
                "match_id": m["match_id"],
                "matchup": m.get("matchup_key"),
                "result": result,
                "our_comp": our,
                "enemy_comp": enemy,
                "opening_target": field_value(m, "opening_target"),
                "opening_cc": m.get("opening_cc"),
                "kill_target": field_value(m, "kill_target"),
                "source_batch": (m.get("provenance") or {}).get("source_batch"),
                "source_clip": (m.get("provenance") or {}).get("source_clip"),
                "quality_flags": m.get("quality_flags") or [],
                "confidence": m.get("confidence_from_source"),
                "analysis_status": m.get("analysis_status_from_source"),
                "observed": (m.get("evidence_notes") or {}).get("observed") or [],
                "inferred": (m.get("evidence_notes") or {}).get("inferred") or [],
                "unknown": (m.get("evidence_notes") or {}).get("unknown") or [],
                "win_condition_from_source": m.get("apparent_win_condition_from_source"),
                "failure_from_source": m.get("failure_or_turning_point_from_source"),
            }
        )

    bands = Counter(coverage_band(st["total_games"]) for st in stats)
    health = {
        "valid_2v2": len(matches),
        "assigned": sum(1 for m in matches if m.get("matchup_key")),
        "unresolved": len(unresolved),
        "excluded": len(excluded),
        "matchup_groups": len(stats),
        "friendly_comps": [
            {
                "name": name,
                "status": "evidence_available" if games else "no_evidence",
                "matchup_count": len(friendly_matchups.get(name, ())),
                "games": games,
            }
            for name, games in sorted(friendly_games.items())
        ],
        "coverage": {
            "high": bands.get("high", 0),
            "medium": bands.get("medium", 0),
            "low": bands.get("low", 0),
        },
        "coverage_note": "high/medium/low here are sample-size bands (>=30 / >=10 / <10 games), not strategic confidence.",
    }

    (out / "matches-slim.json").write_text(json.dumps(slim), encoding="utf-8")
    (out / "corpus-health.json").write_text(json.dumps(health, indent=2), encoding="utf-8")

    if canonical_path.exists():
        after = canonical_path.read_bytes()
        if before_canonical is not None and after != before_canonical:
            raise SystemExit("refusing to continue: canonical-package.json changed during evidence export")
    elif before_canonical is not None:
        raise SystemExit("canonical-package.json disappeared during evidence export")

    print(f"wrote {len(slim)} matches and corpus-health -> {out}")
    print(f"left {CANONICAL_NAME} untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
