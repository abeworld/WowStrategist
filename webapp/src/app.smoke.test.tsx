/** @vitest-environment jsdom */
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { act } from "react";
import { createRoot, type Root } from "react-dom/client";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeAll, describe, expect, it } from "vitest";
import App from "./App";
import type { CanonicalPackage, SlimMatch } from "./data/types";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pkg = JSON.parse(readFileSync(resolve(rootDir, "public/data/canonical-package.json"), "utf8")) as CanonicalPackage;
const matches = JSON.parse(readFileSync(resolve(rootDir, "public/data/matches-slim.json"), "utf8")) as SlimMatch[];
const health = JSON.parse(readFileSync(resolve(rootDir, "public/data/corpus-health.json"), "utf8"));

let container: HTMLDivElement;
let root: Root;

beforeAll(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  globalThis.fetch = async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes("canonical-package.json")) return jsonResponse(pkg);
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
    expect(container.textContent).toContain("487");
    await typeQuery("hpal war");
    expect(container.textContent).toContain("Arms / HPal");
    await typeQuery("pala warrior");
    expect(container.textContent).toContain("Arms / HPal");
  });

  it("renders the Arms/HPal card with empty default plan, role tabs, and evidence", async () => {
    await renderAt("/matchup/SPR_vs_Arms_HPal");
    expect(container.textContent).toContain("vs Arms / HPal");
    expect(container.textContent).toContain("SPR_vs_Arms_HPal_v1");
    expect(container.textContent).toContain("No approved strategy text");
    expect(container.textContent).toContain("provisional");
    expect(container.textContent).toContain("80 games");
    const rogue = Array.from(container.querySelectorAll("button")).find((b) => b.textContent === "Rogue POV");
    expect(rogue).toBeTruthy();
    await act(async () => {
      rogue!.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });
    expect(container.textContent).toContain("Rogue POV");
    expect(container.textContent).toContain("Unknown — not in canonical package");
    expect(container.textContent).toContain("Opening target");
    expect(container.textContent).toContain("Supporting wins");
  });

  it("shows a missing-strategy empty state", async () => {
    await renderAt("/matchup/DiscSub_vs_Arms_HPal");
    expect(container.textContent).toContain("No strategy for");
  });

  it("lists coverage including Disc/Sub with no evidence", async () => {
    await renderAt("/coverage");
    expect(container.textContent).toContain("Coverage");
    expect(container.textContent).toContain("Disc / Sub");
    expect(container.textContent).toContain("insufficient_evidence");
    expect(container.textContent).toContain("Arms / HPal");
  });

  it("does not invent a Disc/Sub strategy from lookup", async () => {
    await renderAt("/");
    const select = container.querySelector("select");
    if (!select) throw new Error("missing friendly select");
    await act(async () => {
      select.value = "Discipline Priest / Subtlety Rogue";
      select.dispatchEvent(new Event("change", { bubbles: true }));
    });
    expect(container.textContent).toContain("No Discipline Priest / Subtlety Rogue evidence");
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
