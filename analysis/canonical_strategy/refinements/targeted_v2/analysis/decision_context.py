"""Manually reviewed first healer-branch states. Unknown is not absence.
P = first healer commitment after a damage-opener in W. The time of the first P
episode is the reference point, not the final kill. 'during' locates the reported
spend during that commitment and does not assert availability throughout its lead-in.
"""
from review_annotations import REVIEWS
FIRST_SWITCH = {}
def rows(key, text):
 for line in text.strip().splitlines():
  alias,damage_escape,healer_escape,healed,control,note=line.split('|',5)
  FIRST_SWITCH[alias]={'strategy_key':key,'damage_opponent_trinket_at_first_healer_commitment':damage_escape,
   'healer_trinket_at_first_healer_commitment':healer_escape,'substantive_damage_opponent_pressure_healed_before_switch':healed,
   'partner_control_timing':control,'chronological_basis':note,
   'scope':'First P episode among matches containing W; not a final-kill state or a full cooldown timeline.'}
rows('SPR_vs_Arms_HPal','''
M006|spent_before|spent_before|unknown|overlap_order_unknown|Warrior 65 / Paladin 68; switch108; Blind113 follows switch.
M023|spent_before|spent_during|unknown|unknown|Warrior94 before Paladin115.5; Paladin124 during; later defenses and returns separate.
M024|spent_before|spent_before|yes|after_switch|Both86.5; Warrior healed full; switch113 then Blind117.
M026|spent_before|spent_before|yes|unknown|Both66/66.5 precede first Paladin110; first Warrior-control application not established.
M032|spent_before|spent_before|unknown|overlap_order_unknown|Warrior71/Paladin74 precede first Paladin93; later Warrior recovered escape belongs to final return.
M046|spent_before|spent_before|yes|before_switch|Warrior94/Paladin100; Warrior Blind108 then Sap110 precede Paladin124.
M052|spent_before|spent_during|yes|before_switch|Warrior94; first Paladin swap follows Warrior control; Paladin139 during earlier healer commitment, not before all attempts.
M053|unknown|unknown|yes|overlap_order_unknown|Initial Warrior65 cannot be carried to first timed Paladin230; second Warrior273 belongs to later cycle.
M056|spent_before|unknown|yes|ended_before_switch|Warrior93.5; Gouge159–163 precedes Paladin165–167 but has ended; Blind application unconfirmed.
M057|spent_before|spent_before|yes|before_switch|Warrior80.5/Paladin113; Fear152 precedes Paladin156 and ends near transition; Kidney156.5 follows.
M058|spent_during|spent_before|yes|overlap_order_unknown|Paladin133 before short Paladin158–161; Warrior161 during it. Gouge173.5 pertains to later attempt.
M063|spent_before|unknown|yes|after_switch|Warrior94.5; first Paladin161 then Warrior Fear162. Renewed escapes in later cycle.
M070|ready|ready|no_deep_prior_attempt|overlap_order_unknown|Warrior engagement57–59.5 is brief; both escapes retained through Paladin death. Warrior Kidney59.5 overlaps Paladin59.
M072|ready|unknown|no_deep_prior_attempt|before_switch|Warrior Kidney85–90; Priest Paladin damage86, Rogue return90.5; Warrior escape explicitly ready until160.
M076|spent_before|spent_before|unknown|overlap_order_unknown|Both87.5; friendly Priest Mind Control104–107 overlaps brief Paladin damage.
M077|unknown|ready|no_deep_prior_attempt|unknown|Warrior62 then Paladin65; first reported Warrior spend128 is much later; Paladin retains escape until188.
M079|unknown|unknown|no_deep_prior_attempt|before_switch|Warrior control82.5/85 precedes Paladin85.5; both late spends148/150.5 do not establish first-switch depletion.
M081|unknown|ready|no_deep_prior_attempt|overlap_order_unknown|Split opener with1% Warrior damage; Paladin63; Paladin retains escape until135. Warrior spend110 belongs to later branch.
M083|unknown|spent_before|yes|before_switch|Paladin56; Warrior Fear113–121 before Paladin115. Warrior spend157.5 is in later Warrior attack.
M085|unknown|spent_during|unknown|unknown|Paladin61–66 before Paladin71 escape in same early pressure episode; Warrior116 is later.
M087|unknown|ready|no_deep_prior_attempt|after_switch|Warrior50 then Paladin52, Warrior Fear55; Paladin retains escape through death.
M096|unknown|spent_before|unknown|unknown|Paladin52.5 before Rogue Paladin63–65; Warrior110.5 is after Shield/Warrior return.
M097|spent_before|spent_before|yes|after_switch|Both80/105.5 before Paladin127; Warrior initially free, Blind133.5 later.
M099|ready|unknown|no_deep_prior_attempt|overlap_order_unknown|Warrior66 then Paladin69 with Warrior stun69; Paladin escape91 belongs to post-Shield return.
M117|spent_before|spent_during|unknown|unknown|Warrior49–50; Paladin escape55 coincides with sustained Paladin pressure.
M126|spent_before|spent_before|yes|overlap_order_unknown|Warrior84/Paladin105; Warrior11% heals91%; Sap covers Paladin decline but precise switch-vs-Sap order unrecorded.
M127|spent_during|unknown|no_deep_prior_attempt|overlap_order_unknown|Brief Warrior then Paladin before60; Warrior64–65 and Blind65 during healer pressure; Paladin83–85 later.
M131|spent_before|spent_before|yes|before_switch|Both269–270; Warrior heals97%, friendly Rogue recovers and Warrior re-Sap precedes Paladin313.
M140|spent_before|ready|yes|overlap_order_unknown|Warrior54, healed full70; Paladin90, Warrior Sap visible95; precise initial application unknown.
M142|spent_during|unknown|no_deep_prior_attempt|overlap_order_unknown|Warrior98–100% before Paladin90; Warrior104 during ongoing healer sequence, not before initial choice.
M180|unknown|unknown|no_deep_prior_attempt|before_switch|Warrior stun77 before Paladin79; Warrior111/Paladin141 spends occur after first healer/immunity branch.
M186|unknown|spent_before|no_deep_prior_attempt|before_switch|Paladin61; renewed Warrior control61 before Paladin62; Warrior115.5 during final return.
M213|spent_before|spent_before|yes|before_switch|Paladin59/Warrior65.5; Warrior recovery before Blind93 and Paladin98.
M227|coincident|unknown|unknown|after_switch|Warrior escape and Paladin pressure56, Blind57; Paladin80 after first protection.
M229|ready|ready|no_deep_prior_attempt|before_switch|Warrior chip90%; Warrior Sap75–83 before Paladin80; both escapes retained.
M317|unknown|spent_during|no_deep_prior_attempt|before_switch|Warrior near full; Fear87.5 before Paladin90.5; Paladin97 during it.
M321|spent_before|spent_before|yes|unknown|Both61–61.5 before first brief Paladin test77–94; Warrior protection precedes branch, Blind90 joins later.
M327|spent_during|ready|unknown|ended_before_switch|Warrior control90–92.5 before Paladin93; Warrior96 during healer pressure. Paladin ready throughout.
M329|spent_before|ready|yes|unknown|Warrior73/protection77–89 before Paladin112; later Warrior Blind134.5 cannot be initial trigger.
M342|spent_before|spent_before|unknown|after_switch|Both70/75 before Paladin88; Blind92 follows; second sequence kept separate.
M357|spent_before|unknown|unknown|unknown|Warrior43 before Paladin selection51/damage57; no confirmed Warrior control55–64.
M374|unknown|spent_before|unknown|after_switch|Paladin43 before first Paladin82; Warrior Fear91 follows; Warrior159 belongs to later cycle.
M376|spent_before|spent_before|yes|unknown|Both49/50; actual first Paladin99, not earlier selection87; final Blind145 not assigned to first choice.
M387|spent_before|spent_before|unknown|overlap_order_unknown|Both47/49; first Paladin and Warrior Blind begin73. Later fresh escapes174/204 separate.
M390|spent_before|spent_before|yes|after_switch|Both51/61; shallow Paladin76, Blind77; final Warrior return differs.
M401|ready|unknown|no_deep_prior_attempt|before_switch|Warrior98% controlled before Paladin86.5; source explicitly early attempt with Warrior escape ready. Paladin120 later.
M414|unknown|unknown|no_deep_prior_attempt|unknown|Paladin74 before both reported spends101/104; no inferred unavailable state from future events.
M444|spent_before|spent_before|unknown|overlap_order_unknown|Both89 then Paladin93–99 with Warrior controlled; no precise lead time given.
M472|ready|spent_before|yes|after_switch|Paladin58, Warrior healed full and escape ready; Paladin95, Warrior Fear101.
M474|ready|spent_before|no_deep_prior_attempt|before_switch|Paladin68; Warrior Fear75 precedes deep Paladin attempt/Shield86.5; Warrior escape remains ready then.
M475|spent_before|ready|unknown|before_switch|Warrior61 then Blind82 preceding observed Paladin decline86–87; Paladin retains Trinket through Shield88.
M479|spent_before|spent_during|yes|after_switch|Warrior55.5 healed full81; Paladin86 then Blind92, Paladin escape94.5 during attempt.
''')
rows('SPR_vs_SP_Sub','''
M021|spent_before|spent_during|unknown|before_switch|Rogue69.5; Blind79 then Priest80; Priest81.5 during attack.
M078|spent_before|spent_during|yes|before_switch|Rogue75.5; disengagement/recovery; Blind99 then Priest pressure, Priest106 during it.
M084|unknown|spent_during|unknown|unknown|Rogue opener75 then Priest80/escape81; Rogue97 belongs to later cycle.
M086|spent_during|spent_during|unknown|before_switch|Rogue Blind82, Priest pressure85; Rogue escapes88 and Priest95.5 during it.
M103|spent_before|spent_during|unknown|before_switch|Rogue64; Blind77 then Priest78; Priest85 during it.
M125|spent_before|spent_during|yes|overlap_order_unknown|Rogue95 then Hymn recovery; Rogue Blind and Priest branch125, Priest escape125.
M147|spent_before|spent_during|no_deep_prior_attempt|after_switch|Rogue78 before Priest80; Priest84 and Rogue Blind visible90 later.
M189|unknown|spent_before|no_deep_prior_attempt|before_switch|Priest77, Rogue control82–89.5; Priest84.5; Rogue spend100 is cleanup only.
M190|spent_during|unknown|yes|after_switch|Priest135.5; Blind138.5 then Rogue escape140.5, enemy Priest full at failure.
M192|spent_before|spent_before|no_deep_prior_attempt|overlap_order_unknown|Priest40/Rogue53; Priest already49% before Rogue selects Priest55; new Rogue control simultaneously.
M194|spent_before|spent_before|yes|unknown|Priest40/Rogue60–67 and Hymn; first Priest67–88 later heals.
M195|unknown|spent_before|yes|unknown|Priest120; actual Priest144–167; Rogue184 is later return.
M200|unknown|spent_before|yes|unknown|Priest88, Rogue heals97%; Priest132–139; Rogue147 is post-death.
M202|spent_before|spent_before|unknown|overlap_order_unknown|Priest80/Rogue88; Priest94–108 with brief Rogue control of unresolved onset.
M203|ready|spent_before|no_deep_prior_attempt|unknown|Priest88; Rogue7% and escape ready before Priest89 switch; avoidance/disarm not confirmed incapacitation.
M205|spent_before|spent_before|unknown|before_switch|Both72; Blind/Sap Rogue90–109.5 precedes Priest96; first stun has little damage.
M210|spent_before|spent_before|yes|unknown|Rogue74/Priest75 before Priest94; Blind macros unconfirmed.
M220|spent_before|spent_before|unknown|unknown|Priest88/Rogue98 before Priest102; exact preceding Rogue isolation not established.
M224|spent_before|coincident|unknown|after_switch|Rogue115; Priest121 near onset of Priest damage; Rogue Blind130 follows healing.
M226|spent_before|ready|yes|unknown|Rogue110 then low Rogue recovers; brief Priest pressure135 before Rogue return150; Priest escape ready through finish.
M246|unknown|spent_before|no_deep_prior_attempt|before_switch|Rogue3% chip before substantive Priest100; Priest86, Rogue Fear described before Priest commitment; Rogue120.5 later.
M265|spent_during|spent_before|no_deep_prior_attempt|before_switch|Priest101; Rogue Fear/Sap precedes brief Priest pressure115–118; Rogue escapes117 during it.
M267|spent_before|spent_before|yes|after_switch|Priest71/Rogue92 then Hymn; Priest105, Rogue Gouge118 later.
M285|ready|spent_during|no_deep_prior_attempt|unknown|Rogue chip133; Priest135–144 draws escape144; Rogue escape ready through later kill.
M286|unknown|spent_during|no_deep_prior_attempt|unknown|Rogue contact109, substantive Priest115 draws escape122; Rogue125 return later.
M291|unknown|spent_before|no_deep_prior_attempt|unknown|Priest95; shallow Rogue damage then Priest99–110; Blind macros unconfirmed.
M293|spent_during|unknown|no_deep_prior_attempt|unknown|First damage99 on both, Priest58%109; Rogue119 occurs during healer sequence, Priest146 only later.
M296|spent_during|spent_before|no_deep_prior_attempt|after_switch|Priest47; Priest59–60 before Rogue Gouge63/Fear69.5; Rogue71.5 then Blind during it.
M298|spent_during|spent_before|no_deep_prior_attempt|unknown|Priest79, Priest damage81; Rogue88 during it; no preceding long Rogue isolation established.
M300|spent_before|spent_during|yes|before_switch|Rogue143; Blind159 before Priest162, Priest165 during it.
M302|unknown|spent_before|yes|before_switch|Priest67; Rogue Gouge81–86 immediately precedes Priest87; Blind89 after friendly death.
M303|unknown|spent_before|yes|unknown|Priest85; healed Rogue contact then Priest92; Rogue Gouge106 joins late and Blind after death.
M339|unknown|spent_during|unknown|unknown|Rogue91–96 then Priest; precise first switch vs Rogue100/Blind101 unresolved; Priest104 during it.
M383|spent_before|spent_during|yes|absent_as_recorded|Rogue106; enemy Rogue explicitly free130–155.5; Priest136, escape142.5.
M386|unknown|ready|yes|unknown|Rogue141 healed, Priest175–184 shallow; Rogue198–199 during later return, Priest ready.
M416|unknown|spent_before|no_deep_prior_attempt|unknown|Priest91, absorbed Rogue95–101 then Priest102; Rogue127 belongs to later return.
M419|spent_before|spent_during|no_deep_prior_attempt|after_switch|Rogue79; Priest86 then Priest93; confirmed Rogue Blind94, earlier macros unconfirmed.
M428|spent_before|spent_before|unknown|unknown|Priest73/Rogue81 before first Priest82–87; Priest Blind87 is on damage target near branch end.
''')
rows('SPR_vs_Disc_Feral','''
M054|spent_before|spent_during|yes|unknown|Feral77 then low-health recovery; Priest92–99 and escape100; Priest Blind100.5 supports return Feral.
M308|spent_before|spent_before|yes|unknown|Priest126.5/Feral134 before Priest155; later Cyclone161–165 interrupts friendly Rogue.
M319|unknown|unknown|unknown|unknown|First brief Priest attack embedded in62–95 mixed series; exact timing/resources unknown, later escapes164/182.5 separate.
M382|spent_before|spent_during|yes|before_switch|Feral55 and full recovery75; Blind85/Sap94 before actual Priest99; Priest102 then restun.
M392|unknown|ready|no_deep_prior_attempt|before_switch|Feral95% then stun87; Priest87.5 with ready escape; Feral spend101 is cleanup, no pre-kill depletion asserted.
M432|unknown|spent_during|no_deep_prior_attempt|before_switch|Feral98% before Fear99; Priest101, escape110 during commitment.
M438|spent_before|unknown|yes|before_switch|Feral92.5 and healing before Blind128 and joint Priest switch; Priest escape unobserved, not assumed ready.
M439|ready|ready|no_deep_prior_attempt|before_switch|Absorbed Feral opener, Fear56 before Priest56.5; both escapes ready throughout.
M451|ready|spent_during|unknown|overlap_order_unknown|Feral attack68–72 then Priest/Gouge Feral72.5; Priest77.5 during attack; Feral escape ready through duel.
M454|ready|ready|no_deep_prior_attempt|before_switch|Shallow Feral with stun59.5–64 before Priest61.5; both escapes ready. Later split damage separate.
''')

