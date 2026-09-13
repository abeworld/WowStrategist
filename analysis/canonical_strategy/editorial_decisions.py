"""Human-readable analytical decisions; references are snapshot-specific review IDs.

These are cross-match interpretations, never new footage observations.
"""
DECISIONS = {}


def add(group, confidence, objective, condition, manufacture, conversion, reset, refs,
        challenge, challenge_refs, failures=(), branches=(), resources=(), roles=None):
    DECISIONS[group] = dict(confidence=confidence, objective=objective, condition=condition,
        manufacture=manufacture, conversion=conversion, reset=reset, refs=refs.split(),
        challenge=challenge, challenge_refs=challenge_refs.split(), failures=list(failures),
        branches=list(branches), resources=list(resources), roles=roles or {})


def branch(trigger, response, refs, classification='real reactive branch'):
    return dict(trigger=trigger, response=response, refs=refs.split(), classification=classification)


def failure(text, refs):
    return dict(text=text, refs=refs.split())


def resource(name, role, refs, counter=''):
    return dict(name=name, role=role, refs=refs.split(), counter=counter.split())


add(1, 'medium',
    'Use Warrior pressure to develop a damaging window; decide between a covered Paladin commitment and continued Warrior pressure from the actual health and control state.',
    'A reachable enemy is losing meaningful health while partner disruption limits recovery or counterpressure long enough to finish. This is a useful conversion state, not a proven necessary or sufficient condition.',
    'Open Warrior in the usual line, pair pressure with Paladin control, and watch the response. Repeated healed Warrior attempts can lead to Warrior control and a Paladin swap; a low Warrior can instead be finished.',
    'Commit to the vulnerable target and renew short control or interrupts around the health decline. Warrior Blind/Sap into Paladin damage is a repeated line; it is not the only winning line.',
    'After a Paladin immunity or healed attempt, return pressure to Warrior and stabilise; renew Paladin pressure when immunity ends if a fresh window exists. Recheck cooldowns after long exchanges.',
    'M006 M026 M096 M321 M342 M479 M048 M322 M403',
    'Mandatory double-Trinket removal, mandatory Warrior Blind, continuous partner isolation, and an inevitable Paladin kill all fail as universal rules. Some kills succeed with escapes ready or the partner active; a Paladin kill can still lose the round.',
    'M070 M087 M088 M091 M098 M099 M142 M322 M334 M431 M472 M053',
    failures=[failure('A Paladin low is protected by Divine Shield; later resource expenditure fails to recreate the low-health window before a friendly death.', 'M052 M090 M475'),
              failure('The first enemy kill is followed by a lost survival/cleanup exchange.', 'M053')],
    branches=[branch('Paladin immunity stops the healer attempt and Warrior remains attackable.', 'Return Warrior; renew Paladin disruption and finish Warrior if the next health decline persists.', 'M023 M039 M127 M474'),
              branch('Paladin recovers through immunity, then a fresh partner-control window is established after it ends.', 'Renew Paladin pressure and control; check current escape availability rather than carrying an old spend forward.', 'M006 M026 M096 M479'),
              branch('Warrior becomes killable during the opening or renewed Warrior pressure.', 'Finish Warrior; a healer swap is unnecessary in this line.', 'M048 M088 M152 M322')],
    resources=[resource('PvP Trinket', 'Conditional control-window resource. Escapes and recovered cooldowns change the available control, but neither enemy Trinket is a universal pre-kill requirement.', 'M026 M321 M475', 'M087 M098 M099 M322 M431'),
               resource('Divine Shield', 'A repeatedly observed interruption of Paladin conversion. Its expiry/recovery can redirect or delay the next attempt; a prior spend is not required for every kill.', 'M006 M052 M475 M479', 'M070 M088'),
               resource('Berserker Rage', 'unknown: no repeated verified role established; excluded from the plan.', '', 'M444')])

