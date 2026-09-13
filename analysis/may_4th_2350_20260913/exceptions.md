# May 4th +2350 MMR — extraction checks and exceptions

Applied the attached V6 instructions to the requested folder. The supplied path contained escaped underscores; the existing source folder is `C:\Users\Gary Goldman\Downloads\Codex_work\Wow strategist\output\2v2_SPR_+2350_MMR_May_4th_Stream_VOD_WOW_R1_Gladiator_Rogue_Arena_PVP_-_Warmane_WOTLK`. Outputs are a new batch; earlier validated corpora and videos were preserved.

## Coverage

| Check | Count |
|---|---:|
| Discovered / requested MP4 files | 65 / 65 |
| Manifest source rows | 65 |
| Valid normal2v2 games / JSONL lines | 56 / 56 |
| Analysed / uncertain / failed records | 51 / 5 / 0 |
| Ignored non2v2 / excluded abnormal2v2 | 1 / 8 |
| Recorded wins / losses | 53 / 3 |
| High / medium / low confidence | 44 / 12 / 0 |

Count reconciliation: **65 = 56 + 8 + 1**. No mismatches. One flat line per valid game. No additional completed normal2v2 game found inside a clip; late preparation and carryover are described in the manifest.

## Excluded footage

- `match_001.mp4`: 3v3, manifest only.
- `match_011`, `032`, `035`, `039`, `049`, `051`, `053`: aborted, unopposed or administratively ended before meaningful normal2v2 combat; individual reasons in the manifest.
- `match_059`: effectively one-opponent interaction before first death. The second opponent becomes visible88s, Priest dies89s, with no established normal2v2 exchange. Do not infer disconnection from absence. The opening carryover in060 is not a second game.

## Material uncertainties retained

- **015:** alternating Rogue/Mage pressure leads to both Rogues dying, then a Priest-versus-Mage continuation. The original off-target control continuity and whether its intended win condition was reached are unresolved (`null`). Mage trinket recovers before the final1v1 victory.
- **018, 043, 060:** victories are visible, but a particular first player death is not established. `kill_target=unknown`; do not infer a kill from a low-health frame or the victory announcement.
- **047:** Blind106-107s is verified, then another effect appears while Paladin Holy Light casts109-110.5s. Later control/Mind Control interpretation remains unresolved; no continuous Blind claim.
- **048, 062, 063 losses:** failure stages and enemy escape states are retained. Exact friendly defensive use/timing is unknown. Post-round chat is not treated as proof of a landed/missed ability or defensive spend.

## Evidence safeguards

Enemy offensive Blind is recorded as spent, without automatically marking it forced. Macro announcements are attempts unless the UI confirms application. Hunter apparent deaths that reverse to alive are distinguished from real deaths. Zero displayed health alone is not a death (notably061 at206s).

Earlier cooldown spends are re-evaluated at conversion, including recovered trinkets in033,044,061 and Mage recovery in015. In065 Shaman trinket recovers after Paladin death, not before it. Successful conversions with ready enemy escapes or free off-targets are preserved in their individual records; no matchup-wide prerequisite is inferred here.

Review used ~4s inactive sampling,1s active combat and targeted0.5s decisive windows, followed by all-file beginning/end review. Minor unnamed effects remain unknown. The evidence is sampled video/UI, not a combat log.

Validation checks cover source coverage, JSON parsing, consistent flat fields, unique IDs, clip bounds, forced-resource subsets, loss completeness and conversion-failure semantics. Cross-match synthesis and matchup cards remain a separate later step.
