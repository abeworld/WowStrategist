# Shadow Priest / Subtlety Rogue vs Arms Warrior / Holy Paladin — targeted v2 review

Reviewed all **80 matches (66 wins, 14 losses)** from this key; overall confidence remains medium, status provisional. The source extraction was read, not independently verified against footage. The recorded Arms Warrior opener appears in **69/80 matches**. The semantic ledger contains **52/69 damage-opening matches with a healer branch**, and **17/69 with no established healer damage branch**; these are action classifications with chip/absorbed/utility qualifications, not deterministic facts about intent. In the mirror, the narrative-qualified opener set differs from the label set; the identical totals do not imply identical membership.

All count numerators and denominators have full match-ID sets in [review statistics](review_statistics.json); every family also has exact window references and source-batch counts in [sequence counts](sequence_counts.json). Aliases such as M026 resolve through the copied [match reference map](../evidence_review/match_references.json); the [decision ledger](decision_ledger.jsonl) retains exact source pointers, original notes, unknowns, exceptions and per-match reasoning.


## Candidate comparison and resulting default

The strongest account is a Warrior opening that has real kill value and frequently develops into repeated Paladin commitments. This is more specific than “develop pressure,” but narrower than a fixed plan to kill Paladin in every game. The strongest alternative is primarily Warrior pressure with opportunistic healer swaps. The actions alone cannot fully distinguish those intentions: the extraction seldom contains a plan stated before combat. The candidate therefore keeps Warrior as the default start, makes the control-and-Paladin continuation explicit, and retains substantial Warrior attacks as a real alternative.

M048 is particularly useful: sustained Warrior damage begins under Sap, both opponents spend escapes only near the death, and immediate Paladin Horror supports the direct Warrior finish. M322 instead shows repeated Warrior health deficits through healing, then a renewed stun and confirmed Kick. These are deliberate damage sequences, not residual kill-target labels. M026 provides the competing arc: Warrior pressure and escape expenditure, a deep Paladin attempt answered by unidentified protection, a Warrior return/recovery, then renewed Paladin damage with Warrior Blind extended by Sap. Its first failed healer attempt remains visible alongside the later finish.

The observed continuation across the whole group matters more than whether every winning endpoint matches the opening target. The frequency tables count actions and preceding reviewed episodes, including losses and recoveries inside wins. They do not estimate which plan is globally best.

## What exists before the choice

The first-switch table concerns only damage-opening games with a reviewed healer branch. It distinguishes each enemy's escape separately and uses the first meaningful Paladin episode, rather than the eventual kill. “Spent during” is evidence about that episode; it does not certify that the escape was available throughout the preceding decision interval. Unknown entries remain unknown.

M131 gives a useful pre-action sequence: Warrior has healed, the friendly Rogue recovers, Warrior is re-Sapped, and Paladin becomes the damage target. M046 has Warrior Blind/Sap before the later healer commitment. By contrast, in M006, M342 and M479 the later confirmed Blind begins after the target has already changed. It can support the attempt without being the preceding selection trigger. M056's Warrior Gouge ends before the shallow Paladin damage; a Blind announcement does not fill that gap.

M090 is the strongest check on a simplistic resource selector. After Shield ends, Paladin still lacks its escape and Warrior is controlled, yet damage stays on recovered Warrior. M079 also obtains late escapes without a completed Paladin return while friendly survival deteriorates. These are not automatically player errors or evidence that Paladin was accessible. They show that the extracted resource state alone cannot choose the branch. The revised card exposes that unresolved priority instead of replacing it with “Paladin becomes the target.”

## Resource advantage, protection and recovery

Warrior escape use is relevant to keeping later control in place, while Paladin escape use is relevant to renewing healer stuns/control. They are different interactions. In M321 the fresh Warrior escape and friendly First Aid precede the final healer commitment; Paladin has recovered its escape and spends it during that attempt, followed by renewed Kidney and Silence. M122 likewise finishes Paladin after its escape has returned. M032 starts its final window with Warrior controlled, then Warrior's escape becomes ready before Paladin dies. These timings preserve the setup's possible value without inventing a mandatory unavailable state through death.

Confirmed Shield is distinct from an unidentified immunity-like display. M026's long protection remains unnamed. M032 and M039 contain Mass Dispel attempts without demonstrated early removal. M046 records casts followed by early Shield disappearance, but the refinement does not independently verify the cause. The actionable response supported by several narratives is to pressure Warrior or stabilize during protection, then build fresh control for a renewed Paladin attempt. Continuing after protection ends also occurs. No single reset choice is established as compulsory.

Blind, Sap, Fear, Gouge and stuns retain their own timings. A later Sap is not silently renamed Fear; an expired Blind is not continuous coverage. M444 explicitly leaves Warrior anti-control identity unresolved, so no Berserker Rage requirement is assigned. Friendly Priest Mind Control in M066/M076 and Rogue target/stun work in M180/M186 recover some actor-specific responsibilities, but do not establish a universal rotation.

