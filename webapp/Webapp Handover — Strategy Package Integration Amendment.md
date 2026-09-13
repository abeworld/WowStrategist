# Strategy package is versioned and may change during development

The canonical strategy content is still being refined in parallel with this webapp.

Do **not** block webapp development waiting for the strategy refinement.

The canonical schema remains `1.0.0`, but:

- package versions may increase;
- individual strategies may receive new versions;
- e.g. `SPR_vs_Arms_HPal_v1` may become `SPR_vs_Arms_HPal_v2`;
- wording, confidence, branches, failure modes and supporting evidence may change;
- strategy status may remain `provisional` until Gary explicitly approves it.

Therefore the webapp must treat the canonical strategy package as **external versioned content**, not hardcoded application logic.

## Stable identity vs version identity

Use:

`strategy_key`

as the stable logical identity of a matchup strategy.

Example:

`SPR_vs_Arms_HPal`

Treat:

`strategy_id`

as the identity of a specific strategy version.

Example:

`SPR_vs_Arms_HPal_v1`
`SPR_vs_Arms_HPal_v2`

Do not build routes, UI logic or application state that assumes `_v1` is permanently current.

The application must be able to replace v1 with v2 through a data-package update without requiring UI code changes.

## Data-loading principle

Create a clean strategy data/repository layer between the JSON package and UI components.

Conceptually:

```text
canonical strategy package
        ↓
strategy repository / parser
        ↓
normalized application view model
        ↓
UI
```

UI components must not directly contain matchup-specific strategy text.

Do not hardcode:

- opening targets;
- objectives;
- win conditions;
- branches;
- cooldown relevance;
- matchup-specific instructions;
- confidence;
- evidence counts.

All such content comes from the canonical strategy package.

## Current strategy resolution

Use the package/index metadata to determine the current strategy version.

The application should support a package refresh where:

```text
SPR_vs_Arms_HPal_v1
```

is replaced by:

```text
SPR_vs_Arms_HPal_v2
```

without requiring component changes.

Historical versions may eventually be exposed, but version-history UI is not required for the first webapp unless already trivial to support.

## Provisional content

Do not present provisional analysis as established fact.

Respect source fields such as:

- `status`
- `confidence`
- `version`
- evidence sample size

Example statuses may include:

- `provisional`
- `insufficient_evidence`
- future `approved`

The UI may visually distinguish these statuses, but must not invent approval states.

## Missing evidence

Do not generate filler when canonical data says `unknown`, has insufficient evidence, or a composition has no evidence.

In particular, Discipline Priest / Subtlety Rogue currently has no evidence and must not receive fabricated strategies.

An unavailable strategy should render a proper empty / insufficient-evidence state.

## Forward compatibility

The UI should be tolerant of:

- missing optional sections;
- `unknown` player responsibilities;
- zero branches;
- multiple branches;
- insufficient-evidence strategies;
- strategies gaining richer content later.

Do not make every strategy fit the structure of the three largest current matchups.

## Development fixture

The current package is valid as development data.

Build against it now.

When the parallel Astra refinement finishes, replace/import the new canonical package and verify that:

1. the new package loads without code changes;
2. newly versioned strategies resolve as current;
3. updated cards/content render correctly;
4. unaffected matchups remain unchanged;
5. provisional/confidence states remain correctly represented.

If loading the refined package requires rewriting matchup-specific UI code, the data/application boundary is too tightly coupled.