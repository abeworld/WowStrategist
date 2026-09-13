# May 18 +2500 batch: exceptions and verification

Source folder: `2v2_SPR_+2500_MMR_May_18th_Stream_VOD_WOW_R1_Gladiator_Rogue_Arena_PVP_-_Warmane_WOTLK`.

Applied `ARENA_ANALYSIS_INSTRUCTIONS.md` V6 to raw extraction. Full clips were reviewed with one-second active-combat samples; detected decisive windows received half-second review. Preparation and loading were distinguished from combat. This is frame-based evidence, not a combat log. Times are clip-relative.

| Count check | Total |
| --- | ---: |
| MP4 files discovered | 78 |
| MP4 files requested and reviewed | 78 |
| Distinct normal 2v2 games found | 74 |
| Flat JSONL game records | 74 |
| Analysed | 57 |
| Uncertain | 17 |
| Failed | 0 |
| Ignored non-2v2 | 1 |
| Excluded abnormal/non-evidentiary 2v2 | 3 |
| Count mismatches | 0 |

Record balance: 54 wins, 20 losses; confidence 57 high, 17 medium, 0 low. These are extraction counts, not matchup-wide strategic conclusions.

Excluded footage (manifest only):

- `match_001.mp4`: 3v3 arena; three opponents established.
- `match_027.mp4`: Unopposed/aborted 2v2; no meaningful enemy combat.
- `match_028.mp4`: Unopposed/aborted 2v2; no meaningful enemy combat.
- `match_031.mp4`: Unopposed/aborted 2v2; no meaningful enemy combat.

Material uncertainties retained:

| Source | Limitation |
| --- | --- |
| `match_018.mp4` | Paladin spec is not established; failure sequence is visible. |
| `match_025.mp4` | Exact Paladin immunity/defensive combination is unresolved; the record preserves a reached window followed by conversion failure. |
| `match_026.mp4` | Exact Paladin defensive response during Hunter conversion is unresolved. |
| `match_029.mp4` | Exact Paladin defensive response is unresolved; loss is inferred from teammate death and departure. |
| `match_030.mp4` | Paladin spec and exact defensive response are unresolved. |
| `match_032.mp4` | Exact Paladin defensive identities during the renewed isolation sequence are unresolved. |
| `match_034.mp4` | Paladin spec is unknown; Rogue control and Paladin death are established. |
| `match_036.mp4` | Exact Paladin defensive response affecting recovery is unresolved. |
| `match_038.mp4` | Exact Paladin defensive response before renewed isolation is unresolved. |
| `match_040.mp4` | Exact defensive identities during repeated recovery windows are unresolved. |
| `match_042.mp4` | Exact Paladin defensive response is unresolved; Warrior is free during the final Paladin damage. |
| `match_044.mp4` | Exact Paladin defensive response is unresolved; both enemy Trinkets remain available at conversion. |
| `match_046.mp4` | Friendly Priest spec is not established from displayed casts. |
| `match_049.mp4` | Victory is established but Rogue remains displayed at 4%; no specific player death is established. |
| `match_058.mp4` | Victory is established without visible death; immediate Shaman control reapplication after Trinket is unclear. |
| `match_061.mp4` | First committed opening target is ambiguous; early Rogue chip precedes substantial Priest damage. |
| `match_075.mp4` | Paladin spec is not established in this short game; previous clips do not substitute for current spec evidence. |

Overlap handling: `match_044.mp4` 0-5s repeats the ending already recorded from `match_043.mp4`; its new game is a separate record. Next-game preparation inside clips does not create another game record. `match_072.mp4` includes preparation overlapping `match_071.mp4`, with no duplicate combat record.

Timestamp precision: existing whole-second record ends are preserved. `match_022.mp4` end 133s versus exact duration 132.850s; `match_024.mp4` end 111s versus exact duration 110.850s; `match_035.mp4` end 140s versus exact duration 139.850s; `match_036.mp4` end 101s versus exact duration 100.550s; `match_037.mp4` end 93s versus exact duration 92.650s. These subsecond rounding differences are also flagged in the manifest; no additional footage is implied.

Calibration cautions: team colors vary, so results use scoreboard/chat and friendly identities. Macro announcements establish attempts only; landed effects use UI evidence. Long buffs during visible casts are not automatically CC. Unresolved protection is not renamed Divine Shield/Hand of Protection without supporting evidence. Zero health is not automatically death; DEAD state or equivalent death evidence is required.

Successful games with an enemy Trinket still available are preserved in their individual records. Enemy offensive Blind/Bloodlust spends are separated from pressure-forced resources. Cooldowns spent after a friendly death are not retroactively unavailable at the failure point. Reached win conditions are retained in conversion-failed losses.

Verification passed: all sources covered once in the manifest; unique flat records; required fields and allowed status/confidence values; clip starts within exact durations and ends within whole-second duration rounding; forced resources are subsets of observed spends; loss fields populated; conversion-failed losses marked reached; excluded sources absent from JSONL. Record bytes were preserved during finalization. Source videos were read only. No cross-match synthesis or matchup cards were generated.
