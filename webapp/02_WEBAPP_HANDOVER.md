# WoW Arena Strategist — Web App Track Handover

## Recommended model / reasoning

**Run with: Terra · High reasoning**

Most of this track should become specification-driven product engineering once the canonical strategy contract is stable.

Terra High is the preferred default to conserve cost/tokens.

Escalate to **Sol · Medium/High** when:
- changing the canonical data contract;
- making architectural choices with long-term consequences;
- adding complex evidence querying;
- designing synchronization with generated addon assets;
- debugging a difficult full-stack issue.

Do not use the highest model merely for repetitive UI implementation.

---

# Mission

Build the **human-readable reference implementation** of the WoW Arena Strategist knowledge system.

The web app is:

- an encyclopedia;
- a fast matchup lookup;
- an evidence explorer;
- a strategy audit surface;
- the guaranteed fallback if the live addon is unavailable.

It is **not** the source of strategic truth.

The canonical strategy corpus is the source of truth.

Architecture:

```text
matches.jsonl
    ↓
canonical strategy synthesis
    ↓
CANONICAL STRATEGY CORPUS
       ↓
     WEB APP
```

The web app should never independently invent a strategy from raw matches.

---

# Environment / domain

Primary game:

- Warmane
- WotLK 3.3.5
- 2v2 arena

Primary friendly compositions:

- Shadow Priest / Subtlety Rogue
- Discipline Priest / Subtlety Rogue

The app must support both friendly POVs:

- Priest
- Rogue

A strategy is keyed by:

```text
our_comp + enemy_comp
```

---

# Product principle

The fastest useful answer should be available in seconds before queueing.

The primary question is:

> "What do we do as SPR into HPal/War?"

The answer should not require browsing raw match logs.

The app should show the already-approved canonical strategy immediately.

---

# Core product layers

## Layer 1 — Instant matchup lookup

User selects friendly composition once:

```text
Shadow Priest / Subtlety Rogue
```

Then searches enemy composition using forgiving aliases:

```text
hpal war
pala warrior
war hpal
holy arms
```

All should normalize to the same canonical matchup.

Primary result:

```text
HPal / Arms

Evidence: 32 games · confidence high

Start:
Objective:
Win condition:
Convert:
Alternative:
Failure:
Reset:
```

Main lookup should be deterministic.

No LLM is needed to answer a known canonical matchup.

---

## Layer 2 — Role views

Every matchup should support:

```text
TEAM
PRIEST POV
ROGUE POV
```

### Team
What the composition is trying to accomplish.

### Priest POV
The Priest's responsibilities during each strategic state.

### Rogue POV
The Rogue's responsibilities during each strategic state.

Do not create separate strategy copies per role.

All role views derive from the same canonical strategy object.

---

## Layer 3 — Branch/state explorer

The canonical strategy may contain:

- default line;
- reactive branches;
- conversion state;
- reset/recovery state;
- failure modes.

The app should make the default line visually dominant.

Branches should be available without overwhelming the user.

Conceptual presentation:

```text
DEFAULT
Start Warrior
→ create condition X
→ CC
→ convert

IF opponent does Y
→ branch A

IF conversion fails
→ reset
```

Do not display every rare event as an equal "strategy".

---

## Layer 4 — Evidence explorer

Every strategic claim should be auditable.

The evidence view should eventually show:

- sample size;
- wins/losses;
- opening target frequency;
- kill target frequency;
- repeated resource patterns;
- supporting match IDs;
- contradicting match IDs;
- representative matches/clips;
- confidence;
- strategy version.

The purpose is not to recreate second-by-second match recaps.

The purpose is to explain:

> Why do we believe this is the default strategy?

---

## Layer 5 — Coverage / corpus health

Provide a coverage view such as:

```text
Matchup                Games   Confidence   Status
HPal / Arms              32       High      Approved
Mage / Rogue             21       High      Approved
Lock / Shaman             7       Medium    Review
DK / Ret                  2       Low       Sparse
```

This helps identify where more footage is needed.

---

## Layer 6 — Strategy history

Approved strategy versions should be visible.

Example:

```text
v1 — based on 32 games
v2 — based on 51 games

Changes:
- branch X promoted;
- reset condition refined;
- player responsibility updated.
```

The website should make strategy changes explainable.

---

# Source data

The web app should consume two conceptual layers.

## Canonical strategy files

Primary read model.

Contains:

- matchup identity;
- approved default line;
- states;
- branches;
- Priest/Rogue instructions;
- confidence;
- evidence references;
- strategy version.

## Match evidence

Used only for deeper evidence exploration.

Likely source:

```text
matches.jsonl
```

The app must not recompute strategic truth on the fly from all raw matches.

---

# One source of truth

Avoid separate manually-maintained content such as:

```text
website_strategy.json
addon_strategy.lua
matchup_guide.md
```

that can drift.

Target architecture:

