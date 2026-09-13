# Readiness report

**Status: READY_WITH_KNOWN_GAPS**

## Counts

- Total candidate primary records: 489
- Valid 2v2 matches: 487
- Excluded non-2v2 / unusable: 2
- Duplicate / suspected duplicate groups: 0
- Unresolved (valid 2v2, insufficient spec for matchup key): 19
- Assigned to canonical matchup: 468
- Canonical matchup groups: 49

- Result known: 486/487
- Opening target known: 485/487
- Kill target known: 398/487
- Our composition spec-complete: 484/487
- Enemy composition spec-complete: 471/487

- Records with quality flags: 135
- Records with source exceptions attached: 117

- Provenance retained on every normalized match: True
- valid assigned + valid unresolved = valid 2v2: True (468+19=487)

## Largest matchup groups

- `Shadow Priest / Subtlety Rogue__vs__Shadow Priest / Subtlety Rogue`: 104 games (67W/37L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Arms Warrior / Holy Paladin`: 80 games (66W/14L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Discipline Priest / Feral Druid`: 31 games (29W/2L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Balance Druid / Subtlety Rogue`: 20 games (17W/3L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Arms Warrior / Restoration Druid`: 19 games (14W/4L/1 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Arms Warrior / Discipline Priest`: 18 games (16W/2L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Marksmanship Hunter / Retribution Paladin`: 17 games (12W/5L/0 unknown result)
- `Shadow Priest / Subtlety Rogue__vs__Destruction Warlock / Holy Paladin`: 16 games (15W/1L/0 unknown result)

## Known gaps

- Some enemy/our specs remain class-only (Priest/Rogue/Paladin/Warrior/Mage/Druid/Warlock spec unknown); those valid 2v2s sit in unresolved_matches.jsonl rather than a canonical matchup.
- Opening and kill targets sometimes use class-only labels (Rogue, Hunter, Priest); stats keep those distinct from spec-qualified labels.
- Kill target is unknown on a substantial minority of records (including wins without a visible DEAD frame).
- September 11 V6 is a documented repair of V5 without reopening MP4s; both files are preserved.
- Project-root first-10 January 5 file is inventoried but not double-counted.
- Exception notes are attached when a match id/filename is mentioned; free-text exceptions that do not name a match remain batch-level in the source files.

## Confirmation

No strategic synthesis was performed. Source-level hypotheses were copied, not created.
Prepared corpus path: `C:\Users\Gary Goldman\Downloads\Codex_work\Wow strategist\analysis\prepared_corpus`
