import type { CardPresentation } from "./types";

const LABELS: [keyof CardPresentation, string[]][] = [
  ["start", ["Start"]],
  ["objective", ["Objective"]],
  ["win", ["Win condition"]],
  ["create", ["Create it"]],
  ["convert", ["Convert"]],
  ["alternative", ["Alternative"]],
  ["failure", ["Failure mode", "Failure"]],
  ["reset", ["Reset"]],
];

export function parseCardMarkdown(markdown: string, source?: string): CardPresentation {
  const out: CardPresentation = source ? { source } : {};
  for (const [key, labels] of LABELS) {
    for (const label of labels) {
      const match = markdown.match(new RegExp(`\\*\\*${label}:\\*\\*\\s*(.+)`));
      if (match?.[1]) {
        out[key] = match[1].trim();
        break;
      }
    }
  }
  return out;
}

export function firstSentence(text: string): string {
  const trimmed = text.trim();
  const match = trimmed.match(/^[^.!?]+[.!?]?/);
  return (match ? match[0] : trimmed).trim();
}