# Explicitly bounded comparisons supplement first-switch coverage; these are examples,
# not the set of all opportunities. They attach to a specified existing episode.
EXTRA = {
 'M090:4':('After Shield ends174.5: Warrior controlled and Paladin escape still unavailable; both have recovered.','Warrior: spent149.5; Paladin: spent68.5, still unavailable176, recovered188.5.','Continue Warrior; no Paladin return despite this state.'),
 'M079:4':('Both escapes just spent148/150.5; Warrior Fear, but friendly Priest nearly mana-empty and critically low.','Warrior: spent during this late interval; Paladin: spent during same interval.','Damage stays Warrior; survival fails before healer return.'),
 'M321:4':('Fresh Warrior escape193 and friendly Rogue First Aid/recovery202 precede Paladin212.5.','Warrior: spent_before; Paladin: recovered181–182, spends during at217.','Blind216.5 joins after switch; Kidney218 follows Paladin escape, Silence224.5.'),
 'M122:4':('Previous Paladin attempt has healed; fresh Warrior Sap236 extends new healer attack.','Warrior: second use203 still unavailable; Paladin: recovered and ready235–239.','Paladin kill despite recovered healer escape.'),
 'M032:4':('Paladin post-Shield return185–186 under Warrior stun185–190.','Warrior: unavailable at start, recovered191 before kill; Paladin: unavailable through death.','Warrior recovery does not erase earlier stun coverage or stop observed kill.'),
 'M475:4':('Shield has ended; renewed Warrior Fear supports Paladin stun before escape113.5.','Warrior: earlier61 spend; Paladin: spends_during113.5 then immediately restunned.','Paladin remains74–83%, heals93%; the extraction/restun did not recreate the low window.'),
 'M048:1':('Paladin Sap already applied; Warrior attack starts46 before either escape.','Warrior and Paladin: both spend_during at55 near Warrior death55.5.','Immediate Paladin Horror after escape supports staying Warrior.'),
 'M322:2':('Warrior repeatedly below30% after partial healing; renewed stun then Kick128.5.','Warrior and Paladin: both ready throughout.','Same-target continuation under a heal interruption, no mandatory healer switch.'),
 'M208:2':('Rogue2% then recovers18% during enemy Hymn100–106.','Enemy Rogue/Priest: both ready; enemy Hymn actively healing.','Continued Rogue damage kills105; recovery does not dictate Priest switch.'),
 'M337:1':('Enemy Priest Sap91–96 before Rogue damage96; Silence100–106 follows.','Enemy Rogue/Priest: both ready.','Direct Rogue attack converts without escape extraction.'),
 'M292:1':('Enemy Priest escape57, confirmed Priest Blind63–73; Rogue pressure starts66.','Enemy Priest: spent_before attack; enemy Rogue: spends_during at73.','Rogue stays roughly95–100% through Blind; isolation alone fails to produce damage.'),
 'M417:2':('Both enemy escapes spent; renewed Priest attack80 under Rogue Fear only until82.5.','Enemy Priest: spent63; enemy Rogue: spent72; Blind after82.5 not confirmed.','Priest reaches8–9% only after Rogue control expires; friendly Priest dies86.'),
 'M419:4':('Confirmed Dispersion99–104.5 has ended; Rogue Blind94 replaced by Sap103.5.','Enemy Rogue: spent79; enemy Priest: spent93; Dispersion ended before Horror105.','Priest Horror and damage resume after protection; final attack distinct from initial switch86.'),
 'M307:4':('Repeated Feral attack healed; Feral escape142.5 followed by confirmed Blind144 and Sap154.','Feral: spent_before; Priest: ready through kill.','Joint Priest commitment after known Feral isolation, with partial healer recovery overcome.'),
 'M326:5':('Friendly Rogue Cyclone129.5–135.5 ends; Feral healed15% to42%; friendly Priest has continued pressure.','Feral: spent99; Priest: spent131; Kick135.5 then confirmed Priest Gouge139.5.','Resume Feral stuns140.5, kill142.5; Cyclone interruption did not force a healer switch.'),
 'M448:2':('Feral20% healed65%; fresh Priest Sap110–115.5 precedes repeated Feral attack.','Both enemy escapes ready; Priest free Penance115.5–117; Feral stun119.5 follows.','Stay Feral and finish121 after healer control ended.'),
 'M453:3':('Feral repeatedly healed, friendly Rogue restored103.5; renewed Feral stuns113.5/119.','Feral: spent98.5; Priest: ready; Gouge120.5 joins during burst.','Same-target Feral finish after friendly recovery, not automatic healer swap.')
}

