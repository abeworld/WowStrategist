import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  currentStrategies,
  currentStrategy,
  lookupStrategies,
  normalizeFriendly,
  tokenizeQuery,
} from "./normalize";
import { hasApprovedLine, hasRoleText } from "./repo";
import type { CanonicalPackage, SlimMatch, Strategy } from "./types";
import { validateCanonicalPackage, validateMatches } from "./validate";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const SPR = "Shadow Priest / Subtlety Rogue";
const DISC = "Discipline Priest / Subtlety Rogue";

function line(partial: Partial<Strategy["default_line"]> = {}): Strategy["default_line"] {
  return {
    start: null,
    objective: null,
    win_condition: null,
    convert: null,
    alternative: null,
    reset: null,
    ...partial,
  };
}

const EMPTY_EVIDENCE: Strategy["evidence"] = {
  games: 10,
  wins: 6,
  losses: 4,
  unknown_result: 0,
  opening_target_known: 10,
  opening_target_unknown: 0,
  opening_targets: {},
  kill_target_known: 8,
  kill_target_unknown: 2,
  kill_targets: {},
  source_batches: {},
  supporting_match_ids: [],
  counterexample_match_ids: [],
  all_match_ids: [],
};

function strategy(partial: Partial<Strategy> & Pick<Strategy, "strategy_key" | "strategy_id" | "enemy_comp">): Strategy {
  return {
    version: 1,
    status: "provisional",
    confidence: "medium",
    our_comp: SPR,
    enemy_short: partial.enemy_short ?? partial.enemy_comp,
    default_line: line(),
    roles: {
      team: { summary: null, responsibilities: [] },
      priest: { summary: null, responsibilities: [] },
      rogue: { summary: null, responsibilities: [] },
    },
    branches: [],
    failure_modes: [],
    evidence: { ...EMPTY_EVIDENCE },
    history: [],
    ...partial,
  };
}

const catalog = [
  strategy({
    strategy_key: "SPR_vs_Arms_HPal",
    strategy_id: "SPR_vs_Arms_HPal_v1",
    enemy_comp: "Arms Warrior / Holy Paladin",
    enemy_short: "Arms / HPal",
    evidence: {
      ...EMPTY_EVIDENCE,
      games: 80,
      supporting_match_ids: ["win-1"],
      counterexample_match_ids: ["loss-1"],
    },
  }),
  strategy({
    strategy_key: "SPR_vs_Frost_SP",
    strategy_id: "SPR_vs_Frost_SP_v1",
    enemy_comp: "Frost Mage / Shadow Priest",
    enemy_short: "Frost / SP",
  }),
  strategy({
    strategy_key: "SPR_vs_Fury_HPal",
    strategy_id: "SPR_vs_Fury_HPal_v1",
    enemy_comp: "Fury Warrior / Holy Paladin",
    enemy_short: "Fury / HPal",
    status: "insufficient_evidence",
    confidence: "low",
    evidence: { ...EMPTY_EVIDENCE, games: 2 },
  }),
  strategy({
    strategy_key: "SPR_vs_Destro_Ele",
    strategy_id: "SPR_vs_Destro_Ele_v2",
    version: 2,
    enemy_comp: "Destruction Warlock / Elemental Shaman",
    enemy_short: "Destro / Ele",
    default_line: line({ start: "Open lock", objective: "Force healer trinket" }),
    roles: {
      team: { summary: "Kill lock after healer trinket", responsibilities: ["Hold lock"] },
      priest: { summary: "Fear healer on go", responsibilities: ["Fear on go"] },
      rogue: { summary: "Stay on lock", responsibilities: ["Kidney lock"] },
    },
    branches: [{ when: "healer trinkets early", then: "swap lock" }],
    failure_modes: ["No kick on chaos bolt"],
  }),
  strategy({
    strategy_key: "SPR_vs_Destro_Ele",
    strategy_id: "SPR_vs_Destro_Ele_v1",
    version: 1,
    enemy_comp: "Destruction Warlock / Elemental Shaman",
    enemy_short: "Destro / Ele",
    default_line: line({ start: "stale v1 line" }),
  }),
];

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
    expect(forward[0]?.enemy_comp).toBe("Arms Warrior / Holy Paladin");
  });

  it("does not invent a Disc/Sub catalog", () => {
    expect(lookupStrategies(catalog, DISC, "hpal war")).toEqual([]);
  });

  it("returns empty for an unknown enemy query", () => {
    expect(lookupStrategies(catalog, SPR, "demo hunter")).toEqual([]);
  });
});

