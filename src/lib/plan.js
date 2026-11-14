// Der fertige 5-Tage-Plan als gemeinsame Quelle für Planer und Rechner:
// Grundplan, Anpassung an Vorlieben, eigene Tausche. Zustand aus localStorage smlPlaner.
import { RECIPES, BY_SLUG, PLAN, nutrition, add, check } from './nutrition.js';

export const PREF_RX = {
  pilze: /Champignon|Pilz/i, huelsen: /Kichererbsen|Linsen|Bohnen|Erbsen/i, kokos: /Kokos/i, nuesse: /Walnuss|Mandel|Cashew/i,
  aubergine: /Aubergine/i, zucchini: /Zucchini/i, paprika: /Rote Paprika/i, kuerbis: /Hokkaido/i, kohl: /kohl|Wirsing|Pak Choi/i,
  rotebete: /Rote Bete/i, suesskartoffel: /Süßkartoffel/i, tomate: /Tomat/i, sesam: /Sesam|Tahin/i, koriander: /Koriander/i, scharf: /Chili|Currypaste|Meerrettich/i,
};
export const hits = (r, keys) => keys.filter((k) => r.ingredients.some((i) => PREF_RX[k]?.test(i.name)));
const ZERO = nutrition({ ingredients: [] });
export const total = (list, f) => list.reduce((acc, it) => add(acc, nutrition(BY_SLUG[it.recipe], it.portion * f)), ZERO);
const r5 = (x) => Math.round(x * 20) / 20;
const SWAPPABLE = ['main', 'snack', 'breakfast'];

export const withBreakfast = (st) => !!st?.breakfast && !!PLAN.breakfastDays;
export const swapKey = (st) => (withBreakfast(st) ? 'swapsBf' : 'swaps');
const prefsOf = (st) => st?.prefs || { like: [], no: [] };

/** Mögliche Tausch-Gerichte für Position idx, Portion so, dass die Kalorien gleich bleiben. */
export function candidatesFor(day, list, idx, f, max = 30) {
  const cur = list[idx];
  const curK = nutrition(BY_SLUG[cur.recipe], cur.portion).kcal;
  const used = new Set(list.map((x) => x.recipe));
  const pool = RECIPES.filter((r) => r.slot === cur.type && !used.has(r.slug) && !['nussmix', 'oliven'].includes(r.slug));
  return pool.map((r) => {
    const portion = r5(Math.min(1.4, Math.max(0.7, cur.portion * curK / nutrition(r).kcal)));
    const next = list.map((x, i) => (i === idx ? { ...x, recipe: r.slug, portion } : x));
    const c = check(day, total(next, f), f);
    const sh = c.shares; const ref = c.ref;
    const score = Math.abs(sh.protein - ref.protein) + Math.abs(sh.fat - ref.fat) + Math.abs(sh.carbs - ref.carbs);
    return { r, portion, ok: c.ok, score, kcal: nutrition(r, portion * f).kcal };
  }).sort((a, b) => (Number(b.ok) - Number(a.ok)) || a.score - b.score).slice(0, max);
}

// Grundplan, an die Vorlieben angepasst: Gerichte mit „lieber nicht“ werden getauscht, Lieblingszutaten bevorzugt, solange der Tag passt.
const cache = new Map();
export function autoPlan(st) {
  const bf = withBreakfast(st); const prefs = prefsOf(st);
  const key = JSON.stringify([prefs, bf]);
  if (cache.has(key)) return cache.get(key);
  const AUTO = {};
  const { like, no } = prefs; const picked = new Set();
  for (let d = 1; d <= 5; d++) {
    const list = (bf ? PLAN.breakfastDays : PLAN.days)[d].map((it) => ({ ...it }));
    list.forEach((it, idx) => {
      if (!SWAPPABLE.includes(it.type) || (!like.length && !no.length)) return;
      const r = BY_SLUG[it.recipe]; const bad = hits(r, no).length > 0; const good = hits(r, like).length > 0;
      if (!bad && (good || !like.length)) return;
      const c = candidatesFor(d, list, idx, 1).filter((x) => !hits(x.r, no).length && !picked.has(x.r.slug))
        .map((x) => ({ ...x, liked: hits(x.r, like).length }))
        .sort((a, b) => (Number(b.ok) - Number(a.ok)) || (b.liked - a.liked) || a.score - b.score);
      const best = c[0];
      if (!best) return;
      if (bad || (best.liked && best.ok)) { list[idx] = { ...it, recipe: best.r.slug, portion: best.portion, auto: true }; picked.add(best.r.slug); }
    });
    AUTO[d] = list;
  }
  cache.set(key, AUTO);
  return AUTO;
}

/** Gerichte eines Plantags (1 bis 5) inklusive eigener Tausche, Portionen für Faktor 1. */
export function planDay(st, day) {
  const base = autoPlan(st)[day] || (withBreakfast(st) ? PLAN.breakfastDays : PLAN.days)[day] || [];
  return base.map((it, idx) => {
    const s = st?.[swapKey(st)]?.[day]?.[idx];
    return s ? { ...it, recipe: s.recipe, portion: s.portion, swapped: true, auto: false } : { ...it };
  });
}

/** Plantag für ein Datum aus dem Startdatum (YYYY-MM-DD), sonst null. */
export function planDayFor(start, today = new Date()) {
  if (!start) return null;
  const s = new Date(`${start}T12:00:00`);
  const d = new Date(today); d.setHours(12, 0, 0, 0);
  const n = Math.round((d.getTime() - s.getTime()) / 86400000) + 1;
  return n >= 1 && n <= 5 ? n : null;
}
