# February 3rd stream batch: exceptions and uncertainty

Raw V6 extraction only. All 28 MP4s were reviewed for format and embedded games. Twenty-three normal 2v2 engagements are retained as flat game records: 21 analysed/high confidence and two uncertain/medium confidence. Recorded outcomes are 21 wins, one inferred loss and one unknown result. These are coverage counts, not matchup strategy conclusions.

## Scope exclusions

`match_024.mp4` through `match_028.mp4` contain 3v3 games, confirmed by three friendly players, three enemy arena frames and/or the rated 3v3 entry display. Full-duration classification scans found no embedded 2v2 engagement. These five files are `ignored_non_2v2` in the manifest and have no JSONL records. No abnormal/unopposed 2v2 game was found.

## Material uncertainties

| Source | Uncertainty and handling |
| --- | --- |
| match_014.mp4 | Ends during active combat with all four players alive. Result and eventual kill target are unknown. The following source has different opponents and does not resolve the outcome. Retained as uncertain/medium; not counted as a win or loss. |
| match_017.mp4 | Friendly Rogue dies around 240s while Priest and both enemies remain alive; arena exit follows. Loss is inferred without a final defeat banner. Repeated enemy recovery, friendly low health and low Priest mana support `survival_failed`; no single execution error is proven. Later chat reports lag, but its causal effect is unknown. Retained as uncertain/medium, with medium loss information value. |

## Preserved exceptions and decisive resource states

These are individual-game observations, not general prerequisites or matchup rules.

- **001:** Warrior's earlier Trinket recovers before the last Druid attack; its second spend around 186.5s, rather than the earlier spend, supports the final Blind window.
- **006:** Warrior Trinket becomes available again just before Paladin death. The Paladin kill cannot be described as requiring Warrior Trinket to remain unavailable throughout conversion.
- **007–008:** The opposing Priest can heal during the finishing damage. Final healer CC is not established; later control cannot retrospectively explain the first kill. No Ice Block or Priest Trinket spend is confirmed in 008.
- **011:** Druid's preceding control expires before death and friendly Rogue is Cycloned near the kill. Continuing Priest pressure is visible; the exact killing spell is unresolved.
- **012:** Warrior Trinket remains available at the decisive Warrior kill. Druid control has also just expired; earlier control is preserved separately from the actual death moment.
- **018:** Mass Dispel is followed by early removal of Paladin Divine Shield. Warrior Hand of Protection persists until approximately 94s; do not describe it as removed by the same cast.
- **019:** Death Knight magic protection is visible, but the exact ability is unknown. Paladin leaves while Death Knight remains alive; departure is distinguished from a Paladin kill. Both opponents participated in normal combat before departure.
- **021:** Druid remains free and has Trinket available at Warrior death. The subsequent Fear lands after that death.
- **023:** Both enemy Trinkets remain available. Druid control expires before the kill; Warrior Sap continues through it. Druid partially recovers before renewed damage finishes him.

## Review limits and boundaries

Preparation and full-duration classification were scanned at approximately four-second intervals; active valid 2v2 combat at one-second intervals; important decisive windows at approximately half-second intervals. Supporting timestamps are approximate and relative to the named clip. Frame sampling does not provide a complete combat log. An unconfirmed macro announcement is treated as an attempt, not a landed effect.

Following-game preparation in 004 overlaps 005 and is not a second distinct game record. Loading, city footage and unused preparation at clip edges do not become game records. Existing older analysis files and corpora were preserved; the new batch is stored separately.
