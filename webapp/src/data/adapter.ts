import type {
  Branch,
  CanonicalBranch,
  CanonicalPackage,
  CanonicalState,
  CanonicalStrategy,
  Claim,
  DefaultLine,
  RawCanonicalPackage,
  RoleView,
  SampleBand,
  Strategy,
} from "./types";

const ABBREV: Record<string, string> = {
  "Shadow Priest": "SP",
  "Discipline Priest": "Disc",
  "Subtlety Rogue": "Sub",
  "Assassination Rogue": "Assa",
  "Combat Rogue": "Combat",
  "Arms Warrior": "Arms",
  "Fury Warrior": "Fury",
  "Protection Warrior": "ProtWar",
  "Holy Paladin": "HPal",
  "Retribution Paladin": "Ret",
  "Protection Paladin": "ProtPal",
  "Frost Mage": "Frost",
  "Arcane Mage": "Arcane",
  "Fire Mage": "Fire",
  "Feral Druid": "Feral",
  "Balance Druid": "Balance",
  "Restoration Druid": "RDruid",
  "Restoration Shaman": "RSham",
  "Elemental Shaman": "Ele",
  "Enhancement Shaman": "Enh",
  "Unholy Death Knight": "Unholy",
  "Frost Death Knight": "FrostDK",
  "Blood Death Knight": "Blood",
  "Marksmanship Hunter": "MM",
  "Beast Mastery Hunter": "BM",
  "Survival Hunter": "Surv",
  "Destruction Warlock": "Destro",
  "Affliction Warlock": "Aff",
  "Demonology Warlock": "Demo",
};

export function shortEnemy(comp: string): string {
  return comp
    .split(" / ")
    .map((part) => ABBREV[part.trim()] ?? part.trim())
    .join(" / ");
}

export function sampleBand(games: number): SampleBand {
  if (games >= 30) return "high";
  if (games >= 10) return "medium";
  return "low";
}

export function claimText(claim: Claim | string | null | undefined): string | null {
  if (claim == null) return null;
  const text = typeof claim === "string" ? claim : claim.text;
  if (typeof text !== "string") return null;
  const trimmed = text.trim();
  if (!trimmed) return null;
  if (trimmed.toLowerCase() === "unknown") return null;
  return trimmed;
}

export function hasStrategyContent(line: DefaultLine): boolean {
  return Boolean(
    line.start || line.objective || line.win_condition || line.create || line.convert || line.alternative || line.reset,
  );
}

export function isApproved(status: string): boolean {
  return status === "approved";
}

function roleFromState(state: CanonicalState | undefined, field: "team_objective" | "priest_instruction" | "rogue_instruction"): RoleView {
  const text = claimText(state?.[field]);
  return { summary: text, responsibilities: text ? [text] : [] };
}

function pickState(states: CanonicalState[] | undefined): CanonicalState | undefined {
  if (!states?.length) return undefined;
  return states.find((s) => s.state_id === "opening") ?? states[0];
}

function alternativeFromBranches(branches: CanonicalBranch[] | undefined): string | null {
  const hits = (branches ?? []).filter((b) => (b.classification ?? "").toLowerCase().includes("alternative"));
  const texts = hits.map((b) => claimText(b.response) ?? claimText(b.team_objective)).filter(Boolean) as string[];
  return texts[0] ?? null;
}

function adaptBranch(branch: CanonicalBranch): Branch {
  const when = claimText(branch.trigger) ?? (typeof branch.trigger?.text === "string" ? branch.trigger.text : "unknown");
  const then = claimText(branch.response) ?? claimText(branch.team_objective) ?? "unknown";
  return { when, then, classification: branch.classification };
}

function countMap(values: Record<string, number> | undefined): { known: number; unknown: number; values: Record<string, number> } {
  const out: Record<string, number> = {};
  let known = 0;
  let unknown = 0;
  for (const [name, n] of Object.entries(values ?? {})) {
    const key = name.toLowerCase();
    if (!name || key === "unknown" || key.startsWith("unknown") || key.includes("no_enemy") || key === "none observed") {
      unknown += n;
    } else {
      out[name] = n;
      known += n;
    }
  }
  return { known, unknown, values: out };
}

export function adaptStrategy(raw: CanonicalStrategy): Strategy {
  const line = raw.default_line ?? {};
  const state = pickState(raw.states);
  const opening = countMap(raw.facts?.opening_targets);
  const kills = countMap(raw.facts?.kill_targets);
  const supporting = raw.evidence.supporting_match_ids ?? [];
  const contradicting = raw.evidence.contradicting_match_ids ?? [];
  const history = (raw.version_history ?? []).map((h) => ({
    strategy_id: `${raw.strategy_key}_v${h.version}`,
    version: h.version,
    note: [h.change, h.reason].filter(Boolean).join(" — ") || `Version ${h.version}`,
  }));
  const default_line: DefaultLine = {
    start: claimText(line.opening_target),
    objective: claimText(line.initial_objective),
    win_condition: claimText(line.win_condition),
    create: claimText(line.manufacture),
    convert: claimText(line.conversion),
    alternative: alternativeFromBranches(raw.branches),
    reset: claimText(line.reset),
  };
  return {
    strategy_key: raw.strategy_key,
    strategy_id: raw.strategy_id,
    version: raw.version,
    status: raw.status,
    confidence: raw.evidence.confidence,
    sample_band: sampleBand(raw.evidence.total_games),
    our_comp: raw.our_comp,
    enemy_comp: raw.enemy_comp,
    enemy_short: shortEnemy(raw.enemy_comp),
    default_line,
    roles: {
      team: roleFromState(state, "team_objective"),
      priest: roleFromState(state, "priest_instruction"),
      rogue: roleFromState(state, "rogue_instruction"),
    },
    branches: (raw.branches ?? []).map(adaptBranch),
    failure_modes: (raw.failure_modes ?? []).map((f) => claimText(f)).filter(Boolean) as string[],
    evidence: {
      games: raw.evidence.total_games,
      wins: raw.evidence.wins,
      losses: raw.evidence.losses,
      unknown_result: raw.evidence.unknown_result,
      opening_target_known: opening.known,
      opening_target_unknown: opening.unknown,
      opening_targets: opening.values,
      kill_target_known: kills.known,
      kill_target_unknown: kills.unknown,
      kill_targets: kills.values,
      source_batches: raw.evidence.source_batches ?? {},
      supporting_match_ids: supporting,
      contradicting_match_ids: contradicting,
      classification_present: supporting.length > 0 || contradicting.length > 0,
      all_match_ids: raw.evidence.all_match_ids ?? [],
    },
    history,
  };
}

export function adaptPackage(raw: RawCanonicalPackage): CanonicalPackage {
  return {
    schema_version: raw.schema_version,
    package_version: raw.package_version,
    created_date: raw.created_date,
    prepared_corpus_version: raw.prepared_corpus_version,
    notes: raw.notes,
    friendly_comps: raw.friendly_comps,
    current: raw.current,
    strategies: raw.strategies.map(adaptStrategy),
  };
}
