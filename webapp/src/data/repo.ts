import { adaptPackage, hasStrategyContent, isApproved } from "./adapter";
import { currentStrategies, currentStrategy } from "./normalize";
import type { CanonicalPackage, CorpusHealth, RawCanonicalPackage, SlimMatch, Strategy } from "./types";
import { validateCanonicalPackage } from "./validate";

export { hasStrategyContent, isApproved };

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

export function parsePackage(raw: unknown): CanonicalPackage {
  const errors = validateCanonicalPackage(raw as RawCanonicalPackage);
  if (errors.length) {
    throw new Error(`Invalid canonical package:\n- ${errors.join("\n- ")}`);
  }
  return adaptPackage(raw as RawCanonicalPackage);
}

export async function loadPackage(): Promise<CanonicalPackage> {
  const raw = await loadJson<RawCanonicalPackage>(dataUrl("canonical-package.json"));
  return parsePackage(raw);
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

export function hasRoleText(strategy: Strategy): boolean {
  return (["team", "priest", "rogue"] as const).some((role) => {
    const view = strategy.roles[role];
    return Boolean(view.summary) || view.responsibilities.length > 0;
  });
}

export function emptyFriendlyMessage(name: string): string {
  return `No strategies for ${name} in the current canonical package.`;
}
