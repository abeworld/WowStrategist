import type { CanonicalPackage, SlimMatch, Strategy } from "./types";

export function validateCanonicalPackage(pkg: CanonicalPackage): string[] {
  const errors: string[] = [];
  if (!pkg.schema_version) errors.push("missing schema_version");
  if (!pkg.package_version) errors.push("missing package_version");
  if (!Array.isArray(pkg.strategies)) errors.push("strategies is not an array");
  if (!pkg.current || typeof pkg.current !== "object") errors.push("missing current map");
  if (!Array.isArray(pkg.friendly_comps) || pkg.friendly_comps.length === 0) {
    errors.push("friendly_comps missing");
  }

  const byId = new Map<string, Strategy>();
  for (const s of pkg.strategies ?? []) {
    if (!s.strategy_key) errors.push("strategy missing strategy_key");
    if (!s.strategy_id) errors.push(`strategy ${s.strategy_key} missing strategy_id`);
    if (byId.has(s.strategy_id)) errors.push(`duplicate strategy_id ${s.strategy_id}`);
    byId.set(s.strategy_id, s);
    if (!s.our_comp || !s.enemy_comp) errors.push(`${s.strategy_id} missing comps`);
    if (!s.default_line || typeof s.default_line !== "object") {
      errors.push(`${s.strategy_id} missing default_line`);
    }
    if (!s.roles?.team || !s.roles?.priest || !s.roles?.rogue) {
      errors.push(`${s.strategy_id} missing role views`);
    }
    if (!Array.isArray(s.branches)) errors.push(`${s.strategy_id} branches must be an array`);
    if (!s.evidence || typeof s.evidence.games !== "number") {
      errors.push(`${s.strategy_id} missing evidence.games`);
    }
  }

  for (const [key, id] of Object.entries(pkg.current ?? {})) {
    const hit = byId.get(id);
    if (!hit) errors.push(`current ${key} points at missing ${id}`);
    else if (hit.strategy_key !== key) errors.push(`current ${key} points at ${id} with key ${hit.strategy_key}`);
  }
  return errors;
}

export function validateMatches(matches: SlimMatch[], pkg: CanonicalPackage): string[] {
  const errors: string[] = [];
  const ids = new Set(matches.map((m) => m.match_id));
  for (const s of pkg.strategies) {
    for (const id of s.evidence.supporting_match_ids ?? []) {
      if (!ids.has(id)) errors.push(`${s.strategy_id} supporting match missing: ${id}`);
    }
    for (const id of s.evidence.counterexample_match_ids ?? []) {
      if (!ids.has(id)) errors.push(`${s.strategy_id} counterexample missing: ${id}`);
    }
  }
  return errors;
}
