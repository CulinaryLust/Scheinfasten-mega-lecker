// Lebensmittel-Rechner: verteilt das Tagesbudget nach Prof. Dr. Valter Longo auf die Lebensmittel,
// die jemand zu Hause hat, und baut daraus Mahlzeiten. Läuft im Browser und in Node (Tests).
import foodsJson from '../data/foods.json' with { type: 'json' };
import { PLAN, RECIPES, nutrition, shares } from './nutrition.js';

export const FOODS = foodsJson;
export const BY_NAME = Object.fromEntries(FOODS.map((f) => [f.name, f]));

// Übliche Portion je Gruppe in Gramm. Der Rechner bleibt in der Nähe dieser Mengen, solange Longos Werte das zulassen.
const TYPICAL = {
  gemuese: 150, blatt: 60, pilze: 150, kraeuter: 8, wuerze: 10, fett: 10, nuss: 15, fettfrucht: 30,
  knolle: 100, huelsen: 50, getreide: 60, obst: 80, soja: 40, getraenk: 150,
};
const TYPICAL_FOOD = {
  Knoblauch: 4, Ingwer: 6, Kapern: 5, Gemüsebrühe: 300, 'Tomaten, passiert': 150, Tomatenmark: 15,
  'Paprikapulver, geräuchert': 1, 'Helle Misopaste': 8, 'Rote Currypaste': 8, Zitronensaft: 15, Limettensaft: 15,
  Balsamico: 8, Apfelessig: 10, Meerrettich: 8, Avocado: 60, 'Kokosmilch (vollfett)': 40, Haferflocken: 20,
  Leinsamen: 8, Chiasamen: 8, Paranüsse: 5, Kresse: 5, 'Mandeldrink ungesüßt': 100,
};

/** Normalisiert Suchtext: klein, ohne Akzente, ß als ss. */
export const norm = (s) => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss').trim();

/** Sucht Lebensmittel nach Name und Synonymen. Treffer am Wortanfang zuerst. */
export function search(q, limit = 8) {
  const t = norm(q);
  if (t.length < 2) return [];
  const scored = [];
  for (const f of FOODS) {
    const keys = [f.name, ...f.syn].map(norm);
    let best = 0;
    for (const k of keys) {
      if (k === t) best = Math.max(best, 4);
      else if (k.startsWith(t)) best = Math.max(best, 3);
      else if (k.split(/[\s,()-]+/).some((w) => w.startsWith(t))) best = Math.max(best, 2);
      else if (k.includes(t)) best = Math.max(best, 1);
    }
    if (best) scored.push([best + (keys[0].startsWith(t) ? 0.5 : 0), f]);
  }
  return scored.sort((a, b) => b[0] - a[0] || a[1].name.localeCompare(b[1].name, 'de')).slice(0, limit).map((x) => x[1]);
}

/** Portionsfaktor wie im Planer: Bedarf nach Mifflin-St Jeor geteilt durch 2.000 kcal, begrenzt auf 0,9 bis 1,15. */
export function profile({ sex, age, h, w, pal }) {
  const off = sex === 'm' ? 5 : sex === 'w' ? -161 : -78;
  const bmr = 10 * w + 6.25 * h - 5 * age + off;
  const tdee = bmr * pal;
  const raw = tdee / 2000;
  return { age, bmi: w / Math.pow(h / 100, 2), tdee, raw, f: Math.min(1.15, Math.max(0.9, raw)) };
}

/** Zielwerte eines Tages in kcal und Gramm. day: 1 oder 2 (steht für Tag 2 bis 5). */
export function targets(day, factor = 1) {
  const ref = day === 1 ? PLAN.reference.day1 : PLAN.reference.day2to5;
  const kcal = ref.kcal * factor;
  return { ref, kcal, protein: kcal * ref.protein / 100 / 4, fat: kcal * ref.fat / 100 / 9, carbs: kcal * ref.carbs / 100 / 4 };
}

const typical = (f) => Math.min(f.cap, TYPICAL_FOOD[f.name] ?? TYPICAL[f.group] ?? 50);

