// Tagesbilanz: zählt, was jemand an einem Fastentag schon gegessen hat, vergleicht es mit dem Tageslimit
// nach Longo und schlägt vor, wie sich der Rest des Tages passend füllen lässt.
// Läuft im Browser und in Node (Tests).
import { BY_NAME, FOODS, search, solve, totals, verdict, norm } from './rechner.js';
import { RECIPES, BY_SLUG, PLAN, nutrition } from './nutrition.js';

/** Eine kleine Tasse Kaffee in ml. Mehr als eine pro Tag ist nicht vorgesehen (Empfehlung des ProLon-Herstellers). */
export const CUP_ML = 150;
/** Kürbis an Tag 2 bis 5: höchstens ca. 200 g, sonst geht zu viel vom Zuckerbudget drauf. */
export const PUMPKIN_MAX = 200;
const PUMPKIN = ['Hokkaido-Kürbis', 'Gartenkürbis'];
const COFFEE = 'Kaffee';
const TEA_CUP = 200;

/** Einheiten, in denen sich ein Lebensmittel oder Rezept eintragen lässt: [Schlüssel, Bezeichnung, Gramm je Einheit]. */
export function units(entry) {
  if (entry.type === 'recipe') return [['portion', 'Portion', 1]];
  const f = BY_NAME[entry.name];
  const fluid = f.group === 'getraenk' || f.name === 'Gemüsebrühe' || /saft|essig|Balsamico|Sojasauce/i.test(f.name);
  const out = [[fluid ? 'ml' : 'g', fluid ? 'ml' : 'g', 1]];
  if (f.name === COFFEE) out.push(['cup', 'kleine Tasse', CUP_ML]);
  else if (f.group === 'getraenk') out.push(['cup', 'Tasse', TEA_CUP]);
  if (f.piece) out.push(['piece', f.piece[0], f.piece[1]]);
  return out;
}

/** Vorschlag für die Menge, wenn jemand ein Lebensmittel neu einträgt. */
export function defaultAmount(entry) {
  if (entry.type === 'recipe') return { qty: 1, unit: 'portion' };
  const f = BY_NAME[entry.name];
  if (f.piece && ['gemuese', 'knolle', 'obst', 'blatt', 'pilze'].includes(f.group)) return { qty: 1, unit: 'piece' };
  if (f.group === 'getraenk') return { qty: 1, unit: 'cup' };
  const g = { fett: 10, nuss: 15, kraeuter: 5, wuerze: 5, fettfrucht: 20 }[f.group] ?? 100;
  return { qty: g, unit: units(entry)[0][0] };
}

/** Gramm eines Eintrags (bei Rezepten: Portionen). */
export function grams(entry) {
  const u = units(entry).find((x) => x[0] === entry.unit) || units(entry)[0];
  return Math.max(0, +entry.qty || 0) * u[2];
}

/** Text für die Menge eines Eintrags, z. B. „1 Stück (200 g)“ oder „1,5 Portionen“. */
export function qtyLabel(entry) {
  const q = Number(entry.qty).toLocaleString('de-DE', { maximumFractionDigits: 1 });
  if (entry.type === 'recipe') return `${q} ${+entry.qty === 1 ? 'Portion' : 'Portionen'}`;
  const u = units(entry).find((x) => x[0] === entry.unit) || units(entry)[0];
  if (u[2] === 1) return `${q} ${u[1]}`;
  const unit = units(entry)[0][1];
  return `${q} ${+entry.qty === 1 || u[0] === 'piece' ? u[1] : u[1] === 'Tasse' ? 'Tassen' : u[1].replace('kleine Tasse', 'kleine Tassen')} (${Math.round(grams(entry))} ${unit})`;
}

/** Löst Einträge in Lebensmittel mit Gramm auf. Rezepte werden in ihre Zutaten zerlegt. */
export function expand(entries) {
  const m = new Map();
  for (const e of entries) {
    if (e.type === 'recipe') {
      const r = BY_SLUG[e.slug];
      if (!r) continue;
      for (const i of r.ingredients) m.set(i.name, (m.get(i.name) || 0) + i.amount * grams(e));
    } else if (BY_NAME[e.name]) m.set(e.name, (m.get(e.name) || 0) + grams(e));
  }
  return [...m].filter(([, g]) => g > 0).map(([name, g]) => ({ name, g }));
}

