export const SUPPORTED_SCHEMA = "1.0.0";

export type StrategyStatus = "provisional" | "insufficient_evidence" | "approved" | "superseded";
export type StrategyConfidence = "high" | "medium" | "low" | "insufficient";
export type SampleBand = "high" | "medium" | "low";

export interface Claim {
  text: string;
  basis?: string;
  confidence?: string;
  supporting_match_ids?: string[];
  contradicting_match_ids?: string[];
  evidence_scope?: string;
}

export interface CanonicalDefaultLine {
  opening_target?: Claim | null;
  initial_objective?: Claim | null;
  win_condition?: Claim | null;
  manufacture?: Claim | null;
  conversion?: Claim | null;
  reset?: Claim | null;
  important_resources?: unknown[];
}

export interface CanonicalState {
  state_id: string;
  description?: string;
  team_objective?: Claim | null;
  priest_instruction?: Claim | null;
  rogue_instruction?: Claim | null;
}

export interface CanonicalBranch {
  branch_id?: string;
  trigger?: Claim | null;
  response?: Claim | null;
  classification?: string;
  team_objective?: Claim | null;
  priest_instruction?: Claim | null;
  rogue_instruction?: Claim | null;
}

export interface CanonicalStrategy {
  strategy_key: string;
  strategy_id: string;
  version: number;
  schema_version?: string;
  status: StrategyStatus;
  our_comp: string;
  enemy_comp: string;
  evidence: {
    total_games: number;
    wins: number;
    losses: number;
    unknown_result: number;
    confidence: StrategyConfidence;
    supporting_match_ids: string[];
    contradicting_match_ids: string[];
    representative_match_ids?: string[];
    all_match_ids: string[];
    data_quality_notes?: string[];
    source_batches?: Record<string, number>;
  };
  facts?: {
    opening_targets?: Record<string, number>;
    kill_targets?: Record<string, number>;
  };
  default_line: CanonicalDefaultLine;
  states?: CanonicalState[];
  branches?: CanonicalBranch[];
  failure_modes?: Claim[];
  version_history?: { version: number; date?: string; change?: string; reason?: string }[];
}

export interface FriendlyComp {
  name: string;
  status: string;
  matchup_count: number;
}

export interface RawCanonicalPackage {
  schema_version: string;
  package_version: string;
  created_date?: string;
  prepared_corpus_version?: string;
  notes?: string;
  friendly_comps: FriendlyComp[];
  current: Record<string, string>;
  strategies: CanonicalStrategy[];
}

export interface DefaultLine {
  start: string | null;
  objective: string | null;
  win_condition: string | null;
  create: string | null;
  convert: string | null;
  alternative: string | null;
  reset: string | null;
}

export interface RoleView {
  summary: string | null;
  responsibilities: string[];
}

export interface Branch {
  when: string;
  then: string;
  classification?: string;
}

export interface Strategy {
  strategy_key: string;
  strategy_id: string;
  version: number;
  status: StrategyStatus;
  confidence: StrategyConfidence;
  sample_band: SampleBand;
  our_comp: string;
  enemy_comp: string;
  enemy_short: string;
  default_line: DefaultLine;
  roles: {
    team: RoleView;
    priest: RoleView;
    rogue: RoleView;
  };
  branches: Branch[];
  failure_modes: string[];
  evidence: {
    games: number;
    wins: number;
    losses: number;
    unknown_result: number;
    opening_target_known: number;
    opening_target_unknown: number;
    opening_targets: Record<string, number>;
    kill_target_known: number;
    kill_target_unknown: number;
    kill_targets: Record<string, number>;
    source_batches: Record<string, number>;
    supporting_match_ids: string[];
    contradicting_match_ids: string[];
    classification_present: boolean;
    all_match_ids: string[];
  };
  history: { strategy_id: string; version: number; note: string }[];
}

export interface CanonicalPackage {
  schema_version: string;
  package_version: string;
  created_date?: string;
  prepared_corpus_version?: string;
  notes?: string;
  friendly_comps: FriendlyComp[];
  current: Record<string, string>;
  strategies: Strategy[];
}

export interface SlimMatch {
  match_id: string;
  matchup: string | null;
  result: string | null;
  our_comp: string | null;
  enemy_comp: string | null;
  opening_target: string | null;
  opening_cc: string | null;
  kill_target: string | null;
  source_batch: string | null;
  source_clip: string | null;
  quality_flags: string[];
  confidence: string | null;
  analysis_status: string | null;
  observed: string[];
  inferred: string[];
  unknown: string[];
  win_condition_from_source: string | null;
  failure_from_source: string | null;
}

export interface CorpusHealth {
  valid_2v2: number;
  assigned: number;
  unresolved: number;
  excluded: number;
  matchup_groups: number;
  friendly_comps: FriendlyComp[];
  coverage: { high: number; medium: number; low: number };
}
