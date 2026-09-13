"""Reviewed v2 strategy content. No source evidence is rewritten."""
CONTENT = {
'SPR_vs_Arms_HPal': {
 'opening': ('Start on Warrior with Paladin Sap/control. The recorded Warrior opener is the observed default; brief or split openings are qualified in the ledger.', 'M036 M048 M088 M152 M322 M334 M446', 'medium'),
 'objective': ('Use a real Warrior attack to threaten a finish and draw escape responses, while developing a later Paladin commitment through renewed Warrior control. Repeated healer commitments are a leading observed continuation; a preplanned healer kill in every opener is not established.', 'M006 M026 M032 M052 M131 M321 M342 M387 M479', 'medium'),
 'win_condition': ('For the healer line, combine Paladin stun/damage with effective Warrior containment; after a protection response, rebuild that control for another Paladin attempt. A recent Warrior Trinket spend improves this specific control opportunity, while Paladin escape or Shield may still answer the attack.', 'M026 M052 M096 M131 M321 M342 M475 M479', 'medium'),
 'manufacture': ('Pressure and stun Warrior under Paladin control. For the healer line, establish fresh Warrior control and apply Paladin stuns/damage; confirmed Blind may be extended by Sap, or a separately observed Fear/Gouge/stun may support the attempt. Record each enemy escape at the current window, not just its first use.', 'M006 M026 M070 M096 M131 M321 M342 M374 M479', 'medium'),
 'conversion': ('A documented option after Warrior spends Trinket is fresh Warrior control followed by a Paladin commitment. Renew Paladin control if its escape is spent during the attempt. This is an actionable setup sequence, but its priority over continued Warrior damage is unresolved; many observed switches begin before the later Blind lands.', 'M026 M052 M096 M131 M321 M342 M475', 'medium'),
 'reset': ('A confirmed Shield/protection response ends the immediate low-health opportunity. Observed responses include Warrior damage while Paladin recovers, friendly stabilization, and renewed Paladin control after the protection ends. Recheck both current escapes before the next attempt; a Mass Dispel cast does not prove removal.', 'M006 M026 M032 M039 M052 M072 M321 M444 M479', 'medium'),
 'alternative': ('Continue or return to Warrior through partial healing, renew its stuns and disrupt Paladin healing casts. This is a substantive attack line, including direct openings and returns after failed healer attempts; it need not wait for both escapes to be spent.', 'M036 M048 M091 M123 M322 M403 M431 M456 M474', 'medium'),
 'failure': ('Healer commitments can reach low health, meet protection or healing, and fail to recreate that deficit before friendly survival ends. Control/resource progress does not measure remaining friendly capacity to finish. A Paladin kill can also be followed by a lost Warrior cleanup.', 'M052 M053 M057 M090 M097 M213 M317 M328 M475', 'medium'),
 'unknown': 'Which pre-choice state selects the first Paladin commitment over another Warrior attack? Healed Warrior pressure, escape depletion and Warrior control all occur without uniquely determining that choice.',
 'resources': [
  ('Arms Warrior PvP Trinket','M006 M026 M321 M342 M479','Its recent use can permit a fresh Warrior Blind/Sap or other control interval for Paladin damage. Availability must be checked again after long recoveries; it is useful control context, not an automatic target selector.','M090 M079 M032 M142 M472'),
  ('Holy Paladin PvP Trinket','M048 M052 M321 M374 M475','A spend during Paladin control can be followed by renewed stun/control; do not demand it before beginning the attack. It may have recovered before later healer returns.','M087 M122 M327 M401'),
  ('Holy Paladin Divine Shield / separately unidentified protection','M006 M032 M052 M072 M479','Confirmed Shield can stop a low Paladin attempt and motivate Warrior pressure/recovery before a renewed healer line. Keep unnamed protection separate. No verified removal credited solely from Mass Dispel attempts.','M026 M039 M046 M079 M090 M456'),
  ('Warrior Blind, Sap, Fear, Gouge and stuns','M026 M070 M096 M131 M374 M479','Blind-to-Sap is one repeated control sequence; Fear, Gouge and stuns are separate observed options. Check application and coverage. The source does not resolve a Berserker Rage requirement for a particular branch.','M056 M097 M327 M357 M444')],
 'roles': {
  'rogue': ('Explicit narratives place the Rogue on Warrior opening stuns and later Paladin damage/stun returns. For these documented lines, coordinate that damage switch with the observed partner control; unseen cooldown readiness remains unknown.','M039 M180 M186 M414','medium'),
  'priest': ('Explicit friendly Priest narratives include Warrior ranged pressure, Mind Control on Warrior during some Paladin setups, and recovery with Divine Hymn. These are supported options, not a fixed spell rotation or proof of availability on demand.','M036 M066 M076 M077 M444 M456','low')},
 'card': [
 ('Start','Warrior, with Paladin Sap/control.'),
 ('Objective','Threaten a Warrior finish and draw escapes while building a later Paladin commitment.'),
 ('Win condition','Paladin stun/damage with Warrior contained; protection may require another attempt.'),
 ('Create it','Warrior pressure → fresh Warrior control → Paladin stuns/damage; track each current Trinket.'),
 ('Convert','After Warrior escape use, renewed control supports a Paladin go. Renew Paladin control after its escape.'),
 ('Alternative','Continue Warrior through partial heals; renew stuns and interrupt Paladin healing.'),
 ('Failure','Protection or healing can erase the healer attempt before friendly survival allows another.'),
 ('Reset','On Shield, pressure Warrior or stabilize; rebuild control for a post-immunity Paladin return.'),
 ('Unresolved','What makes the first Paladin go preferable to renewed Warrior pressure remains unknown.')]
},
'SPR_vs_SP_Sub': {
 'opening': ('Start on enemy Rogue with enemy Priest Sap/control. The recorded Rogue opener is the default, but some labels reflect chip damage or absorbed attacks; Priest-first commitments also recur.', 'M021 M067 M103 M208 M337 M421 M435', 'medium'),
 'objective': ('The Rogue opener serves two observed continuations: a direct or repeated Rogue attack with Priest disruption, and a Priest commitment supported by renewed Rogue control. Escape depletion can create the second opportunity, but the evidence does not establish one compulsory conversion or a preference between them.', 'M021 M103 M194 M205 M208 M337 M419 M421', 'medium'),
 'win_condition': ('Two useful states recur: Rogue held in renewed damage/stuns while Priest support is disrupted, or Priest taking committed damage while Rogue control limits interference. Both require actual damage follow-through; a confirmed isolation with healthy enemies can still produce no conversion.', 'M021 M103 M205 M292 M337 M419 M430', 'medium'),
 'manufacture': ('Build an actual Rogue attack under Priest control. One recurring follow-up is Rogue escape → confirmed Rogue Blind → Priest attack → Sap extension. Another is renewed Rogue stuns with fresh Priest control or a heal interruption after the first Rogue attempt recovers.', 'M021 M103 M196 M205 M337 M419 M430 M435', 'medium'),
 'conversion': ('Document Rogue Blind into a Priest commitment, with Sap extension where confirmed, as a recurrent option after Rogue escape use. Selection over renewed Rogue damage remains unresolved. A Priest target selection or Blind announcement alone is not a valid trigger.', 'M021 M103 M205 M339 M419', 'medium'),
 'reset': ('If a Rogue attack is healed, renewed Rogue pressure with fresh Priest disruption is a supported continuation; a Priest branch also occurs. Recover through countercontrol before rebuilding an actual damage window. After a friendly death, treat the next action as a solo/trade continuation rather than the original two-player plan.', 'M071 M125 M194 M196 M253 M306 M380 M426 M435', 'medium'),
 'alternative': ('Retain Rogue through partial healing and renew Priest control or an observed cast interruption for the next stun attack. Priest-first damage is a real alternative opening; its selection reason is not established from enemy stealth, position or accessibility in this evidence.', 'M092 M102 M196 M208 M218 M337 M421 M430 M461', 'medium'),
 'failure': ('Friendly Priest death repeatedly ends the intact-team attempt before a low enemy can be finished; both escapes may already be spent or only be spent afterwards. Short/escaped control and countercontrol can leave no damaging follow-up. A later solo kill must not retroactively validate the original setup.', 'M064 M073 M080 M249 M266 M292 M294 M297 M302 M306 M417 M423 M426', 'medium'),
 'unknown': 'Which pre-switch cue selects Priest over continued Rogue damage? Rogue escape use and recovery are insufficient discriminators; friendly readiness, accessibility and control timing remain incompletely recorded.',
 'resources': [
  ('Enemy Subtlety Rogue PvP Trinket','M021 M103 M205 M296 M339','Recent escape use can make renewed Rogue Blind/Sap useful for Priest pressure. In other games the spend occurs after Priest damage begins, or the team continues Rogue instead.','M203 M208 M337 M419 M421'),
  ('Enemy Shadow Priest PvP Trinket','M021 M103 M205 M241 M430','Opening Priest control can obtain escape before Rogue damage; a Priest attack can also obtain it during that attack. Immediate renewed control is a useful observed follow-up, not a prerequisite for starting every line.','M218 M255 M257 M272'),
  ('Enemy Priest Dispersion and recovery channels','M071 M196 M267 M419 M435','Confirmed Dispersion in the reviewed Priest attempt stalls damage until it ends; Rogue Blind-to-Sap can bridge that interval. Enemy Hymn may restore Rogue, be interrupted, or fail to save it. Distinguish the friendly Priest channel and post-death enemy channels.','M208 M253 M294 M435'),
  ('Confirmed enemy control versus offensive Blind / stealth','M021 M103 M292 M380 M397 M419','Require an applied effect for a control claim, and preserve gaps. Enemy offensive Blind is not a forced defensive; an announcement alone is not verified use. Observed stealth does not establish Vanish.','M190 M266 M270 M383 M417')],
 'roles': {
  'rogue': ('Explicit narratives show the friendly Rogue delivering the opening attack, switching damage between enemy Rogue and Priest, and sometimes Sapping/Blinding enemy Priest after its escape. Coordinate a selected damage line; exact per-window readiness is unrecorded.','M416 M425 M428 M435 M461','medium'),
  'priest': ('Explicit narratives show friendly Priest countercontrol exposure and recovery through Divine Hymn during continued Rogue pressure. Damage attribution and a recurring offensive control rotation remain insufficiently resolved to assign a fixed Priest sequence.','M064 M205 M435','low')},
 'card': [
 ('Start','Enemy Rogue, with enemy Priest Sap/control.'),
 ('Objective','Threaten Rogue while drawing escapes that can also enable a controlled Priest attack.'),
 ('Win condition','Rogue damage with Priest disrupted, or Priest damage with Rogue contained.'),
 ('Create it','Build Rogue pressure; after its escape, confirmed Blind → Priest attack → Sap is a recurring sequence.'),
 ('Convert','That Priest line is a documented option; its priority over renewed Rogue damage is unknown.'),
 ('Alternative','Stay Rogue through partial heals; renew Priest control or interrupt healing. Priest-first also occurs.'),
 ('Failure','Friendly Priest death can end the team attempt before or after escape extraction.'),
 ('Reset','Survive countercontrol, rebuild damage/control, and distinguish a trade or solo continuation from a two-player finish.'),
 ('Unresolved','No reliable pre-choice rule selects Priest over Rogue from the recorded states.')]
},
'SPR_vs_Disc_Feral': {
 'opening': ('Start on Feral with Priest control. Repeated Feral damage/stuns form the observed default; absorbed attacks remain real commitments, while selecting Priest for control does not establish a healer damage opener.', 'M054 M128 M138 M277 M325 M434 M448 M453', 'medium'),
 'objective': ('Develop repeated Feral stun attacks with renewed healer disruption, maintaining a damage deficit across partial recoveries. A distinct Priest commitment is also recurrent when Feral control supports it; healed Feral pressure alone does not choose that branch.', 'M054 M307 M325 M370 M382 M438 M448 M453', 'medium'),
 'win_condition': ('For the Feral line, retain a Feral health deficit into renewed stuns while disrupting Priest recovery. For the healer line, attack Priest during actual Feral control. These states describe useful opportunities; free healing, ready escapes or a later control gap do not erase earlier setup value.', 'M277 M307 M325 M370 M382 M438 M439 M448 M453', 'medium'),
 'manufacture': ('Repeat Feral stuns with separately confirmed Priest Gouge, Silence, Fear or Sap. If pursuing Priest, build actual Feral control before committing damage: a recent Feral escape followed by Blind/Sap is one supported sequence; short Fear or stun setups also occur without escape depletion.', 'M307 M325 M382 M392 M432 M438 M439 M453', 'medium'),
 'conversion': ('Repeated Feral damage is a defensible continuation after partial heals; renew its stuns and Priest disruption. Fresh Feral control can support a documented Priest switch, but its priority over another Feral attempt remains unresolved. Do not switch merely because Feral was healed.', 'M307 M326 M370 M382 M438 M439 M448 M453', 'medium'),
 'reset': ('After a healed or interrupted attempt, stabilize and rebuild control for another attack. The evidence includes resumed Feral pressure after Cyclone, renewed Feral attempts after substantial healing, and Priest switches under fresh Feral control. The observed interruption alone does not determine the next target.', 'M308 M319 M326 M370 M398 M438 M448 M452 M453', 'medium'),
 'alternative': ('A Priest attack after Feral escape → Blind/Sap is a repeated option; brief Feral Fear/stun into Priest damage also occurs with escapes retained. Priest-first and split-damage finishes exist, so a Priest selection must be checked against actual attacks and actor-specific damage.', 'M065 M307 M382 M392 M432 M438 M439 M454', 'medium'),
 'failure': ('The two losses are distinct: one has repeated healed Feral attempts, then Cyclone-stalled Priest pressure and Rogue death; the other has an absorbed Priest opener, shallow healed Feral damage and rapid friendly Priest death. Neither is a well-established common error or universal Cyclone failure rule.', 'M308 M450', 'low'),
 'unknown': 'What selects a Priest commitment over another Feral attempt? Feral healing, escape expenditure and Cyclone do not independently resolve that choice; friendly readiness and accessibility remain incomplete.',
 'resources': [
  ('Feral Druid PvP Trinket','M307 M325 M382 M438 M453','A recent Feral escape can support renewed Feral stuns or a Blind/Sap-to-Priest line. Those are different uses of the same resource state; the spend itself does not select the target.','M138 M277 M392 M439 M448'),
  ('Discipline Priest PvP Trinket','M054 M308 M323 M326 M382','A Priest escape can be followed by renewed healer control for Feral damage or renewed Priest stuns in a healer commitment. Track which attempt obtained it; later Feral cleanup escapes do not precede the healer kill.','M307 M325 M370 M439 M453'),
  ('Priest recovery and Feral Cyclone','M308 M319 M326 M398 M434 M436 M452','Record each actual interruption: Cyclone may interrupt a Priest attempt, be kicked, or temporarily stop one friendly while damage resumes on Feral. Enemy Hymn/Penance may restore a window without selecting the next target. Unnamed Feral buffs stay unnamed.','M236 M326 M434 M436'),
  ('Feral Blind/Sap or shorter Fear/stun; Priest control','M307 M325 M382 M392 M432 M438 M439','Blind-to-Sap after a Feral escape is one healer setup, while fresh short Fear/stun also precedes fast Priest commitments. Renewing Priest control supports repeated Feral damage. These effects are not interchangeable event counts.','M308 M370 M438 M454')],
 'roles': {
  'rogue': ('Explicit narratives show Rogue damage switches and later return to Feral; friendly Rogue Cyclone can interrupt that contribution. Coordinate actual damage rather than reading every Priest selection as a kill switch. A fixed universal control rotation is not established.','M326 M439 M454','low'),
  'priest': ('Narratives explicitly show friendly Priest continuing damage while Rogue is Cycloned, and retaining Priest damage when Rogue returns Feral. This supports a coordinated continuing-damage option, not a universal target-splitting assignment.','M326 M454','low')},
 'card': [
 ('Start','Feral, with Priest control; keep attacking through initial absorbs.'),
 ('Objective','Build repeated Feral attacks with renewed healer disruption.'),
 ('Win condition','Feral remains damaged into renewed stuns, or Priest takes damage while Feral is contained.'),
 ('Create it','Renew Feral stuns with Priest Gouge/Silence/Fear; track each escape separately.'),
 ('Convert','Repeat Feral after partial heals. Fresh Feral control supports a documented Priest alternative.'),
 ('Alternative','Feral escape → Blind/Sap → Priest occurs; short Fear/stun swaps also occur with escapes retained.'),
 ('Failure','Two losses: stalled attacks and friendly collapse; one Priest attempt is interrupted by Cyclone.'),
 ('Reset','Recover and rebuild an attack after healing or Cyclone; resumed Feral pressure is documented.'),
 ('Unresolved','A healed Feral does not select the Priest switch; its priority remains unknown.')]
}
}
