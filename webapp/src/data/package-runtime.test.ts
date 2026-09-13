import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { adaptPackage, renderField } from "./adapter";
import { parseCardMarkdown } from "./presentation";
import { parsePackage } from "./repo";
import type { RawCanonicalPackage } from "./types";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const raw = JSON.parse(readFileSync(resolve(root, "public/data/canonical-package.json"), "utf8")) as RawCanonicalPackage;
const pkg = parsePackage(raw);

function current(key: string) {
  const id = pkg.current[key];
  const hit = pkg.strategies.find((s) => s.strategy_id === id);
  expect(hit, key).toBeTruthy();
  return hit!;
}

describe("runtime package is canonical 1.1.0, not the evidence fixture", () => {
  it("rejects a silent revert to package 0.1.0", () => {
    expect(raw.package_version).not.toBe("0.1.0");
    expect(raw.package_id).toBeUndefined();
    expect(raw.package_version).toBe("1.1.0");
    expect(raw.presentations?.SPR_vs_Destro_HPal_v1?.start).toMatch(/Destruction Warlock/);
    const fixtureNotes = String(raw.notes || "");
    expect(fixtureNotes).not.toMatch(/until Astra supplies approved strategy versions/i);
  });
});

describe("current matchups from installed package", () => {
  it("Arms/HPal v2 has a populated plan, states, and branches", () => {
    const s = current("SPR_vs_Arms_HPal");
    expect(s.strategy_id).toBe("SPR_vs_Arms_HPal_v2");
    expect(s.quick_plan.start).toMatch(/Warrior/);
    expect(s.default_line.start.kind).toBe("present");
    expect(s.states.map((st) => st.state_id)).toEqual(expect.arrayContaining(["opening", "pressure", "conversion", "recovery"]));
    expect(s.branches.length).toBeGreaterThan(0);
    expect(s.failure_modes.some((f) => f.kind === "present")).toBe(true);
    expect(s.resources.length).toBeGreaterThan(0);
  });

  it("SP/Sub v2 and Disc/Feral v2 are current and have start text", () => {
    const mirror = current("SPR_vs_SP_Sub");
    expect(mirror.strategy_id).toBe("SPR_vs_SP_Sub_v2");
    expect(mirror.quick_plan.start).toBeTruthy();
    const feral = current("SPR_vs_Disc_Feral");
    expect(feral.strategy_id).toBe("SPR_vs_Disc_Feral_v2");
    expect(feral.quick_plan.start).toMatch(/Feral/i);
  });

  it("Destro/HPal v1 is populated from canonical data, with explicit unknown roles", () => {
    const s = current("SPR_vs_Destro_HPal");
    expect(s.strategy_id).toBe("SPR_vs_Destro_HPal_v1");
    expect(s.quick_plan.start).toMatch(/Destruction Warlock/);
    expect(s.quick_plan.objective).toBeTruthy();
    expect(s.quick_plan.win).toBeTruthy();
    expect(s.quick_plan.create).toBeTruthy();
    expect(s.quick_plan.convert).toBeTruthy();
    expect(s.quick_plan.reset).toBeTruthy();
    expect(s.quick_plan.alternative).toMatch(/Paladin/);
    expect(s.default_line.start.kind).toBe("present");
    expect(s.default_line.objective.kind).toBe("present");
    expect(s.default_line.win_condition.kind).toBe("present");
    expect(s.default_line.create.kind).toBe("present");
    expect(s.default_line.convert.kind).toBe("present");
    expect(s.default_line.reset.kind).toBe("present");
    expect(s.states.some((st) => st.team.kind === "present")).toBe(true);
    expect(s.branches.some((b) => (b.classification || "").includes("reactive"))).toBe(true);
    expect(s.failure_modes.some((f) => f.kind === "present")).toBe(true);
    expect(s.resources.map((r) => r.name).join(" ")).toMatch(/Succubus/);
    expect(s.resources.map((r) => r.name).join(" ")).toMatch(/Divine Shield/);
    expect(s.resources.every((r) => (r.relevance || "").includes("conditional") || r.requirement)).toBe(true);
    const priestUnknown = s.states.filter((st) => st.priest.kind === "explicit_unknown");
    expect(priestUnknown.length).toBeGreaterThan(0);
    expect(renderField(priestUnknown[0].priest, "priest")).toMatch(/No reliable Priest-specific instruction/);
    expect(renderField(s.states[0].rogue, "rogue")).toMatch(/No reliable Rogue-specific instruction/);
    expect(renderField(s.states[0].priest, "priest")).not.toMatch(/not in canonical package/);
  });

  it("keeps a sparse matchup as insufficient without inventing a plan", () => {
    const s = current("SPR_vs_Enh_Sub");
    expect(s.status).toBe("insufficient_evidence");
    expect(s.confidence).toBe("insufficient");
  });
});

describe("card presentation parser", () => {
  it("reads compact Start/Alternative lines without inventing text", () => {
    const card = parseCardMarkdown(
      "**Start:** Destruction Warlock; recorded in 13/16 games.\n**Alternative:** Repeated later Paladin branches also convert.\n",
    );
    expect(card.start).toBe("Destruction Warlock; recorded in 13/16 games.");
    expect(card.alternative).toMatch(/Paladin/);
  });
});

describe("adapter does not drop a real reactive branch", () => {
  it("keeps branches whose classification is not the word alternative", () => {
    const adapted = adaptPackage(raw);
    const destro = adapted.strategies.find((s) => s.strategy_id === adapted.current.SPR_vs_Destro_HPal)!;
    expect(destro.branches).toHaveLength(1);
    expect(destro.branches[0].classification).toBe("real reactive branch");
  });
});
