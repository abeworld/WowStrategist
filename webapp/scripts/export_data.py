"""Export a versioned canonical package + slim evidence from prepared_corpus.

Does not invent strategy text. Default-line fields stay null until a real
canonical package supplies them. Evidence frequencies are facts only.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

CORPUS = Path(r"C:\Users\Gary Goldman\Downloads\Codex_work\Wow strategist\analysis\prepared_corpus")
OUT = Path(__file__).resolve().parents[1] / "public" / "data"

FRIENDLY = [
    "Shadow Priest / Subtlety Rogue",
    "Discipline Priest / Subtlety Rogue",
]

ABBREV = {
    "Shadow Priest": "SP",
    "Discipline Priest": "Disc",
    "Subtlety Rogue": "Sub",
    "Assassination Rogue": "Sin",
    "Combat Rogue": "Combat",
    "Arms Warrior": "Arms",
    "Fury Warrior": "Fury",
    "Protection Warrior": "ProtWar",
    "Holy Paladin": "HPal",
    "Retribution Paladin": "Ret",
    "Protection Paladin": "ProtPal",
    "Frost Mage": "Frost",
    "Arcane Mage": "Arcane",
    "Fire Mage": "Fire",
    "Feral Druid": "Feral",
    "Balance Druid": "Boomkin",
    "Restoration Druid": "Resto",
    "Restoration Shaman": "Rsham",
    "Elemental Shaman": "Ele",
    "Enhancement Shaman": "Enh",
    "Unholy Death Knight": "Unholy",
    "Frost Death Knight": "FrostDK",
    "Blood Death Knight": "Blood",
    "Marksmanship Hunter": "MM",
    "Beast Mastery Hunter": "BM",
    "Survival Hunter": "Surv",
    "Destruction Warlock": "Destro",
    "Affliction Warlock": "Aff",
    "Demonology Warlock": "Demo",
}

FRIENDLY_KEY = {
    "Shadow Priest / Subtlety Rogue": "SPR",
    "Discipline Priest / Subtlety Rogue": "DiscSub",
}


def short_enemy(comp: str) -> str:
    parts = [p.strip() for p in comp.split(" / ")]
    return " / ".join(ABBREV.get(p, p) for p in parts)


def strategy_key(our: str, enemy: str) -> str:
    our_k = FRIENDLY_KEY.get(our, re.sub(r"[^A-Za-z0-9]+", "", our))
    enemy_k = "_".join(ABBREV.get(p.strip(), re.sub(r"[^A-Za-z0-9]+", "", p)) for p in enemy.split(" / "))
    return f"{our_k}_vs_{enemy_k}"


def confidence(games: int) -> str:
    if games >= 30:
        return "high"
    if games >= 10:
        return "medium"
    return "low"


def status(games: int) -> str:
    if games < 5:
        return "insufficient_evidence"
    return "provisional"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stats = json.loads((CORPUS / "matchup_stats.json").read_text(encoding="utf-8"))
    index = json.loads((CORPUS / "matchup_index.json").read_text(encoding="utf-8"))
    matches = load_jsonl(CORPUS / "normalized_matches.jsonl")
    unresolved = load_jsonl(CORPUS / "unresolved_matches.jsonl")
    excluded = load_jsonl(CORPUS / "excluded_records.jsonl")

    by_matchup = defaultdict(list)
    for row in index:
        if row.get("matchup"):
            by_matchup[row["matchup"]].append(row)

    matches_by_id = {m["match_id"]: m for m in matches}

    current = {}
    strategies = []
    for st in stats:
        our, enemy = st["matchup_key"].split("__vs__")
        key = strategy_key(our, enemy)
        sid = f"{key}_v1"
        current[key] = sid
        rows = by_matchup.get(st["matchup_key"], [])
        wins = [r["match_id"] for r in rows if r.get("result") == "win"]
        losses = [r["match_id"] for r in rows if r.get("result") == "loss"]
        games = st["total_games"]
        strategies.append(
            {
                "strategy_key": key,
                "strategy_id": sid,
                "version": 1,
                "status": status(games),
                "confidence": confidence(games),
                "our_comp": our,
                "enemy_comp": enemy,
                "enemy_short": short_enemy(enemy),
                "default_line": {
                    "start": None,
                    "objective": None,
                    "win_condition": None,
                    "convert": None,
                    "alternative": None,
                    "reset": None,
                },
                "roles": {
                    "team": {"summary": None, "responsibilities": []},
                    "priest": {"summary": None, "responsibilities": []},
                    "rogue": {"summary": None, "responsibilities": []},
                },
                "branches": [],
                "failure_modes": [],
                "evidence": {
                    "games": games,
                    "wins": st["wins"],
                    "losses": st["losses"],
                    "unknown_result": st["unknown_result"],
                    "opening_target_known": st["opening_target_known"],
                    "opening_target_unknown": st["opening_target_unknown"],
                    "opening_targets": st["opening_targets"],
                    "kill_target_known": st["kill_target_known"],
                    "kill_target_unknown": st["kill_target_unknown"],
                    "kill_targets": st["kill_targets"],
                    "source_batches": st["source_batch_distribution"],
                    "supporting_match_ids": wins[:40],
                    "counterexample_match_ids": losses[:20],
                    "all_match_ids": [r["match_id"] for r in rows],
                },
                "history": [
                    {
                        "strategy_id": sid,
                        "version": 1,
                        "note": "Evidence snapshot generated from prepared_corpus. No approved strategy text.",
                    }
                ],
            }
        )

    package = {
        "schema_version": "1.0.0",
        "package_version": "0.1.0",
        "package_id": "wow-arena-strategist-canonical",
        "generated_from": "analysis/prepared_corpus",
        "notes": "Provisional evidence package. Default-line and role text are empty until Astra supplies approved strategy versions.",
        "friendly_comps": FRIENDLY,
        "current": current,
        "strategies": strategies,
    }

    slim = []
    for m in matches:
        slim.append(
            {
                "match_id": m["match_id"],
                "matchup": m.get("matchup_key"),
                "result": (m.get("result") or {}).get("value"),
                "our_comp": (m.get("our_comp") or {}).get("normalized"),
                "enemy_comp": (m.get("enemy_comp") or {}).get("normalized"),
                "opening_target": (m.get("opening_target") or {}).get("normalized"),
                "opening_cc": m.get("opening_cc"),
                "kill_target": (m.get("kill_target") or {}).get("normalized"),
                "source_batch": m.get("provenance", {}).get("source_batch"),
                "source_clip": m.get("provenance", {}).get("source_clip"),
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

    health = {
        "valid_2v2": len(matches),
        "assigned": sum(1 for m in matches if m.get("matchup_key")),
        "unresolved": len(unresolved),
        "excluded": len(excluded),
        "matchup_groups": len(stats),
        "disc_sub_evidence": 0,
    }

    (OUT / "canonical-package.json").write_text(json.dumps(package, indent=2), encoding="utf-8")
    (OUT / "matches-slim.json").write_text(json.dumps(slim), encoding="utf-8")
    (OUT / "corpus-health.json").write_text(json.dumps(health, indent=2), encoding="utf-8")
    print(f"wrote {len(strategies)} strategies, {len(slim)} matches -> {OUT}")


if __name__ == "__main__":
    main()
