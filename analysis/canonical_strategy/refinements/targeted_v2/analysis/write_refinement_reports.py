"""Render the authored analyses with counts from the reviewed ledger."""
from review_work import *
from refined_content import CONTENT
import re

PROSE = {
KEYS[0]: r'''
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
''',
KEYS[1]: r'''
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
''',
KEYS[2]: r'''
## Candidate comparison and resulting default

Repeated Feral attacks with renewed Priest disruption are the strongest practical default. Priest commitments are nevertheless real and recurrent, not merely healer selections for utility. The strongest alternative interpretation is that Feral is primarily a setup target for a planned Priest kill. That describes some clear sequences, but cannot explain all the renewed Feral attacks after deep healing recovery. The revised guidance therefore recommends a repeated Feral line while documenting the control-and-Priest alternative and leaving its priority unresolved.

M325 shows a Feral near-kill, escape and partial recovery followed by renewed Feral stun and Priest Silence/Fear. M448 has a deep Feral attempt healed substantially, then another Feral attack that finishes after the Priest's control has ended and Penance resumes. M453 also remains on Feral through several saves and friendly Rogue recovery. These examples support a meaningful continuation after failure, rather than an instruction to attack whichever target is already described as vulnerable.

The competing healer sequence is especially clear in M307 and M382: Feral escape expenditure and recovery are followed by confirmed Feral Blind/Sap, then actual Priest damage. M438 has joint damage change to Priest after Feral Blind, with renewed Blind supporting the attack through a partial healer recovery. These are specific manufacturing sequences. They do not make Feral escape expenditure a universal requirement: M439 uses a fresh short Fear before a fast Priest switch while both enemy escapes remain ready.

## Does healing identify the branch

The complete first-switch table covers Feral-opening games with an established Priest commitment; a separate ambiguous utility/damage episode is retained outside that set. M398 is that ambiguity. Its brief Priest selection/stun coincides with health loss, but the original extraction explicitly does not establish an intended healer kill swap. The refinement conservatively leaves substantive commitment versus utility/spread damage unresolved. It does not count the episode as a confirmed Priest branch merely to increase a frequency.

M392, M432 and M439 show Priest switches after very shallow or absorbed Feral opening pressure, with fresh Feral stun or Fear preceding the change. They do not require a failed deep Feral attempt. Conversely, M325, M370, M448 and M453 continue Feral after substantial recovery. Thus “Feral healed” fails the actionability test as a target selector. It describes a common background event shared by different choices. More precise information about available friendly damage, control, access and intent would be needed to prefer Priest at a given decision point.

Absorbed attacks remain attacks. M434 continues Feral through early absorbed stuns and later heals, while M450 begins with a genuinely attempted Priest stun/damage sequence that is absorbed. The absence of health loss alone cannot turn those commitments into mere selection. M065 and M323, by contrast, describe Feral control at full health before actual Priest opening damage, so those Feral stuns are not invented Feral damage openers. The ledger retains the source's recorded opener alongside these qualifications.

## Resources, Cyclone and recovery

Feral escape use has at least two tactical uses in the narratives: renewed Feral stuns in the same-target line, and more durable Feral isolation for a Priest attack. Priest escape use can likewise be answered by renewed Priest control while attacking Feral, or by renewed Priest stuns in a healer attack. The actor and target matter more than a pooled “both Trinkets” state. M323 places the Feral escape and subsequent Blind after the Priest kill; M392 likewise has the Feral escape only in cleanup. M307 kills Priest with its escape retained, while M325 and M453 kill Feral with Priest escape ready.

Cyclone does not select one universal response. In M308 it interrupts the friendly Rogue during a Priest attempt, after which Penance restores the healer. In M326 a later Cyclone interrupts Rogue during Feral pressure while the friendly Priest continues damage; after it ends, a confirmed Kick and Priest Gouge precede resumed Feral stuns and the finish. M398 records an interrupted Cyclone before continued Feral damage. M434 kills Feral despite late Cyclone on the friendly Priest; M436 also records Cyclone around the final death. These are separate local outcomes, not one event-frequency proxy or a deterministic failure rule.

The long M437 sequence also prevents carrying an early escape spend forward indefinitely. Both opponents' timers recover and are used again; the last Feral escape belongs to a later attempt. Priest recovery channels, unnamed Feral buffs, bear form and healing are retained as described without assigning unsupported defensive names. The split finish in M454 is especially important for actor identity: Rogue returns to Feral while friendly Priest continues damaging Priest, who dies. The Rogue's selected target is not the team's sole kill target.

## The two losses and change from v1

Both losses are fully represented. M308 has several healed Feral attempts, then a Cyclone-stalled Priest attack and eventual Rogue death. M450 has an absorbed Priest opener, a shallow Feral attack healed by a free Priest, and rapid friendly Priest death. The original M450 record supplies some friendly Rogue cooldown expenditures, but leaves friendly Priest defensive choices unknown; it does not establish which alternative could have saved the game. Neither individual explanation is called a common mistake.

Failed attempts inside wins provide the wider recovery comparison. M319 preserves repeated Feral and Priest recoveries in one game across overlapping clips; it is counted once. M451 kills the enemy Priest before losing the friendly Priest and requires a separate Rogue/Feral duel. Its solo Feral kill is not evidence for an intact-team Feral setup. Where friendly death order is unestablished, the ledger explicitly leaves the phase unknown.

The largest batch contributes strongly, and the family table exposes that concentration. M319 and M323 explicitly name the same opponents, so repeated records are not independent opponents. V2 makes repeated Feral attacks and the concrete Feral-control/Priest alternative usable, replaces a healed-target switch assumption with a precise unresolved question, and preserves low confidence in the two-loss failure generalization. Overall strategy confidence remains medium and provisional.
'''
}

