import { describe, expect, it } from "vitest";
import { adaptPackage, hasStrategyContent, isApproved } from "./adapter";
import { CurrentPointerError, currentStrategy, lookupStrategies, normalizeFriendly, tokenizeQuery } from "./normalize";
import type { CanonicalStrategy, Claim, RawCanonicalPackage } from "./types";
import { validateCanonicalPackage } from "./validate";

const SPR = "Shadow Priest / Subtlety Rogue";
const DISC = "Discipline Priest / Subtlety Rogue";

function claim(text: string, extras: Partial<Claim> = {}): Claim {
  return {
    text,
    basis: "inferred",
    confidence: "medium",
    supporting_match_ids: [],
    contradicting_match_ids: [],
    evidence_scope: "none",
    ...extras,
  };
}

function rawStrategy(
  partial: Partial<CanonicalStrategy> & Pick<CanonicalStrategy, "strategy_key" | "strategy_id" | "enemy_comp">,
): CanonicalStrategy {
  return {
    version: 1,
    schema_version: "1.0.0",
    status: "provisional",
    our_comp: SPR,
    evidence: {
      total_games: 10,
      wins: 6,
      losses: 4,
      unknown_result: 0,
      confidence: "medium",
      supporting_match_ids: ["win-but-wrong-line"],
      contradicting_match_ids: ["loss-executes-plan"],
      all_match_ids: ["win-but-wrong-line", "loss-executes-plan"],
    },
    facts: { opening_targets: { "Arms Warrior": 8, unknown: 2 }, kill_targets: { "Holy Paladin": 7 } },
    default_line: {
      opening_target: claim("Start Warrior"),
      initial_objective: claim("Draw Paladin trinket"),
      win_condition: claim("Kill Paladin"),
      manufacture: claim("Blind Warrior"),
      conversion: claim("Go Paladin"),
      reset: claim("After Shield, rebuild"),
    },
    states: [
      {
        state_id: "opening",
        team_objective: claim("Team opens Warrior"),
        priest_instruction: claim("Priest Saps Paladin"),
        rogue_instruction: claim("Rogue stuns Warrior"),
      },
    ],
    branches: [],
    failure_modes: [claim("Protection ends the go")],
    version_history: [{ version: 1, change: "initial" }],
    ...partial,
  };
}

function pkg(partial: Partial<RawCanonicalPackage> & Pick<RawCanonicalPackage, "current" | "strategies">): RawCanonicalPackage {
  return {
    schema_version: "1.0.0",
    package_version: "test",
    friendly_comps: [
      { name: SPR, status: "evidence_available", matchup_count: 1 },
      { name: DISC, status: "no_evidence", matchup_count: 0 },
    ],
    ...partial,
  };
}

describe("alias normalization", () => {
  it("maps friendly composition aliases", () => {
    expect(normalizeFriendly("SPR")).toBe(SPR);
    expect(normalizeFriendly("sp/r")).toBe(SPR);
    expect(normalizeFriendly("Shadow Rogue")).toBe(SPR);
    expect(normalizeFriendly("disc/sub")).toBe(DISC);
    expect(normalizeFriendly("not a comp")).toBeNull();
  });

  it("tokenizes punctuation the same way for common arena shorthand", () => {
    expect(tokenizeQuery("hpal/war")).toEqual(["hpal", "war"]);
    expect(tokenizeQuery("SP/R")).toEqual(["sp", "r"]);
  });
});

describe("matchup lookup", () => {
  const catalog = [
    rawStrategy({ strategy_key: "SPR_vs_Arms_HPal", strategy_id: "SPR_vs_Arms_HPal_v1", enemy_comp: "Arms Warrior / Holy Paladin" }),
    rawStrategy({ strategy_key: "SPR_vs_Frost_SP", strategy_id: "SPR_vs_Frost_SP_v1", enemy_comp: "Frost Mage / Shadow Priest" }),
    rawStrategy({ strategy_key: "SPR_vs_Fury_HPal", strategy_id: "SPR_vs_Fury_HPal_v1", enemy_comp: "Fury Warrior / Holy Paladin" }),
  ];

  it("resolves hpal war, pala warrior, war hpal, and holy arms to Arms/HPal", () => {
    for (const q of ["hpal war", "pala warrior", "war hpal", "holy arms"]) {
      const hits = lookupStrategies(catalog, SPR, q);
      expect(hits[0]?.strategy_key, q).toBe("SPR_vs_Arms_HPal");
    }
  });

  it("treats reversed enemy order as the same matchup", () => {
    const forward = lookupStrategies(catalog, SPR, "arms hpal");
    const reversed = lookupStrategies(catalog, SPR, "hpal arms");
    expect(forward.map((s) => s.strategy_key)).toEqual(reversed.map((s) => s.strategy_key));
  });

  it("does not invent a Disc/Sub catalog", () => {
    expect(lookupStrategies(catalog, DISC, "hpal war")).toEqual([]);
  });
});