add(13, 'medium',
    'Develop Shaman health pressure while disrupting Warlock and pet interference.',
    'Shaman health collapses under renewed pressure with enough disruption to prevent recovery; complete Warlock isolation is not a universal requirement.',
    'Shaman is the most frequent opening player target. Some games first pressure Warlock or interact with the Succubus, then transfer damage to Shaman.',
    'Commit Shaman, renew stuns/short control and disrupt recovery. All seven recorded wins identify Shaman as the enemy killed.',
    'When Shaman self-heals or earlier pressure stalls, renew the Shaman attempt. Pet interruption is evidenced; permanent pet removal is not established.',
    'M124 M207 M209 M211 M344 M353',
    'Warlock Trinket removal, continuous Warlock isolation and killing the Succubus are not supported prerequisites. The one Warlock-focused loss is an association, not proof that targeting Warlock causes defeat.',
    'M209 M211 M115 M204',
    failures=[failure('Warlock pressure remains nonlethal with Shaman active; friendly Rogue dies before a renewed damaging isolated window.', 'M204')],
    branches=[branch('Initial Warlock pressure does not finish and Shaman becomes the meaningful damage target.', 'Transfer pressure to Shaman with renewed Warlock disruption.', 'M115 M207')],
    resources=[resource('PvP Trinket', 'May expose a renewed control window, but Warlock escape removal is not required by all observed wins.', 'M124 M115', 'M209 M211')])

# The sparse validation case deliberately supplies no actionable default.
add(35, 'insufficient', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown',
    'M148',
    'Only one win and one inferred loss from one batch. Both start Priest; the win eventually kills Paladin. Both escapes are also spent in the loss, without threatening health pressure. Final Priest control in the win is not a second Blind.',
    'M145 M148')

add(0, 'medium',
    'Create effective damage before countercontrol costs a teammate; use pressure on the exposed Rogue to find either a Rogue finish or a Priest conversion.',
    'Low enemy health and usable friendly damage overlap with enough partner disruption to prevent recovery. Neither a fixed kill target nor an empty pair of Trinkets is established as necessary.',
    'Rogue is the most frequent opener. Pressure with Priest disruption, then retain Rogue or transfer to Priest when Rogue control supports a real damage window.',
    'Finish the opponent whose health pressure can be sustained; repeated Rogue-control/Priest-swap and Priest-control/Rogue-finish sequences both occur.',
    'Healing often restores the first window. Stabilise and renew a same-target attempt or a supported switch; a full stealth reset is not established as the universal recovery pattern.',
    'M021 M103 M194 M205 M296 M339 M084 M241 M293 M380 M435',
    'The nearly balanced enemy-kill split rejects a single compulsory kill target. Ready Trinkets, active healing and short control gaps occur in wins. Counter-kills after a friendly death must be separated from intact-team conversions.',
    'M208 M255 M272 M337 M421 M294 M297 M306 M426 M078',
    failures=[failure('Control or escape extraction occurs too late, or produces little damage before friendly Priest death.', 'M073 M080 M252 M270 M292'),
              failure('The target survives at very low health as partner control expires; a friendly dies before the finish.', 'M136 M417 M423')],
    branches=[branch('Enemy Rogue is controlled and Priest becomes the sustained damage target.', 'Commit Priest and extend useful Rogue control where available.', 'M021 M103 M205 M339'),
              branch('Rogue health can be driven low while Priest support is interrupted.', 'Keep or renew Rogue pressure through the finish.', 'M084 M241 M293 M380 M435')],
    resources=[resource('PvP Trinket', 'A conditional escape resource; late or unused escapes do not define whether the target can die.', 'M021 M241 M380', 'M208 M337 M421'),
               resource('Divine Hymn', 'Repeated enemy recovery can interrupt progress; several wins nevertheless finish through or after the healing.', 'M196 M253 M435 M397', 'M208')])

