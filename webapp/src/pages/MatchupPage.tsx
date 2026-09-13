import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { hasApprovedLine, loadMatches, loadPackage, resolveCurrent } from "../data/repo";
import type { CanonicalPackage, SlimMatch, Strategy } from "../data/types";

function Dist({ title, known, unknown, values }: { title: string; known: number; unknown: number; values: Record<string, number> }) {
  const total = known + unknown;
  const entries = Object.entries(values).sort((a, b) => b[1] - a[1]);
  return (
    <div className="panel">
      <div className="kicker">{title}</div>
      <p>
        Known in {known}/{total}
        {unknown ? <span className="muted"> · {unknown} unknown</span> : null}
      </p>
      {entries.map(([name, n]) => (
        <div key={name} style={{ marginBottom: 8 }}>
          <div className="row" style={{ justifyContent: "space-between" }}>
            <span>{name}</span>
            <span className="muted">
              {n}/{known || 1}
            </span>
          </div>
          <div className="bar">
            <span style={{ width: `${known ? (100 * n) / known : 0}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function Line({ label, value }: { label: string; value: string | null }) {
  return (
    <>
      <dt>{label}</dt>
      <dd className={value ? undefined : "empty"}>{value || "No approved strategy text"}</dd>
    </>
  );
}

export default function MatchupPage() {
  const { strategyKey = "" } = useParams();
  const [pkg, setPkg] = useState<CanonicalPackage | null>(null);
  const [matches, setMatches] = useState<SlimMatch[]>([]);
  const [role, setRole] = useState<"team" | "priest" | "rogue">("team");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void Promise.all([loadPackage(), loadMatches()])
      .then(([p, m]) => {
        setPkg(p);
        setMatches(m);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, []);

  if (error) return <p className="empty">Failed to load corpus: {error}</p>;
  if (!pkg) return <p className="muted">Loading…</p>;
  const strategy: Strategy | undefined = resolveCurrent(pkg, strategyKey);
  if (!strategy) {
    return (
      <div className="panel">
        <p>No strategy for `{strategyKey}`.</p>
        <Link to="/">Back to lookup</Link>
      </div>
    );
  }

  const related = matches.filter((m) => strategy.evidence.all_match_ids.includes(m.match_id));
  const roleView = strategy.roles[role];
  const approved = hasApprovedLine(strategy);

  return (
    <div className="stack">
      <section className="hero">
        <div className="kicker">{strategy.our_comp}</div>
        <h2>vs {strategy.enemy_short}</h2>
        <p className="muted">{strategy.enemy_comp}</p>
        <div className="row">
          <span className={`badge ${strategy.status}`}>{strategy.status}</span>
          <span className={`badge ${strategy.confidence}`}>{strategy.confidence} confidence</span>
          <span className="badge">
            {strategy.evidence.games} games · {strategy.evidence.wins}W/{strategy.evidence.losses}L
          </span>
          <span className="badge">{strategy.strategy_id}</span>
          <span className="badge">package {pkg.package_version}</span>
        </div>
      </section>

      <section className="panel plan">
        <div className="kicker">Default plan</div>
        {!approved && (
          <p className="empty">
            No approved canonical line yet. Do not treat the frequencies below as a game plan.
          </p>
        )}
        <dl>
          <Line label="Start" value={strategy.default_line.start} />
          <Line label="Objective" value={strategy.default_line.objective} />
          <Line label="Win condition" value={strategy.default_line.win_condition} />
          <Line label="Convert" value={strategy.default_line.convert} />
          <Line label="Alternative" value={strategy.default_line.alternative} />
          <Line label="Reset" value={strategy.default_line.reset} />
        </dl>
      </section>

      <div className="row">
        {(["team", "priest", "rogue"] as const).map((id) => (
          <button key={id} className={`tab ${role === id ? "active" : ""}`} onClick={() => setRole(id)}>
            {id === "team" ? "Team" : id === "priest" ? "Priest POV" : "Rogue POV"}
          </button>
        ))}
      </div>
      <section className="panel">
        <div className="kicker">{role === "team" ? "Team" : role === "priest" ? "Priest POV" : "Rogue POV"}</div>
        <p className={roleView.summary ? undefined : "empty"}>{roleView.summary || "Unknown — not in canonical package"}</p>
        {roleView.responsibilities.length > 0 && (
          <ul>
            {roleView.responsibilities.map((r) => (
              <li key={r}>{r}</li>
            ))}
          </ul>
        )}
      </section>

      <section className="panel">
        <div className="kicker">Important branches</div>
        {strategy.branches.length ? (
          <ul>
            {strategy.branches.map((b) => (
              <li key={b.when}>
                <strong>If {b.when}</strong> → {b.then}
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty">No branches in this package version.</p>
        )}
      </section>

      <section className="panel">
        <div className="kicker">Failure modes</div>
        {strategy.failure_modes.length ? (
          <ul>
            {strategy.failure_modes.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
        ) : (
          <p className="empty">None recorded.</p>
        )}
      </section>

      <div className="kicker">Why we believe this (evidence, not strategy)</div>
      <div className="grid two-col">
        <Dist
          title="Opening target"
          known={strategy.evidence.opening_target_known}
          unknown={strategy.evidence.opening_target_unknown}
          values={strategy.evidence.opening_targets}
        />
        <Dist
          title="Kill target"
          known={strategy.evidence.kill_target_known}
          unknown={strategy.evidence.kill_target_unknown}
          values={strategy.evidence.kill_targets}
        />
      </div>

      <section className="panel">
        <div className="kicker">Supporting wins</div>
        <p className="muted">Up to 12 recent supporting match IDs.</p>
        <div className="row">
          {strategy.evidence.supporting_match_ids.slice(0, 12).map((id) => (
            <Link key={id} to={`/match/${encodeURIComponent(id)}`}>
              {id.split("__").pop()}
            </Link>
          ))}
        </div>
        <div className="kicker" style={{ marginTop: 16 }}>
          Counterexample losses
        </div>
        <div className="row">
          {strategy.evidence.counterexample_match_ids.length ? (
            strategy.evidence.counterexample_match_ids.slice(0, 8).map((id) => (
              <Link key={id} to={`/match/${encodeURIComponent(id)}`}>
                {id.split("__").pop()}
              </Link>
            ))
          ) : (
            <span className="empty">None listed</span>
          )}
        </div>
        <p className="muted" style={{ marginTop: 12 }}>
          {related.length} evidence records in this matchup.
        </p>
      </section>

      <section className="panel">
        <div className="kicker">Version history</div>
        {strategy.history.map((h) => (
          <p key={h.strategy_id}>
            <strong>{h.strategy_id}</strong> — {h.note}
          </p>
        ))}
      </section>
    </div>
  );
}