def enrich():
 for alias, row in FIRST_SWITCH.items():
  review=REVIEWS[alias]; specs=review['episodes'].split(';'); i=next(j for j,s in enumerate(specs,1) if s.startswith('P:'))
  review['context'][str(i)]={'before':row['chronological_basis'],'resources':row}
 for ref,(before,resources,response) in EXTRA.items():
  alias,i=ref.split(':'); REVIEWS[alias]['context'][i]={'before':before,'resources':{'chronology':resources,'observed_response':response,'basis':'reviewer_annotation_of_source_chronology'}}
 # A recorded victory/kill alone does not prove the ordering of friendly deaths.
 # Retain explicit trade/solo classifications; make gaps in remaining wins visible.
 explicit_both_alive=set('M036 M048 M070 M083 M085 M087 M088 M091 M098 M099 M227 M229 M321 M322 M327 M329 M334 M335 M431 M067 M071 M084 M092 M202 M218 M226 M228 M230 M234 M239 M241 M244 M246 M255 M257 M337 M428 M429 M430 M054 M236 M245 M248 M323 M325 M326 M448'.split())
 for alias,r in REVIEWS.items():
  if r['death']=='enemy_before_friendly' and alias not in explicit_both_alive:
   r['death']='enemy_death_confirmed_friendly_order_unknown'
