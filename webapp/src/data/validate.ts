import { SUPPORTED_SCHEMA, type CanonicalStrategy, type RawCanonicalPackage, type SlimMatch } from "./types";

const STATUSES = new Set(["provisional", "insufficient_evidence", "approved", "superseded"]);
const CONFIDENCES = new Set(["high", "medium", "low", "insufficient"]);
const LINE_FIELDS = ["opening_target", "initial_objective", "win_condition", "manufacture", "conversion", "reset"] as const;

function isClaim(value: unknown): boolean {
  return Boolean(value) && typeof value === "object" && "text" in (value as object);
}

export function validateCanonicalPackage(pkg: RawCanonicalPackage): string[] {
  const errors: string[] = [];
  if (!pkg || typeof pkg !== "object") return ["package is not an object"];
  if (pkg.schema_version !== SUPPORTED_SCHEMA) {
    errors.push(`unsupported schema_version ${String(pkg.schema_version)}`);
  }
  if (!pkg.package_version) errors.push("missing package_version");
  if (!Array.isArray(pkg.strategies)) errors.push("strategies is not an array");
  if (!pkg.current || typeof pkg.current !== "object" || Array.isArray(pkg.current)) {
    errors.push("missing current map");
  }
  if (!Array.isArray(pkg.friendly_comps)) errors.push("friendly_comps missing");

  const byId = new Map<string, CanonicalStrategy>();
  for (const s of pkg.strategies ?? []) {
    if (!s?.strategy_key) errors.push("strategy missing strategy_key");
    if (!s?.strategy_id) errors.push(`strategy ${s?.strategy_key ?? "?"} missing strategy_id`);
    if (s?.strategy_id && byId.has(s.strategy_id)) errors.push(`duplicate strategy_id ${s.strategy_id}`);
    if (s?.strategy_id) byId.set(s.strategy_id, s);
    if (!s?.our_comp || !s?.enemy_comp) errors.push(`${s?.strategy_id ?? "?"} missing comps`);
    if (!STATUSES.has(s?.status)) errors.push(`${s?.strategy_id ?? "?"} invalid status ${String(s?.status)}`);
    if (!s?.evidence || typeof s.evidence.total_games !== "number") {
      errors.push(`${s?.strategy_id ?? "?"} missing evidence.total_games`);
    } else if (!CONFIDENCES.has(s.evidence.confidence)) {
      errors.push(`${s.strategy_id} invalid evidence.confidence ${String(s.evidence.confidence)}`);
    }
    if (!Array.isArray(s?.evidence?.supporting_match_ids) || !Array.isArray(s?.evidence?.contradicting_match_ids)) {
      errors.push(`${s?.strategy_id ?? "?"} evidence classification arrays required`);
    }
    if (!Array.isArray(s?.evidence?.all_match_ids)) errors.push(`${s?.strategy_id ?? "?"} missing evidence.all_match_ids`);
    if (!s?.default_line || typeof s.default_line !== "object") {
      errors.push(`${s?.strategy_id ?? "?"} missing default_line`);
    } else {
      for (const field of LINE_FIELDS) {
        if (!(field in s.default_line)) errors.push(`${s.strategy_id} missing default_line.${field}`);
        const claim = s.default_line[field];
        if (claim != null && !isClaim(claim)) errors.push(`${s.strategy_id} default_line.${field} is not a claim`);
      }
    }
    if (s?.states != null && !Array.isArray(s.states)) errors.push(`${s.strategy_id} states must be an array`);
    if (s?.states) {
      for (const state of s.states) {
        if (!state.team_objective || !state.priest_instruction || !state.rogue_instruction) {
          errors.push(`${s.strategy_id} state ${state.state_id} missing role claims`);
        }
      }
    }
    if (s?.branches != null && !Array.isArray(s.branches)) errors.push(`${s.strategy_id} branches must be an array`);
    if (s?.failure_modes != null && !Array.isArray(s.failure_modes)) {
      errors.push(`${s.strategy_id} failure_modes must be an array`);
    }
  }

  for (const [key, id] of Object.entries(pkg.current ?? {})) {
    const hit = byId.get(id);
    if (!hit) errors.push(`current ${key} points at missing ${id}`);
    else if (hit.strategy_key !== key) errors.push(`current ${key} points at ${id} with key ${hit.strategy_key}`);
  }
  return errors;
}

export function validateMatches(matches: SlimMatch[], pkg: { strategies: { strategy_id: string; evidence: { supporting_match_ids?: string[]; contradicting_match_ids?: string[] } }[] }): string[] {
  const errors: string[] = [];
  const ids = new Set(matches.map((m) => m.match_id));
  for (const s of pkg.strategies) {
    for (const id of s.evidence.supporting_match_ids ?? []) {
      if (!ids.has(id)) errors.push(`${s.strategy_id} supporting match missing: ${id}`);
    }
    for (const id of s.evidence.contradicting_match_ids ?? []) {
      if (!ids.has(id)) errors.push(`${s.strategy_id} contradicting match missing: ${id}`);
    }
  }
  return errors;
}
