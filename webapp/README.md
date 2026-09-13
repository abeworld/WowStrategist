# WoW Arena Strategist — web app

Static encyclopedia for Warmane WotLK 3.3.5 2v2. It is a **reader** of a versioned canonical strategy package, not a strategy generator.

```text
prepared_corpus  →  scripts/export_data.py  →  public/data/*.json  →  UI
```

Lookup is deterministic. There is no LLM in the matchup path.

## V1 information architecture

| Route | Purpose |
| --- | --- |
| `/` | Friendly-comp selector + enemy alias search |
| `/matchup/:strategyKey` | Default plan, Team/Priest/Rogue tabs, branches, evidence |
| `/coverage` | Corpus health and per-matchup sample size |
| `/match/:matchId` | Single evidence record |

Identity:

- `strategy_key` — stable matchup id, used in routes (`SPR_vs_Arms_HPal`)
- `strategy_id` — a specific version (`SPR_vs_Arms_HPal_v1`, `_v2`, …)
- `current` in the package — which `strategy_id` is live

Until an approved Astra package exists, default-line and role text stay empty. The UI shows **No approved strategy text** and evidence frequencies only. Discipline Priest / Subtlety Rogue has no evidence and is not given a fabricated card.

## Run

```powershell
cd "C:\Users\Gary Goldman\Downloads\Codex_work\Wow strategist\webapp"
npm install
npm test
npm run dev
```

Then open http://127.0.0.1:5173/

Live site (GitHub Pages): https://abeworld.github.io/WowStrategist/

Production build:

```powershell
npm run build
npm run preview
```

`dist/` is a static site. Any static host works. No database, auth, or backend.

GitHub Actions builds `webapp/` on every push to `main` and publishes GitHub Pages. Deep links use `404.html` as an SPA fallback. The Vite `base` path is `/WowStrategist/` in CI so assets and `/data/*.json` resolve on the project site.

## Refresh evidence from prepared_corpus

```powershell
npm run export-data
```

This rewrites:

- `public/data/canonical-package.json`
- `public/data/matches-slim.json`
- `public/data/corpus-health.json`

It does **not** invent start/objective/win-condition text.

## Load a new canonical strategy release

Replace `public/data/canonical-package.json` with the new package (schema `1.0.0`).

Required:

1. `current` maps each `strategy_key` to the live `strategy_id`
2. Both v1 and v2 may live in `strategies[]`; the UI reads `current`, not a `_v1` suffix
3. `status` remains `provisional` / `insufficient_evidence` / `approved` as the package says
4. Missing optional sections (`branches`, role summaries, default line) render as empty states

Do **not** edit matchup copy in React components. If the new package needs a UI code change to show a specific matchup, the data boundary is too tight.

Optional: keep `matches-slim.json` in sync if evidence IDs changed.

Then `npm test` and `npm run build`. Unaffected matchups should render from the new JSON without component edits.

## Tests

`npm test` covers alias normalization, reversed enemy order, current-version resolution, missing/sparse strategies, role/branch fields, and schema validation of the on-disk package.