/** Nährwerte eines einzelnen Eintrags. */
export function entryTotals(e) {
  return e.type === 'recipe' ? nutrition(BY_SLUG[e.slug], grams(e)) : totals([{ name: e.name, g: grams(e) }]);
}

/** Sucht Lebensmittel und Rezepte der Seite. Rezepte zuerst, wenn der Titel passt. */
export function searchAll(q, limit = 8) {
  const t = norm(q);
  if (t.length < 2) return [];
  // Rezepte nach vorn, wenn ihr Kurzname mit dem Suchwort beginnt (z. B. „Minestrone“), sonst nach den Lebensmitteln.
  const rec = RECIPES.filter((r) => [r.title, r.short].some((s) => norm(s).split(/[\s,()-]+/).some((w) => w.startsWith(t))))
    .map((r) => ({ type: 'recipe', slug: r.slug, label: r.title, top: norm(r.short).startsWith(t) }));
  const foods = search(q, limit).map((f) => ({ type: 'food', name: f.name, label: f.name, light: f.light }));
  const top = rec.filter((r) => r.top).slice(0, 3);
  const rest = rec.filter((r) => !r.top).slice(0, 2);
  return [...top, ...foods.slice(0, limit - top.length - rest.length), ...rest];
}

/**
 * Stand des Tages: gegessen, Ziel, Rest und Hinweise.
 * entries: [{type: 'food', name, qty, unit} | {type: 'recipe', slug, qty, unit: 'portion'}]
 * t: Zielwerte aus targets(), day: 1 bis 5.
 */
export function status(entries, t, day) {
  const items = expand(entries);
  const sum = totals(items);
  const v = verdict(sum, t);
  const tolP = PLAN.reference.tolerance.proteinPoints ?? PLAN.reference.tolerance.macroPoints;
  // Eiweiß: Longo 9 bis 11 %, die Seite erlaubt bis Ziel plus Toleranz. Darüber gilt es als zu viel.
  const proteinMax = t.kcal * (t.ref.protein + tolP) / 100 / 4;
  const bar = (key, label, eaten, target, max, kind) => {
    const pct = target ? eaten / target * 100 : 0;
    const state = eaten > max + 0.5 ? 'over' : pct >= 90 ? 'full' : 'open';
    return { key, label, eaten, target, max, kind, pct, rest: Math.max(0, target - eaten), state };
  };
  const bars = [
    bar('kcal', 'Kalorien', sum.kcal, t.kcal, t.kcal * (1 + PLAN.reference.tolerance.kcalPercent / 100), 'ziel'),
    bar('protein', 'Eiweiß', sum.protein, t.protein, proteinMax, 'ziel'),
    bar('fat', 'Fett', sum.fat, t.fat, t.fat * 1.12, 'ziel'),
    bar('carbs', 'Kohlenhydrate', sum.carbs, t.carbs, t.carbs * 1.12, 'ziel'),
    bar('sugar', 'Zucker', sum.sugar, v.sugarMax, v.sugarMax, 'max'),
  ];
  const notes = [];
  const g = (n) => items.filter((i) => n.includes(i.name)).reduce((a, i) => a + i.g, 0);
  const coffee = g([COFFEE]);
  if (coffee > CUP_ML + 1) notes.push({ key: 'kaffee', text: `Du bist bei ${Math.round(coffee)} ml Kaffee. Mehr als eine kleine Tasse am Tag ist beim Scheinfasten nicht vorgesehen. Gegen das Tief helfen Kräutertee und viel Wasser.` });
  const pumpkin = g(PUMPKIN);
  if (day >= 2 && pumpkin > PUMPKIN_MAX) notes.push({ key: 'kuerbis', text: `Heute schon ${Math.round(pumpkin)} g Kürbis. An Tag 2 bis 5 sind ca. ${PUMPKIN_MAX} g genug, sonst geht zu viel vom Zuckerbudget drauf. Für den Rest lieber Zucchini, Blumenkohl oder Kartoffeln.` });
  for (const i of items) {
    const f = BY_NAME[i.name];
    if (f.light === 'r') notes.push({ key: 'rot', name: f.name, text: `${f.name} gehört eigentlich nicht in die Fastentage. ${f.why} Passiert ist passiert: Mach einfach normal weiter.`, alts: f.alts.filter((a) => BY_NAME[a]) });
  }
  return { items, sum, verdict: v, bars, notes, done: v.ok, over: bars[0].state === 'over' };
}

