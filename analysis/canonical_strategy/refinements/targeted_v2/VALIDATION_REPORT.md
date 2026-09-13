# Validation report — PASS

All required structural, evidence, count and package checks passed for the staged candidate. These checks establish internal consistency, not strategic truth.

- All six pinned baseline file hashes unchanged; snapshot agrees with the attached baseline.
- Evidence and unresolved copies byte-identical; schema file unchanged.
- All 49 strategy objects satisfy every constraint declared by the supplied schema and the reused baseline claim/domain walker; compositions, facts and counts reconcile.
- Only three strategy versions changed to v2; other 46 objects and individual JSON/cards are byte-preserved where applicable. No new approval or automatic observability certification.
- Exactly 80 + 104 + 31 ledger entries cover every scoped ID once, including all 53 losses; source notes, exceptions, match membership and individual source field/item pointers verified.
- Every claim, challenge and precise review request resolves to the correct matchup and source-backed reviewed windows; qualified challenges are separately scoped.
- Family matches/windows, local versus round outcomes, batch coverage and first-switch counts independently reconciled to ledger; exact attack counts remain unknown.
- Current-version index paths, aggregate and individual files, history, counts and historical-versus-active contradiction identities agree; every indexed path exists inside candidate.
- All JSON/JSONL parses; all local Markdown links resolve inside candidate; three cards have ten labeled lines and stay within 180 words. Reports are within the requested approximate length.

Verified totals: **49 strategies, 3 revised, 46 unchanged, 215 reviewed matches, 53 losses**. Evidence copies are byte-identical. All strategies retain their prior confidence/status distribution and no automatic detection is certified.

There are 599 reviewed episode windows and 1685 checked source references. Episodes can collapse repeated attacks: exact individual attempt counts remain unknown.

## Commands

Run from the project workspace:

```powershell
python analysis\canonical_strategy\refinements\targeted_v2\analysis\build_candidate.py
python analysis\canonical_strategy\refinements\targeted_v2\analysis\write_refinement_reports.py
python analysis\canonical_strategy\refinements\targeted_v2\analysis\validate_refinement.py
```

The scoped validator reuses the existing baseline claim/domain checks and checks every constraint present in the unchanged schema. A general JSON Schema library is unavailable in both local Python runtimes; this limitation does not bypass any declared constraint in the supplied schema.

## Semantic self-check

- **circular triggers:** Healer-line selection trigger is explicitly unknown; response gives a concrete manufacturing sequence. Recovered health or an already changed target is not used as an automatic selector.
- **proxies and inferences:** No old win-condition boolean, lexical CC tally, source-label frequency, target endpoint or recovery-text coverage is used as an event/strategy success count. Source narratives and observations retain distinct basis labels.
- **chronology:** Manual annotations separate during/before/coincident/ready/unknown first-switch states, recovered escapes, post-death continuations and unknown friendly death ordering. Unnamed protections and cast attempts remain qualified.
- **ambiguous damage:** M398 utility-versus-commitment uncertainty excluded from established Priest-switch counts; M461 recorded opener unchanged but substantive damage qualification retained.
- **failure calibration:** Feral losses described separately with low failure confidence; Cyclone counterexamples and failed attempts inside wins retained.
- **limits:** This is a manual semantic self-review, not a mechanical proof of strategic correctness. No video, causality, gameplay or webapp integration test was performed.

The build initially encountered a missing closing brace and missing output-folder initialization; both were corrected before this successful validation. No failing check is reported as passed.

Machine-readable commands, counts, word counts and results: [validation_results.json](validation_results.json).
