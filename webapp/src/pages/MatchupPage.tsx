import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { hasStrategyContent, isApproved, missingFieldMessage, renderField } from "../data/adapter";
import { loadMatches, loadPackage, resolveCurrent } from "../data/repo";
import type { CanonicalField, CanonicalPackage, SlimMatch, Strategy } from "../data/types";

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
      <p className="muted">Frequencies are evidence counts, not a recommended plan.</p>
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

function PlanLine({ label, value }: { label: string; value: string | null }) {
  if (!value) return null;
  return (
    <>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </>
  );
}

function DetailLine({ label, field, role }: { label: string; field: CanonicalField; role?: "priest" | "rogue" | "team" }) {
  return (
    <>
      <dt>{label}</dt>
      <dd className={field.kind === "present" ? undefined : "empty"}>{renderField(field, role)}</dd>
    </>
  );
}

function statusNote(strategy: Strategy): string | null {
  if (isApproved(strategy.status)) return "Approved canonical strategy.";
  if (strategy.status === "provisional") {
    return "Provisional canonical analysis. Visible for study; not human-approved.";
  }
  if (strategy.status === "insufficient_evidence") {
    return "Insufficient evidence for a usable strategy. Any remaining text is not a complete plan.";
  }
  return null;
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
  const content = hasStrategyContent(strategy.default_line);
  const note = statusNote(strategy);
  const qp = strategy.quick_plan;

  return (
    <div className="stack">
      <section className="hero">
        <div className="kicker">{strategy.our_comp}</div>
        <h2>vs {strategy.enemy_short}</h2>
        <p className="muted">{strategy.enemy_comp}</p>
        <div className="row">
          <span className={`badge ${strategy.status}`}>{strategy.status}</span>
          <span className={`badge ${strategy.confidence}`}>{strategy.confidence} strategy confidence</span>
          <span className={`badge ${strategy.sample_band}`}>
            {strategy.evidence.games} games · sample {strategy.sample_band}
          </span>
          <span className="badge">{strategy.strategy_id}</span>
          <span className="badge">package {pkg.package_version}</span>
        </div>
        {note ? <p className={isApproved(strategy.status) ? "muted" : "empty"}>{note}</p> : null}
      </section>

      <section className="panel plan">
        <div className="kicker">Quick plan</div>
        <p className="muted">
          {qp.source === "card"
            ? "Compact card from the canonical-strategy track."
            : "First sentence of canonical claims; no compact card was installed."}
        </p>
        {!qp.start && !qp.objective && !qp.win && (
          <p className="empty">No strategy text in this package version. Do not treat the frequencies below as a game plan.</p>
        )}
        <dl>
          <PlanLine label="Start" value={qp.start} />
          <PlanLine label="Objective" value={qp.objective} />
          <PlanLine label="Win" value={qp.win} />
          <PlanLine label="Create" value={qp.create} />
          <PlanLine label="Convert" value={qp.convert} />
          <PlanLine label="Alternative" value={qp.alternative} />
          <PlanLine label="Failure" value={qp.failure} />
          <PlanLine label="Reset" value={qp.reset} />
        </dl>
      </section>

      <section className="panel plan">
        <div className="kicker">Detailed canonical analysis</div>
        {!content && <p className="empty">{missingFieldMessage()}</p>}
        <dl>
          <DetailLine label="Start" field={strategy.default_line.start} />
          <DetailLine label="Objective" field={strategy.default_line.objective} />
          <DetailLine label="Win condition" field={strategy.default_line.win_condition} />
          <DetailLine label="Create it" field={strategy.default_line.create} />
          <DetailLine label="Convert" field={strategy.default_line.convert} />
          <DetailLine label="Reset" field={strategy.default_line.reset} />
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
        {strategy.states.length ? (
          strategy.states.map((state) => (
            <div key={state.state_id} style={{ marginBottom: 12 }}>
              <div className="kicker">{state.label}</div>
              <p className={state[role].kind === "present" ? undefined : "empty"}>{renderField(state[role], role)}</p>
            </div>
          ))
        ) : (
          <p className="empty">{missingFieldMessage()}</p>
        )}
      </section>

      <section className="panel">
        <div className="kicker">Important resources</div>
        {strategy.resources.length ? (
          <ul>
            {strategy.resources.map((r) => (
              <li key={r.name}>
                <strong>{r.name}</strong>
                {r.relevance ? <span className="muted"> · {r.relevance}</span> : null}
                <div className={r.assessment.kind === "present" ? undefined : "empty"}>{renderField(r.assessment)}</div>
                {r.requirement ? <div className="muted">{r.requirement}</div> : null}
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty">None recorded in this package version.</p>
        )}
      </section>

      <section className="panel">
        <div className="kicker">Important branches</div>
        {strategy.branches.length ? (
          <ul>
            {strategy.branches.map((b, i) => (
              <li key={b.id ?? `${i}`}>
                <strong>If {renderField(b.when)}</strong> → {renderField(b.then)}
                <div className="muted">
                  {b.classification ?? "unclassified"}
                  {b.confidence ? ` · ${b.confidence}` : ""}
                </div>
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
            {strategy.failure_modes.map((f, i) => (
              <li key={i} className={f.kind === "present" ? undefined : "empty"}>
                {renderField(f)}
              </li>
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
        <div className="kicker">Supporting matches</div>
        {strategy.evidence.classification_present ? (
          <>
            <p className="muted">Canonical synthesis citations, not “every win”.</p>
            <div className="row">
              {strategy.evidence.supporting_match_ids.length ? (
                strategy.evidence.supporting_match_ids.slice(0, 12).map((id) => (
                  <Link key={id} to={`/match/${encodeURIComponent(id)}`}>
                    {id.split("__").pop()}
                  </Link>
                ))
              ) : (
                <span className="empty">None listed</span>
              )}
            </div>
            <div className="kicker" style={{ marginTop: 16 }}>
              Contradicting matches
            </div>
            <div className="row">
              {strategy.evidence.contradicting_match_ids.length ? (
                strategy.evidence.contradicting_match_ids.slice(0, 8).map((id) => (
                  <Link key={id} to={`/match/${encodeURIComponent(id)}`}>
                    {id.split("__").pop()}
                  </Link>
                ))
              ) : (
                <span className="empty">None listed</span>
              )}
            </div>
          </>
        ) : (
          <p className="empty">Evidence classification unavailable in this package version.</p>
        )}
        <p className="muted" style={{ marginTop: 12 }}>
          {related.length} evidence records in this matchup.
        </p>
      </section>

      <section className="panel">
        <div className="kicker">Version history</div>
        {strategy.history.length ? (
          strategy.history.map((h) => (
            <p key={`${h.strategy_id}-${h.version}`}>
              <strong>{h.strategy_id}</strong> — {h.note}
            </p>
          ))
        ) : (
          <p className="empty">No history notes in this package version.</p>
        )}
      </section>
    </div>
  );
}
