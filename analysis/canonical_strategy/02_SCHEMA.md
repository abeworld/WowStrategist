# Canonical strategy contract · 1.0.0

The schema was first exercised on Warrior/Holy Paladin (80 games, multiple conversions), Destruction Warlock/Elemental Shaman (8 games, a repeated Shaman finish), and Retribution Paladin/Shadow Priest (2 games, insufficient evidence). Their serialized examples are retained in `schema_validation/`. The serialization is frozen for this initial package; strategy content remains provisional.

`strategies.json` is an envelope with `schema_version`, `package_version`, `created_date`, `prepared_corpus_version`, and `strategies`. Individual objects are also stored under `strategies/<strategy_id>.json`. `strategy.schema.json` describes an individual object.

| Field | Meaning |
|---|---|
| `strategy_id`, `strategy_key`, `version` | Versioned identity includes **our composition and enemy composition**. `SPR` means Shadow Priest/Subtlety Rogue, not Discipline. |
| `status` | `provisional` or `insufficient_evidence`. No entry is represented as human-approved. |
| `evidence` | Sample/result counts, confidence, all match IDs, cited support, challenges and representative examples. |
| `facts` | Recomputed target distributions by result, endpoint sequences, coverage and labeled search aids. |
| `hypotheses` | Candidate explanations, disposition, support and challenges. |
| `default_line` | Opening target, objective, relevant resources, conversion state, its manufacture, conversion and recovery. |
| `states` | Team objective and separate Priest/Rogue instructions for opening, pressure, conversion and recovery. |
| `branches` | Trigger, response, evidence, classification and state references. An adaptation is not automatically a new default. |
| `failure_modes` | Evidence-grounded failure descriptions, separately labeled as interpretation. |
| `runtime_observability` | Unvalidated automatic event candidates, possible manual confirmations and knowledge suitable only for the web. |
| `uncertainties`, `mechanics_context` | Unresolved questions; external mechanics are empty in this edition. |
| `provenance`, `version_history` | Input snapshot hash, matchup/review files and changes from prior versions. |

Every strategic claim uses `text`, `basis`, `confidence`, `supporting_match_ids`, `contradicting_match_ids`, and `evidence_scope`. Basis is `observed`, `inferred`, `pattern`, or `unknown`; confidence is `high`, `medium`, `low`, or `insufficient`. Unknown claims explicitly say `unknown` and have insufficient confidence. Interpretations are **not** promoted to observed facts merely because several source analysts used similar wording.

`evidence_scope=cited_examples_not_exhaustive_frequency` means IDs illustrate a reviewed claim; their length is not a measured pattern prevalence. The opening-target claim and `facts` use complete group counts. `facts.opening_to_reported_enemy_kill` records only endpoints, never a proven CC chain or causal transition. W/L always means the **round** result. Enemy kills may occur after a friendly death; see the source chronology.

`evidence_matches.json` provides the complete normalized match records by ID, including separately preserved `evidence_notes.observed`, `.inferred`, `.unknown`, source hypotheses, exceptions and source paths. Review IDs such as `M321` are convenience aliases for this snapshot; application consumers should use the full namespaced match IDs. `evidence_review/match_references.json` resolves the aliases.

Some prepared target labels are class-only prose; a documented read-only analysis view maps them to a unique already-known enemy member. Pets remain distinct, and explicit “no enemy killed” entries are excluded from identified-player-kill counts. `provenance.prepared_stats` preserves original statistics and `evidence_review/target_reconciliation.json` exposes every mapping. Prepared input files were not repaired or rewritten.

Source-listed resources and lexical CC mentions are retrieval aids. They can include uncertain, negated or post-death events; their counts must not be displayed as uses, successful casts, forced resources or causal prerequisites. Recovery text presence is coverage, **not reset frequency**.

Render cards from their Markdown or the object fields. List entries with their confidence/status, expose cited matches and hypothesis challenges, and show unknown role responsibilities honestly. The empty `automatic` list means no live transition was certified; `automatic_candidates` are explicitly untested possibilities, not ready addon rules. Human interpretation must not be inferred automatically from target selection alone.

Future approved versions should receive a new versioned ID and change-history entry, preserving the earlier approved object. No website or addon is built by this package.