/** Nährwerte einer Liste {name, g}. */
export function totals(items) {
  const s = { kcal: 0, protein: 0, fat: 0, carbs: 0, sugar: 0 };
  for (const { name, g } of items) {
    const n = BY_NAME[name].n;
    s.kcal += n[0] * g / 100; s.protein += n[1] * g / 100; s.fat += n[2] * g / 100; s.carbs += n[3] * g / 100; s.sugar += n[4] * g / 100;
  }
  return s;
}

/** Prüft eine Summe gegen Longos Referenz (gleiche Toleranz wie der Planer). */
export function verdict(sum, t) {
  const tol = PLAN.reference.tolerance;
  const sh = shares(sum);
  const dk = sum.kcal ? (sum.kcal - t.kcal) / t.kcal * 100 : -100;
  const dev = { protein: sh.protein - t.ref.protein, fat: sh.fat - t.ref.fat, carbs: sh.carbs - t.ref.carbs };
  const kcalOk = Math.abs(dk) <= tol.kcalPercent;
  const macrosOk = Object.values(dev).every((d) => Math.abs(d) <= tol.macroPoints);
  // Zucker: höchstens sugarMaxPercent der Zielkalorien (eigene Regel, Longo nennt keine Grammzahl)
  const sugarMax = t.kcal * PLAN.reference.sugarMaxPercent / 100 / 4;
  const sugarOk = sum.sugar <= sugarMax;
  return { ok: kcalOk && macrosOk && sugarOk, kcalOk, macrosOk, sugarOk, sugarMax, dk, dev, shares: sh };
}

/** Ein Lösungslauf: Koordinatenabstieg mit Schranken auf einer quadratischen Zielfunktion. */
function fit(list, t, lambda, W) {
  const free = list.filter((p) => p.g == null && !p.off && p.f.n[0] > 5);
  const T = [t.kcal, t.protein, t.fat, t.carbs];
  const row = (f) => [f.n[0] / 100, f.n[1] / 100, f.n[2] / 100, f.n[3] / 100, f.n[4] / 100];
  const SMAX = t.kcal * PLAN.reference.sugarMaxPercent / 100 / 4 * 0.98;
  const base = [0, 0, 0, 0, 0];
  for (const p of list) {
    if (free.includes(p)) continue;
    p.x = p.off ? 0 : p.g ?? (p.f.n[0] <= 5 ? typical(p.f) : 0);
    row(p.f).forEach((v, k) => (base[k] += v * p.x));
  }
  const A = free.map((p) => row(p.f));
  const tp = free.map((p) => typical(p.f));
  const x = tp.slice();
  const sum = base.slice();
  A.forEach((a, i) => a.forEach((v, k) => (sum[k] += v * x[i])));
  for (let it = 0; it < 500; it++) {
    let moved = 0;
    for (let i = 0; i < free.length; i++) {
      // Zielfunktion in x_i: sum_k W_k ((Rest_k + a_ik x_i - T_k) / T_k)^2 + lambda ((x_i - tp_i) / tp_i)^2
      let num = lambda / tp[i], den = lambda / (tp[i] * tp[i]);
      for (let k = 0; k < 4; k++) {
        const a = A[i][k];
        if (!a) continue;
        const r = sum[k] - a * x[i] - T[k];
        num -= W[k] * a * r / (T[k] * T[k]);
        den += W[k] * a * a / (T[k] * T[k]);
      }
      // Zucker über der Grenze wird stark bestraft (einseitig, nur wenn die Grenze sonst überschritten wäre)
      const sa = A[i][4];
      if (sa) {
        const rs = sum[4] - sa * x[i];
        const cand = Math.min(free[i].f.cap, Math.max(0, num / den));
        if (rs + sa * cand > SMAX) {
          const WS = 40;
          num -= WS * sa * (rs - SMAX) / (SMAX * SMAX);
          den += WS * sa * sa / (SMAX * SMAX);
        }
      }
      const nx = Math.min(free[i].f.cap, Math.max(0, num / den));
      const d = nx - x[i];
      if (d) { for (let k = 0; k < 5; k++) sum[k] += A[i][k] * d; x[i] = nx; moved += Math.abs(d); }
    }
    if (moved < 0.01) break;
  }
  free.forEach((p, i) => (p.x = x[i]));
  const items = list.map((p) => ({ name: p.name, g: roundG(p.f, p.x), fixed: p.g != null, cap: p.f.cap, light: p.f.light }));
  const sum2 = totals(items);
  return { items, sum: sum2, verdict: verdict(sum2, t) };
}

