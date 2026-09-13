# Canonical strategy corpus · version 1.0.0

Created 13 September 2026. **49 matchup objects and cards cover all 468 composition-resolved games.** Another 19 valid games remain separate because compositions are unresolved.

**26 provisional strategy interpretations:** 6 medium confidence and 20 low confidence. **23 insufficient-evidence cards.** No high-confidence or human-approved strategies are claimed.

All resolved evidence is **Shadow Priest / Subtlety Rogue**. There is no identified Discipline Priest / Subtlety Rogue sample, so no Discipline strategies were inferred.

[Read all matchup cards](ALL_MATCHUP_CARDS.md) · [Review queue](03_REVIEW_QUEUE.md) · [Machine-readable strategies](strategies.json) · [Contract](02_SCHEMA.md) · [Verification](VALIDATION.json)

## Evidence and limits

- Input gate: READY_WITH_KNOWN_GAPS; independent count/group checks passed.
- Valid corpus: 487 games, 394 wins / 92 losses / 1 unknown result. Resolved subset: 468 games, 378 wins / 89 losses / 1 unknown result.
- Original VODs were not reopened. Source extraction uncertainty, repaired records, repeated opponents and selected footage limit interpretation.
- Dedicated role fields are empty; Priest/Rogue guidance is mostly unknown. A few explicit friendly-actor narratives support limited guidance.
- Read-only target reconciliation and removal of explicit non-kill labels are documented; input files remain unchanged.
- Automatic addon detection is untested. Strategies are independent of runtime feasibility.

## Strongest repeated findings

- [Arms Warrior / Holy Paladin](cards/SPR_vs_Arms_HPal_v1.md): Warrior is the labeled opener in **69/80** games. The 66 wins include **38 Paladin kills, 27 Warrior kills and 1 unconfirmed kill**. Use a flexible pressure/conversion line; neither a compulsory Paladin swap nor double-Trinket removal fits all wins.
- [Shadow/Subtlety mirror](cards/SPR_vs_SP_Sub_v1.md): Rogue is the labeled opener in **76/104** games, but the 67 wins split into **32 Rogue kills, 29 Priest kills and 6 unconfirmed kills**. Both conversion targets recur; survival and actual health pressure matter more than an assumed fixed target.
- [Discipline Priest / Feral Druid](cards/SPR_vs_Disc_Feral_v1.md): Feral is opened in **25/31** games; the 29 wins finish **18 Ferals and 11 Priests**. Renewed Feral pressure and a supported healer-switch option both belong in the model.
- [Destruction Warlock / Elemental Shaman](cards/SPR_vs_Destro_Ele_v1.md): all **7 wins** identify Shaman as the enemy killed. This is the clearest repeated kill-target pattern among the three validation cases, but the single loss cannot establish causality or resource prerequisites.
- [Discipline Priest / Subtlety Rogue](cards/SPR_vs_Disc_Sub_v1.md): **6/9** games open Priest while **8/9** wins identify Rogue as the enemy killed. Opening target and eventual kill target must remain separate.
- Across several matchups, a first low-health attempt heals back before a later conversion. “Reset” often means stabilization and renewed pressure, not necessarily a full stealth disengage.
- Confirmed kills occur in losses, and some wins have no confirmed death. The round result and individual kill evidence are never treated as interchangeable.

These counts describe selected records, not expected win rates, conditional kill probabilities or proof of strategic intent. [Method and limitations](01_SYNTHESIS_METHOD.md) · [Ordered examples](04_SEQUENCE_REVIEW.md).

## Highest-value Gary review

Start with [Arms Warrior / Holy Paladin](cards/SPR_vs_Arms_HPal_v1.md), [the mirror](cards/SPR_vs_SP_Sub_v1.md), [Arms Warrior / Restoration Druid](cards/SPR_vs_Arms_RDruid_v1.md), and [Balance Druid / Subtlety Rogue](cards/SPR_vs_Balance_Sub_v1.md): large or important samples still leave target-selection triggers unresolved. Then review pet/player timing against [Destruction Warlock / Holy Paladin](cards/SPR_vs_Destro_HPal_v1.md) and [Destruction Warlock / Restoration Shaman](cards/SPR_vs_Destro_RSham_v1.md), and the repaired evidence concentration in [Discipline Priest / Marksmanship Hunter](cards/SPR_vs_Disc_MM_v1.md).

