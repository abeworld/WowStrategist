# WoW Arena Strategist — web app

Static encyclopedia for Warmane WotLK 3.3.5 2v2. It is a **reader** of a versioned canonical strategy package, not a strategy generator.

```text
canonical-strategy track  →  npm run install-canonical  →  public/data/canonical-package.json
prepared_corpus           →  npm run export-data        →  public/data/matches-slim.json
                                                        →  public/data/corpus-health.json
                                                              ↓
                                                            Vite UI
```

Lookup is deterministic. There is no LLM in the matchup path.

The live encyclopedia must show **package 1.1.0** (or later). If you see **package 0.1.0** and empty Start/Objective fields, you are on the old evidence fixture — usually a leftover Vite process from `Downloads\...\webapp\start.bat`. Close that window and start from this repo’s `webapp\start.bat`. Data fetches use `cache: "no-store"` plus `?v=<package_version>` so GitHub Pages JSON is not stuck on a 10-minute CDN cache of 0.1.0.

Do **not** edit matchup copy, branches, roles, confidence, or supporting/contradicting IDs in React. Those belong to the canonical package.

## Information architecture

| Route | Purpose |
| --- | --- |
| `/` | Friendly-comp selector + enemy alias search |
| `/matchup/:strategyKey` | Default plan, Team/Priest/Rogue tabs, branches, evidence |
| `/coverage` | Corpus health and per-matchup sample size vs strategy confidence |
| `/match/:matchId` | Single evidence record |

Identity:

- `strategy_key` — stable matchup id, used in routes (`SPR_vs_Arms_HPal`)
- `strategy_id` — a specific version (`SPR_vs_Arms_HPal_v1`, `_v2`, …)
- `current` in the installed package — which `strategy_id` is live

`current` is authoritative. If v1 and v2 both exist and `current` points at v1, the UI shows v1. There is no highest-version fallback. A broken `current` pointer fails validation and is not rendered.

## Status vs content

- **Strategy text present** — canonical analysis exists (Start/Objective/…).
- **`provisional`** — display that text, labelled provisional. Not approved.
- **`approved`** — package explicitly marks it approved.
- **`insufficient_evidence`** — too sparse for a usable strategy.

Do not infer approval from non-null default-line fields.

Strategic **confidence** is authored in the canonical package. Coverage **sample-size** bands (`>=30` high, `>=10` medium, else low) are a separate corpus metric.

Supporting / contradicting match IDs come from canonical synthesis. A win is not automatically supporting. A loss is not automatically a counterexample.

## Run

Double-click `start.bat`, or from `webapp/`:

```powershell
npm install
npm test
npm start
```

Live site: https://abeworld.github.io/WowStrategist/

`npm run build` produces `dist/` for any static host. GitHub Actions deploys Pages from `main`.

## Install a canonical strategy package

```powershell
python scripts/install_canonical.py --source "C:\path\to\canonical_strategy\refinements\targeted_v2"
# or
npm run install-canonical -- --source "C:\path\to\strategies.json"
```

Source may be:

- a directory containing `strategies.json` and optionally `matchup_index.json`
- a `strategies.json` file (sibling `matchup_index.json` is used if present)

The installer validates schema `1.0.0`, unique `strategy_id`s, `current` pointers, status/confidence enums, default-line claims, role structure, and evidence arrays. On failure the previous `public/data/canonical-package.json` is left unchanged.

Do not copy JSON over the live file by hand unless you have already validated it.

## Refresh evidence

```powershell
python scripts/export_data.py --corpus "C:\path\to\analysis\prepared_corpus"
# or set WAS_CORPUS and run:
npm run export-data
```

This rewrites **only**:

- `public/data/matches-slim.json`
- `public/data/corpus-health.json`

It never writes or mutates `canonical-package.json`. It does not invent strategy text, branches, roles, approval, strategic confidence, or supporting/counterexample labels.

## Tests

```powershell
npm test
npm run test-pipeline
npm run build
```

`npm test` covers aliases, reversed enemy order, current-version resolution, approval vs content, Disc/Sub data-driven empty/present states, and package validation. `npm run test-pipeline` proves evidence export cannot clobber canonical JSON and that invalid installs are rejected.

## What not to edit manually

- Matchup strategy wording in `src/pages/*`
- `current` by guessing `_v2`
- Opening-target labels in React (normalization belongs upstream; the UI reads canonical `facts`)