add(2, 'medium',
    'Start from Feral pressure with Priest disruption; retain a Feral finish and a healer-switch option.',
    'A meaningful Feral health deficit persists through renewed pressure, or Feral control opens a damaging Priest commitment.',
    'Apply pressure to Feral and renew short Priest control/interrupts around actual health loss. If Feral pressure heals out, a real Priest switch is supported by several games.',
    'Usually finish Feral; convert onto Priest when Feral control and actual Priest damage align.',
    'Repeat Feral pressure after partial or full heals; a healed Feral can also precede renewed Feral control and a Priest swap.',
    'M054 M277 M325 M436 M437 M448 M307 M382 M438',
    'Both-Trinkets-spent and continuous Priest denial are not necessary. Some Priest wins happen with Feral free or escapes still ready. Cyclone is not automatically fatal: both a loss and wins occur around it.',
    'M245 M248 M280 M439 M448 M454 M308 M326 M434',
    failures=[failure('Healing restores the Feral window; Cyclone interrupts later Priest pressure and the team cannot survive another attempt.', 'M308'),
              failure('Opening attacks cause little lasting damage while Priest freely restores Feral and friendly Priest dies.', 'M450')],
    branches=[branch('Feral pressure heals out and Feral is controlled during a meaningful Priest switch.', 'Commit Priest with renewed short lockdown; do not infer a Priest swap from target selection alone.', 'M307 M382 M438 M432')],
    resources=[resource('PvP Trinket', 'Conditional control resistance; low-health conversion sometimes follows its use, but many wins retain one or both escapes.', 'M325 M437', 'M245 M277 M439 M448')])

add(3, 'low', 'Develop pressure on the accessible target while limiting Druid healing and Rogue counterpressure.',
    'A low Rogue or Druid remains vulnerable during renewed pressure; the corpus does not identify a reliable initial target-selection trigger.',
    'The two opening targets are close in frequency. Rogue pressure with Druid disruption is repeated; Druid openings also convert directly or later switch Rogue.',
    'Rogue is killed more often, but sustained Druid conversions are repeated too. Choose from the actual damage/control state; a deterministic choice rule is unknown.',
    'Renew pressure after Nourish/Regrowth/Tranquility recoveries; a healed Druid sometimes prompts the later Rogue commitment.',
    'M150 M157 M158 M162 M167 M168 M170 M173 M177',
    'Nineteen of twenty games come from one source batch. Opening families are nearly balanced; their triggers are not established. Druid Trinket removal and continuous Druid control are not necessary for every Rogue kill.',
    'M150 M160 M165 M167 M173 M360',
    failures=[failure('Druid healing restores the first target and counterpressure kills a friendly before the next attempt.', 'M153 M174 M175')],
    branches=[branch('A sustained Druid attempt recovers and a later Rogue damage window forms.', 'Transfer to Rogue with renewed Druid disruption.', 'M157 M158 M167')])

add(4, 'low', 'Develop Druid pressure with Warrior disruption, retaining a Warrior finish when healer pressure recovers.',
    'Druid damage and useful Warrior control overlap, or a Warrior health deficit persists during Druid disruption.',
    'Druid is the more frequent opener. Repeated stuns and brief Warrior control support healer pressure; low-health Warrior branches can also emerge.',
    'Commit Druid if the healer window develops; finish Warrior when Druid control supports that branch. There is no proven universal escape-removal requirement.',
    'Alternate or renew pressure after heals, stabilise friendly health, and update cooldown state after long games. Several late wins follow fresh Warrior escape use.',
    'M027 M049 M466 M038 M042 M264 M464 M465',
    'Both targets win; some kills retain Trinkets or happen after partner control ends. One active-combat clip has no result and must not enter win/loss comparisons.',
    'M049 M095 M047 M350 M040',
    failures=[failure('Healer health loss occurs while Warrior is free, then Blind lands after the healer has recovered; repeated Cyclones interrupt renewed pressure.', 'M467 M468'),
              failure('Druid breaks Blind, restores Warrior and disrupts renewed pressure before friendly Priest death.', 'M463')],
    branches=[branch('Druid pressure heals back and a Warrior attempt has effective Druid disruption.', 'Switch or return Warrior and renew pressure around the healer control.', 'M038 M042 M047 M384')],
    resources=[resource('PvP Trinket', 'Relevant to renewing control in long exchanges; earlier expenditure can expire before the next go.', 'M027 M464 M465', 'M049 M095')])