describe("current strategy version", () => {
  const current = {
    SPR_vs_Arms_HPal: "SPR_vs_Arms_HPal_v1",
    SPR_vs_Destro_Ele: "SPR_vs_Destro_Ele_v2",
    SPR_vs_Frost_SP: "SPR_vs_Frost_SP_v1",
    SPR_vs_Fury_HPal: "SPR_vs_Fury_HPal_v1",
  };

  it("uses the current map, not the _v1 suffix", () => {
    const hit = currentStrategy(catalog, current, "SPR_vs_Destro_Ele");
    expect(hit?.strategy_id).toBe("SPR_vs_Destro_Ele_v2");
    expect(hit?.default_line.start).toBe("Open lock");
  });

  it("does not keep stale v1 as current when v2 is published", () => {
    const live = currentStrategies(catalog, current);
    const dest = live.find((s) => s.strategy_key === "SPR_vs_Destro_Ele");
    expect(dest?.strategy_id).toBe("SPR_vs_Destro_Ele_v2");
    expect(live.filter((s) => s.strategy_key === "SPR_vs_Destro_Ele")).toHaveLength(1);
  });

  it("returns undefined for a missing strategy key", () => {
    expect(currentStrategy(catalog, current, "DiscSub_vs_Arms_HPal")).toBeUndefined();
  });
});

describe("sparse and empty strategy rendering inputs", () => {
  it("flags missing default line as not approved", () => {
    const empty = catalog.find((s) => s.strategy_key === "SPR_vs_Arms_HPal")!;
    expect(hasApprovedLine(empty)).toBe(false);
    expect(hasRoleText(empty)).toBe(false);
  });

  it("keeps insufficient_evidence status instead of inventing approval", () => {
    const sparse = catalog.find((s) => s.strategy_key === "SPR_vs_Fury_HPal")!;
    expect(sparse.status).toBe("insufficient_evidence");
    expect(sparse.confidence).toBe("low");
    expect(sparse.evidence.games).toBeLessThan(5);
    expect(hasApprovedLine(sparse)).toBe(false);
  });

  it("exposes priest and rogue views from the same object", () => {
    const rich = catalog.find((s) => s.strategy_id === "SPR_vs_Destro_Ele_v2")!;
    expect(rich.roles.priest.summary).toContain("Fear");
    expect(rich.roles.rogue.summary).toContain("lock");
    expect(rich.branches).toHaveLength(1);
    expect(rich.failure_modes).toHaveLength(1);
    expect(hasApprovedLine(rich)).toBe(true);
    expect(hasRoleText(rich)).toBe(true);
  });
});

describe("canonical package on disk", () => {
  const pkg = JSON.parse(
    readFileSync(resolve(root, "public/data/canonical-package.json"), "utf8"),
  ) as CanonicalPackage;
  const matches = JSON.parse(readFileSync(resolve(root, "public/data/matches-slim.json"), "utf8")) as SlimMatch[];

  it("validates schema and current-version pointers", () => {
    expect(validateCanonicalPackage(pkg)).toEqual([]);
    expect(pkg.schema_version).toBe("1.0.0");
    expect(pkg.friendly_comps).toContain(DISC);
    expect(pkg.strategies.some((s) => s.our_comp === DISC)).toBe(false);
  });

  it("does not invent approved strategy text", () => {
    for (const s of pkg.strategies) {
      expect(hasApprovedLine(s), s.strategy_id).toBe(false);
      expect(s.default_line.start).toBeNull();
      expect(s.branches).toEqual([]);
      expect(["provisional", "insufficient_evidence"]).toContain(s.status);
    }
  });

  it("looks up Arms/HPal from the real package with reversed aliases", () => {
    const hits = lookupStrategies(pkg.strategies, SPR, "war hpal");
    expect(hits[0]?.strategy_key).toBe("SPR_vs_Arms_HPal");
    expect(hits[0]?.evidence.games).toBeGreaterThan(0);
    expect(hits[0]?.strategy_id).toBe(pkg.current.SPR_vs_Arms_HPal);
  });

  it("keeps evidence match ids resolvable", () => {
    const errors = validateMatches(matches, pkg);
    expect(errors).toEqual([]);
    const sample = pkg.strategies.find((s) => s.strategy_key === "SPR_vs_Arms_HPal")!;
    expect(sample.evidence.supporting_match_ids.length).toBeGreaterThan(0);
    const match = matches.find((m) => m.match_id === sample.evidence.supporting_match_ids[0]);
    expect(match?.enemy_comp).toBe("Arms Warrior / Holy Paladin");
  });
});
