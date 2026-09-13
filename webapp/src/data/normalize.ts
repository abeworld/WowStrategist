const SPEC_ALIASES: Record<string, string> = {
  spr: "Shadow Priest / Subtlety Rogue",
  "sp/r": "Shadow Priest / Subtlety Rogue",
  "sp/rogue": "Shadow Priest / Subtlety Rogue",
  "sp rogue": "Shadow Priest / Subtlety Rogue",
  "shadow rogue": "Shadow Priest / Subtlety Rogue",
  "shadow priest / subtlety rogue": "Shadow Priest / Subtlety Rogue",
  "subtlety rogue / shadow priest": "Shadow Priest / Subtlety Rogue",
  discsub: "Discipline Priest / Subtlety Rogue",
  "disc/sub": "Discipline Priest / Subtlety Rogue",
  "disc rogue": "Discipline Priest / Subtlety Rogue",
  "disc/rogue": "Discipline Priest / Subtlety Rogue",
  "discipline priest / subtlety rogue": "Discipline Priest / Subtlety Rogue",
  hpal: "Holy Paladin",
  hpala: "Holy Paladin",
  "holy paladin": "Holy Paladin",
  "holy pala": "Holy Paladin",
  pala: "Paladin",
  paladin: "Paladin",
  ret: "Retribution Paladin",
  "ret pala": "Retribution Paladin",
  "retribution paladin": "Retribution Paladin",
  arms: "Arms Warrior",
  "arms warrior": "Arms Warrior",
  war: "Warrior",
  warr: "Warrior",
  warrior: "Warrior",
  fury: "Fury Warrior",
  protwar: "Protection Warrior",
  "prot warrior": "Protection Warrior",
  frost: "Frost Mage",
  "frost mage": "Frost Mage",
  mage: "Mage",
  arcane: "Arcane Mage",
  fire: "Fire Mage",
  feral: "Feral Druid",
  boomkin: "Balance Druid",
  balance: "Balance Druid",
  "balance druid": "Balance Druid",
  resto: "Restoration Druid",
  "resto druid": "Restoration Druid",
  rsham: "Restoration Shaman",
  "resto sham": "Restoration Shaman",
  ele: "Elemental Shaman",
  enh: "Enhancement Shaman",
  unholy: "Unholy Death Knight",
  dk: "Death Knight",
  mm: "Marksmanship Hunter",
  hunter: "Hunter",
  destro: "Destruction Warlock",
  lock: "Warlock",
  aff: "Affliction Warlock",
  sp: "Shadow Priest",
  "shadow priest": "Shadow Priest",
  disc: "Discipline Priest",
  "disc priest": "Discipline Priest",
  sub: "Subtlety Rogue",
  rogue: "Rogue",
  sin: "Assassination Rogue",
};

export function tokenizeQuery(input: string): string[] {
  return input
    .toLowerCase()
    .replace(/[+/_,-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .split(" ")
    .filter(Boolean);
}

export function expandToken(token: string): string {
  return SPEC_ALIASES[token] ?? token;
}

export function normalizeFriendly(input: string): string | null {
  const key = input.toLowerCase().replace(/\s+/g, " ").trim();
  if (SPEC_ALIASES[key]) {
    const value = SPEC_ALIASES[key];
    if (value.includes("/")) return value;
  }
  if (key === "shadow priest / subtlety rogue") return "Shadow Priest / Subtlety Rogue";
  if (key === "discipline priest / subtlety rogue") return "Discipline Priest / Subtlety Rogue";
  return null;
}

function tokensMatchMember(tokens: string[], member: string): boolean {
  const hay = member.toLowerCase();
  const short = hay
    .split(" ")
    .map((w) => w[0])
    .join("");
  return tokens.some((t) => {
    const expanded = expandToken(t).toLowerCase();
    return (
      hay.includes(t) ||
      hay.includes(expanded) ||
      expanded.includes(hay) ||
      short === t ||
      member.toLowerCase().replace(/\s+/g, "") === t
    );
  });
}

export function scoreEnemyQuery(query: string, enemyComp: string): number {
  const tokens = tokenizeQuery(query);
  if (!tokens.length) return 0;
  const members = enemyComp.split(" / ").map((s) => s.trim());
  let hits = 0;
  for (const member of members) {
    if (tokensMatchMember(tokens, member)) hits += 1;
  }
  const joined = enemyComp.toLowerCase();
  const raw = query.toLowerCase();
  if (joined.includes(raw)) hits += 2;
  return hits;
}

export function lookupStrategies<T extends { our_comp: string; enemy_comp: string; strategy_key: string }>(
  strategies: T[],
  ourComp: string,
  enemyQuery: string,
): T[] {
  const ours = strategies.filter((s) => s.our_comp === ourComp);
  const q = enemyQuery.trim();
  if (!q) return ours.slice().sort((a, b) => a.enemy_comp.localeCompare(b.enemy_comp));
  return ours
    .map((s) => ({
      s,
      score:
        scoreEnemyQuery(q, s.enemy_comp) +
        scoreEnemyQuery(q, (s as { enemy_short?: string }).enemy_short ?? ""),
    }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score || a.s.enemy_comp.localeCompare(b.s.enemy_comp))
    .map((x) => x.s);
}

export class CurrentPointerError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CurrentPointerError";
  }
}

export function currentStrategy<T extends { strategy_key: string; strategy_id: string }>(
  strategies: T[],
  current: Record<string, string>,
  strategyKey: string,
): T | undefined {
  if (!Object.prototype.hasOwnProperty.call(current, strategyKey)) return undefined;
  const currentId = current[strategyKey];
  const hit = strategies.find((s) => s.strategy_id === currentId);
  if (!hit) {
    throw new CurrentPointerError(`current ${strategyKey} points at missing ${currentId}`);
  }
  if (hit.strategy_key !== strategyKey) {
    throw new CurrentPointerError(`current ${strategyKey} points at ${currentId} with key ${hit.strategy_key}`);
  }
  return hit;
}

export function currentStrategies<T extends { strategy_key: string; strategy_id: string }>(
  strategies: T[],
  current: Record<string, string>,
): T[] {
  const out: T[] = [];
  for (const key of Object.keys(current)) {
    const hit = currentStrategy(strategies, current, key);
    if (hit) out.push(hit);
  }
  return out;
}