**Berserker Rage remains of unknown strategic relevance against Arms/Holy and is omitted from the concise plan.**

## Coverage

| Enemy composition | Games | W/L/? | Confidence | Status |
|---|---:|---:|---|---|
| [Shadow Priest / Subtlety Rogue](cards/SPR_vs_SP_Sub_v1.md) | 104 | 67/37/0 | medium | provisional |
| [Arms Warrior / Holy Paladin](cards/SPR_vs_Arms_HPal_v1.md) | 80 | 66/14/0 | medium | provisional |
| [Discipline Priest / Feral Druid](cards/SPR_vs_Disc_Feral_v1.md) | 31 | 29/2/0 | medium | provisional |
| [Balance Druid / Subtlety Rogue](cards/SPR_vs_Balance_Sub_v1.md) | 20 | 17/3/0 | low | provisional |
| [Arms Warrior / Restoration Druid](cards/SPR_vs_Arms_RDruid_v1.md) | 19 | 14/4/1 | low | provisional |
| [Arms Warrior / Discipline Priest](cards/SPR_vs_Arms_Disc_v1.md) | 18 | 16/2/0 | low | provisional |
| [Marksmanship Hunter / Retribution Paladin](cards/SPR_vs_MM_Ret_v1.md) | 17 | 12/5/0 | medium | provisional |
| [Destruction Warlock / Holy Paladin](cards/SPR_vs_Destro_HPal_v1.md) | 16 | 15/1/0 | medium | provisional |
| [Discipline Priest / Marksmanship Hunter](cards/SPR_vs_Disc_MM_v1.md) | 13 | 11/2/0 | low | provisional |
| [Retribution Paladin / Unholy Death Knight](cards/SPR_vs_Ret_Unholy_v1.md) | 12 | 9/3/0 | low | provisional |
| [Frost Mage / Shadow Priest](cards/SPR_vs_Frost_SP_v1.md) | 11 | 11/0/0 | low | provisional |
| [Discipline Priest / Frost Mage](cards/SPR_vs_Disc_Frost_v1.md) | 9 | 9/0/0 | low | provisional |
| [Discipline Priest / Subtlety Rogue](cards/SPR_vs_Disc_Sub_v1.md) | 9 | 9/0/0 | low | provisional |
| [Destruction Warlock / Elemental Shaman](cards/SPR_vs_Destro_Ele_v1.md) | 8 | 7/1/0 | medium | provisional |
| [Enhancement Shaman / Retribution Paladin](cards/SPR_vs_Enh_Ret_v1.md) | 8 | 7/1/0 | low | provisional |
| [Balance Druid / Frost Mage](cards/SPR_vs_Balance_Frost_v1.md) | 7 | 6/1/0 | low | provisional |
| [Destruction Warlock / Restoration Shaman](cards/SPR_vs_Destro_RSham_v1.md) | 7 | 5/2/0 | low | provisional |
| [Destruction Warlock / Restoration Druid](cards/SPR_vs_Destro_RDruid_v1.md) | 5 | 5/0/0 | low | provisional |
| [Discipline Priest / Unholy Death Knight](cards/SPR_vs_Disc_Unholy_v1.md) | 5 | 5/0/0 | low | provisional |
| [Fire Mage / Subtlety Rogue](cards/SPR_vs_Fire_Sub_v1.md) | 5 | 4/1/0 | low | provisional |
| [Frost Mage / Subtlety Rogue](cards/SPR_vs_Frost_Sub_v1.md) | 5 | 4/1/0 | low | provisional |
| [Retribution Paladin / Subtlety Rogue](cards/SPR_vs_Ret_Sub_v1.md) | 5 | 2/3/0 | low | provisional |
| [Shadow Priest / Unholy Death Knight](cards/SPR_vs_SP_Unholy_v1.md) | 5 | 2/3/0 | low | provisional |
| [Arms Warrior / Retribution Paladin](cards/SPR_vs_Arms_Ret_v1.md) | 4 | 4/0/0 | low | provisional |
| [Assassination Rogue / Retribution Paladin](cards/SPR_vs_Assa_Ret_v1.md) | 4 | 3/1/0 | low | provisional |
| [Destruction Warlock / Discipline Priest](cards/SPR_vs_Destro_Disc_v1.md) | 4 | 4/0/0 | low | provisional |
| [Arcane Mage / Subtlety Rogue](cards/SPR_vs_Arcane_Sub_v1.md) | 3 | 3/0/0 | insufficient | insufficient evidence |
| [Arms Warrior / Balance Druid](cards/SPR_vs_Arms_Balance_v1.md) | 3 | 3/0/0 | insufficient | insufficient evidence |
| [Elemental Shaman / Retribution Paladin](cards/SPR_vs_Ele_Ret_v1.md) | 3 | 3/0/0 | insufficient | insufficient evidence |
| [Feral Druid / Restoration Shaman](cards/SPR_vs_Feral_RSham_v1.md) | 3 | 3/0/0 | insufficient | insufficient evidence |
| [Fury Warrior / Holy Paladin](cards/SPR_vs_Fury_HPal_v1.md) | 2 | 2/0/0 | insufficient | insufficient evidence |
| [Protection Paladin / Restoration Shaman](cards/SPR_vs_ProtPal_RSham_v1.md) | 2 | 2/0/0 | insufficient | insufficient evidence |
| [Protection Warrior / Retribution Paladin](cards/SPR_vs_ProtWar_Ret_v1.md) | 2 | 2/0/0 | insufficient | insufficient evidence |
| [Protection Warrior / Unholy Death Knight](cards/SPR_vs_ProtWar_Unholy_v1.md) | 2 | 2/0/0 | insufficient | insufficient evidence |
| [Restoration Shaman / Unholy Death Knight](cards/SPR_vs_RSham_Unholy_v1.md) | 2 | 2/0/0 | insufficient | insufficient evidence |
| [Retribution Paladin / Shadow Priest](cards/SPR_vs_Ret_SP_v1.md) | 2 | 1/1/0 | insufficient | insufficient evidence |
| [Affliction Warlock / Restoration Shaman](cards/SPR_vs_Aff_RSham_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Assassination Rogue / Discipline Priest](cards/SPR_vs_Assa_Disc_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Balance Druid / Holy Paladin](cards/SPR_vs_Balance_HPal_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Discipline Priest / Fire Mage](cards/SPR_vs_Disc_Fire_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Discipline Priest / Retribution Paladin](cards/SPR_vs_Disc_Ret_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Enhancement Shaman / Marksmanship Hunter](cards/SPR_vs_Enh_MM_v1.md) | 1 | 0/1/0 | insufficient | insufficient evidence |
| [Enhancement Shaman / Subtlety Rogue](cards/SPR_vs_Enh_Sub_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Feral Druid / Marksmanship Hunter](cards/SPR_vs_Feral_MM_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Feral Druid / Shadow Priest](cards/SPR_vs_Feral_SP_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Holy Paladin / Shadow Priest](cards/SPR_vs_HPal_SP_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Marksmanship Hunter / Protection Warrior](cards/SPR_vs_MM_ProtWar_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Marksmanship Hunter / Unholy Death Knight](cards/SPR_vs_MM_Unholy_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |
| [Protection Warrior / Restoration Druid](cards/SPR_vs_ProtWar_RDruid_v1.md) | 1 | 1/0/0 | insufficient | insufficient evidence |

## Provenance

Prepared snapshot: `sha256:90f807125699c79a984c8d4ea23ffd9aff9853cab3acc764f79694750eb9c4df`.

The complete input file fingerprints are in [input_fingerprints.json](evidence_review/input_fingerprints.json). Each strategy retains its source matchup file, original statistics, all record IDs and specific supporting/challenging examples. The 19 unresolved records remain in [unresolved_matches.json](unresolved_matches.json).
