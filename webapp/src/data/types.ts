export type StrategyStatus = "provisional" | "insufficient_evidence" | "approved";

export interface DefaultLine {
  start: string | null;
  objective: string | null;
  win_condition: string | null;
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
}

export interface Strategy {
  strategy_key: string;
  strategy_id: string;
  version: number;
  status: StrategyStatus;
  confidence: "high" | "medium" | "low";
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
    counterexample_match_ids: string[];
    all_match_ids: string[];
  };
  history: { strategy_id: string; version: number; note: string }[];
}

export interface CanonicalPackage {
  schema_version: string;
  package_version: string;
  package_id: string;
  notes: string;
  friendly_comps: string[];
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
  disc_sub_evidence: number;
}