```text
canonical strategy
       /     \
      /       \
 web rendering  generated addon catalog
```

The web app is one consumer.

---

# Search and normalization

Search should be forgiving.

Support:

- spec names;
- class names;
- common arena abbreviations;
- reversed enemy order;
- friendly comp aliases.

Examples:

```text
SPR
SP/R
Shadow Rogue
HPal War
War HPal
Pala Warrior
```

Normalization logic should be explicit and testable.

Do not depend on an LLM for matching common composition aliases.

---

# V1 scope

Keep V1 intentionally boring and useful.

## Required

1. Friendly comp selector.
2. Enemy comp search.
3. Matchup strategy card.
4. Team / Priest / Rogue tabs.
5. Default line + important branches.
6. Evidence/sample size/confidence.
7. Failure mode + reset.
8. Supporting/contradicting match references.
9. Coverage page.
10. Strategy version display.

## Nice later

- representative video clip embeds;
- richer statistics;
- strategy timeline visualization;
- training/flashcard mode;
- AI evidence Q&A;
- personal annotations;
- compare versions.

Do not let later features delay the core encyclopedia.

---

# AI policy

Main lookup is deterministic.

Do **not** ask an LLM:

> "What should I do against HPal/War?"

when an approved canonical strategy exists.

Return the canonical answer.

An optional later AI feature may answer questions such as:

> "Why do we start on Warrior here?"

by querying the evidence layer and canonical rationale.

AI is an evidence-exploration feature, not the primary strategy engine.

---

# UX priorities

Priority order:

1. Speed.
2. Clarity.
3. Default strategy prominence.
4. Easy access to branches.
5. Evidence transparency.
6. Visual polish.

The app should work well on:

- desktop;
- second monitor;
- phone/tablet as fallback during play.

The live addon may eventually be the best in-game interface, but the web app must remain fully useful by itself.

---

# Matchup detail page concept

Conceptual hierarchy:

```text
[ OUR COMP ] vs [ ENEMY COMP ]

Evidence / confidence / version

DEFAULT PLAN
Start:
Objective:
Win:
Convert:
Reset:

[ Team ] [ Priest ] [ Rogue ]

IMPORTANT BRANCHES
- If ...
- If ...

FAILURE MODES
- ...

WHY?
supporting evidence
contradictions
representative matches

VERSION HISTORY
```

The default plan must remain above the fold / immediately visible.

---

# Data contract boundary

This track should **not** casually redefine the canonical strategy schema.

If the UI exposes a missing requirement:

1. document the requirement;
2. take it back to the canonical-strategy track;
3. update the canonical contract there;
4. then consume the revised contract.

Do not let frontend convenience silently corrupt the strategy model.

---

# Provenance

For every meaningful claim the UI should be able to trace:

```text
strategy claim
→ canonical strategy version
→ supporting / contradicting match IDs
→ match record
→ clip where available
```

This is a key differentiator of the product.

---

# Technology choice

Technology stack is intentionally **not locked yet**.

Choose the stack only after inspecting:

- expected hosting;
- local vs cloud use;
- whether raw clips need serving;
- canonical file format;
- desired future authentication;
- whether the app should be installable as a PWA;
- deployment preferences.

Prefer a boring, maintainable stack.

Do not introduce a database, backend, AI service, or authentication unless the V1 actually needs it.

A static/generated site consuming canonical files may be enough initially.

Challenge complexity aggressively.

---

# Testing expectations

At minimum test:

- composition alias normalization;
- matchup lookup;
- reversed enemy order;
- missing strategy behavior;
- sparse evidence behavior;
- strategy version rendering;
- Priest/Rogue role selection;
- branch display;
- evidence links;
- canonical schema validation.

Representative strategies should include:

- a simple matchup;
- a branch-heavy matchup;
- a low-confidence matchup.

---

# Deliverables for this track

1. Product specification.
2. UX/navigation design.
3. Canonical data contract consumer.
4. Search/normalization logic.
5. Matchup card UI.
6. Team/Priest/Rogue role views.
7. Branch explorer.
8. Evidence explorer.
9. Coverage page.
10. Version history.
11. Deployment approach.
12. Tests.
13. Documentation for loading a new canonical strategy release.

---

# Out of scope for this chat

Do not own:

- raw VOD processing;
- canonical strategy synthesis;
- Warmane combat-event detection;
- Lua state machine;
- WeakAuras implementation.

This chat owns:

```text
approved canonical strategy
→ excellent human-readable encyclopedia
```

---

# First action in the new chat

Before coding:

1. inspect the available canonical strategy schema / examples;
2. propose the smallest V1 information architecture;
3. propose 2–3 implementation stacks with trade-offs;
4. choose the minimum viable architecture;
5. show how one canonical matchup would render in Team / Priest / Rogue views;
6. get Gary's approval before implementation.

The web app should remain the transparent, understandable reference layer even after the live addon exists.