add(5, 'low', 'Use Warrior opening pressure to develop either a Warrior finish or a Priest commitment under Warrior control.',
    'A low target can be pressured through a short recovery-disruption window; neither target is a fixed outcome of the opener.',
    'Open Warrior in the usual line with Priest control. Repeated healed Warrior pressure commonly precedes a controlled-Warrior Priest swap.',
    'Continue Warrior if the health deficit persists; otherwise commit Priest during useful Warrior control and renew damage after the healer escape.',
    'A healed first Priest attempt can be followed by recovery, renewed Warrior Fear/Sap and another Priest commitment.',
    'M004 M007 M008 M110 M114 M116 M120',
    'Successful healer kills can outlast Warrior control or leave Priest Trinket ready; direct Warrior kills are frequent enough to reject a compulsory healer swap.',
    'M010 M263 M393 M287 M427',
    failures=[failure('Short Warrior isolation produces little Priest damage; Penance restores the healer before friendly survival fails.', 'M002 M013')],
    branches=[branch('Warrior health pressure is repeatedly healed and Warrior control is usable for a healer attempt.', 'Commit Priest, then renew pressure or control if the first healer window recovers.', 'M007 M008 M110'),
              branch('Warrior remains vulnerable during Priest disruption.', 'Stay Warrior and finish.', 'M004 M114 M116 M120')])

add(6, 'medium', 'Develop Hunter pressure while disrupting Paladin support; retain a covered Paladin return as an alternative.',
    'Hunter loses meaningful health through renewed pressure and enough support disruption to prevent recovery, or a covered Paladin branch becomes vulnerable.',
    'Usually open Hunter; renew short Paladin control and actual damage after defensive or healing pauses.',
    'Usually finish Hunter. A Paladin return is supported in a small number of wins and is not automatically implied by selecting Paladin.',
    'Resume Hunter pressure after healing or avoidance pauses; first verify that a temporary DEAD display is followed by persistent death before treating it as a kill.',
    'M019 M106 M385 M394 M399 M404',
    'Some Hunter wins retain both escapes or happen while Paladin heals. Paladin immunity is not healer incapacitation; many protective icons remain unnamed.',
    'M069 M214 M068 M062',
    failures=[failure('An early or renewed Hunter attempt is healed; the next control window creates shallow damage and friendly Priest dies before another setup.', 'M378 M388'),
              failure('A low Hunter recovers before friendly Rogue dies; the later solo attempt does not finish.', 'M061')],
    branches=[branch('Hunter pressure/control is followed by a meaningful covered Paladin commitment.', 'Commit Paladin and sustain pressure through partial healing.', 'M060 M068', 'low-frequency adaptation')],
    resources=[resource('PvP Trinket', 'Conditional control resource; extraction alone does not create a lethal Hunter state.', 'M106 M404', 'M069 M388')])

add(7, 'medium', 'Develop Warlock pressure while disrupting Paladin healing and Succubus interference.',
    'Warlock is vulnerable to renewed pressure while healing and pet interference are sufficiently constrained; permanent pet removal is not an established prerequisite.',
    'Usually open Warlock. Repeated pet pressure and Seduction/summon interruptions occur between player attempts; return to meaningful player damage with healer disruption.',
    'Usually commit Warlock. Later Paladin branches also convert when Warlock control and real healer damage align.',
    'After player or pet recovery, renew disruption and return to a fresh player-pressure window; replacement summons mean pet absence cannot be assumed to persist.',
    'M315 M364 M366 M367 M462 M481',
    'Pet work is not sufficient, and kills occur with a pet still present or Paladin free late. The three Paladin kills differ: only one explicitly shows severe mana depletion.',
    'M156 M368 M478 M482 M483 M485',
    failures=[failure('The low Warlock window occurs after healer control expires; later pet work fails to coincide with renewed lethal player pressure.', 'M485')],
    branches=[branch('Warlock pressure recovers and later control supports a genuine Paladin damage commitment.', 'Commit Paladin; renew pressure after immunity/healing when observed.', 'M482 M483')],
    resources=[resource('Succubus / replacement summon', 'Repeated support-interference problem. Pressure and interruptions are observed; pet death and permanent removal are often unconfirmed.', 'M315 M462 M481', 'M156 M485'),
               resource('Divine Shield', 'Stops or delays some Paladin branches; applicability is conditional on a confirmed immunity.', 'M482 M483')])

