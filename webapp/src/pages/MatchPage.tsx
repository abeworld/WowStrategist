import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { loadMatches, loadPackage, resolveCurrent } from "../data/repo";
import type { CanonicalPackage, SlimMatch } from "../data/types";

export default function MatchPage() {
  const { matchId = "" } = useParams();
  const id = decodeURIComponent(matchId);
  const [pkg, setPkg] = useState<CanonicalPackage | null>(null);
  const [match, setMatch] = useState<SlimMatch | null | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void Promise.all([loadPackage(), loadMatches()])
      .then(([p, rows]) => {
        setPkg(p);
        setMatch(rows.find((m) => m.match_id === id) ?? null);
      })
      .catch((err: unknown) => setError(err instanceof Error ? err.message : String(err)));
  }, [id]);

  if (error) return <p className="empty">Failed to load evidence: {error}</p>;
  if (match === undefined) return <p className="muted">Loading…</p>;
  if (!match) return <p>Match not found.</p>;

  const key =
    match.our_comp && match.enemy_comp && pkg
      ? pkg.strategies.find((s) => s.our_comp === match.our_comp && s.enemy_comp === match.enemy_comp)
          ?.strategy_key
      : undefined;
  const strategy = key && pkg ? resolveCurrent(pkg, key) : undefined;

  return (
    <div className="stack">
      <section className="hero">
        <div className="kicker">Evidence record</div>
        <h2>{match.match_id.split("__").pop()}</h2>
        <p>
          {match.our_comp} vs {match.enemy_comp}
        </p>
        <p>
          Result:{" "}
          <strong className={match.result === "win" ? "win" : match.result === "loss" ? "loss" : undefined}>
            {match.result ?? "unknown"}
          </strong>
          {match.source_clip ? <span className="muted"> · {match.source_clip}</span> : null}
        </p>
        {strategy && (
          <p>
            Canonical: <Link to={`/matchup/${strategy.strategy_key}`}>{strategy.enemy_short}</Link> ·{" "}
            {strategy.strategy_id}
          </p>
        )}
      </section>
      <section className="panel">
        <p>Opening target: {match.opening_target || "unknown"}</p>
        <p>Opening CC: {match.opening_cc || "unknown"}</p>
        <p>Kill target: {match.kill_target || "unknown"}</p>
        <p className="muted">Batch {match.source_batch}</p>
        {match.quality_flags.length > 0 && <p>Flags: {match.quality_flags.join(", ")}</p>}
      </section>
      <section className="panel">
        <div className="kicker">Observed</div>
        {match.observed.length ? (
          <ul>
            {match.observed.map((o) => (
              <li key={o}>{o}</li>
            ))}
          </ul>
        ) : (
          <p className="empty">None recorded.</p>
        )}
        <div className="kicker">Inferred in source</div>
        {match.inferred.length ? (
          <ul>
            {match.inferred.map((o) => (
              <li key={o}>{o}</li>
            ))}
          </ul>
        ) : (
          <p className="empty">None recorded.</p>
        )}
        {match.win_condition_from_source && (
          <p>
            <span className="kicker">Source win-condition hypothesis</span>
            <br />
            {match.win_condition_from_source}
          </p>
        )}
        {match.failure_from_source && (
          <p>
            <span className="kicker">Source failure / turning point</span>
            <br />
            {match.failure_from_source}
          </p>
        )}
      </section>
    </div>
  );
}