/**
 * Verteilt das Tagesbudget auf die gewählten Lebensmittel.
 * picks: [{name, g?}], g = feste Menge, die der Nutzer selbst eingetragen hat.
 * Ziel: Kalorien und Makros nach Longo treffen, nie über der Obergrenze (cap) eines Lebensmittels liegen
 * und dabei so nah wie möglich an üblichen Portionen bleiben. Der Rechner probiert erst alltagsnahe Mengen
 * und weicht nur so weit davon ab, wie es für Longos Werte nötig ist. Winzige Restmengen fallen weg.
 */
export function solve(picks, t, opt = {}) {
  const list = picks.map((p) => ({ ...p, f: BY_NAME[p.name] })).filter((p) => p.f && p.f.light !== 'r');
  const W = opt.W || [3, 1, 2, 2];
  let res;
  for (const lambda of opt.lambda != null ? [opt.lambda] : [0.03, 0.01, 0.003, 0.001]) {
    list.forEach((p) => (p.off = false));
    res = fit(list, t, lambda, W);
    // Mengen unter einem Viertel der üblichen Portion streichen und neu rechnen
    for (let round = 0; round < 3; round++) {
      const tiny = list.filter((p, i) => p.g == null && !p.off && p.f.n[0] > 5 && res.items[i].g < typical(p.f) / 4);
      if (!tiny.length) break;
      tiny.forEach((p) => (p.off = true));
      res = fit(list, t, lambda, W);
    }
    if (res.verdict.ok) break;
  }
  return res;
}

function roundG(f, g) {
  if (g <= 0) return 0;
  if (['fett', 'nuss', 'wuerze', 'kraeuter'].includes(f.group) || g < 30) return Math.max(1, Math.round(g));
  return Math.round(g / 5) * 5;
}

// Ergänzungen, wenn die eigenen Lebensmittel Longos Verteilung nicht hergeben
const FIX = {
  fat: ['Olivenöl', 'Walnusskerne', 'Grüne Oliven', 'Mandeln', 'Avocado'],
  carbs: ['Kartoffeln', 'Karotten', 'Hokkaido-Kürbis', 'Rote Bete (vorgegart)', 'Apfel'],
  kcal: ['Olivenöl', 'Grüne Oliven', 'Mandeln', 'Kartoffeln', 'Hirse (gegart)', 'Walnusskerne', 'Avocado'],
  lessProtein: ['Karotten', 'Zucchini', 'Olivenöl', 'Hokkaido-Kürbis'],
  lowSugar: ['Kartoffeln', 'Hirse (gegart)', 'Kichererbsen (gegart)', 'Zucchini', 'Blumenkohl', 'Olivenöl', 'Walnusskerne'],
};

/** Schlägt bis zu drei Lebensmittel vor, mit denen der Tag (besser) in Longos Fenster passt. */
export function suggestAdditions(picks, t, res = solve(picks, t)) {
  if (res.verdict.ok) return [];
  const v = res.verdict;
  const have = new Set(picks.map((p) => p.name));
  let pool = [];
  if (v.dev.fat < -5) pool.push(...FIX.fat);
  if (v.dev.carbs < -5) pool.push(...FIX.carbs);
  if (v.dev.protein > 5) pool.push(...FIX.lessProtein);
  if (v.dk < -5) pool.push(...FIX.kcal);
  if (!v.sugarOk) pool.push(...FIX.lowSugar);
  if (!pool.length) pool = [...FIX.fat, ...FIX.carbs];
  const err = (r) => Math.abs(r.verdict.dk) / 5 + Object.values(r.verdict.dev).reduce((a, d) => a + Math.abs(d), 0) / 5 + Math.max(0, r.sum.sugar - r.verdict.sugarMax) / 2;
  const base = err(res);
  return [...new Set(pool)].filter((n) => !have.has(n))
    .map((n) => { const r = solve([...picks, { name: n }], t); return { name: n, g: r.items.find((i) => i.name === n).g, ok: r.verdict.ok, gain: base - err(r) }; })
    .filter((s) => s.gain > 0.2 && s.g > 0)
    .sort((a, b) => Number(b.ok) - Number(a.ok) || b.gain - a.gain)
    .slice(0, 3);
}