add(8, 'low', 'Develop Hunter pressure through absorbs and healing while limiting Priest support.',
    'Hunter has a sustained health deficit during renewed pressure, with useful healer disruption or a decisive late interrupt.',
    'Hunter is the most frequent opening player target; pet-first and Priest-first records are retained separately. Actual health damage may start substantially after control.',
    'Usually finish Hunter; a healed or absorbed Hunter attempt sometimes leads to a Priest switch under Hunter control.',
    'Renew Hunter pressure after recovery. Defensive Vanish alone did not guarantee stabilization in the losses.',
    'M139 M149 M409 M411 M424 M459',
    'Most evidence comes from the repaired September 11 batch. Wins occur with ready Trinkets and active Priest healing; pet removal is not a proven requirement.',
    'M420 M422 M406 M407',
    failures=[failure('Hunter isolation expires before meaningful Priest damage starts; friendly Rogue is already critically low and cannot survive another conversion.', 'M407'),
              failure('Pet work and absorbed Hunter attacks do not create threatening player damage before friendly Rogue death.', 'M406')],
    branches=[branch('Hunter pressure is absorbed or healed and Hunter control supports an actual Priest switch.', 'Commit Priest and renew pressure around the healer escape.', 'M413 M418')])

add(9, 'low', 'Develop Death Knight pressure while disrupting Paladin healing, with a possible Paladin return.',
    'Death Knight health pressure persists into renewed control or an interrupt; alternatively Paladin becomes vulnerable while Death Knight is controlled.',
    'Usually open Death Knight. Renew Paladin disruption after recoveries; observed Gargoyle interruptions are support disruption, not evidence that a summon or pet must be removed.',
    'Usually finish Death Knight. Some repeated Paladin branches use Death Knight control to support actual Paladin damage.',
    'Renew the same target after healing, or recommit Paladin after its protection/recovery. Do not label unidentified protective effects.',
    'M134 M191 M225 M258 M262 M242 M254',
    'Wins occur with ready escapes or active Paladin healing; spending both escapes also occurs without threatening enemy health in losses.',
    'M262 M254 M261 M250 M259',
    failures=[failure('Paladin healing restores Death Knight and friendly countercontrol/survival breaks before a renewed finish.', 'M247 M250 M259')],
    branches=[branch('Death Knight control supports meaningful Paladin pressure after initial Death Knight attempts.', 'Commit or renew Paladin pressure through partial recovery.', 'M242 M254')])

add(10, 'low', 'Create caster health pressure and use disruption to maintain the chosen target through healing or immunity responses.',
    'A Priest or Mage remains vulnerable through renewed short control; no single resource prerequisite is established.',
    'Openers are nearly split. Priest is the more frequent confirmed kill; Mage control into Priest pressure is repeated, but direct Mage finishes also occur.',
    'Commit Priest under available Mage disruption, or resume Mage after Block if that target remains the actual damage opportunity.',
    'Mage immunity can lead to a Priest switch or to renewed Mage pressure after it ends; partial Priest healing is often met with continued pressure.',
    'M050 M144 M197 M349 M440 M442',
    'All eleven records are wins, so loss discrimination is unavailable. Kills can occur with partner active or escapes ready; one victory has no confirmed enemy death.',
    'M356 M442 M135 M441',
    branches=[branch('Mage immunity stops the first attempt.', 'A Priest switch and a renewed Mage attempt are both observed; their selection trigger is unknown.', 'M144 M440 M442', 'unknown')],
    resources=[resource('Ice Block', 'An observed interruption of Mage pressure with two different follow-ups, not proof of an automatic switch.', 'M144 M440 M442')])

add(11, 'low', 'Develop sustained Priest pressure while limiting Mage interference when possible.',
    'Priest health loss persists through renewed short lockdown and partial healing; continuous Mage isolation is not established as necessary.',
    'Open either caster in the observed sample, but most games develop a Priest commitment; Mage control can support the switch.',
    'Usually finish Priest through renewed stuns/short disruption and continued damage.',
    'Repeat Priest pressure after partial heals. A failed Mage opening can transition to Priest, but a full reset is not universal.',
    'M031 M141 M330 M346 M400 M433',
    'Nine wins and no losses limit validation. One direct Mage kill contradicts an exclusive Priest-kill rule, and some Priest wins retain escapes or tolerate an active Mage.',
    'M034 M151 M346',
    branches=[branch('Mage opening damage recovers or is blocked while Priest becomes attackable under Mage control.', 'Transfer pressure to Priest.', 'M141 M330 M400')])

