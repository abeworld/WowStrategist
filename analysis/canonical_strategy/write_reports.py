"""Build readable navigation and the review queue from the serialized package."""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    p = json.loads((OUT/'strategies.json').read_text(encoding='utf-8'))
    ss = p['strategies']
    confidence = collections.Counter(s['evidence']['confidence'] for s in ss)
    by_group = {s['provenance']['review_group']: s for s in ss}
    def link(g, label=None):
        s = by_group[g]
        return f"[{label or s['enemy_comp']}](cards/{s['strategy_id']}.md)"
    lines = [
        '# Canonical strategy corpus · version 1.0.0', '',
        'Created 13 September 2026. **49 matchup objects and cards cover all 468 composition-resolved games.** Another 19 valid games remain separate because compositions are unresolved.', '',
        '**26 provisional strategy interpretations:** 6 medium confidence and 20 low confidence. **23 insufficient-evidence cards.** No high-confidence or human-approved strategies are claimed.', '',
        'All resolved evidence is **Shadow Priest / Subtlety Rogue**. There is no identified Discipline Priest / Subtlety Rogue sample, so no Discipline strategies were inferred.', '',
        '[Read all matchup cards](ALL_MATCHUP_CARDS.md) · [Review queue](03_REVIEW_QUEUE.md) · [Machine-readable strategies](strategies.json) · [Contract](02_SCHEMA.md) · [Verification](VALIDATION.json)', '',
        '## Evidence and limits', '',
        '- Input gate: READY_WITH_KNOWN_GAPS; independent count/group checks passed.',
        '- Valid corpus: 487 games, 394 wins / 92 losses / 1 unknown result. Resolved subset: 468 games, 378 wins / 89 losses / 1 unknown result.',
        '- Original VODs were not reopened. Source extraction uncertainty, repaired records, repeated opponents and selected footage limit interpretation.',
        '- Dedicated role fields are empty; Priest/Rogue guidance is mostly unknown. A few explicit friendly-actor narratives support limited guidance.',
        '- Read-only target reconciliation and removal of explicit non-kill labels are documented; input files remain unchanged.',
        '- Automatic addon detection is untested. Strategies are independent of runtime feasibility.', '',
        '## Strongest repeated findings', '',
        f"- {link(1)}: Warrior is the labeled opener in **69/80** games. The 66 wins include **38 Paladin kills, 27 Warrior kills and 1 unconfirmed kill**. Use a flexible pressure/conversion line; neither a compulsory Paladin swap nor double-Trinket removal fits all wins.",
        f"- {link(0, 'Shadow/Subtlety mirror')}: Rogue is the labeled opener in **76/104** games, but the 67 wins split into **32 Rogue kills, 29 Priest kills and 6 unconfirmed kills**. Both conversion targets recur; survival and actual health pressure matter more than an assumed fixed target.",
        f"- {link(2)}: Feral is opened in **25/31** games; the 29 wins finish **18 Ferals and 11 Priests**. Renewed Feral pressure and a supported healer-switch option both belong in the model.",
        f"- {link(13)}: all **7 wins** identify Shaman as the enemy killed. This is the clearest repeated kill-target pattern among the three validation cases, but the single loss cannot establish causality or resource prerequisites.",
        f"- {link(12)}: **6/9** games open Priest while **8/9** wins identify Rogue as the enemy killed. Opening target and eventual kill target must remain separate.",
        '- Across several matchups, a first low-health attempt heals back before a later conversion. “Reset” often means stabilization and renewed pressure, not necessarily a full stealth disengage.',
        '- Confirmed kills occur in losses, and some wins have no confirmed death. The round result and individual kill evidence are never treated as interchangeable.', '',
        'These counts describe selected records, not expected win rates, conditional kill probabilities or proof of strategic intent. [Method and limitations](01_SYNTHESIS_METHOD.md) · [Ordered examples](04_SEQUENCE_REVIEW.md).', '',
        '## Highest-value Gary review', '',
        f"Start with {link(1)}, {link(0, 'the mirror')}, {link(4)}, and {link(3)}: large or important samples still leave target-selection triggers unresolved. Then review pet/player timing against {link(7)} and {link(16)}, and the repaired evidence concentration in {link(8)}.", '',
        '**Berserker Rage remains of unknown strategic relevance against Arms/Holy and is omitted from the concise plan.**', '',
        '## Coverage', '',
        '| Enemy composition | Games | W/L/? | Confidence | Status |',
        '|---|---:|---:|---|---|']
    for s in ss:
        e=s['evidence'];g=s['provenance']['review_group']
        lines.append(f"| {link(g)} | {e['total_games']} | {e['wins']}/{e['losses']}/{e['unknown_result']} | {e['confidence']} | {s['status'].replace('_',' ')} |")
    lines += ['', '## Provenance', '', f"Prepared snapshot: `{p['prepared_corpus_version']}`.", '',
              'The complete input file fingerprints are in [input_fingerprints.json](evidence_review/input_fingerprints.json). Each strategy retains its source matchup file, original statistics, all record IDs and specific supporting/challenging examples. The 19 unresolved records remain in [unresolved_matches.json](unresolved_matches.json).', '']
    (OUT/'00_CORPUS_SUMMARY.md').write_text('\n'.join(lines), encoding='utf-8')
    high=[1,0,4,3,7,8,16,22]
    queue=['# Gary review queue', '', 'All entries remain provisional or insufficient. Priority measures the value of human review, not confidence or urgency to approve. All listed matchups use Shadow Priest/Subtlety Rogue on our side.', '',
           '## High priority', '', '| Matchup | Evidence | Decision to review |', '|---|---|---|']
    for g in high:
        s=by_group[g];e=s['evidence']
        queue.append(f"| {link(g)} | {e['total_games']} games; {e['confidence']} | {s['uncertainties'][0]} |")
    queue += ['', 'For Arms/Holy, compare M026/M321 (covered healer conversion), M322/M431 (Warrior wins with both escapes ready), M475 (failed post-immunity recreation) and M053 (Paladin kill but round loss). In the mirror, compare M103/M205 with M337/M421 and M417/M423. [Reference map](evidence_review/match_references.json).', '',
              '## Medium priority', '', '| Matchup | Evidence | Decision to review |', '|---|---|---|']
    for s in ss:
        g=s['provenance']['review_group'];e=s['evidence']
        if g in high or s['status']=='insufficient_evidence':continue
        queue.append(f"| {link(g)} | {e['total_games']} games; {e['confidence']} | {s['uncertainties'][0]} |")
    queue += ['', '## Low priority: collect evidence before choosing a default', '',
              'These groups contain one to three records. Read their observations if useful, but prioritize additional games and losses over polishing a speculative plan.', '', '| Matchup | Games |', '|---|---:|']
    for s in ss:
        if s['status']=='insufficient_evidence': queue.append(f"| {link(s['provenance']['review_group'])} | {s['evidence']['total_games']} |")
    queue += ['', '## Cross-cutting review', '',
              '- Obtain identified Discipline/Subtlety evidence before adding that friendly composition.',
              '- Clarify Priest and Rogue responsibilities from actor-visible footage, especially opener coordination, recovery and trade cleanup.',
              '- Resolve the 19 composition-uncertain games before assigning them to a canonical matchup.',
              '- Preserve corrections as extraction error, interpretation error, incorrect generalization, missing branch or mechanics misunderstanding; recheck the source before changing a strategy.',
              '- Give future approved revisions new versioned IDs and preserve their predecessors.', '']
    (OUT/'03_REVIEW_QUEUE.md').write_text('\n'.join(queue), encoding='utf-8')
    cards=['# All matchup cards', '', 'Shadow Priest / Subtlety Rogue · version 1 · provisional or insufficient evidence. Evidence counts describe the selected footage; unknown means the corpus does not establish a reliable instruction.', '',
           '[Summary](00_CORPUS_SUMMARY.md) · [Review queue](03_REVIEW_QUEUE.md)', '']
    for s in ss:
        card=(OUT/'cards'/f"{s['strategy_id']}.md").read_text(encoding='utf-8')
        cards.append(card.replace('# Shadow Priest / Subtlety Rogue vs ', '## ').replace('(../strategies/', '(strategies/').replace('(../evidence_review/', '(evidence_review/'))
        cards += ['---', '']
    (OUT/'ALL_MATCHUP_CARDS.md').write_text('\n'.join(cards), encoding='utf-8')
    questions=['# Unresolved strategy questions', '',
        '1. Which observable positioning, race, timing or health cues select the first conversion target in Arms/Holy and the mirror? The current corpus shows several outcomes without a reliable universal trigger.',
        '2. When is sustained damage through an active partner preferable to another control/recovery attempt? Wins with active healing refute universal isolation rules but do not establish a replacement decision rule.',
        '3. Which specific enemy escape state changes the next control sequence, rather than merely accompanying pressure? Berserker Rage has no verified repeated role in Arms/Holy.',
        '4. What should Priest and Rogue preserve or do separately during recovery? Source narratives rarely establish a repeated role allocation.',
        '5. How can the team protect the first-kill advantage instead of losing the surviving-enemy duel? Counter-kills and trade wins need dedicated review.',
        '6. Against Warlock teams, when should pet pressure give way to a player commitment? Pet replacement and temporary disappearance cannot establish lasting pet removal.',
        '7. Why do the two opener families occur against Balance/Subtlety and Enhancement/Ret? The record does not justify assigning invented positioning triggers.',
        '8. Do the win-only groups retain their apparent target patterns in losses? Additional losses are needed before generating failure rules.',
        '9. Can the 19 composition-unresolved games be identified from original evidence? They remain excluded from canonical grouping.',
        '10. Where is identified Discipline Priest/Subtlety Rogue evidence? None is present in this input.',
        '11. Which transitions are reliably detectable on the actual Warmane 3.3.5 client? No event or strategic detector has been tested here.',
        '12. Would harmonizing “opening target” into first chip, first Rogue commitment and first sustained team pressure materially change any defaults? Current counts preserve the labeled source meaning.', '',
        'See [the prioritized queue](03_REVIEW_QUEUE.md) and [candidate-rule challenges](contradiction_index.json) for match-specific evidence.', '']
    (OUT/'unresolved_strategy_questions.md').write_text('\n'.join(questions), encoding='utf-8')
    print(f'Reports and combined cards written for {len(ss)} matchups; confidence {dict(confidence)}')


if __name__ == '__main__': main()
