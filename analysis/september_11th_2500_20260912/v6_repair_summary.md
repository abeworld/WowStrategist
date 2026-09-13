# V5 → V6 repair — September 11 batch

Repaired all 40 existing game records using the full current V6 instructions, V5 JSONL, exceptions, manifests/validation and saved visual evidence. No MP4 was reopened; no cross-match synthesis was performed. Original V5 files remain unchanged.

Every record now has `enemy_resources_spent`; `resources_forced` contains only its pressure/control-linked subset. Important confirmed offensive Mind Control/Hex uses and unattributed post-kill trinkets are spent-only. Announcement-only enemy Blinds remain supporting attempts, not confirmed cooldown expenditure. Ordinary heals, interrupts, availability statements and pet removal itself are not automatically cooldown spends; visible Penance/Hymn and pressure-linked mana/resummon cast time are retained when strategically significant. Unknown defensive names remain unknown.

All conditions were checked as pre-kill states. Losses 028 and 034 now have `win_condition_obtained = true`; losses 017 and 018 remain false because their required overlaps never existed. Objectives below are explicitly supported in `inferred`, not presented as directly proven intent. Unresolved objectives remain `unknown`.

Material changes (suffixes of `sep11_2500_match_…`; all rows also receive the resource-field split):

| Record | Change and evidence reason |
|---|---|
| 001 | Infer Feral-control purpose; move the post-kill Feral trinket to spent-only because causal attribution is unclear. |
| 002 | Infer extended Priest isolation; preserve that Warrior trinket follows the initial swap. |
| 003 | Keep mana depletion as pressure-linked spend; remove unsupported named Gouge application. |
| 004 | Infer Priest escape extraction; Polymorph announcements remain attempts, not proven applications. |
| 005 | Infer renewed Warrior window; favourable state precedes healer control expiry. |
| 006 | Infer Sap-trinket-Blind isolation; reported enemy Blind is attempt-only; restealth is a state, not proven Vanish. |
| 007 | Infer repeat Feral window after escape extraction; brief Priest control is not a proven intended kill swap. |
| 008 | Replace finish wording with a pre-death Fear/low-health state; retain unknown defensive name. |
| 009 | Infer Mage-control purpose; trinkets are spent after the initial Priest switch. |
| 010 | Infer repeated healer isolation; preserve Paladin trinket recovery at final commitment. |
| 012a | Infer Warlock-control setup for Shaman; replace lethal-damage tautology and preserve unused trinkets. |
| 013 | Infer renewed Warrior window; define reduced-health stun plus interrupted heal before death. |
| 015 | Infer deliberate Blind extraction before damage; replace lethal-health wording with renewed control state. |
| 016 | Replace lethal-damage wording with overlapping Shaman control/Warlock Fear; no pet kill inferred. |
| 017 | Infer pet-removal purpose but retain inferred death; add confirmed Mind Control spent-only; confidence medium. |
| 018 | Infer Hunter-Blind isolation objective; condition stays false because health pressure starts after Blind; remove non-use from spent. |
| 019 | Replace pet-removal bucket with visible resummon cast-time spend; add Hex spent-only; opening purpose stays unknown. |
| 020 | Define low Hunter plus Priest-stun state; conflicting chat does not establish opening purpose. |
| 021 | Infer sustain/escape extraction; add documented mana expenditure and remove availability-only bucket. |
| 022 | Keep initial pet purpose unknown; track WOTF separately and include pressure-linked Penance use. |
| 023 | Infer Shaman escape/support denial; off-target pet Blind remains distinct from Warlock CC. |
| 024 | Infer Hunter escape extraction for Priest switch; condition exists before Blind expires, not throughout kill. |
| 025 | Infer repeated Paladin-isolation purpose; unknown defensive names remain unknown. |
| 026 | Infer Hunter-Blind recovery purpose; favourable state is renewed same-target pressure after recovery. |
| 027 | Infer initial Priest-trinket/Blind setup for Rogue; preserve later Priest-switch branch and Hymn. |
| 028 | Condition false -> true at ~80-82s despite loss; Fear expires before finish and Blind is unconfirmed; add later Mind Control spent-only. |
| 029 | Infer Blind escape-extraction branch; preserve WOTF distinction and Blind expiry before Priest kill. |
| 030 | Infer Rogue escape extraction; define post-Dispersion state; early Blind reports remain attempt-only. |
| 031 | Define health-exposure plus Priest-control state; Hunter trinket ready, Priest racial tracked separately. |
| 032 | Replace kill tautology; post-death Priest trinket spent-only; enemy Blind report stays attempt-only. |
| 033 | Define denied late heal before death; interrupt/non-use are not resources spent; retain Penance. |
| 034 | Condition false -> true at ~76-78s despite loss; Priest free before near-kill; enemy Blind report attempt-only. |
| 035 | Infer renewed Hunter escape/control window; confirmed offensive Mind Control spent-only. |
| 036 | Infer escape extraction and later isolation; replace action sequence with pre-kill state. |
| 037 | Define first favourable Rogue window before trade; Blind report attempt-only; confidence medium for inferred final Priest conversion. |
| 038 | Infer repeated Warrior window; replace conversion actions with stun/Fear state and include Penance recovery. |
| 039 | Infer Rogue extraction for later Priest branch; replace successful-finish wording with low Priest under off-target Fear. |
| 040 | Infer renewed Rogue window; condition excludes immediate Blind break and later Priest cleanup. |
| 041 | Infer Priest escape extraction for healer isolation; enemy Blind report attempt-only; cleanup Mind Control spent-only. |
| 042b | Replace damage-exceeds-health tautology with reduced-health renewed-stun state; empty spent/forced arrays, trinkets unused. |

Confidence self-check: 38 high/analysed, 2 medium/uncertain (017: principal pet-removal event inferred; 037: final Priest conversion inferred). Both conversion-failed losses retain high confidence because the favourable windows, their expiry and first friendly deaths are clear; missing fatal-GCD detail does not change that interpretation. Existing exclusions and valid observations, IDs, source names, results and game boundaries are preserved.

Validation: 42 source files, 44 manifest segments, 40 unique valid games/JSONL lines, 4 excluded abnormal rounds (011, 012b, 014, 042a), zero excluded/non-2v2 records admitted. The exclusions inside sources 012 and 042 remain separate from valid 012a and 042b. Results remain 36 wins/4 losses. The source folder is already archived under `output/done`; filenames and sizes are checked against the original inventory, without reopening footage. See `validation_v6.json` for checks/input hashes and `v6_repair_changes.json` for exact before/after values. Original `exceptions.md` remains a historical V5 report; this summary and the V6 manifest record the repairs.

Limits: saved frame sampling provides approximate times, not a combat log. Unconfirmed CC applications, pet-death instants, named defensive abilities and death-versus-departure endings stay qualified. No matchup-wide rules were derived.