describe("current strategy version", () => {
  const v1 = rawStrategy({
    strategy_key: "SPR_vs_Arms_HPal",
    strategy_id: "SPR_vs_Arms_HPal_v1",
    version: 1,
    enemy_comp: "Arms Warrior / Holy Paladin",
    default_line: {
      opening_target: claim("v1 start"),
      initial_objective: claim("v1 objective"),
      win_condition: claim("v1 win"),
      manufacture: claim("v1 create"),
      conversion: claim("v1 convert"),
      reset: claim("v1 reset"),
    },
  });
  const v2 = rawStrategy({
    strategy_key: "SPR_vs_Arms_HPal",
    strategy_id: "SPR_vs_Arms_HPal_v2",
    version: 2,
    enemy_comp: "Arms Warrior / Holy Paladin",
    default_line: {
      opening_target: claim("v2 start"),
      initial_objective: claim("v2 objective"),
      win_condition: claim("v2 win"),
      manufacture: claim("v2 create"),
      conversion: claim("v2 convert"),
      reset: claim("v2 reset"),
    },
  });
  const strategies = [v1, v2];

  it("uses current v1 even when v2 exists", () => {
    const hit = currentStrategy(strategies, { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" }, "SPR_vs_Arms_HPal");
    expect(hit?.strategy_id).toBe("SPR_vs_Arms_HPal_v1");
    expect(hit?.default_line.opening_target?.text).toBe("v1 start");
  });

  it("uses current v2 when the package points at v2", () => {
    const hit = currentStrategy(strategies, { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v2" }, "SPR_vs_Arms_HPal");
    expect(hit?.strategy_id).toBe("SPR_vs_Arms_HPal_v2");
  });

  it("fails clearly when current points at a missing version", () => {
    expect(() => currentStrategy(strategies, { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v3" }, "SPR_vs_Arms_HPal")).toThrow(
      CurrentPointerError,
    );
  });

  it("does not fall back to the highest version when the key is absent from current", () => {
    expect(currentStrategy(strategies, {}, "SPR_vs_Arms_HPal")).toBeUndefined();
  });
});

describe("approval semantics", () => {
  it("renders provisional text without calling it approved", () => {
    const adapted = adaptPackage(
      pkg({
        current: { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" },
        strategies: [
          rawStrategy({
            strategy_key: "SPR_vs_Arms_HPal",
            strategy_id: "SPR_vs_Arms_HPal_v1",
            enemy_comp: "Arms Warrior / Holy Paladin",
            status: "provisional",
          }),
        ],
      }),
    ).strategies[0];
    expect(hasStrategyContent(adapted.default_line)).toBe(true);
    expect(adapted.default_line.start).toEqual(expect.objectContaining({ kind: "present", text: "Start Warrior" }));
    expect(isApproved(adapted.status)).toBe(false);
    expect(adapted.status).toBe("provisional");
  });

  it("marks approved only from status", () => {
    const adapted = adaptPackage(
      pkg({
        current: { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" },
        strategies: [
          rawStrategy({
            strategy_key: "SPR_vs_Arms_HPal",
            strategy_id: "SPR_vs_Arms_HPal_v1",
            enemy_comp: "Arms Warrior / Holy Paladin",
            status: "approved",
          }),
        ],
      }),
    ).strategies[0];
    expect(isApproved(adapted.status)).toBe(true);
  });

  it("keeps insufficient_evidence even if some text exists", () => {
    const adapted = adaptPackage(
      pkg({
        current: { SPR_vs_Sparse: "SPR_vs_Sparse_v1" },
        strategies: [
          rawStrategy({
            strategy_key: "SPR_vs_Sparse",
            strategy_id: "SPR_vs_Sparse_v1",
            enemy_comp: "Fury Warrior / Holy Paladin",
            status: "insufficient_evidence",
            evidence: {
              total_games: 2,
              wins: 2,
              losses: 0,
              unknown_result: 0,
              confidence: "insufficient",
              supporting_match_ids: [],
              contradicting_match_ids: [],
              all_match_ids: ["a", "b"],
            },
            default_line: {
              opening_target: claim("unknown"),
              initial_objective: claim("unknown"),
              win_condition: claim("unknown"),
              manufacture: claim("unknown"),
              conversion: claim("unknown"),
              reset: claim("unknown"),
            },
          }),
        ],
      }),
    ).strategies[0];
    expect(adapted.status).toBe("insufficient_evidence");
    expect(hasStrategyContent(adapted.default_line)).toBe(false);
    expect(adapted.confidence).toBe("insufficient");
    expect(adapted.sample_band).toBe("low");
  });
});

describe("evidence classification", () => {
  it("does not treat result as supporting or contradicting", () => {
    const adapted = adaptPackage(
      pkg({
        current: { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" },
        strategies: [
          rawStrategy({
            strategy_key: "SPR_vs_Arms_HPal",
            strategy_id: "SPR_vs_Arms_HPal_v1",
            enemy_comp: "Arms Warrior / Holy Paladin",
          }),
        ],
      }),
    ).strategies[0];
    expect(adapted.evidence.supporting_match_ids).toEqual(["win-but-wrong-line"]);
    expect(adapted.evidence.contradicting_match_ids).toEqual(["loss-executes-plan"]);
  });

  it("uses canonical facts, not dirty prepared labels", () => {
    const adapted = adaptPackage(
      pkg({
        current: { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" },
        strategies: [
          rawStrategy({
            strategy_key: "SPR_vs_Arms_HPal",
            strategy_id: "SPR_vs_Arms_HPal_v1",
            enemy_comp: "Arms Warrior / Holy Paladin",
            facts: { opening_targets: { "Arms Warrior": 69, "Holy Paladin": 11 } },
          }),
        ],
      }),
    ).strategies[0];
    expect(adapted.evidence.opening_targets["Arms Warrior"]).toBe(69);
    expect(adapted.evidence.opening_targets["Warrior"]).toBeUndefined();
  });
});

describe("package validation", () => {
  const valid = pkg({
    current: { SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1" },
    strategies: [
      rawStrategy({
        strategy_key: "SPR_vs_Arms_HPal",
        strategy_id: "SPR_vs_Arms_HPal_v1",
        enemy_comp: "Arms Warrior / Holy Paladin",
      }),
    ],
  });

  it("accepts a well-formed package", () => {
    expect(validateCanonicalPackage(valid)).toEqual([]);
  });

  it("rejects duplicate ids", () => {
    const dup = structuredClone(valid);
    dup.strategies.push(dup.strategies[0]);
    expect(validateCanonicalPackage(dup).some((e) => e.includes("duplicate"))).toBe(true);
  });

  it("rejects a broken current pointer", () => {
    const broken = structuredClone(valid);
    broken.current.SPR_vs_Arms_HPal = "SPR_vs_Arms_HPal_v3";
    expect(validateCanonicalPackage(broken).some((e) => e.includes("missing SPR_vs_Arms_HPal_v3"))).toBe(true);
  });

  it("rejects current pointer to the wrong key", () => {
    const broken = structuredClone(valid);
    broken.strategies[0].strategy_key = "SPR_vs_Other";
    expect(validateCanonicalPackage(broken).some((e) => e.includes("with key"))).toBe(true);
  });

  it("rejects invalid status and confidence", () => {
    const broken = structuredClone(valid);
    broken.strategies[0].status = "maybe" as CanonicalStrategy["status"];
    broken.strategies[0].evidence.confidence = "sure" as CanonicalStrategy["evidence"]["confidence"];
    const errors = validateCanonicalPackage(broken);
    expect(errors.some((e) => e.includes("status"))).toBe(true);
    expect(errors.some((e) => e.includes("confidence"))).toBe(true);
  });

  it("rejects unsupported schema version", () => {
    const broken = structuredClone(valid);
    broken.schema_version = "9.9.9";
    expect(validateCanonicalPackage(broken).some((e) => e.includes("unsupported schema"))).toBe(true);
  });

  it("rejects missing default_line structure", () => {
    const broken = structuredClone(valid);
    broken.strategies[0].default_line = null as unknown as CanonicalStrategy["default_line"];
    expect(validateCanonicalPackage(broken).some((e) => e.includes("default_line"))).toBe(true);
  });
});

describe("data-driven friendly comps", () => {
  it("shows Disc/Sub only from package metadata, and can include it when strategies exist", () => {
    const withDisc = pkg({
      friendly_comps: [{ name: DISC, status: "evidence_available", matchup_count: 1 }],
      current: { DiscSub_vs_Arms_HPal: "DiscSub_vs_Arms_HPal_v1" },
      strategies: [
        rawStrategy({
          strategy_key: "DiscSub_vs_Arms_HPal",
          strategy_id: "DiscSub_vs_Arms_HPal_v1",
          our_comp: DISC,
          enemy_comp: "Arms Warrior / Holy Paladin",
        }),
      ],
    });
    const adapted = adaptPackage(withDisc);
    expect(adapted.friendly_comps.some((c) => c.name === DISC)).toBe(true);
    expect(lookupStrategies(adapted.strategies, DISC, "hpal war")[0]?.strategy_key).toBe("DiscSub_vs_Arms_HPal");
  });
});
