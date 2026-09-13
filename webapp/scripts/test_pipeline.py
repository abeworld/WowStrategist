"""Round-trip tests for evidence export vs canonical install."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import export_data  # noqa: E402
import install_canonical  # noqa: E402


def claim(text: str) -> dict:
    return {
        "text": text,
        "basis": "inferred",
        "confidence": "medium",
        "supporting_match_ids": [],
        "contradicting_match_ids": [],
        "evidence_scope": "none",
    }


def mini_strategy(strategy_id: str, key: str, status: str = "provisional", confidence: str = "medium") -> dict:
    return {
        "strategy_id": strategy_id,
        "strategy_key": key,
        "version": int(strategy_id.rsplit("_v", 1)[-1]),
        "schema_version": "1.0.0",
        "status": status,
        "our_comp": "Shadow Priest / Subtlety Rogue",
        "enemy_comp": "Arms Warrior / Holy Paladin",
        "evidence": {
            "total_games": 2,
            "wins": 1,
            "losses": 1,
            "unknown_result": 0,
            "confidence": confidence,
            "supporting_match_ids": ["win-executes-plan"],
            "contradicting_match_ids": ["win-but-wrong-line"],
            "all_match_ids": ["win-executes-plan", "win-but-wrong-line", "loss-executes-plan"],
        },
        "facts": {"opening_targets": {"Arms Warrior": 2}, "kill_targets": {"Holy Paladin": 2}},
        "default_line": {
            "opening_target": claim("Start Warrior"),
            "initial_objective": claim("Draw Paladin trinket"),
            "win_condition": claim("Kill Paladin"),
            "manufacture": claim("Blind Warrior"),
            "conversion": claim("Go Paladin"),
            "reset": claim("After Shield, rebuild"),
        },
        "states": [
            {
                "state_id": "opening",
                "team_objective": claim("Team opens Warrior"),
                "priest_instruction": claim("Priest Saps Paladin"),
                "rogue_instruction": claim("Rogue stuns Warrior"),
            }
        ],
        "branches": [],
        "failure_modes": [claim("Protection ends the go")],
        "version_history": [{"version": 1, "change": "initial", "reason": "first"}],
    }


class PipelineTests(unittest.TestCase):
    def test_export_does_not_overwrite_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "data"
            out.mkdir()
            corpus = Path(tmp) / "corpus"
            corpus.mkdir()
            (corpus / "matchup_stats.json").write_text("[]", encoding="utf-8")
            (corpus / "normalized_matches.jsonl").write_text("", encoding="utf-8")
            canonical = out / "canonical-package.json"
            payload = {"sentinel": "do-not-touch", "text": "Start Warrior"}
            canonical.write_text(json.dumps(payload), encoding="utf-8")
            before = canonical.read_bytes()
            rc = export_data.main(["--corpus", str(corpus), "--out", str(out)])
            self.assertEqual(rc, 0)
            self.assertEqual(canonical.read_bytes(), before)
            self.assertTrue((out / "matches-slim.json").exists())
            self.assertTrue((out / "corpus-health.json").exists())
            health = json.loads((out / "corpus-health.json").read_text(encoding="utf-8"))
            self.assertIn("coverage", health)
            self.assertNotIn("disc_sub_evidence", health)

    def test_export_does_not_mark_wins_as_supporting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "data"
            corpus = Path(tmp) / "corpus"
            corpus.mkdir()
            (corpus / "matchup_stats.json").write_text("[]", encoding="utf-8")
            row = {
                "match_id": "m1",
                "matchup_key": "SPR__vs__Arms",
                "result": {"value": "win"},
                "our_comp": {"normalized": "Shadow Priest / Subtlety Rogue"},
                "enemy_comp": {"normalized": "Arms Warrior / Holy Paladin"},
                "opening_target": {"normalized": "Arms Warrior"},
                "kill_target": {"normalized": "Holy Paladin"},
                "provenance": {},
            }
            (corpus / "normalized_matches.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
            export_data.main(["--corpus", str(corpus), "--out", str(out)])
            slim = json.loads((out / "matches-slim.json").read_text(encoding="utf-8"))
            self.assertEqual(slim[0]["result"], "win")
            self.assertNotIn("supporting_match_ids", slim[0])
            self.assertNotIn("counterexample_match_ids", slim[0])

    def test_install_valid_and_reject_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "canonical-package.json"
            source = Path(tmp) / "src"
            source.mkdir()
            v1 = mini_strategy("SPR_vs_Arms_HPal_v1", "SPR_vs_Arms_HPal")
            v2 = mini_strategy("SPR_vs_Arms_HPal_v2", "SPR_vs_Arms_HPal")
            v2["default_line"]["opening_target"] = claim("Start Paladin DRAFT")
            envelope = {
                "schema_version": "1.0.0",
                "package_version": "9.9.9",
                "strategies": [v1, v2],
            }
            (source / "strategies.json").write_text(json.dumps(envelope), encoding="utf-8")
            (source / "matchup_index.json").write_text(
                json.dumps(
                    {
                        "friendly_compositions": [
                            {"name": "Shadow Priest / Subtlety Rogue", "status": "evidence_available", "matchup_count": 1},
                            {"name": "Discipline Priest / Subtlety Rogue", "status": "no_evidence", "matchup_count": 0},
                        ],
                        "strategies": [{"strategy_id": "SPR_vs_Arms_HPal_v1"}],
                    }
                ),
                encoding="utf-8",
            )
            rc = install_canonical.main(["--source", str(source), "--dest", str(dest)])
            self.assertEqual(rc, 0)
            installed = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(installed["current"]["SPR_vs_Arms_HPal"], "SPR_vs_Arms_HPal_v1")
            self.assertEqual(len(installed["strategies"]), 2)

            broken = Path(tmp) / "broken.json"
            bad = dict(installed)
            bad["current"] = {"SPR_vs_Arms_HPal": "SPR_vs_Arms_HPal_v3"}
            broken.write_text(json.dumps(bad), encoding="utf-8")
            before = dest.read_bytes()
            rc = install_canonical.main(["--source", str(broken), "--dest", str(dest)])
            self.assertEqual(rc, 1)
            self.assertEqual(dest.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