// Austauschbare Zutaten für den Abgleich mit den Rezepten
const SAME = [
  ['Tomaten', 'Kirschtomaten'], ['Zwiebeln', 'Rote Zwiebel', 'Schalotten'], ['Hokkaido-Kürbis', 'Gartenkürbis'],
  ['Babyspinat', 'Mangold'], ['Zitronensaft', 'Limettensaft'], ['Rote Paprika', 'Gelbe Paprika', 'Grüne Paprika'],
  ['Grüne Oliven', 'Schwarze Oliven'], ['Olivenöl', 'Rapsöl'], ['Blattsalat', 'Romanasalat', 'Eisbergsalat'],
  ['Weiße Bohnen (gegart)', 'Kidneybohnen (gegart)'], ['Rote Linsen (gegart)', 'Linsen (gegart)'],
  ['Hirse (gegart)', 'Quinoa (gegart)', 'Buchweizen (gegart)', 'Vollkornreis (gegart)'],
  ['Champignons', 'Austernpilze', 'Shiitake', 'Pfifferlinge'], ['Walnusskerne', 'Pekannüsse'],
];
const KIND = {};
SAME.forEach((g, i) => g.forEach((n) => (KIND[n] = `k${i}`)));
const kind = (n) => KIND[n] || n;
const MINOR = new Set(['kraeuter', 'wuerze', 'fett']);

/** Rezepte der Seite, sortiert danach, wie viele Hauptzutaten jemand schon hat. */
export function matchRecipes(names, limit = 6) {
  const have = new Set(names.map(kind));
  return RECIPES.filter((r) => !['nussmix', 'oliven'].includes(r.slug)).map((r) => {
    const main = [...new Set(r.ingredients.map((i) => i.name).filter((n) => !MINOR.has(BY_NAME[n]?.group)))];
    const hit = main.filter((n) => have.has(kind(n)));
    return { recipe: r, hit, miss: main.filter((n) => !have.has(kind(n))), score: hit.length + hit.length / main.length };
  }).filter((m) => m.hit.length > 0).sort((a, b) => b.score - a.score).slice(0, limit)
    .map((m) => ({ ...m, n: nutrition(m.recipe) }));
}

// Mahlzeiten aus den eigenen Lebensmitteln bauen
const RAW = new Set(['Gurke', 'Tomaten', 'Kirschtomaten', 'Radieschen', 'Rettich', 'Kresse', 'Avocado', 'Rote Bete (vorgegart)',
  'Frühlingszwiebeln', 'Kohlrabi', 'Fenchel', 'Rote Paprika', 'Gelbe Paprika', 'Karotten', 'Rotkohl', 'Gewürzgurken', 'Sauerkraut']);
const SOUP = new Set(['Hokkaido-Kürbis', 'Gartenkürbis', 'Karotten', 'Lauch', 'Kartoffeln', 'Süßkartoffel', 'Blumenkohl', 'Brokkoli',
  'Knollensellerie', 'Pastinaken', 'Erbsen (TK)', 'Rote Linsen (gegart)', 'Linsen (gegart)', 'Tomaten, passiert', 'Staudensellerie',
  'Weiße Bohnen (gegart)', 'Kichererbsen (gegart)', 'Steckrübe', 'Rote Bete (vorgegart)', 'Kokosmilch (vollfett)', 'Zucchini']);
const OVEN = new Set(['Hokkaido-Kürbis', 'Gartenkürbis', 'Karotten', 'Kartoffeln', 'Süßkartoffel', 'Blumenkohl', 'Brokkoli', 'Rosenkohl',
  'Aubergine', 'Rote Paprika', 'Gelbe Paprika', 'Grüne Paprika', 'Zucchini', 'Pastinaken', 'Knollensellerie', 'Rote Zwiebel',
  'Fenchel', 'Rote Bete (vorgegart)', 'Kichererbsen (gegart)', 'Grünkohl', 'Tomaten', 'Kirschtomaten', 'Champignons', 'Steckrübe']);
const SNACK = new Set(['nuss', 'obst', 'fettfrucht', 'getraenk']);

