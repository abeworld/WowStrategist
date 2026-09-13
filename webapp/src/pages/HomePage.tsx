import { useEffect, useMemo, useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { lookupStrategies } from "../data/normalize";
import { emptyFriendlyMessage, loadHealth, loadPackage, resolveCatalog } from "../data/repo";
import type { CanonicalPackage, CorpusHealth } from "../data/types";

const FRIENDLY_KEY = "was.friendly";

export default function HomePage() {
  const navigate = useNavigate();
  const [pkg, setPkg] = useState<CanonicalPackage | null>(null);
  const [health, setHealth] = useState<CorpusHealth | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [friendly, setFriendly] = useState(
    () => localStorage.getItem(FRIENDLY_KEY) || "Shadow Priest / Subtlety Rogue",
  );
  const [query, setQuery] = useState("");

  useEffect(() => {
    void Promise.all([loadPackage(), loadHealth()])
      .then(([p, h]) => {
        setPkg(p);
        setHealth(h);
        const names = p.friendly_comps.map((c) => c.name);
        if (names.length && !names.includes(friendly)) setFriendly(names[0]);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, []);

  useEffect(() => {
    localStorage.setItem(FRIENDLY_KEY, friendly);
  }, [friendly]);

  const catalog = useMemo(() => (pkg ? resolveCatalog(pkg) : []), [pkg]);
  const hits = useMemo(() => lookupStrategies(catalog, friendly, query), [catalog, friendly, query]);
  const friendlyMeta = pkg?.friendly_comps.find((c) => c.name === friendly);
  const noFriendlyStrategies = Boolean(pkg) && !hits.length && !query;

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (hits[0]) navigate(`/matchup/${hits[0].strategy_key}`);
  }

  if (error) return <p className="empty">Failed to load corpus: {error}</p>;
  if (!pkg) return <p className="muted">Loading corpus…</p>;

  return (
    <div className="stack">
      <section className="hero">
        <div className="kicker">Instant matchup lookup</div>
        <h2>What do we do into this comp?</h2>
        <p className="muted">
          Canonical package {pkg.package_version} · {health?.valid_2v2 ?? "—"} valid 2v2 evidence records. Lookup is
          deterministic. Strategy text comes only from the installed package.
        </p>
        <form className="row" style={{ marginTop: 12 }} onSubmit={onSubmit}>
          <label>
            Friendly
            <div>
              <select value={friendly} onChange={(e) => setFriendly(e.target.value)}>
                {pkg.friendly_comps.map((c) => (
                  <option key={c.name} value={c.name}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
          </label>
          <label style={{ flex: 1 }}>
            Enemy
            <div>
              <input
                autoFocus
                placeholder="hpal war · pala warrior · frost mage…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </label>
          <button className="tab" type="submit" disabled={!hits.length}>
            Open top hit
          </button>
        </form>
      </section>
      {noFriendlyStrategies && (
        <div className="panel empty">
          {emptyFriendlyMessage(friendly)}
          {friendlyMeta ? ` Package status: ${friendlyMeta.status} · ${friendlyMeta.matchup_count} matchups.` : ""}
        </div>
      )}
      <ul className="list">
        {hits.map((s) => (
          <li key={s.strategy_key}>
            <Link to={`/matchup/${s.strategy_key}`}>
              <strong>{s.enemy_short}</strong>
              <span className="muted"> · {s.enemy_comp}</span>
            </Link>
            <div className="muted">
              {s.evidence.games} games · {s.evidence.wins}W/{s.evidence.losses}L · strategy {s.confidence} · {s.status}
            </div>
          </li>
        ))}
        {!hits.length && !noFriendlyStrategies && query && <li className="empty">No matchup matches that search.</li>}
      </ul>
    </div>
  );
}