REQUESTS = {
 KEYS[0]: [
 ('M090','174.5–180s','automatic_switch','What target access and friendly damage/control readiness existed immediately after Shield ended, while Warrior was controlled and Paladin escape unavailable?','If a ready healer attack existed, resource state still did not determine the choice; if friendly readiness/access was absent, qualify the option by that missing condition.'),
 ('M342','84–92s and 139–148s','conversion','What was known before each Paladin switch, since the confirmed Warrior Blind begins afterwards?','A preceding actionable signal could refine selection; control planned only after the choice leaves the trigger unresolved.'),
 ('M321','193–218s, compare M322 118–131s','objective','Did the players explicitly choose the healer line after recovery, and what differed from continued Warrior damage against the same displayed opponents?','A stated or visible preceding constraint may distinguish the two lines; absent one, retain competing observed continuations without priority.'),
 ('M026','117–129s','resource-3','Can the long unnamed Paladin protection and its ending be identified from readable buff/cast evidence?','Confirmed identity/removal would sharpen that recovery example; an ambiguous indicator stays unnamed and cannot create a named removal rule.')],
 KEYS[1]: [
 ('M339','96–104s','conversion','When does substantial Priest commitment begin relative to enemy Rogue Trinket and the actual Blind application?','A switch after confirmed isolation supports a pre-action cue; a switch before it supports a planned control follow-up, not an application trigger.'),
 ('M203','87–90s','automatic_switch','Why is Priest chosen while Rogue is already critically low and retains its escape; what friendly readiness or enemy state is visible before selection?','An identifiable constraint could qualify the target choice; without it, low Rogue health and healing recovery do not select a single branch.'),
 ('M383','130–142.5s','win_condition','What makes the Priest commitment possible while enemy Rogue is explicitly free, and is any preceding control/access cue missing from extraction?','A confirmed preceding condition would broaden the documented option; absent it, keep this as a free-Rogue alternative with unresolved selection.'),
 ('M078','114–118s','failure','What actually ends the round while enemy Priest is low and no death is established?','A verified death or departure changes the local outcome classification; otherwise keep the loss termination unknown, without inventing a failed kill or trade.')],
 KEYS[2]: [
 ('M398','89–94.5s','alternative','Is the brief Priest selection a substantive Rogue damage commitment or control/interrupt utility while other damage ticks?','A confirmed commitment adds a Priest-switch episode; utility leaves it outside established Priest-branch frequencies.'),
 ('M439','53–57s','conversion','What precedes the short Fear-to-Priest choice while both escapes are ready and Feral damage is absorbed?','A visible readiness/access condition may distinguish this fast healer line from renewed Feral pressure; otherwise preserve it as an observed option.'),
 ('M308','153–165s','reset','At the Priest switch, which Feral control and friendly follow-up were actually available before Cyclone landed?','If interruption was avoidable through an observed ready response, qualify the recovery branch; if readiness is absent or unknown, do not infer a missed execution.'),
 ('M450','77.5–82.5s','failure','Which friendly Priest defensive or recovery options, if any, were available immediately before the rapid death?','A demonstrated available option can refine this case-specific survival response; absent evidence, keep the cause and counterfactual unresolved.')]
}

