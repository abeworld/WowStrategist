"""Install a canonical strategy package into public/data.

Validates before replacing. An invalid package never overwrites a previous valid file.

Usage:
  python scripts/install_canonical.py --source "C:\\...\\refinements\\targeted_v2"
  python scripts/install_canonical.py --source strategies.json
  npm run install-canonical -- --source "<path>"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

CARD_LABELS = (
    ("start", ("Start",)),
    ("objective", ("Objective",)),
    ("win", ("Win condition",)),
    ("create", ("Create it",)),
    ("convert", ("Convert",)),
    ("alternative", ("Alternative",)),
    ("failure", ("Failure mode", "Failure")),
    ("reset", ("Reset",)),
)


def parse_card_markdown(text: str, source: str | None = None) -> dict:
    out: dict[str, str] = {}
    if source:
        out["source"] = source
    for key, labels in CARD_LABELS:
        if key in out and key != "source":
            continue
        for label in labels:
            match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", text)
            if match:
                out[key] = match.group(1).strip()
                break
    return out


def load_presentations(source: Path, strategies: list[dict]) -> dict[str, dict]:
    cards_dir = source / "cards" if source.is_dir() else source.parent / "cards"
    presentations: dict[str, dict] = {}
    if not cards_dir.is_dir():
        return presentations
    for strategy in strategies:
        sid = strategy.get("strategy_id")
        if not sid:
            continue
        path = cards_dir / f"{sid}.md"
        if path.exists():
            presentations[sid] = parse_card_markdown(path.read_text(encoding="utf-8-sig"), path.name)
    return presentations

OUT = Path(__file__).resolve().parents[1] / "public" / "data"
SUPPORTED_SCHEMA = "1.0.0"
STATUSES = {"provisional", "insufficient_evidence", "approved", "superseded"}
CONFIDENCES = {"high", "medium", "low", "insufficient"}
LINE_FIELDS = ("opening_target", "initial_objective", "win_condition", "manufacture", "conversion", "reset")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_claim(value: object) -> bool:
    return isinstance(value, dict) and "text" in value


def validate_package(pkg: dict) -> list[str]:
    errors: list[str] = []
    if pkg.get("schema_version") != SUPPORTED_SCHEMA:
        errors.append(f"unsupported schema_version {pkg.get('schema_version')}")
    if not pkg.get("package_version"):
        errors.append("missing package_version")
    if not isinstance(pkg.get("strategies"), list):
        errors.append("strategies is not an array")
    if not isinstance(pkg.get("current"), dict):
        errors.append("missing current map")
    if not isinstance(pkg.get("friendly_comps"), list):
        errors.append("friendly_comps missing")

    by_id: dict[str, dict] = {}
    for s in pkg.get("strategies") or []:
        if not isinstance(s, dict):
            errors.append("strategy is not an object")
            continue
        sid = s.get("strategy_id")
        key = s.get("strategy_key")
        if not key:
            errors.append("strategy missing strategy_key")
        if not sid:
            errors.append(f"strategy {key} missing strategy_id")
        if sid in by_id:
            errors.append(f"duplicate strategy_id {sid}")
        if sid:
            by_id[sid] = s
        if not s.get("our_comp") or not s.get("enemy_comp"):
            errors.append(f"{sid} missing comps")
        if s.get("status") not in STATUSES:
            errors.append(f"{sid} invalid status {s.get('status')}")
        evidence = s.get("evidence") or {}
        if not isinstance(evidence.get("total_games"), int):
            errors.append(f"{sid} missing evidence.total_games")
        if evidence.get("confidence") not in CONFIDENCES:
            errors.append(f"{sid} invalid evidence.confidence {evidence.get('confidence')}")
        if not isinstance(evidence.get("supporting_match_ids"), list) or not isinstance(
            evidence.get("contradicting_match_ids"), list
        ):
            errors.append(f"{sid} evidence classification arrays required")
        if not isinstance(evidence.get("all_match_ids"), list):
            errors.append(f"{sid} missing evidence.all_match_ids")
        line = s.get("default_line")
        if not isinstance(line, dict):
            errors.append(f"{sid} missing default_line")
        else:
            for field in LINE_FIELDS:
                if field not in line:
                    errors.append(f"{sid} missing default_line.{field}")
                claim = line.get(field)
                if claim is not None and not is_claim(claim):
                    errors.append(f"{sid} default_line.{field} is not a claim")
        if s.get("states") is not None and not isinstance(s.get("states"), list):
            errors.append(f"{sid} states must be an array")
        for state in s.get("states") or []:
            if not all(state.get(k) for k in ("team_objective", "priest_instruction", "rogue_instruction")):
                errors.append(f"{sid} state {state.get('state_id')} missing role claims")
        if s.get("branches") is not None and not isinstance(s.get("branches"), list):
            errors.append(f"{sid} branches must be an array")
        if s.get("failure_modes") is not None and not isinstance(s.get("failure_modes"), list):
            errors.append(f"{sid} failure_modes must be an array")

    for key, sid in (pkg.get("current") or {}).items():
        hit = by_id.get(sid)
        if not hit:
            errors.append(f"current {key} points at missing {sid}")
        elif hit.get("strategy_key") != key:
            errors.append(f"current {key} points at {sid} with key {hit.get('strategy_key')}")
    return errors


def derive_current(strategies: list[dict], index: dict | None) -> dict[str, str]:
    if isinstance(index, dict) and isinstance(index.get("strategies"), list):
        by_id = {s["strategy_id"]: s for s in strategies}
        current: dict[str, str] = {}
        for row in index["strategies"]:
            sid = row.get("strategy_id")
            obj = by_id.get(sid)
            if not obj:
                raise SystemExit(f"matchup_index current id missing from strategies.json: {sid}")
            key = obj["strategy_key"]
            if key in current and current[key] != sid:
                raise SystemExit(f"matchup_index has two current ids for {key}")
            current[key] = sid
        return current
    keys = [s["strategy_key"] for s in strategies]
    if len(keys) != len(set(keys)):
        raise SystemExit(
            "strategies.json contains multiple versions of the same strategy_key and no matchup_index.json. "
            "Refusing to guess current; provide matchup_index.json or a package with an explicit current map."
        )
    return {s["strategy_key"]: s["strategy_id"] for s in strategies}


def friendly_from_index(index: dict | None, strategies: list[dict]) -> list[dict]:
    if isinstance(index, dict) and isinstance(index.get("friendly_compositions"), list):
        return [
            {
                "name": row.get("name"),
                "status": row.get("status") or "unknown",
                "matchup_count": int(row.get("matchup_count") or 0),
            }
            for row in index["friendly_compositions"]
            if row.get("name")
        ]
    names = sorted({s["our_comp"] for s in strategies})
    counts: dict[str, int] = {}
    for s in strategies:
        counts[s["our_comp"]] = counts.get(s["our_comp"], 0) + 1
    return [{"name": n, "status": "evidence_available", "matchup_count": counts[n]} for n in names]


def load_source(source: Path) -> dict:
    if source.is_dir():
        envelope_path = source / "strategies.json"
        if not envelope_path.exists():
            raise SystemExit(f"no strategies.json in {source}")
        envelope = load_json(envelope_path)
        index = load_json(source / "matchup_index.json") if (source / "matchup_index.json").exists() else None
    elif source.is_file():
        envelope = load_json(source)
        index = None
        sibling = source.parent / "matchup_index.json"
        if sibling.exists():
            index = load_json(sibling)
    else:
        raise SystemExit(f"source not found: {source}")

    if not isinstance(envelope, dict) or not isinstance(envelope.get("strategies"), list):
        raise SystemExit("source is not a canonical strategies envelope")

    presentations = envelope.get("presentations") or load_presentations(source, envelope["strategies"])
    if isinstance(envelope.get("current"), dict) and envelope.get("friendly_comps"):
        envelope = dict(envelope)
        envelope["presentations"] = presentations
        return envelope

    return {
        "schema_version": envelope.get("schema_version", SUPPORTED_SCHEMA),
        "package_version": envelope.get("package_version"),
        "created_date": envelope.get("created_date"),
        "prepared_corpus_version": envelope.get("prepared_corpus_version"),
        "notes": envelope.get("notes")
        or "Installed from canonical-strategy track. Strategies remain as authored; webapp does not synthesize them.",
        "friendly_comps": envelope.get("friendly_comps") or friendly_from_index(index, envelope["strategies"]),
        "current": envelope.get("current") or derive_current(envelope["strategies"], index),
        "presentations": presentations,
        "strategies": envelope["strategies"],
    }


def atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="canonical-", suffix=".json", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and install a canonical strategy package.")
    parser.add_argument("--source", required=True, help="strategies.json file or canonical package directory")
    parser.add_argument("--dest", default=str(OUT / "canonical-package.json"))
    args = parser.parse_args(argv)

    dest = Path(args.dest)
    previous = dest.read_bytes() if dest.exists() else None
    pkg = load_source(Path(args.source))
    errors = validate_package(pkg)
    if errors:
        print("Invalid canonical package; previous file left unchanged.", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    atomic_write(dest, pkg)
    print(f"installed {pkg['package_version']} ({len(pkg['strategies'])} strategies, {len(pkg['current'])} current) -> {dest}")
    if previous is not None:
        print("replaced previous canonical package after validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
