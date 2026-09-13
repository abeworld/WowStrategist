/** @vitest-environment jsdom */
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { act } from "react";
import { createRoot, type Root } from "react-dom/client";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeAll, describe, expect, it } from "vitest";
import App from "./App";
import { parsePackage } from "./data/repo";
import type { CanonicalPackage, SlimMatch } from "./data/types";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pkg: CanonicalPackage = parsePackage(
  JSON.parse(readFileSync(resolve(rootDir, "public/data/canonical-package.json"), "utf8")),
);
const matches = JSON.parse(readFileSync(resolve(rootDir, "public/data/matches-slim.json"), "utf8")) as SlimMatch[];
const health = JSON.parse(readFileSync(resolve(rootDir, "public/data/corpus-health.json"), "utf8"));

let container: HTMLDivElement;
let root: Root;

beforeAll(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  globalThis.fetch = async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes("canonical-package.json")) {
      return jsonResponse(JSON.parse(readFileSync(resolve(rootDir, "public/data/canonical-package.json"), "utf8")));
    }
    if (url.includes("matches-slim.json")) return jsonResponse(matches);
    if (url.includes("corpus-health.json")) return jsonResponse(health);
    return new Response("not found", { status: 404 });
  };
});

afterEach(() => {
  act(() => {
    root.unmount();
  });
  container.remove();
});

function jsonResponse(data: unknown): Response {
  return new Response(JSON.stringify(data), { headers: { "Content-Type": "application/json" } });
}

async function renderAt(path: string) {
  container = document.createElement("div");
  document.body.appendChild(container);
  root = createRoot(container);
  await act(async () => {
    root.render(
      <MemoryRouter initialEntries={[path]}>
        <App />
      </MemoryRouter>,
    );
  });
  await act(async () => {
    await Promise.resolve();
  });
}

async function typeQuery(value: string) {
  const input = container.querySelector("input");
  if (!input) throw new Error("missing enemy input");
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value")?.set;
  await act(async () => {
    setter?.call(input, value);
    input.dispatchEvent(new Event("input", { bubbles: true }));
  });
}

describe("encyclopedia smoke", () => {
  it("looks up hpal war and reversed pala warrior", async () => {
    await renderAt("/");
    expect(container.textContent).toContain("Instant matchup lookup");
    await typeQuery("hpal war");
    expect(container.textContent).toContain("Arms / HPal");
    await typeQuery("pala warrior");
    expect(container.textContent).toContain("Arms / HPal");
  });

  it("renders provisional Arms/HPal text from the current package pointer", async () => {
    await renderAt("/matchup/SPR_vs_Arms_HPal");
    expect(container.textContent).toContain("vs Arms / HPal");
    expect(container.textContent).toContain("SPR_vs_Arms_HPal_v2");
    expect(container.textContent).toContain("provisional");
    expect(container.textContent).toContain("Start on Warrior");
    expect(container.textContent).not.toContain("No approved strategy text");
    expect(container.textContent).toContain("not human-approved");
    expect(container.textContent).toContain("80 games");
    const rogue = Array.from(container.querySelectorAll("button")).find((b) => b.textContent === "Rogue POV");
    expect(rogue).toBeTruthy();
    await act(async () => {
      rogue!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });
    expect(container.textContent).toContain("Rogue POV");
    expect(container.textContent).toContain("Opening target");
    expect(container.textContent).toContain("Supporting matches");
    expect(container.textContent).toContain("Contradicting matches");
  });

  it("shows a missing-strategy empty state", async () => {
    await renderAt("/matchup/DiscSub_vs_Arms_HPal");
    expect(container.textContent).toContain("No strategy for");
  });

  it("lists coverage including data-driven empty friendly comps", async () => {
    await renderAt("/coverage");
    expect(container.textContent).toContain("Coverage");
    expect(container.textContent).toContain("Discipline Priest / Subtlety Rogue");
    expect(container.textContent).toContain("Arms / HPal");
    expect(container.textContent).toContain("Sample size");
    expect(container.textContent).toContain("Strategy confidence");
  });

  it("does not invent a Disc/Sub strategy from lookup", async () => {
    await renderAt("/");
    const select = container.querySelector("select");
    if (!select) throw new Error("missing friendly select");
    await act(async () => {
      select.value = "Discipline Priest / Subtlety Rogue";
      select.dispatchEvent(new Event("change", { bubbles: true }));
    });
    expect(container.textContent).toContain("No strategies for Discipline Priest / Subtlety Rogue");
    expect(container.textContent).not.toContain("Arms / HPal");
  });

  it("opens a supporting match evidence record", async () => {
    const arms = pkg.strategies.find((s) => s.strategy_key === "SPR_vs_Arms_HPal")!;
    const id = arms.evidence.supporting_match_ids[0];
    await renderAt(`/match/${encodeURIComponent(id)}`);
    expect(container.textContent).toContain("Evidence record");
    expect(container.textContent).toContain("Arms Warrior");
    expect(container.textContent).toContain("SPR_vs_Arms_HPal");
  });
});