## Failures, concentration and change from v1

The losses include healer attempts restored by protection or healing, shallow attempts without sustained damage, and friendly survival ending before another go. M052 and M475 show resource progress followed by nonconversion; M328 shows repeated restoration and recovered escapes in a long game. M053 kills Paladin before losing both friendly players. M324 instead trades both Priests simultaneously and wins a separate Rogue/Warrior duel. Neither should be summarized simply as a successful intact-team healer plan.

The family and batch table shows whether the patterns extend beyond the largest source batch. Repetition is explicitly visible within the data: M321/M322 name the same opponents, M046/M048 name the same opponents, and M335 identifies its opponents as those from the preceding clip. Thus even cross-file examples are not automatically independent opponents. Batch titles are labels, not verified gameplay dates.

V1 correctly challenged universal prerequisites, but its general win-condition language did not specify the repeated manufacturing sequence. V2 keeps that caution while naming the Warrior opening, the control-and-healer line, immediate recontrol after a spend, and protection/recovery responses. Overall confidence remains medium and status provisional. The unresolved question is the pre-choice preference between another Warrior attempt and the first or next Paladin commitment, especially when both appear possible.

## Sequence families and coverage

Families overlap within a match. Windows are reviewed analytical episodes, sometimes a collapsed series; **exact attempt counts are unknown**. Local outcomes below count those windows, while W/L counts distinct matches containing the family. Neither is an estimate of ladder performance. D is post-first-death continuation; X is unclassified/utility uncertainty. Later episodes with unresolved friendly death order have unknown phase and are not certified intact-team kills.

| Family | Operational definition | Matches / group | Reviewed episode windows | Round W/L | Source batches | Local episode outcomes |
|---|---|---:|---:|---|---:|---|
| W | Warrior attack before a substantive Paladin commitment | 69/80 | 81 | 59/10 | 11 | escape_spend: 14, recovered: 30, enemy_kill: 17, continued_pressure: 19, protection_response: 1 |
| P | Paladin damage commitment following Warrior pressure | 57/80 | 64 | 44/13 | 11 | protection_response: 28, recovered: 12, unknown_ending: 1, continued_pressure: 1, escape_spend: 3, no_kill: 4, enemy_kill: 12, friendly_death: 2, trade: 1 |
| R | Return to Warrior after a substantive Paladin commitment | 45/80 | 59 | 33/12 | 10 | enemy_kill: 10, continued_pressure: 12, recovered: 19, escape_spend: 8, friendly_death: 10 |
| H | Paladin opening damage commitment | 11/80 | 11 | 7/4 | 4 | continued_pressure: 6, protection_response: 2, escape_spend: 1, recovered: 2 |
| I | Paladin recommit after a recorded protection response | 27/80 | 27 | 23/4 | 10 | enemy_kill: 16, friendly_death: 1, recovered: 6, escape_spend: 2, protection_response: 1, continued_pressure: 1 |
| B | Renewed Paladin attack without a newly established protection interval | 13/80 | 16 | 10/3 | 7 | enemy_kill: 10, protection_response: 3, recovered: 1, escape_spend: 1, no_kill: 1 |
| D | Post-first-death continuation | 4/80 | 4 | 1/3 | 3 | friendly_death: 1, protection_response: 1, enemy_kill: 1, recovered: 1 |

The dominant source batch in the whole group is january_4th_2700_20260913 (25/80 matches). Family-specific distribution remains in the sidecar so the dominant batch can be excluded without treating remaining batches as independent opponents.

### First healer-choice context

This table counts one first healer episode per annotated damage-opening game that takes that branch. **It excludes later returns and the games with no healer branch.** It is not a frequency of all possible switch opportunities. Each cell has its own full supporting ID set in review statistics. “No deep prior attempt” is not proof that no chip damage ever healed; “unknown” is not absence.

| Field | Reviewed state counts (common denominator shown in each cell) |
|---|---|
| damage opponent trinket at first healer commitment | coincident: 1/52; ready: 7/52; spent_before: 27/52; spent_during: 4/52; unknown: 13/52 |
| healer trinket at first healer commitment | ready: 9/52; spent_before: 24/52; spent_during: 6/52; unknown: 13/52 |
| substantive damage opponent pressure healed before switch | no_deep_prior_attempt: 16/52; unknown: 15/52; yes: 21/52 |
| partner control timing | after_switch: 10/52; before_switch: 15/52; ended_before_switch: 2/52; overlap_order_unknown: 14/52; unknown: 11/52 |

Phase coverage of reviewed episode windows: intact_2v2=151, unknown=107, post_first_death=4. These are windows, not games or exact attempts. See first-death classifications for match-level outcome ordering.
