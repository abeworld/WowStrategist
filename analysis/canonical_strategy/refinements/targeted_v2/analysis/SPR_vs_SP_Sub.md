# Shadow Priest / Subtlety Rogue vs Shadow Priest / Subtlety Rogue — targeted v2 review

Reviewed all **104 matches (67 wins, 37 losses)** from this key; overall confidence remains medium, status provisional. The source extraction was read, not independently verified against footage. The recorded Subtlety Rogue opener appears in **76/104 matches**. The semantic ledger contains **38/76 damage-opening matches with a healer branch**, and **38/76 with no established healer damage branch**; these are action classifications with chip/absorbed/utility qualifications, not deterministic facts about intent. In the mirror, the narrative-qualified opener set differs from the label set; the identical totals do not imply identical membership.

All count numerators and denominators have full match-ID sets in [review statistics](review_statistics.json); every family also has exact window references and source-batch counts in [sequence counts](sequence_counts.json). Aliases such as M026 resolve through the copied [match reference map](../evidence_review/match_references.json); the [decision ledger](decision_ledger.jsonl) retains exact source pointers, original notes, unknowns, exceptions and per-match reasoning.


## Candidate comparison and resulting default

The Rogue opener supports two recurring continuations: sustained or repeated Rogue attacks with Priest disruption, and a Priest commitment with Rogue containment. A model in which Rogue pressure only exists to manufacture a Priest kill is too narrow. So is a model that treats Priest damage as an incidental endpoint after a uniformly Rogue-focused plan. Both sequences are observed, including real returns between them. The evidence does not establish a preferred conversion from the shared opener.

M021 and M103 supply particularly clear order: enemy Rogue spends its escape, a confirmed Rogue Blind precedes the Priest switch, Priest spends during the attack, and Sap extends Rogue isolation. M337 and M421 provide direct Rogue attacks under Priest control with enemy escapes retained. M196 shows a Rogue attempt surviving a temporary avoidance/stealth interval and partial healing before continued damage finishes it. Those are useful alternative actions even without a healer switch.

The opening label is not always the first substantial commitment. M246 has early Rogue chip before the main Priest attack; its role in an opening-default statistic is qualified. In M461 the source labels Priest as opener, but its narrative shows mostly Priest control before meaningful Rogue damage. The ledger therefore keeps that initial Priest commitment unresolved rather than inventing a damage swap. Recorded labels remain unchanged in the evidence and factual distributions.

## What would select Priest rather than Rogue

The first-switch table is a complete classification of the annotated Rogue-opening games containing a real Priest branch. It is not the denominator of all opportunities the players could have taken. The distinction is decisive: a count of resource states among taken branches does not show how the same players behaved at every untaken opportunity.

M103 makes a fresh confirmed control window available before the Priest action. That is a useful way to create an option. However, M419 starts its Priest attack before the confirmed Rogue Blind; Priest first heals and spends its escape, then Blind supports the renewed attempt. M339 does not precisely establish the first Priest selection relative to the Rogue escape/Blind. The original extraction was checked and did not resolve that ordering. The new machine-readable branch therefore has an unknown selection trigger and a specific observed response, rather than the circular instruction to commit Priest because Priest has become the damage target.

The strongest alternate-response checks are M196 and M208: Rogue recovery is followed by more Rogue damage. M203 switches to Priest when Rogue is already critically low, before Binding Heal restores Rogue. A switch does not require a fully healed Rogue. M383 commits Priest while enemy Rogue is explicitly free; the Blind announcements never establish a landed effect. That is a real challenge to presenting Rogue containment as a prerequisite for every Priest attack, but does not erase its utility in the clear Blind/Sap sequences.

## Separate the enemy resources and the actors

Enemy Priest escape use can precede Rogue damage by answering opening control, or happen during a Priest commitment. Enemy Rogue escape use can precede Rogue isolation, happen during an already-started Priest attack, or belong only to cleanup. M189 and M272 place the Rogue escape after the enemy Priest death. M294 and M306 have important escape/control events after the friendly Priest has died; those events cannot manufacture the earlier intact-team plan.

The record supports a concrete protection response in M419: confirmed Dispersion stalls Priest health loss, Rogue Blind is extended by Sap, and Horror/damage after Dispersion ends precede the kill. This is one named defensive sequence, not evidence for assuming Dispersion in other blue or ambiguous icons. Enemy Hymn has several outcomes: it is interrupted in M196, partially restores Rogue without saving it in M208/M253, and accompanies a substantial recovery before another target or attack in other games. In M435 both Priests channel Hymn; friendly recovery must not be counted as an enemy resource forced by pressure.

Enemy offensive Blind remains separate from a defensive escape and from our off-target Blind. M397, M417 and M419 retain announcements whose applications are unconfirmed. Priest or Rogue selections used for interrupts/control are not automatically damage commitments, and stealth is not automatically Vanish. Explicit Rogue damage-switch narratives support a bounded responsibility, while the empty dedicated role fields and incomplete Priest cast attribution still prevent a fixed offensive Priest rotation.