const TEMPLATES = {
  salat: { title: 'Bunter Salat', kind: 'Salat', min: 10, steps: (m) => [
    `${list(m.veg)} waschen, putzen und mundgerecht schneiden.`,
    m.base.length ? `${list(m.base)} untermischen.` : null,
    `Dressing anrühren: ${m.oil ? `${m.oil} g Öl` : 'etwas Wasser'}${m.acid.length ? `, ${list(m.acid)}` : ', etwas Essig oder Zitrone'}, Salz und Pfeffer.`,
    m.top.length ? `Mit ${list(m.top)} bestreuen.` : null,
    m.herb.length ? `Zum Schluss ${list(m.herb)} darüberzupfen.` : null] },
  suppe: { title: 'Cremige Suppe', kind: 'Suppe', min: 30, steps: (m) => [
    `${list(m.veg)} klein schneiden.`,
    `${m.oil ? `${m.oil} g Öl` : 'Einen Schluck Brühe'} im Topf erhitzen, ${m.aroma.length ? `${list(m.aroma)} und ` : ''}das Gemüse 4 Minuten anschwitzen.`,
    `Mit ${m.liquid || 'Wasser oder salzarmer Brühe'} auffüllen, sodass alles knapp bedeckt ist. Zugedeckt 15 bis 20 Minuten weich kochen.`,
    m.base.length ? `${list(m.base)} zugeben und 3 Minuten mitziehen lassen.` : null,
    `Fein pürieren oder stückig lassen, mit Salz, Pfeffer${m.acid.length ? ` und ${list(m.acid)}` : ''} abschmecken.`,
    m.top.length || m.herb.length ? `Mit ${list([...m.top, ...m.herb])} servieren.` : null] },
  ofen: { title: 'Ofengemüse vom Blech', kind: 'Ofengericht', min: 35, steps: (m) => [
    'Ofen auf 200 °C Umluft vorheizen.',
    `${list(m.veg)} in gleich große Stücke schneiden.`,
    `Mit ${m.oil ? `${m.oil} g Öl` : 'einem Schluck Brühe'}, Salz, Pfeffer${m.aroma.length ? `, ${list(m.aroma)}` : ''} und Rosmarin oder Thymian mischen.`,
    'Auf dem Blech verteilen und 25 bis 30 Minuten rösten, nach der Hälfte wenden.',
    m.base.length ? `${list(m.base)} in den letzten 10 Minuten mit aufs Blech geben.` : null,
    m.liquid ? `${m.liquid} in einem kleinen Topf erhitzen und als Soße dazu reichen.` : null,
    `${m.acid.length ? `Mit ${list(m.acid)} beträufeln` : 'Abschmecken'}${m.top.length || m.herb.length ? ` und mit ${list([...m.top, ...m.herb])} bestreuen` : ''}.`] },
  pfanne: { title: 'Gemüsepfanne', kind: 'Pfanne', min: 20, steps: (m) => [
    `${list(m.veg)} in Streifen oder Scheiben schneiden.`,
    `${m.oil ? `${m.oil} g Öl` : 'Einen Schluck Brühe'} in einer großen Pfanne stark erhitzen. Festes Gemüse zuerst, zartes zuletzt anbraten.`,
    m.aroma.length ? `${list(m.aroma)} 1 Minute mitbraten.` : null,
    m.liquid ? `${m.liquid} angießen und 5 Minuten köcheln lassen.` : null,
    m.base.length ? `${list(m.base)} unterheben und heiß werden lassen.` : null,
    `Mit Salz, Pfeffer${m.acid.length ? ` und ${list(m.acid)}` : ''} abschmecken${m.top.length || m.herb.length ? `, mit ${list([...m.top, ...m.herb])} anrichten` : ''}.`] },
  snack: { title: 'Snack', kind: 'Snack', min: 5, steps: (m) => [
    `${list([...m.veg, ...m.top])} portionieren.`, 'Langsam essen, dazu ein großes Glas Wasser oder Kräutertee.'] },
};