def main():
 seq=read(ROOT/'analysis/sequence_counts.json')['groups']; stat=read(ROOT/'analysis/review_statistics.json')['groups']
 for k in KEYS:
  s=STRATEGIES[k];e=s['evidence']; fs=seq[k]['families'];d=stat[k]
  opening = {'SPR_vs_Arms_HPal':'Arms Warrior','SPR_vs_SP_Sub':'Subtlety Rogue','SPR_vs_Disc_Feral':'Feral Druid'}[k]
  op=d['opening_labels'][opening]; br=d['damage_opening_with_healer_branch']; stay=d['damage_line_without_healer_branch']
  pre=f"# {s['our_comp']} vs {s['enemy_comp']} — targeted v2 review\n\n"
  pre+=f"Reviewed all **{e['total_games']} matches ({e['wins']} wins, {e['losses']} losses)** from this key; overall confidence remains medium, status provisional. The source extraction was read, not independently verified against footage. The recorded {opening} opener appears in **{op['distinct_matches']}/{op['denominator']} matches**. The semantic ledger contains **{br['distinct_matches']}/{op['distinct_matches']} damage-opening matches with a healer branch**, and **{stay['distinct_matches']}/{op['distinct_matches']} with no established healer damage branch**; these are action classifications with chip/absorbed/utility qualifications, not deterministic facts about intent. In the mirror, the narrative-qualified opener set differs from the label set; the identical totals do not imply identical membership.\n\n"
  pre+="All count numerators and denominators have full match-ID sets in [review statistics](review_statistics.json); every family also has exact window references and source-batch counts in [sequence counts](sequence_counts.json). Aliases such as M026 resolve through the copied [match reference map](../evidence_review/match_references.json); the [decision ledger](decision_ledger.jsonl) retains exact source pointers, original notes, unknowns, exceptions and per-match reasoning.\n\n"
  table='## Sequence families and coverage\n\nFamilies overlap within a match. Windows are reviewed analytical episodes, sometimes a collapsed series; **exact attempt counts are unknown**. Local outcomes below count those windows, while W/L counts distinct matches containing the family. Neither is an estimate of ladder performance. D is post-first-death continuation; X is unclassified/utility uncertainty. Later episodes with unresolved friendly death order have unknown phase and are not certified intact-team kills.\n\n| Family | Operational definition | Matches / group | Reviewed episode windows | Round W/L | Source batches | Local episode outcomes |\n|---|---|---:|---:|---|---:|---|\n'
  for f,v in fs.items():
   results=v['round_results_by_distinct_match'];outcome=', '.join(f'{a}: {b}' for a,b in v['local_outcomes'].items())
   table+=f"| {f} | {v['definition']} | {v['distinct_matches']}/{e['total_games']} | {v['reviewed_episode_windows']} | {results.get('win',0)}/{results.get('loss',0)} | {len(v['source_batches'])} | {outcome} |\n"
  table+='\nThe dominant source batch in the whole group is '+max(e['source_batches'],key=e['source_batches'].get)+f" ({max(e['source_batches'].values())}/{e['total_games']} matches). Family-specific distribution remains in the sidecar so the dominant batch can be excluded without treating remaining batches as independent opponents.\n\n"
  table+='### First healer-choice context\n\nThis table counts one first healer episode per annotated damage-opening game that takes that branch. **It excludes later returns and the games with no healer branch.** It is not a frequency of all possible switch opportunities. Each cell has its own full supporting ID set in review statistics. “No deep prior attempt” is not proof that no chip damage ever healed; “unknown” is not absence.\n\n| Field | Reviewed state counts (common denominator shown in each cell) |\n|---|---|\n'
  for field,cells in d['first_switch_states'].items():
   table+='| '+field.replace('_',' ')+' | '+'; '.join(f"{v}: {cell['count']}/{cell['denominator']}" for v,cell in cells.items())+' |\n'
  table+='\nPhase coverage of reviewed episode windows: '+', '.join(f'{phase}={n}' for phase,n in d['phase_coverage'].items())+'. These are windows, not games or exact attempts. See first-death classifications for match-level outcome ordering.\n'
  (ROOT/'analysis'/(k+'.md')).write_text(pre+PROSE[k]+ '\n'+table,encoding='utf-8')
 req='# Precise review requests\n\nThese requests refine unresolved decisions; they do not block use of the supported provisional content. Clip names and times are recorded provenance pointers, **not verified playable links**. No footage was watched in this refinement. There are at most four requests per matchup; broad re-extraction is unnecessary.\n'
 structured=[]
 for k,items in REQUESTS.items():
  req+='\n## '+STRATEGIES[k]['enemy_comp']+'\n\n'
  for a,t,cl,q,impact in items:
   r=record(a);req+=f"- **{a} · {k}-{cl}** — `{r['match_id']}`. Recorded clip `{r['provenance']['source_clip']}`, **{t}**; batch `{r['provenance']['source_batch']}`. {q} {impact}\n\n"
   structured.append({'match_id':r['match_id'],'strategy_key':k,'claim_id':k+'-'+cl,'recorded_clip':r['provenance']['source_clip'],'recorded_time':t,'primary_artifact':r['provenance']['primary_artifact'],'question':q,'decision_impact':impact,'clip_availability':'not verified'})
 (ROOT/'REVIEW_REQUESTS.md').write_text(req,encoding='utf-8');save(ROOT/'analysis/review_requests.json',structured)
 checks=[]
 for a in ['M090','M339','M461','M398','M308','M450']:
  m=record(a);p=pathlib.Path(m['provenance']['primary_artifact']);rr=[json.loads(t) for t in p.read_text(encoding='utf-8-sig').splitlines() if t.strip()];original=next(r for r in rr if r.get('match_id') in m['provenance']['source_record_ids'])
  checks.append({'match_id':m['match_id'],'source_path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original_match_id':original['match_id'],'fields_checked':{field:original.get(field) for field in ['source_file','setup_actions','observed','conversion','branch_or_reset','enemy_resources_remaining_at_failure','friendly_resources_spent_at_failure']},'conclusion':'Primary normalized chronology corroborated. No new pre-choice discriminator or footage verification; original M450 additionally lists friendly Rogue expenditures while friendly Priest defenses remain unknown.'})
 save(ROOT/'analysis/supplemental_provenance_checks.json',checks)
 summary='''# Targeted strategy refinement — candidate package 1.1.0

Three strategies have material v2 revisions. They remain provisional at medium overall confidence. All 215 scoped records, including all 53 losses, have an individually authored decision-ledger entry. The other 46 strategy objects and cards are unchanged; no full-corpus strategic reanalysis was performed.

'''
 for k in KEYS:
  summary+=f"## {STRATEGIES[k]['enemy_comp']}\n\n"+(ROOT/'cards'/(k+'_v2.md')).read_text(encoding='utf-8').split('\n\n',1)[1].split('\n\n[Strategy',1)[0]+f"\n\n[Full card](cards/{k}_v2.md) · [Analysis](analysis/{k}.md)\n\n"
 summary+='''## What changed

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
'''
 (ROOT/'REFINEMENT_SUMMARY.md').write_text(summary,encoding='utf-8')
 print('Three reports, review requests and refinement summary written.')
if __name__=='__main__': main()