add(12, 'low', 'Develop Rogue pressure through Priest healing; early Priest contact is often followed by a Rogue commitment.',
    'Rogue remains low through renewed stuns and useful Priest disruption; a later Priest switch is a supported exception, not the dominant kill line.',
    'Many games open Priest, then pressure Rogue and renew Priest control around meaningful Rogue health loss.',
    'Usually finish Rogue; do not confuse an early Priest opener with a required Priest kill.',
    'Rogue commonly recovers from a first near-kill. Renew Rogue pressure and short Priest control after healing; Blind/Sap Rogue can be a recovery interval.',
    'M028 M033 M129 M295 M381 M487',
    'All nine games are wins. Active Hymn/late healing and ready Priest or Rogue escapes occur in successful Rogue finishes; one game ultimately kills Priest.',
    'M284 M381 M372',
    branches=[branch('Repeated Rogue pressure heals back and Rogue is isolated during a renewed Priest commitment.', 'Commit Priest and renew pressure through its late escape.', 'M372', 'low-frequency adaptation')])

add(14, 'low', 'Develop damage on either opponent while constraining the other player’s support and counterpressure.',
    'A renewed Paladin or Shaman commitment causes health loss that persists through short disruption; the initial selection trigger is unknown.',
    'Opening targets are evenly split. Alternating pressure is observed, with both Paladin and Shaman finishes.',
    'Commit the vulnerable target with partner disruption; the corpus cannot rank a universal Paladin-first or Shaman-first plan.',
    'If Paladin heals Shaman or Paladin pressure itself recovers, renew the current target or use a supported switch.',
    'M256 M268 M271 M273 M282 M338',
    'A tied opener and mixed kills do not establish independent default strategies. One Paladin win lacks confirmed Shaman isolation and Shaman escape use.',
    'M358',
    failures=[failure('Both enemies remain healthy enough to continue offense when friendly Priest dies.', 'M279')],
    branches=[branch('One opponent is restored and a later controlled-partner window permits damage to the other.', 'Transfer actual damage, preserving the distinction between control selection and a damage swap.', 'M256 M273 M338')])

add(15, 'low', 'Use initial Mage or Druid pressure to develop a caster finish, with a recurrent Mage-to-Druid transition.',
    'A caster remains vulnerable through renewed control and damage; complete partner isolation and depleted escapes are not universal prerequisites.',
    'Mage is the more frequent opener. If its early damage is blocked or healed, a Druid commitment appears repeatedly.',
    'Often finish Druid after the Mage opening; direct Mage finishes also occur.',
    'Resume damage after Block/healing or transfer to Druid if a real Druid pressure window develops.',
    'M240 M269 M443 M445 M187 M237',
    'Mage-to-Druid is recurrent, not mandatory. Wins occur with ready escapes and active Mage casts; one Druid-first loss cannot prove that opener wrong.',
    'M187 M237 M269 M443 M232',
    failures=[failure('Druid survives the low-health window and recovers; later Mage pressure does not finish before friendly Rogue dies.', 'M232')],
    branches=[branch('Mage opening is stopped by Block or recovery and a Druid commitment becomes available.', 'Transfer damage to Druid.', 'M240 M445')])

add(16, 'low', 'Coordinate player damage with partner and pet disruption, testing a healer commitment without assuming it must finish.',
    'Shaman or Warlock health becomes threatening while control limits recovery and countercontrol; the sample does not identify a single reliable target-selection rule.',
    'Both opening players occur. Shaman commitments include quick direct wins; a failed Shaman window can lead to Warlock pressure with healer control.',
    'Finish the target whose low-health window remains usable; the five wins split between Shaman and Warlock.',
    'After the Shaman recovers, renewed pet/control work can support a Warlock attempt. Pet replacement and recovered Trinkets must be rechecked.',
    'M402 M405 M412 M408 M473',
    'Deep Shaman lows can recover with its Trinket retained, while other Shaman wins retain both escapes. Pet Blind in one record is not Warlock Blind.',
    'M402 M405 M412 M476 M473',
    failures=[failure('The Shaman low occurs after Warlock control ends; Fear/Hex disrupt friendly participation and later trades fail to recreate the opening threat.', 'M476'),
              failure('A Warlock low is healed after main control expires; later pet work does not align with lethal player pressure.', 'M480')],
    branches=[branch('Initial Shaman pressure is healed and a later healer-control window supports Warlock damage.', 'Commit Warlock and renew pressure around current control.', 'M408 M473')])