/** Vorrat, mit dem der Rest des Tages gefüllt wird, wenn der Nutzer im Kühlschrank-Reiter nichts eingetragen hat. */
export const PANTRY = ['Zucchini', 'Brokkoli', 'Karotten', 'Kartoffeln', 'Champignons', 'Tomaten', 'Blattsalat', 'Olivenöl', 'Walnusskerne', 'Grüne Oliven'];

/**
 * Füllt den Rest des Tages mit Lebensmitteln auf, sodass der ganze Tag zu Longos Werten passt.
 * Das Gegessene bleibt fest, nur die Vorratsliste wird verteilt. Rückgabe: nur die zusätzlichen Mengen.
 */
export function fillFoods(entries, t, pantry = PANTRY) {
  const eaten = expand(entries);
  // Auch schon Gegessenes darf im Vorrat bleiben: dann gibt es davon später einfach noch etwas mehr.
  const free = [...new Set(pantry)].filter((n) => BY_NAME[n] && BY_NAME[n].light !== 'r');
  if (!free.length) return null;
  const res = solve([...eaten.map((i) => ({ name: i.name, g: i.g })), ...free.map((name) => ({ name }))], t);
  const add = res.items.filter((i) => !i.fixed && i.g > 0 && BY_NAME[i.name].n[0] > 5);
  return { add, sum: res.sum, verdict: res.verdict };
}

// Abstand eines Tages zu Longos Werten, Überschreiten der Kalorien zählt doppelt.
function err(sum, t) {
  const v = verdict(sum, t);
  const tolP = PLAN.reference.tolerance.proteinPoints ?? 5;
  const over = Math.max(0, v.dk);
  return Math.abs(v.dk) / 5 + over / 2.5 + Math.abs(v.dev.protein) / tolP + Math.abs(v.dev.fat) / 5 + Math.abs(v.dev.carbs) / 5 + Math.max(0, sum.sugar - v.sugarMax) / 2;
}

/**
 * Rezepte der Seite, die am besten in das Restbudget passen. Probiert halbe, ganze und anderthalb Portionen
 * und nimmt je Rezept die Menge, mit der der Tag Longos Werten am nächsten kommt. Nichts, was die Kalorien sprengt.
 */
export function fillRecipes(entries, t, limit = 3, portions = [0.5, 1, 1.5, 2]) {
  const eaten = totals(expand(entries));
  const left = t.kcal - eaten.kcal;
  if (left < t.kcal * 0.08) return [];
  const used = new Set(entries.filter((e) => e.type === 'recipe').map((e) => e.slug));
  const out = [];
  for (const r of RECIPES) {
    if (used.has(r.slug)) continue;
    let best = null;
    for (const portion of portions) {
      const n = nutrition(r, portion);
      if (n.kcal > left * 1.05) continue;
      const sum = { kcal: eaten.kcal + n.kcal, protein: eaten.protein + n.protein, fat: eaten.fat + n.fat, carbs: eaten.carbs + n.carbs, sugar: eaten.sugar + n.sugar };
      const e = err(sum, t);
      if (!best || e < best.err) best = { recipe: r, portion, n, sum, err: e, ok: verdict(sum, t).ok };
    }
    if (best) out.push(best);
  }
  const base = err(eaten, t);
  return out.filter((x) => x.err < base).sort((a, b) => a.err - b.err).slice(0, limit);
}

/** Zyklustag (1 bis 5) aus dem Startdatum im Planer, sonst null. */
export function dayFromStart(start, today = new Date()) {
  if (!start) return null;
  const s = new Date(`${start}T12:00:00`);
  const d = new Date(today); d.setHours(12, 0, 0, 0);
  const diff = Math.round((d.getTime() - s.getTime()) / 86400000) + 1;
  return diff >= 1 && diff <= 5 ? diff : null;
}

export { FOODS, BY_NAME, BY_SLUG };
