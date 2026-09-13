import { useEffect, useMemo, useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { lookupStrategies } from "../data/normalize";
import { loadHealth, loadPackage, resolveCatalog } from "../data/repo";
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
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, []);

  useEffect(() => {
    localStorage.setItem(FRIENDLY_KEY, friendly);
  }, [friendly]);

  const catalog = useMemo(() => (pkg ? resolveCatalog(pkg) : []), [pkg]);
  const hits = useMemo(
    () => lookupStrategies(catalog, friendly, query),
    [catalog, friendly, query],
  );
  const discSub = friendly === "Discipline Priest / Subtlety Rogue";

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
          Canonical strategy text is empty until an approved package is loaded. Lookup still
          returns evidence snapshots from {health?.valid_2v2 ?? "—"} valid 2v2 games · package{" "}
          {pkg.package_version}.
        </p>
        <form className="row" style={{ marginTop: 12 }} onSubmit={onSubmit}>
          <label>
            Friendly
            <div>
              <select value={friendly} onChange={(e) => setFriendly(e.target.value)}>
                {pkg.friendly_comps.map((c) => (
                  <option key={c} value={c}>
                    {c}
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
      {discSub && (
        <div className="panel empty">
          No Discipline Priest / Subtlety Rogue evidence in this corpus. No strategy is invented
          for this friendly composition.
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
              {s.evidence.games} games · {s.evidence.wins}W/{s.evidence.losses}L · {s.confidence} ·{" "}
              {s.status}
            </div>
          </li>
        ))}
        {!hits.length && !discSub && query && <li className="empty">No matchup matches that search.</li>}
      </ul>
    </div>
  );
}
