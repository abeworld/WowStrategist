# Preparation method

This corpus is a mechanical merge of existing extraction artifacts. No new visual analysis and no strategic synthesis were performed.

## Ingestion

1. Inventory every file under `analysis/` plus leftover project-root extraction files.
2. Treat each batch `records/matches.jsonl` as primary, except September 11 where `matches_v6.jsonl` is primary.
3. Attach companion CSV/exception/validation/manifest files as provenance. Exception markdown lines that name a match id or clip are copied onto that record.
4. Do not ingest project-root `matches.jsonl` as additional games.

## Identity

`match_id = {analysis_batch_folder}__{original_match_id}`

Clip names like `match_001.mp4` repeat across VODs, so batch prefix is required.

## Normalization

- Strip parenthetical player names from composition strings.
- Map known spec aliases to canonical spec names.
- Do **not** upgrade class-only or `spec unknown` labels to a guessed spec.
- For matchup keys, sort the two members of each team alphabetically so `Holy Paladin / Arms Warrior` and `Arms Warrior / Holy Paladin` are the same matchup.
- Preserve `raw` and `normalized` for compositions and targets.
- `win_condition`, `initial_objective`, `conversion` remain source-level inference fields.

## Eligibility

Valid 2v2 requires two friendly members and two enemy members, neither enemy member `unknown`.
Unopposed/aborted rounds, one-visible-enemy rounds, and explicit non-2v2 notes are excluded from matchup statistics but kept in `excluded_records.jsonl`.

## Merge / conflict

CSV `result` is compared to JSONL `result`. Mismatch → `result_conflict` and both values stored. No strategic tie-break.

## Statistics

Counts are computed in code from normalized records. Opening/kill distributions use the known denominator only (`opening_target_known` vs `opening_target_unknown`).
