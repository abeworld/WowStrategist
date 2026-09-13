import type { CanonicalPackage, CorpusHealth, SlimMatch, Strategy } from "./types";
import { currentStrategies, currentStrategy } from "./normalize";

function dataUrl(file: string): string {
  const base = import.meta.env.BASE_URL.endsWith("/")
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`;
  return `${base}data/${file}`;
}

async function loadJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}`);
  return (await res.json()) as T;
}

export async function loadPackage(): Promise<CanonicalPackage> {
  return loadJson(dataUrl("canonical-package.json"));
}

export async function loadMatches(): Promise<SlimMatch[]> {
  return loadJson(dataUrl("matches-slim.json"));
}

export async function loadHealth(): Promise<CorpusHealth> {
  return loadJson(dataUrl("corpus-health.json"));
}

export function resolveCurrent(pkg: CanonicalPackage, strategyKey: string): Strategy | undefined {
  return currentStrategy(pkg.strategies, pkg.current, strategyKey);
}

export function resolveCatalog(pkg: CanonicalPackage): Strategy[] {
  return currentStrategies(pkg.strategies, pkg.current);
}

export function hasApprovedLine(strategy: Strategy): boolean {
  const line = strategy.default_line;
  return Boolean(line.start || line.objective || line.win_condition);
}

export function hasRoleText(strategy: Strategy): boolean {
  return (["team", "priest", "rogue"] as const).some((role) => {
    const view = strategy.roles[role];
    return Boolean(view.summary) || view.responsibilities.length > 0;
  });
}