add(17, 'low', 'Develop Warlock pressure with healer and pet disruption, retaining a Druid-switch possibility.',
    'Warlock or Druid health loss persists through renewed pressure; full partner isolation is useful in some wins but not a proven requirement.',
    'All five records open Warlock; repeated healing and pet interactions precede either a renewed Warlock attempt or Druid commitment.',
    'Usually return Warlock with Druid control; two wins instead finish Druid.',
    'Renew player pressure after heals and pet replacement; avoid treating a transient missing pet as permanent removal.',
    'M310 M318 M449 M235 M333',
    'Five wins without losses and two different kill targets limit certainty. A surviving replacement pet and an active Warlock do not preclude observed wins.',
    'M318 M333',
    branches=[branch('Warlock pressure is restored and a later Druid pressure window forms.', 'Commit Druid through partial recovery; long Warlock isolation is not established in every example.', 'M235 M333')])

add(18, 'low', 'Develop Death Knight pressure while disrupting Priest recovery.',
    'Death Knight health remains low under renewed pressure long enough to finish despite partial heals.',
    'Usually open Death Knight; coordinate renewed pressure with short Priest control or a healing interrupt.',
    'Continue Death Knight through the partial recovery and renew damage/control. All five wins identify Death Knight as the first reported enemy kill.',
    'Repeat Death Knight pressure after partial healing; a Priest opener can transfer to Death Knight.',
    'M143 M193 M199 M201 M212',
    'Five wins and no losses cannot validate failure predictors. Ready Priest Trinket and active Hymn/Penance coexist with winning finishes.',
    'M193 M199 M212')

add(19, 'low', 'Open Fire Mage, then use the revealed Rogue state to choose the next meaningful commitment.',
    'Mage or Rogue health can be driven low while the team still has usable damage and enough survival to finish.',
    'All five records open Mage. Brief Rogue control/pressure can lead to either a Mage return or Rogue commitment.',
    'Finish Mage if pressure remains effective; repeated Rogue finishes follow its exposure and control.',
    'No stable full reset is established. Trades into duels occur, so preserve the distinction between the first kill and the result.',
    'M014 M316 M320 M312',
    'Four of five games come from one batch and share the same displayed opponent pair. The sole loss includes a Mage counter-kill after friendly Priest death.',
    'M314 M312',
    failures=[failure('Friendly Priest dies before the Mage counter-kill; the surviving low-health Rogue loses the duel.', 'M314')],
    branches=[branch('Enemy Rogue is exposed and becomes vulnerable during renewed control.', 'Transfer pressure to Rogue.', 'M312 M320')])

add(20, 'low', 'Develop damage after the stealth/control exchange without sacrificing the team before the window.',
    'Mage or Rogue is low during useful partner disruption; the sample does not resolve a stable preferred opening target.',
    'Both player openings occur; a revealed Rogue can be pressured or controlled before the Mage commitment.',
    'Mage and Rogue kills are equally represented in wins. A repeated Rogue-control/Mage-finish line exists, including continued pressure after Block.',
    'A stable intact-team recovery plan is unknown; two wins require the friendly Priest to win a Mage duel after a Rogue trade.',
    'M108 M352 M130 M348',
    'Only five games, mixed targets, and two trade wins. Mage escape removal alone does not guarantee useful control or survival.',
    'M130 M348 M457',
    failures=[failure('Mage escapes Fear and resumes interference; friendly Priest dies with enemy Rogue still alive around 29%.', 'M457')],
    branches=[branch('Rogue control supports actual Mage damage.', 'Commit Mage and continue after a verified short Block interruption if the window persists.', 'M108 M352')])

add(21, 'low', 'Tentatively develop Paladin pressure during useful Rogue disruption.',
    'A renewed Paladin low overlaps enough Rogue disruption to finish before friendly survival fails.',
    'Paladin is the more frequent opener; one win starts Rogue then transfers to Paladin.',
    'Both wins finish Paladin through renewed pressure after earlier recovery. Evidence is tentative, with more losses than wins.',
    'First Paladin protection/recovery can be followed by another Paladin commitment if the team survives.',
    'M217 M223',
    'Two wins and three losses do not establish a dependable default. Exact Paladin defensives remain unidentified, so no named defensive-removal rule is justified.',
    'M051 M215 M221',
    failures=[failure('Paladin defensive recovery defeats the first burst and friendly Priest dies before a renewed low-health attempt.', 'M215 M221')])

