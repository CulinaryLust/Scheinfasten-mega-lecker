// Selbst eingetragene Mahlzeiten aus dem Rechner (localStorage smlRechner.own), gemeinsam für Rechner und Planer.
// Eine Quelle für Einträge, Nährwerte und Einkaufsmengen, damit alle Darstellungen dieselben Zahlen zeigen.
import { mealCheck, expand, grams, BY_NAME, BY_SLUG } from './tagebuch.js';
import { nutrition } from './nutrition.js';
import { totals } from './rechner.js';

/** Feste Mahlzeiten: Schlüssel, Bezeichnung, Platz im Tag (wie im Planer). */
export const OWN_FIXED = [['bf', 'Frühstück', 'Morgens'], ['mi', 'Mittagessen', 'Mittags'], ['ab', 'Abendessen', 'Abends']];

/** Einträge einer Mahlzeit, ein ausgewähltes Rezept als Portionen. */
export function ownEntries(o, k) {
  if (!o) return [];
  const rezept = o.mode?.[k] === 'rezept';
  if (k.startsWith('z') && !rezept) return o.zw?.find((z) => z.id === k)?.items || [];
  if (o.mode?.[k] === 'selbst') return o.items?.[k] || [];
  if (o.mode?.[k] === 'rezept' && o.rec?.[k] && BY_SLUG[o.rec[k].slug]) return [{ type: 'recipe', slug: o.rec[k].slug, qty: o.rec[k].qty, unit: 'portion' }];
  return [];
}

/** Alle eingetragenen Mahlzeiten mit Inhalt, in der Reihenfolge des Tages. */
export function ownMealsOf(o) {
  const out = [];
  if (!o) return out;
  for (const [k, label, slot] of OWN_FIXED) {
    const entries = ownEntries(o, k);
    if (entries.length) out.push({ key: `own-${k}`, k, slot, label, main: true, entries, recipe: o.mode[k] === 'rezept' ? BY_SLUG[o.rec[k].slug] : undefined });
  }
  for (const z of o.zw || []) {
    const entries = ownEntries(o, z.id);
    if (entries.length) out.push({ key: `own-${z.id}`, k: z.id, slot: `Z${z.pos ?? 3}`, label: 'Zwischenmahlzeit', main: false, entries, recipe: o.mode?.[z.id] === 'rezept' ? BY_SLUG[o.rec[z.id].slug] : undefined });
  }
  return out;
}

/** Nährwerte einer Mahlzeit im selben Format wie nutrition() (inklusive Öl in Gramm). */
export function ownNutrition(entries) {
  const out = { kcal: 0, protein: 0, fat: 0, carbs: 0, sugar: 0, oil: 0 };
  for (const e of entries) {
    if (e.type === 'recipe') {
      const r = BY_SLUG[e.slug]; if (!r) continue;
      const n = nutrition(r, grams(e));
      for (const k of Object.keys(out)) out[k] += n[k] || 0;
    } else if (BY_NAME[e.name]) {
      const g = grams(e); const n = totals([{ name: e.name, g }]);
      for (const k of ['kcal', 'protein', 'fat', 'carbs', 'sugar']) out[k] += n[k];
      if (BY_NAME[e.name].group === 'fett') out.oil += g;
    }
  }
  return out;
}

/** Mahlzeiten mit Ampel (mealCheck) und Nährwerten für einen Zyklustag. */
export function ownDay(o, t, day) {
  return ownMealsOf(o).map((m) => ({ ...m, c: mealCheck(m.entries, t, day, m.main), n: ownNutrition(m.entries) }));
}

/** Zutaten in Gramm für die Einkaufsliste. */
export const ownGroceries = (entries) => expand(entries);

/** Gilt eine Mahlzeit als gegessen? Selbst Eingetragenes ja, bis jemand den Haken entfernt; Rezepte erst mit Haken. */
export const ownIsDone = (m, done) => (m.recipe ? !!done?.[m.key] : done?.[m.key] !== false);
