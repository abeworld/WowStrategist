# V2 hardening report

## 1. Files inspected

Webapp: `README.md`, both handover markdown files, `src/data/*`, all pages, `app.smoke.test.tsx`, `scripts/export_data.py`, `public/data/*`, `.github/workflows/deploy-webapp.yml`.

Canonical track: `analysis/canonical_strategy/02_SCHEMA.md`, `strategy.schema.json`, `build_package.py`, `validate_package.py`.

targeted_v2: `REFINEMENT_SUMMARY.md`, `VALIDATION_REPORT.md`, `REVIEW_REQUESTS.md`, `package_counts.json`, `matchup_index.json`, `strategies.json`, `strategy.schema.json`, `strategies/SPR_vs_Arms_HPal_v2.json`, `strategies/SPR_vs_Arms_Ret_v1.json`, plus the cards/index listing.

## 2. targeted_v2 materials found

A complete candidate package, not a handful of markdown notes:

- envelope `strategies.json` (schema 1.0.0, package 1.1.0, 49 strategy objects, ~2.0 MB)
- per-id JSON under `strategies/`
- cards, analysis notes for the three revised matchups
- `matchup_index.json` with current ids and `friendly_compositions`
- decision ledger, claim review, validation report (PASS)

## 3. What those materials represent

**Scenario A + C.** The directory is an installable canonical envelope. Three matchups are material v2 revisions (`SPR_vs_Arms_HPal`, `SPR_vs_SP_Sub`, `SPR_vs_Disc_Feral`). The other 46 objects are unchanged v1. All remain **provisional**; none is approved. Disc/Sub friendly composition is `no_evidence`. The authors state the candidate is suitable for provisional webapp consumption after validation, and that unknown branch selection must stay explicit.

The webapp consumes this package through `install_canonical.py`. Markdown is not hardcoded into React.

Schema field names (`opening_target`, `manufacture`, `contradicting_match_ids`, claim objects) differ from the V1 web fixture. The canonical schema was **not** redefined. An adapter maps claims onto the existing encyclopedia layout.

## 4. Defects fixed

- Evidence export no longer writes `canonical-package.json` or invents strategy fields.
- Hardcoded `C:\Users\Gary Goldman\...` corpus path removed.
- `hasApprovedLine()` replaced with `hasStrategyContent()` / `isApproved()`.
- Provisional text now renders; “No approved strategy text” is not used for existing claims.
- `current` is strict: no highest-version fallback; missing pointer fails validation.
- Runtime `parsePackage()` validates before render.
- Sample-size bands separated from strategy confidence.
- Supporting/contradicting IDs taken from canonical arrays, not W/L.
- Disc/Sub empty state is data-driven from `friendly_comps`.
- Opening/kill distributions on the card come from canonical `facts`, not dirty prepared-stat labels.

## 5. Architecture decisions

Static Vite/React reader preserved. No backend, auth, LLM, or store.

Installed on-disk format is a thin envelope: canonical `strategies[]` plus `current` and `friendly_comps` derived from `matchup_index.json` when the source directory supplies it. That envelope is packaging, not synthesis.

## 6. Canonical installation procedure

```powershell
python scripts/install_canonical.py --source "<canonical dir or strategies.json>"
```

Invalid packages print errors and leave the previous file in place (temp file + `os.replace` only after validation).

## 7. Approval semantics

| Signal | Meaning |
| --- | --- |
| Claim text | Analysis exists |
| `status=provisional` | Displayable, not approved |
| `status=approved` | Explicit package approval |
| `status=insufficient_evidence` | Sparse / not a usable plan |

## 8. Version resolution

`current[strategy_key] -> strategy_id` only. Tests cover current→v1 with v2 present, current→v2, and current→missing v3 (validation failure).

## 9. Evidence vs strategy

Default plan and roles are canonical claims. Opening/kill bars are labelled as counts, not a plan. Supporting/contradicting lists are canonical citations. Match records still expose source observed/inferred notes separately.

## 10. Tests added

- `src/data/normalize.test.ts`: aliases, lookup, strict current, approval vs content, evidence classification, validation rejects, Disc/Sub from data.
- `src/app.smoke.test.tsx`: live 1.1.0 package, provisional Arms/HPal v2 text, coverage sample vs confidence columns.
- `scripts/test_pipeline.py`: export does not clobber canonical JSON; wins are not labelled supporting; invalid install preserves previous file.

## 11. Verification

```
python scripts/install_canonical.py --source "...\targeted_v2"
  installed 1.1.0 (49 strategies, 49 current)

python scripts/export_data.py --corpus "...\prepared_corpus"
  wrote 487 matches; left canonical-package.json untouched
  sha256 2258a590c13fb9743841de4fc725f5cc928ce11fc6a5dfa4a4ca5350ed119f09 unchanged

python scripts/test_pipeline.py
  Ran 3 tests in 0.043s  OK

npm test
  Test Files  2 passed (2)
  Tests  28 passed (28)

npm run build
  tsc --noEmit && vite build  OK (50 modules)
```

GitHub Pages workflow is unchanged: static `webapp/` build, `404.html` SPA fallback, `base` from `GITHUB_REPOSITORY`.

## 12. Still blocked on canonical-strategy work

- No strategy is `approved`.
- Disc/Sub has no matchups until the package says otherwise.
- Alternative default-line is not a first-class claim in schema 1.0.0; the UI fills it only from branches classified as alternative.
- Historical v1 objects for the three revised matchups are not in `strategies.json`; history is `version_history` notes on the current object.
- Dirty prepared-corpus target labels remain in `matches-slim.json` as source strings; the matchup card uses canonical `facts` instead of repairing those strings in React.
- Automatic addon transitions remain uncertified (`runtime_observability.automatic` is empty).
