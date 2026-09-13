import { firstSentence } from "./presentation";
import type {
  Branch,
  CanonicalBranch,
  CanonicalField,
  CanonicalPackage,
  CanonicalResource,
  CanonicalState,
  CanonicalStrategy,
  CardPresentation,
  Claim,
  DefaultLine,
  QuickPlan,
  RawCanonicalPackage,
  SampleBand,
  Strategy,
  StrategyResource,
  StrategyState,
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

const STATE_LABELS: Record<string, string> = {
  opening: "Opening",
  pressure: "Pressure / Setup",
  conversion: "Conversion",
  recovery: "Recovery",
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

export function claimField(claim: Claim | string | null | undefined): CanonicalField {
  if (claim == null) return { kind: "missing" };
  const text = typeof claim === "string" ? claim : claim.text;
  if (typeof text !== "string" || !text.trim()) return { kind: "missing" };
  const trimmed = text.trim();
  const basis = typeof claim === "object" ? claim.basis : undefined;
  const confidence = typeof claim === "object" ? claim.confidence : undefined;
  if (trimmed.toLowerCase() === "unknown" || basis === "unknown") {
    return { kind: "explicit_unknown" };
  }
  return { kind: "present", text: trimmed, basis, confidence };
}

export function fieldText(field: CanonicalField): string | null {
  return field.kind === "present" ? field.text : null;
}

export function hasStrategyContent(line: DefaultLine): boolean {
  return (["start", "objective", "win_condition", "create", "convert", "reset"] as const).some(
    (key) => line[key].kind === "present",
  );
}

export function isApproved(status: string): boolean {
  return status === "approved";
}

export function unknownRoleMessage(role: "priest" | "rogue" | "team"): string {
  if (role === "priest") return "No reliable Priest-specific instruction established from this corpus.";
  if (role === "rogue") return "No reliable Rogue-specific instruction established from this corpus.";
  return "Canonical analysis marks this team instruction as unknown.";
}

export function missingFieldMessage(): string {
  return "Canonical field not present in this package version.";
}

export function renderField(field: CanonicalField, role?: "priest" | "rogue" | "team"): string {
  if (field.kind === "present") return field.text;
  if (field.kind === "explicit_unknown") return unknownRoleMessage(role ?? "team");
  return missingFieldMessage();
}

function stateLabel(id: string): string {
  return STATE_LABELS[id] ?? id.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function adaptState(state: CanonicalState): StrategyState {
  return {
    state_id: state.state_id,
    label: stateLabel(state.state_id),
    team: claimField(state.team_objective),
    priest: claimField(state.priest_instruction),
    rogue: claimField(state.rogue_instruction),
  };
}

function adaptResource(resource: CanonicalResource): StrategyResource {
  return {
    name: resource.name,
    relevance: resource.relevance ?? null,
    assessment: claimField(resource.assessment),
    requirement: resource.requirement ?? null,
  };
}

function adaptBranch(branch: CanonicalBranch): Branch {
  const response = claimField(branch.response);
  return {
    id: branch.branch_id,
    when: claimField(branch.trigger),
    then: response.kind === "missing" ? claimField(branch.team_objective) : response,
    classification: branch.classification,
    confidence: branch.confidence,
  };
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

function fromCardOrClaim(card: string | undefined, field: CanonicalField): string | null {
  if (card) return card;
  if (field.kind === "present") return firstSentence(field.text);
  return null;
}

function adaptQuickPlan(line: DefaultLine, failure: CanonicalField, card?: CardPresentation): QuickPlan {
  const fromCard = Boolean(card && (card.start || card.objective || card.win));
  return {
    start: fromCardOrClaim(card?.start, line.start),
    objective: fromCardOrClaim(card?.objective, line.objective),
    win: fromCardOrClaim(card?.win, line.win_condition),
    create: fromCardOrClaim(card?.create, line.create),
    convert: fromCardOrClaim(card?.convert, line.convert),
    alternative: card?.alternative ?? null,
    failure: fromCardOrClaim(card?.failure, failure),
    reset: fromCardOrClaim(card?.reset, line.reset),
    source: fromCard ? "card" : "claim-first-sentence",
  };
}

export function adaptStrategy(raw: CanonicalStrategy, card?: CardPresentation): Strategy {
  const line = raw.default_line ?? {};
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
    start: claimField(line.opening_target),
    objective: claimField(line.initial_objective),
    win_condition: claimField(line.win_condition),
    create: claimField(line.manufacture),
    convert: claimField(line.conversion),
    reset: claimField(line.reset),
  };
  const failure_modes = (raw.failure_modes ?? []).map((f) => claimField(f));
  const states = (raw.states ?? []).map(adaptState);
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
    quick_plan: adaptQuickPlan(default_line, failure_modes[0] ?? { kind: "missing" }, card),
    default_line,
    states,
    resources: (line.important_resources ?? []).map(adaptResource),
    branches: (raw.branches ?? []).map(adaptBranch),
    failure_modes,
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
    strategies: raw.strategies.map((s) => adaptStrategy(s, raw.presentations?.[s.strategy_id])),
  };
}
