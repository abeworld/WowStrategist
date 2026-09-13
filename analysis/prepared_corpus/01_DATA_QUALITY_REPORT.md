# Data quality report

Valid 2v2 matches ingested: **487**
Assigned to canonical matchup: **468**
Valid but unresolved matchup: **19**
Excluded / unusable: **2**
Duplicate-candidate groups: **0**

## Validation checks

- `unique_match_ids`: **True**
- `matchup_files_homogeneous`: **True**
- `non_2v2_excluded_from_stats`: **True**
- `win_loss_reconcile`: **True**
- `opening_target_reconcile`: **True**
- `kill_target_reconcile`: **True**
- `every_match_has_provenance`: **True**
- `originals_unmodified`: **True**
- `valid_assigned_plus_unresolved_equals_valid`: **True**

## Exclusion reasons

- cannot establish 2v2: 1
- unopposed/aborted arena instance: 1

## Quality flag frequencies (valid 2v2)

- source_exception_present: 117
- truncated_evidence: 55
- weak_spec_identification: 19

## Known gaps

- Some enemy/our specs remain class-only (Priest/Rogue/Paladin/Warrior/Mage/Druid/Warlock spec unknown); those valid 2v2s sit in unresolved_matches.jsonl rather than a canonical matchup.
- Opening and kill targets sometimes use class-only labels (Rogue, Hunter, Priest); stats keep those distinct from spec-qualified labels.
- Kill target is unknown on a substantial minority of records (including wins without a visible DEAD frame).
- September 11 V6 is a documented repair of V5 without reopening MP4s; both files are preserved.
- Project-root first-10 January 5 file is inventoried but not double-counted.
- Exception notes are attached when a match id/filename is mentioned; free-text exceptions that do not name a match remain batch-level in the source files.

## Automated validation blob

```json
{
  "unique_match_ids": true,
  "matchup_files_homogeneous": true,
  "non_2v2_excluded_from_stats": true,
  "win_loss_reconcile": true,
  "opening_target_reconcile": true,
  "kill_target_reconcile": true,
  "every_match_has_provenance": true,
  "originals_unmodified": true,
  "valid_assigned_plus_unresolved_equals_valid": true,
  "counts": {
    "inventory_files": 63,
    "candidate_primary_records": 489,
    "valid_2v2": 487,
    "assigned_matchups": 468,
    "valid_unresolved": 19,
    "excluded": 2,
    "duplicate_candidate_groups": 0,
    "canonical_matchup_groups": 49
  }
}
```