## Local failure, survival and strength of the evidence

M292 has confirmed enemy Priest isolation but almost no Rogue depletion before friendly Priest death. M270 similarly has Blind/Gouge without a damaging follow-through. These failures show why landed CC alone is not the win condition. M417 and M423 instead reach very low enemy health after useful control has expired; a friendly dies before the finish. The missing defensive/readiness evidence prevents calling those outcomes a specific player mistake.

M078 reaches a low Priest under Rogue isolation but ends in a loss without an established death; it remains an unexplained termination, not a fabricated lethal trade. The ledger separately preserves wins with no confirmed enemy death, including explicit administrative endings. M294/M297 counter-kill after a friendly death and lose the duel; M306 wins after a solo counter-kill and a later duel. M426 has the friendly Priest die before enemy Rogue by about a second, then a solo win. These histories are not interchangeable with an enemy-first two-player conversion.

The two large source batches contribute heavily, as the table shows. Recurrent actions also appear outside them, but source batches are neither independent opponents nor verified gameplay dates. No plan is ranked by selected-footage win percentage. V2 strengthens the opener and both manufacturing sequences, removes the circular branch, and makes the unresolved selection criterion prominent. Overall confidence remains medium, with lower confidence in choosing between targets than in identifying the repeated actions.

## Sequence families and coverage

Families overlap within a match. Windows are reviewed analytical episodes, sometimes a collapsed series; **exact attempt counts are unknown**. Local outcomes below count those windows, while W/L counts distinct matches containing the family. Neither is an estimate of ladder performance. D is post-first-death continuation; X is unclassified/utility uncertainty. Later episodes with unresolved friendly death order have unknown phase and are not certified intact-team kills.

| Family | Operational definition | Matches / group | Reviewed episode windows | Round W/L | Source batches | Local episode outcomes |
|---|---|---:|---:|---|---:|---|
| W | Enemy Rogue attack before a substantive Priest commitment | 76/104 | 97 | 49/27 | 10 | escape_spend: 13, friendly_death: 20, recovered: 31, enemy_kill: 17, continued_pressure: 15, unknown_ending: 1 |
| P | Enemy Priest commitment following Rogue pressure | 47/104 | 51 | 36/11 | 8 | enemy_kill: 19, friendly_death: 8, unknown_ending: 3, recovered: 10, escape_spend: 4, continued_pressure: 3, no_kill: 4 |
| R | Return to enemy Rogue after Priest damage commitment | 31/104 | 36 | 27/4 | 6 | escape_spend: 2, recovered: 11, enemy_kill: 13, continued_pressure: 4, no_kill: 1, friendly_death: 2, unknown_ending: 3 |
| H | Enemy Priest opening commitment | 26/104 | 27 | 18/8 | 6 | continued_pressure: 8, recovered: 9, friendly_death: 3, escape_spend: 4, enemy_kill: 3 |
| B | Renewed enemy Priest commitment | 11/104 | 12 | 8/3 | 5 | friendly_death: 3, enemy_kill: 7, recovered: 1, protection_response: 1 |
| X | Sequence not established | 3/104 | 3 | 1/2 | 3 | friendly_death: 2, control_only: 1 |
| D | Post-first-death continuation | 25/104 | 29 | 2/23 | 6 | no_kill: 8, escape_spend: 6, recovered: 5, friendly_death: 4, enemy_kill: 5, unknown_ending: 1 |

The dominant source batch in the whole group is may_18th_2500_20260913 (30/104 matches). Family-specific distribution remains in the sidecar so the dominant batch can be excluded without treating remaining batches as independent opponents.

### First healer-choice context

This table counts one first healer episode per annotated damage-opening game that takes that branch. **It excludes later returns and the games with no healer branch.** It is not a frequency of all possible switch opportunities. Each cell has its own full supporting ID set in review statistics. “No deep prior attempt” is not proof that no chip damage ever healed; “unknown” is not absence.

| Field | Reviewed state counts (common denominator shown in each cell) |
|---|---|
| damage opponent trinket at first healer commitment | ready: 2/38; spent_before: 18/38; spent_during: 6/38; unknown: 12/38 |
| healer trinket at first healer commitment | coincident: 1/38; ready: 2/38; spent_before: 20/38; spent_during: 13/38; unknown: 2/38 |
| substantive damage opponent pressure healed before switch | no_deep_prior_attempt: 14/38; unknown: 10/38; yes: 14/38 |
| partner control timing | absent_as_recorded: 1/38; after_switch: 6/38; before_switch: 10/38; overlap_order_unknown: 3/38; unknown: 18/38 |

Phase coverage of reviewed episode windows: intact_2v2=161, unknown=65, post_first_death=29. These are windows, not games or exact attempts. See first-death classifications for match-level outcome ordering.
