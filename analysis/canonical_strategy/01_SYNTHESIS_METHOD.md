# Synthesis method · 13 September 2026

The supplied strategy handover was used as the task brief in the context of Gary's request to proceed. Its examples were not evidence, its model suggestion did not authorize changing settings, and generic theory was not imported into match conclusions.

## Input gate

Read `03_READINESS_REPORT.md` and `01_DATA_QUALITY_REPORT.md` first. Both describe **READY_WITH_KNOWN_GAPS**. Read-only checks independently reconciled 487 valid matches, 468 assigned records, 49 homogeneous matchup files and 19 unresolved records. Match IDs are unique and round results reconcile. These checks supported proceeding; no preprocessing blocker required stopping synthesis.

The actual input is `analysis/prepared_corpus`, as recorded in its readiness report. The path in the request used different underscore/separator placement. No alternate corpus was substituted.

## Important limits retained

- All 468 resolved records are Shadow Priest/Subtlety Rogue. Across the entire valid corpus, 484 friendly labels are Shadow/Subtlety and 3 are Priest/Subtlety with unknown Priest spec. There is **no identified Discipline Priest/Subtlety Rogue evidence**.
- Dedicated Priest and Rogue role fields are empty in every record. A few explicit narrative actor observations support limited role guidance; otherwise responsibility is unknown.
- “Observed” means reported by the source extraction, not independently rewatched in this stage. Source objectives, win conditions, conversions and failures remain source interpretations where not directly corroborated by observations.
- Quality flags affect 135/487 records, including 55 `truncated_evidence` flags and 117 source-exception flags. These categories overlap. Source confidence is not canonical strategy confidence.
- September 11 V6 is a repair without reopening videos. It contributes much of Hunter/Discipline evidence; macro announcements, temporary DEAD displays and post-round health resets need particular care.
- The footage is a selected sample with repeated batches and sometimes repeated opponents. Its W/L is not a prediction of ladder performance or an unbiased causal comparison.

## Deterministic facts and small reporting corrections

The prepared statistics are preserved verbatim inside each object. The synthesis computes separate analysis distributions by win, loss and unknown result. Class-only/prose targets are mapped only to a unique **already identified enemy member**, with an explicit reconciliation record. No unknown specialization is guessed, no pet is promoted to a player target, and no original file is rewritten.

The preparation counts 398 non-null kill labels across all valid records, but 11 explicitly mean no enemy kill. Nine of those are in resolved groups; the analysis view removes those nine from identified-player-kill counts. The read-only view also reconciles 142 class/prose target labels in resolved groups. “Unknown or no enemy kill” is deliberately not a player target.

Opening labels can denote early chip, attempted absorbed pressure, or first sustained engagement. The source sometimes explicitly qualifies them. Therefore opener frequencies describe the **recorded label**, with that limitation, rather than a perfectly harmonized first-damage event definition. The source observations/qualifications are retained.

Resources copied from two source lists duplicate 805 exact entries across the valid corpus. Each exact label is counted at most once per match in the retrieval facts. Text mentioning a resource, CC or reset is not equivalent to a confirmed use, causal requirement or completed reset. Lexical mention counts and reset-text coverage are labeled accordingly. Reliable exhaustive positive-event/reset rates are **unknown**, rather than invented from text matching.

## Review and inference

1. Orient from deterministic group sizes and quality coverage.
2. Validate the representation on the 80-game Warrior/Holy group, 8-game Warlock/Elemental group and 2-game Ret/Shadow group. Retain the three serialized examples and the adversarial review.
3. Review every resolved matchup's observations and conversion evidence, including losses and the one unknown-result record. Consult recovery and failure narratives to distinguish repeated attempts, target switches, trades, and unsupported intent.
4. Compare candidate single-target explanations with complete win/kill endpoint counts. Test stronger resource/control prerequisites against explicitly ready resources, early control endings and losses after extraction. These comparisons do not prove causality.
5. Keep one flexible default where defensible, supported branches or adaptations, and unknown selection triggers. A descriptive endpoint deviation is not automatically an opponent mistake or an execution error.
6. Retain full match references, representative examples, strongest challenges, and per-match descriptive assessments. Narrative sequences are interpreted by reviewing chronology; no keyword counter manufactures a CC chain.
7. Freeze the initial serialization after the three-case check, then emit all 49 objects/cards. Keep the 19 composition-unresolved records separate.

Default-target guidance is withheld if the labeled opener is tied or below 60% of all group records. This is an editorial display rule, not a statistical confidence interval. For this edition, groups of three or fewer games are insufficient for a reusable default. Four-game groups can carry low-confidence tentative patterns when the reviewed evidence supports them. Larger samples remain low where source concentration, mixed lines or missing comparisons limit conclusions. Six groups merit medium confidence; none merit high confidence.

## Evidence language and negative evidence

Observed: a reported health, control, resource or death state with source traceability. Inferred: its possible strategic purpose or a recommended interpretation. Pattern: a repeated descriptive observation, with complete counts when available. Unknown: insufficient evidence.

An event not mentioned is **unknown**, not absent or ready. Explicit ready Trinket icons are stronger counterexamples than silence about Trinket. A Blind macro is not a landed Blind. A name on a selected target is not proof of a damage switch. A buff/disarm is not automatically incapacitation. Zero displayed health is not always confirmed death. A confirmed kill can occur after a friendly death and can still lose the round.

The Berserker Rage example is retained as **unknown strategic relevance** against Arms/Holy. It has no place in the concise plan based on the current evidence.

## Contract and reproducibility

`strategies.json` is the application entry point; `matchup_index.json` lists the 49 objects/cards and explicitly marks Discipline/Subtlety as lacking evidence. `evidence_matches.json` is a local evidence registry; `contradiction_index.json` links challenges to candidate rules. No webapp or addon was built.

The prepared corpus has no supplied semantic version. Its identity is the SHA-256 of `normalized_matches.jsonl`, backed by fingerprints of every prepared file. Version 1 objects are provisional or insufficient, never silently treated as approved. `VALIDATION.json` records the fresh structural, count, reference and input-integrity checks. No footage or live-game validation is claimed.
