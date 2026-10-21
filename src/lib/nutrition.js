// Nährwertberechnung, gemeinsam genutzt von Build (Astro) und Planer (Browser).
import nutrientsJson from '../data/nutrients.json' with { type: 'json' };
import recipesJson from '../data/recipes.json' with { type: 'json' };
import planJson from '../data/plan.json' with { type: 'json' };

export const NUTRIENTS = nutrientsJson;
export const RECIPES = recipesJson;
export const PLAN = planJson;
export const BY_SLUG = Object.fromEntries(RECIPES.map((r) => [r.slug, r]));

/** Summe der Nährwerte eines Rezepts, multipliziert mit factor (Portionen). */
export function nutrition(recipe, factor = 1) {
  const s = { kcal: 0, protein: 0, fat: 0, carbs: 0, sugar: 0, oil: 0 };
  for (const { name, amount } of recipe.ingredients) {
    const v = NUTRIENTS[name];
    if (!v) throw new Error(`Unbekannte Zutat "${name}" in ${recipe.slug}. Bitte in tools/recipes_src.py ergänzen.`);
    const g = (amount / 100) * factor;
    s.kcal += v[0] * g; s.protein += v[1] * g; s.fat += v[2] * g; s.carbs += v[3] * g; s.sugar += v[4] * g;
    if (name === 'Olivenöl' || name === 'Sesamöl') s.oil += amount * factor;
  }
  return s;
}

export function add(a, b) {
  const out = {};
  for (const k of Object.keys(a)) out[k] = a[k] + b[k];
  return out;
}

/** Anteile von Eiweiß, Fett und Kohlenhydraten an den Kalorien in Prozent. */
export function shares(n) {
  if (!n.kcal) return { protein: 0, fat: 0, carbs: 0 };
  return { protein: (n.protein * 4 / n.kcal) * 100, fat: (n.fat * 9 / n.kcal) * 100, carbs: (n.carbs * 4 / n.kcal) * 100 };
}

export function reference(day) {
  return day === 1 ? PLAN.reference.day1 : PLAN.reference.day2to5;
}

/** Prüft eine Tagessumme gegen Longos Referenz, skaliert mit dem Portionsfaktor. */
export function check(day, n, factor = 1) {
  const ref = reference(day);
  const tol = PLAN.reference.tolerance;
  const sh = shares(n);
  const target = ref.kcal * factor;
  const kcalOk = Math.abs(n.kcal - target) / target * 100 <= tol.kcalPercent;
  const macrosOk = ['protein', 'fat', 'carbs'].every((k) => Math.abs(sh[k] - ref[k]) <= tol.macroPoints);
  return { ok: kcalOk && macrosOk, kcalOk, macrosOk, shares: sh, target, ref };
}

/** Tagessumme aus einer Liste von {recipe, portion}. */
export function dayTotal(items, factor = 1) {
  return items.reduce((acc, it) => add(acc, nutrition(BY_SLUG[it.recipe], it.portion * factor)), nutrition({ ingredients: [] }));
}

/** Rezepte, in denen ein Rezept im Standardplan vorkommt. */
export function planDays(slug) {
  return Object.entries(PLAN.days).filter(([, items]) => items.some((i) => i.recipe === slug)).map(([d]) => Number(d));
}

export function amountLabel(name, grams) {
  if (name === 'Gemüsebrühe') return `${Math.round(grams / 10) * 10} ml`;
  if (/saft|essig|Balsamico/i.test(name)) return `${Math.round(grams)} ml`;
  if (grams >= 25) return `${Math.round(grams / 5) * 5} g`;
  return `${Math.max(1, Math.round(grams))} g`;
}

export const fmt = (x, d = 0) => Number(x).toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d });