const label = (it) => `${amount(it.name, it.g)} ${it.name.replace(/ \((gegart|vollfett|TK|vorgegart)\)/, '')}`;
const list = (items) => {
  const xs = items.map((x) => (typeof x === 'string' ? x : label(x)));
  return xs.length > 1 ? `${xs.slice(0, -1).join(', ')} und ${xs[xs.length - 1]}` : xs[0] || '';
};
export function amount(name, g) {
  if (name === 'Gemüsebrühe' || name === 'Mandeldrink ungesüßt' || name === 'Kräutertee') return `${Math.round(g / 10) * 10} ml`;
  if (/saft|essig|Balsamico/i.test(name)) return `${Math.round(g)} ml`;
  return `${Math.round(g)} g`;
}

const split = (it, share) => ({ ...it, g: it.g * share });
const TITLE = {
  'Rote Paprika': 'Paprika', 'Gelbe Paprika': 'Paprika', 'Grüne Paprika': 'Paprika', 'Grüne Oliven': 'Oliven', 'Schwarze Oliven': 'Oliven',
  'Rote Zwiebel': 'Zwiebeln', 'Rote Bete (vorgegart)': 'Roter Bete', 'Tomaten, passiert': 'Tomaten', 'Kokosmilch (vollfett)': 'Kokosmilch',
  'Hokkaido-Kürbis': 'Kürbis', Gartenkürbis: 'Kürbis', Blattsalat: 'Salat', Babyspinat: 'Spinat', 'Mandeldrink ungesüßt': 'Mandeldrink',
};
const short = (n) => TITLE[n] || n.replace(/ \(.*\)/, '');
const names = (xs) => [...new Set(xs.map((i) => short(i.name)))];

/**
 * Baut aus der berechneten Tagesmenge bis zu zwei Hauptmahlzeiten und einen Snack.
 * Die Mengen aller Mahlzeiten ergeben zusammen die Tagesmenge (rundungsbedingt ±1 g),
 * die Nährwerte bleiben also im Rahmen von Longos Vorgaben.
 */