add(22, 'low', 'Tentatively develop Death Knight pressure with Priest disruption, preserving survival after the first kill.',
    'Death Knight health pressure persists through renewed control, followed by a survivable finish against the remaining Priest.',
    'Death Knight is the more frequent opener and every confirmed enemy kill in this sample is Death Knight; Priest opening damage also appears.',
    'Renew Death Knight pressure after heals, then reassess friendly health and the surviving Priest rather than equating the kill with victory.',
    'Repeat Death Knight pressure after healing if the team remains intact; a repeatable safe post-kill recovery is unknown.',
    'M169 M181 M178',
    'Only two wins and three losses from one source batch. One Death Knight kill loses the round to the remaining Priest; an escape is still ready in another win.',
    'M178 M181',
    failures=[failure('Priest healing restores Death Knight before the team survives to a renewed finish.', 'M166 M176'),
              failure('Death Knight dies, but the remaining Priest wins cleanup and the subsequent duel.', 'M178')])

add(23, 'low', 'Tentatively sustain Warrior pressure with Paladin disruption.',
    'Warrior health pressure persists through protection/healing and renewed support disruption.',
    'All four games open Warrior and finish Warrior. A short Paladin branch can draw immunity before returning Warrior.',
    'Renew Warrior pressure; in one explicit protection sequence, Priest damage continues through physical protection and both players recommit afterward.',
    'Return Warrior after a Paladin immunity branch or continue through partial recovery; a universal full reset is not established.',
    'M001 M044 M119 M331',
    'Four wins without losses are too few for a strong default. The physical-protection interaction is one observed case, not a required sequence.', 'M044',
    branches=[branch('Short Paladin pressure is stopped by immunity.', 'Return to Warrior pressure with renewed Paladin disruption.', 'M001', 'low-frequency adaptation')],
    roles={'conversion': {'priest': ('Continue damage during the observed Warrior physical-protection interval.', 'M044'),
                          'rogue': ('Renew Warrior stun pressure after the observed protection interval.', 'M044')}})

add(24, 'low', 'Tentatively develop Rogue pressure while retaining a Paladin switch when the Rogue attempt stalls.',
    'Actual Rogue or Paladin health loss persists through useful partner disruption and friendly survival.',
    'Openers are evenly split; Rogue is the more frequent confirmed kill, but the sample is only four games.',
    'Renew Rogue pressure with Paladin disruption, or commit Paladin if later Rogue control supports actual damage.',
    'Rogue recovery/reappearance can require a renewed attempt; a reliable full reset pattern is unknown.',
    'M309 M313 M363',
    'One Paladin kill and two Rogue kills cannot settle a default target or a mandatory defensive sequence.', 'M311 M313',
    failures=[failure('Rogue survives the low-health window under unidentified protection/avoidance and recovers before friendly Priest dies.', 'M311')])

add(25, 'low', 'Tentatively convert early Warlock contact into meaningful Priest pressure.',
    'Priest health drops under renewed pressure faster than its partial recovery can restore it.',
    'All four records label Warlock as the opener, but some opening damage is absorbed or minimal. A later Priest commitment is the repeated meaningful conversion.',
    'Finish Priest through renewed short control and continued damage; Warlock can be active near the final kill.',
    'Repeat Priest pressure after a healed first window; pet interactions vary and permanent removal is not established.',
    'M179 M182 M183 M184',
    'All four wins come from one source batch. This is a tentative pattern; Priest escape removal, permanent Warlock control and pet death are not established prerequisites.',
    'M179 M183 M184')

# Responsibilities are only populated when the narrative names the friendly actor.
DECISIONS[1]['roles'] = {
    'conversion': {'priest': ('Mass Dispel attempts are observed against Paladin immunity, with variable apparent success. Base the next commitment on the actual immunity ending, not merely the cast attempt.', 'M032 M046 M456')},
    'recovery': {'priest': ('Use the observed healing opportunities to stabilise; friendly Priest healing/Divine Hymn appears between attempts or after the first kill. A mandatory cooldown schedule is unknown.', 'M096 M444 M456')}
}
