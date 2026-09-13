# Targeted strategy refinement — candidate package 1.1.0

Three strategies have material v2 revisions. They remain provisional at medium overall confidence. All 215 scoped records, including all 53 losses, have an individually authored decision-ledger entry. The other 46 strategy objects and cards are unchanged; no full-corpus strategic reanalysis was performed.

## Arms Warrior / Holy Paladin

**Evidence:** 80 games · 66W/14L/0 unknown · medium confidence · provisional · v2  
**Start:** Warrior, with Paladin Sap/control.  
**Objective:** Threaten a Warrior finish and draw escapes while building a later Paladin commitment.  
**Win condition:** Paladin stun/damage with Warrior contained; protection may require another attempt.  
**Create it:** Warrior pressure → fresh Warrior control → Paladin stuns/damage; track each current Trinket.  
**Convert:** After Warrior escape use, renewed control supports a Paladin go. Renew Paladin control after its escape.  
**Alternative:** Continue Warrior through partial heals; renew stuns and interrupt Paladin healing.  
**Failure:** Protection or healing can erase the healer attempt before friendly survival allows another.  
**Reset:** On Shield, pressure Warrior or stabilize; rebuild control for a post-immunity Paladin return.  
**Unresolved:** What makes the first Paladin go preferable to renewed Warrior pressure remains unknown.  

[Full card](cards/SPR_vs_Arms_HPal_v2.md) · [Analysis](analysis/SPR_vs_Arms_HPal.md)

## Shadow Priest / Subtlety Rogue

**Evidence:** 104 games · 67W/37L/0 unknown · medium confidence · provisional · v2  
**Start:** Enemy Rogue, with enemy Priest Sap/control.  
**Objective:** Threaten Rogue while drawing escapes that can also enable a controlled Priest attack.  
**Win condition:** Rogue damage with Priest disrupted, or Priest damage with Rogue contained.  
**Create it:** Build Rogue pressure; after its escape, confirmed Blind → Priest attack → Sap is a recurring sequence.  
**Convert:** That Priest line is a documented option; its priority over renewed Rogue damage is unknown.  
**Alternative:** Stay Rogue through partial heals; renew Priest control or interrupt healing. Priest-first also occurs.  
**Failure:** Friendly Priest death can end the team attempt before or after escape extraction.  
**Reset:** Survive countercontrol, rebuild damage/control, and distinguish a trade or solo continuation from a two-player finish.  
**Unresolved:** No reliable pre-choice rule selects Priest over Rogue from the recorded states.  

[Full card](cards/SPR_vs_SP_Sub_v2.md) · [Analysis](analysis/SPR_vs_SP_Sub.md)

## Discipline Priest / Feral Druid

**Evidence:** 31 games · 29W/2L/0 unknown · medium confidence · provisional · v2  
**Start:** Feral, with Priest control; keep attacking through initial absorbs.  
**Objective:** Build repeated Feral attacks with renewed healer disruption.  
**Win condition:** Feral remains damaged into renewed stuns, or Priest takes damage while Feral is contained.  
**Create it:** Renew Feral stuns with Priest Gouge/Silence/Fear; track each escape separately.  
**Convert:** Repeat Feral after partial heals. Fresh Feral control supports a documented Priest alternative.  
**Alternative:** Feral escape → Blind/Sap → Priest occurs; short Fear/stun swaps also occur with escapes retained.  
**Failure:** Two losses: stalled attacks and friendly collapse; one Priest attempt is interrupted by Cyclone.  
**Reset:** Recover and rebuild an attack after healing or Cyclone; resumed Feral pressure is documented.  
**Unresolved:** A healed Feral does not select the Priest switch; its priority remains unknown.  

[Full card](cards/SPR_vs_Disc_Feral_v2.md) · [Analysis](analysis/SPR_vs_Disc_Feral.md)

## What changed

The revision separates a common opener, its inferred purpose, actual attempted sequences, and a preceding target-choice trigger. Warrior/Paladin now exposes the recurring control-and-healer line alongside real Warrior attacks. The mirror retains two Rogue-opening continuations and an explicitly unknown target-choice rule. Feral now has a repeated Feral line plus concrete Feral-control/Priest alternatives; healing recovery alone is not a switch signal. JSON defaults, resources, states, branches, hypotheses, match assessments and failures agree with the cards.

Both enemies' escapes are reviewed separately in the first healer-branch tables. Recovered cooldowns, control before versus after selection, failed attempts inside wins, ambiguous protection and actor ownership are preserved. A brief ambiguous Priest episode in M398 is excluded from established Priest-switch counts. Recorded opening labels, including M461, are unchanged even where narrative-qualified commitments differ.

All source evidence is unchanged. Evidence and unresolved copies are byte-identical; the prepared-corpus identifier and schema 1.0.0 remain fixed. There are 49 current entries, 26 provisional and 23 insufficient-evidence; none is approved. The friendly Discipline Priest/Subtlety Rogue composition remains no_evidence. Historical v1 universal challenges are separately scoped rather than reused as contradictions to qualified v2 defaults.

## Coverage and limits

The 215 ledger entries are reviewed_with_gaps, with no skipped or blocked primary records. This status is deliberate: source precision and unobserved choice states remain limited even in otherwise clear games. Later windows have unknown phase where an enemy death is confirmed but friendly death ordering is not. A recorded win alone is never used to fill that gap. Exact individual attempt counts inside coarse repeated sequences are unknown; all reported window counts are analytical episodes, not independent games.

Six original extraction records were inspected for material ambiguities. They corroborate the normalized chronology and do not supply the missing target-choice signal. No original VOD was watched. The files retain source observations, source interpretations, unknowns and exceptions separately; semantic annotation is model judgment, while counts are calculated from those annotations. No selected-footage win-rate ranking, generic arena guide or new mechanics claim is used.

## Consumption and reproduction

This candidate is suitable for provisional, informational webapp consumption after validation passes. Load the current IDs and paths from this package's matchup_index.json. Keep the baseline package available as history. Do not run the original v1 generator against this directory. Rebuild only with the three scoped helpers in analysis: build_candidate.py, write_refinement_reports.py, then validate_refinement.py. These helpers are the only added code and write only inside this candidate.

There is no data-package integration blocker for displaying provisional cards and source-linked analysis. Display unknown branch selection explicitly, and keep evidence citations available. A live automatic tactical selector remains blocked by unestablished choice rules and unvalidated detection; the existing empty automatic list and all observability statuses are preserved. This task does not build or test a webapp integration.

The historical provenance.matchup_file paths remain project-relative source paths; the copied evidence records support standalone reading. Use provenance.review_file relative to this candidate. The consumer must honor this existing distinction rather than treating every provenance path as a downloadable package asset.

See [validation results](validation_results.json), [validation report](VALIDATION_REPORT.md), [claim review](analysis/claim_review.json), [input hashes](analysis/input_manifest.json), and [precise review requests](REVIEW_REQUESTS.md). Mechanical validation cannot prove strategy correctness; unresolved choices remain for review rather than being silently automated.