export function buildMeals(items) {
  const f = (i) => BY_NAME[i.name];
  const use = items.filter((i) => i.g > 0 && f(i).n[0] > 0);
  const isSnack = (i) => SNACK.has(f(i).group) && !['Avocado', 'Kokosmilch (vollfett)'].includes(i.name);
  const snack = use.filter(isSnack);
  const rest = use.filter((i) => !isSnack(i));
  const veg = rest.filter((i) => ['gemuese', 'blatt', 'pilze', 'knolle'].includes(f(i).group) || i.name === 'Avocado');
  const base = rest.filter((i) => ['huelsen', 'getreide', 'soja'].includes(f(i).group));
  const oil = rest.filter((i) => f(i).group === 'fett');
  const herb = rest.filter((i) => f(i).group === 'kraeuter');
  const acid = rest.filter((i) => /saft|essig|Balsamico/i.test(i.name));
  const liquid = rest.filter((i) => ['Gemüsebrühe', 'Kokosmilch (vollfett)', 'Tomaten, passiert'].includes(i.name));
  const aroma = rest.filter((i) => f(i).group === 'wuerze' && !acid.includes(i) && !liquid.includes(i));

  const salad = veg.filter((i) => f(i).group === 'blatt' || (RAW.has(i.name) && !SOUP.has(i.name) && !OVEN.has(i.name)));
  const warm = veg.filter((i) => !salad.includes(i));
  const warmTpl = (vs) => {
    const soup = vs.filter((i) => SOUP.has(i.name)).length, oven = vs.filter((i) => OVEN.has(i.name)).length;
    if (liquid.length && soup >= oven) return 'suppe';
    return oven > soup ? 'ofen' : soup > oven ? 'suppe' : 'pfanne';
  };
  // Plan: [Vorlage, Gemüse, Anteil an Beilagen, Öl, Kräutern, Säure, Würze]
  const plan = [];
  if (salad.length && warm.length) plan.push(['salat', salad, 0.4], [warmTpl(warm), warm, 0.6]);
  else if (warm.length === 1) plan.push([warmTpl(warm), warm.map((i) => split(i, 0.5)), 0.5], ['pfanne', warm.map((i) => split(i, 0.5)), 0.5]);
  else if (warm.length) {
    // Zwei verschiedene warme Gerichte: Suppengemüse in die Suppe, Ofengemüse aufs Blech (sonst in die Pfanne),
    // Gemüse, das für beides taugt, wird geteilt.
    const b = warm.some((i) => OVEN.has(i.name) && !SOUP.has(i.name)) || warm.filter((i) => OVEN.has(i.name)).length >= 2 ? 'ofen' : 'pfanne';
    const soupOnly = warm.filter((i) => SOUP.has(i.name) && !OVEN.has(i.name));
    const otherOnly = warm.filter((i) => (b === 'ofen' ? OVEN.has(i.name) && !SOUP.has(i.name) : !SOUP.has(i.name)));
    const both = warm.filter((i) => !soupOnly.includes(i) && !otherOnly.includes(i));
    const A = [...soupOnly, ...both.map((i) => split(i, 0.5))];
    const B = [...otherOnly, ...both.map((i) => split(i, 0.5))];
    if (A.length && B.length) plan.push(['suppe', A, 0.5], [b, B, 0.5]);
    else plan.push([warmTpl(warm), warm.map((i) => split(i, 0.5)), 0.5], [b === 'ofen' ? 'pfanne' : 'ofen', warm.map((i) => split(i, 0.5)), 0.5]);
  } else if (salad.length) plan.push(['salat', salad.map((i) => split(i, 0.5)), 0.5], ['salat', salad.map((i) => split(i, 0.5)), 0.5]);
  else if (base.length || oil.length || liquid.length) plan.push(['pfanne', [], 1]);

  const soupIdx = plan.findIndex((p) => p[0] === 'suppe');
  const meals = plan.map(([tpl, vs, share], idx) => {
    // Flüssigkeiten gehören komplett in die Suppe; ohne Suppe werden sie anteilig verteilt.
    const liq = soupIdx >= 0 ? (idx === soupIdx ? liquid : []) : liquid.map((l) => split(l, share));
    const ctx = {
      veg: vs, base: base.map((b) => split(b, share)), oils: oil.map((o) => split(o, share)), herb: herb.map((h) => split(h, share)),
      acid: acid.map((a) => split(a, share)), aroma: aroma.map((a) => split(a, share)), liq, top: [],
    };
    return { tpl, ...ctx };
  });
  if (snack.length) meals.push({ tpl: 'snack', veg: snack.filter((i) => f(i).group !== 'nuss' && f(i).group !== 'fettfrucht'), top: snack.filter((i) => f(i).group === 'nuss' || f(i).group === 'fettfrucht'), base: [], oils: [], herb: [], acid: [], aroma: [], liq: [] });

  return meals.map((m, idx) => {
    const t = TEMPLATES[m.tpl];
    const big = (xs) => xs.filter((i) => Math.round(i.g) >= 1);
    const main = names([...m.veg].sort((a, b) => f(b).n[0] * b.g - f(a).n[0] * a.g || b.g - a.g)).slice(0, 3);
    const title = m.tpl === 'snack' ? `Snack mit ${list(names([...m.top, ...m.veg]))}`
      : `${t.title} mit ${list(main.length ? main : names(m.base))}`;
    const ctx = { veg: big(m.veg), base: big(m.base), oil: Math.round(m.oils.reduce((a, o) => a + o.g, 0)), acid: big(m.acid),
      aroma: big(m.aroma), herb: big(m.herb), top: big(m.top), liquid: big(m.liq).map(label).join(' und ') };
    const merged = mergeItems([...m.veg, ...m.base, ...m.oils, ...m.herb, ...m.acid, ...m.liq, ...m.aroma, ...m.top]);
    return { slot: m.tpl === 'snack' ? 'Snack' : idx === 0 ? 'Mittags' : 'Abends', kind: t.kind, minutes: t.min, title,
      items: merged, steps: t.steps(ctx).filter(Boolean), sum: totals(merged) };
  });
}

function mergeItems(items) {
  const m = new Map();
  for (const i of items) m.set(i.name, (m.get(i.name) || 0) + i.g);
  return [...m].filter(([, g]) => g >= 0.5).map(([name, g]) => ({ name, g: Math.round(g) }));
}

/** Prüft rote Lebensmittel und liefert Begründung plus Alternativen. */
export function advice(name) {
  const f = BY_NAME[name];
  return { light: f.light, why: f.why, alts: f.alts.filter((a) => BY_NAME[a]) };
}
