import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { loadHealth, loadPackage, resolveCatalog } from "../data/repo";
import type { CanonicalPackage, CorpusHealth } from "../data/types";

export default function CoveragePage() {
  const [pkg, setPkg] = useState<CanonicalPackage | null>(null);
  const [health, setHealth] = useState<CorpusHealth | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    void Promise.all([loadPackage(), loadHealth()])
      .then(([p, h]) => {
        setPkg(p);
        setHealth(h);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, []);
  if (error) return <p className="empty">Failed to load corpus: {error}</p>;
  if (!pkg || !health) return <p className="muted">Loading…</p>;
  const rows = resolveCatalog(pkg)
    .slice()
    .sort((a, b) => b.evidence.games - a.evidence.games);
  const emptyFriendlies = pkg.friendly_comps.filter((c) => c.matchup_count === 0);
  return (
    <div className="stack">
      <section className="hero">
        <div className="kicker">Corpus health</div>
        <h2>Coverage</h2>
        <p className="muted">
          {health.valid_2v2} valid 2v2 · {health.assigned} assigned · {health.unresolved} unresolved ·{" "}
          {health.matchup_groups} matchups · package {pkg.package_version}
        </p>
        <p className="muted">
          Sample-size bands (not strategy confidence): high {health.coverage.high} · medium {health.coverage.medium} ·
          low {health.coverage.low}
        </p>
      </section>
      <div className="panel" style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th>Matchup</th>
              <th>Games</th>
              <th>W/L</th>
              <th>Sample size</th>
              <th>Strategy confidence</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((s) => (
              <tr key={s.strategy_key}>
                <td>
                  <Link to={`/matchup/${s.strategy_key}`}>{s.enemy_short}</Link>
                  <div className="muted">{s.our_comp}</div>
                </td>
                <td>{s.evidence.games}</td>
                <td>
                  <span className="win">{s.evidence.wins}</span>/
                  <span className="loss">{s.evidence.losses}</span>
                </td>
                <td>
                  <span className={`badge ${s.sample_band}`}>{s.sample_band}</span>
                </td>
                <td>
                  <span className={`badge ${s.confidence}`}>{s.confidence}</span>
                </td>
                <td>
                  <span className={`badge ${s.status}`}>{s.status}</span>
                </td>
              </tr>
            ))}
            {emptyFriendlies.map((c) => (
              <tr key={c.name}>
                <td>
                  {c.name}
                  <div className="muted">{c.status}</div>
                </td>
                <td>0</td>
                <td>—</td>
                <td>
                  <span className="badge low">low</span>
                </td>
                <td>
                  <span className="badge insufficient">insufficient</span>
                </td>
                <td>
                  <span className="badge insufficient_evidence">no_evidence</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
