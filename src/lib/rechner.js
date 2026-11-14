// Lebensmittel-Rechner: verteilt das Tagesbudget nach Longo auf die Lebensmittel,
// die jemand zu Hause hat, und baut daraus Mahlzeiten. Läuft im Browser und in Node (Tests).
import foodsJson from '../data/foods.json' with { type: 'json' };
import { PLAN, RECIPES, nutrition, shares } from './nutrition.js';

export const FOODS = foodsJson;
export const BY_NAME = Object.fromEntries(FOODS.map((f) => [f.name, f]));

// Übliche Portion je Gruppe in Gramm. Der Rechner bleibt in der Nähe dieser Mengen, solange Longos Werte das zulassen.
const TYPICAL = {
  gemuese: 150, blatt: 60, pilze: 150, kraeuter: 8, wuerze: 10, fett: 10, nuss: 15, fettfrucht: 30,
  knolle: 100, huelsen: 50, getreide: 60, obst: 80, soja: 40, getraenk: 150, knusper: 10, suppe: 300, pflanz: 50,
};
const TYPICAL_FOOD = {
  Knoblauch: 4, Ingwer: 6, Kapern: 5, Gemüsebrühe: 300, 'Tomaten, passiert': 150, Tomatenmark: 15,
  'Paprikapulver, geräuchert': 1, 'Helle Misopaste': 8, 'Rote Currypaste': 8, Zitronensaft: 15, Limettensaft: 15,
  Balsamico: 8, Apfelessig: 10, Meerrettich: 8, Avocado: 60, 'Kokosmilch (vollfett)': 40, 'Kokosmilch (fettreduziert)': 60, Kokosjoghurt: 60, Mandeljoghurt: 60, Cashewjoghurt: 60, Haferjoghurt: 50, Lupinenjoghurt: 60, Sojaquark: 40,
  Haferkochcreme: 30, Kokoskochcreme: 30, Mandelkochcreme: 30, 'Vegane Schlagcreme': 15, 'Veganer Frischkäse': 20, Kokosmus: 8, Kokoschips: 8, Kokosmehl: 10,
  'Cashewdrink ungesüßt': 100, 'Kokosdrink ungesüßt': 100, 'Macadamiadrink ungesüßt': 100, 'Hanfdrink ungesüßt': 100, Haselnussdrink: 100, 'Erbsendrink ungesüßt': 100,
  Dinkeldrink: 100, 'Reis-Kokos-Drink': 100, 'Haferdrink Barista': 50, Räuchertofu: 30, Reisessig: 10, 'Balsamico bianco': 8, 'Crema di Balsamico': 5, Haferflocken: 20,
  Leinsamen: 8, Chiasamen: 8, Paranüsse: 5, Kresse: 5, 'Mandeldrink ungesüßt': 100,
  Salz: 3, Pfeffer: 1, Kurkuma: 1, Kreuzkümmel: 1, Currypulver: 2, Zimt: 1, Chiliflocken: 0.5, Muskatnuss: 0.5,
  'Oregano (getrocknet)': 1, Thymian: 2, Rosmarin: 2, Nori: 3, Chili: 5, Senf: 8, Sojasauce: 8, Hefeflocken: 5,
  Zitrone: 30, Limette: 20, Mohn: 5, Hummus: 30, Popcorn: 10, 'Getrocknete Tomaten': 10, Wasser: 1500, Mineralwasser: 1000,
  Haferdrink: 100, Reisdrink: 100, Sojadrink: 100, Sojajoghurt: 60, Seidentofu: 60, Kokosraspeln: 5, 'Kokosnuss (frisch)': 20,
  'Apfelmus ungesüßt': 60, 'Peperoni (eingelegt)': 20, Alfalfasprossen: 20,
  'Gemüsebrühe (Pulver)': 5, Ajvar: 20, 'Sambal Oelek': 3, Wasabi: 2, 'Meerrettich (Glas)': 8, 'Sushi-Ingwer': 10, 'Süßer Senf': 5,
  'Kakaopulver (ungesüßt)': 5, Sriracha: 5, Worcestersauce: 3, 'Knoblauch (eingelegt)': 8, Vollkornmehl: 20, Kichererbsenmehl: 20, Speisestärke: 5,
  Haferkleie: 15, Weizenkleie: 10, Weizenkeime: 5, Hirseflocken: 20, Dinkelflocken: 20, 'Müsli (ungesüßt)': 20, 'Haferbrei (mit Wasser)': 150,
  'Kartoffelpüree (mit Wasser)': 150, 'Kartoffelsalat (mit Brühe)': 120, Vollkornbrötchen: 30, Roggenbrot: 40, Maronen: 40,
  'Steinpilze (getrocknet)': 8, 'Mischpilze (getrocknet)': 8, 'Getrocknete Tomaten in Öl': 10, Silberzwiebeln: 20, Cornichons: 40, 'Mixed Pickles': 50,
  Guacamole: 40, Sonnenblumenkernaufstrich: 20, Gemüseaufstrich: 20, 'Vegetarische Pastete': 20, 'Mandel-Streichcreme': 25, Sojakochcreme: 30,
  'Veganer Käse (Kokosöl)': 20, 'Veganer Käse (Cashew)': 20, 'Artischocken in Öl': 40, Kimchi: 60, 'Sushi (vegan)': 120, Misosuppe: 250,
  'Wasser mit Geschmack (ungesüßt)': 500, Getreidekaffee: 200, Espresso: 40, Rooibostee: 300, Früchtetee: 300, Pfefferminztee: 300, Sauerkrautsaft: 100,
};

/** Grund, warum die Obergrenze eines Lebensmittels so liegt (Regel siehe tools/foods_src.py). */
export const CAP_WHY = {
  zucker: 'sonst geht zu viel vom Zuckerbudget drauf',
  eiweiss: 'sonst geht zu viel vom Eiweißbudget drauf',
  kuerbis: 'Richtwert für Kürbis, sonst geht zu viel vom Zuckerbudget drauf',
};

/** Normalisiert Suchtext: klein, ohne Akzente, ß als ss. */
export const norm = (s) => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss').trim();

// Suchschlüssel je Lebensmittel einmal vorbereiten: Name und Synonyme, normalisiert und in Wörter zerlegt
const KEYS = FOODS.map((f) => [f.name, ...f.syn].map((k) => { const n = norm(k); return { n, words: n.split(/[\s,()\-/]+/).filter(Boolean) }; }));
// Treffergüte eines Suchworts in einem Schlüssel: 4 = genau, 3 = Anfang, 2 = Wortanfang, 1,5 = Wortende (z. B. „saft“ in Apfelsaft), 1 = mittendrin
function hit(key, t) {
  if (key.n === t) return 4;
  if (key.n.startsWith(t)) return 3;
  if (key.words.some((w) => w.startsWith(t))) return 2;
  if (key.words.some((w) => w.endsWith(t))) return 1.5;
  return key.n.includes(t) ? 1 : 0;
}

/**
 * Sucht Lebensmittel nach Name und Synonymen (auch Markennamen). Treffer am Wortanfang zuerst.
 * Mehrere Wörter müssen alle passen („tk brokkoli“, „bohnen dose“). Treffer mitten im Wort („cola“ in Chocolat)
 * zählen nur, wenn es sonst kaum Treffer gibt.
 */
export function search(q, limit = 8) {
  const t = norm(q);
  if (t.length < 2) return [];
  const tokens = t.split(/[\s,()\-/]+/).filter(Boolean);
  const scored = [];
  FOODS.forEach((f, i) => {
    const keys = KEYS[i];
    // ganzer Suchtext gegen jeden Schlüssel
    let best = 0;
    for (const k of keys) best = Math.max(best, hit(k, t));
    // sonst: jedes Wort muss in irgendeinem Schlüssel vorkommen, es zählt das schwächste Wort
    if (!best && tokens.length > 1) {
      let min = 9;
      for (const tok of tokens) { let b = 0; for (const k of keys) b = Math.max(b, hit(k, tok)); min = Math.min(min, b); }
      best = min >= 1.5 ? min - 0.25 : 0;
    }
    if (best) scored.push([best + (keys[0].n.startsWith(t) ? 0.5 : 0), f]);
  });
  const good = scored.filter((x) => x[0] > 1);
  const pool = good.length >= 3 ? good : scored;
  return pool.sort((a, b) => b[0] - a[0] || a[1].name.localeCompare(b[1].name, 'de')).slice(0, limit).map((x) => x[1]);
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
  // Eiweiß mit engerer Toleranz (proteinPoints, eigene Regel), Fett und Kohlenhydrate mit macroPoints
  const macrosOk = Object.entries(dev).every(([k, d]) => Math.abs(d) <= (k === 'protein' ? tol.proteinPoints ?? tol.macroPoints : tol.macroPoints));
  // Zucker: höchstens sugarMaxPercent der Zielkalorien (eigene Regel, Longo nennt keine Grammzahl)
  const sugarMax = t.kcal * PLAN.reference.sugarMaxPercent / 100 / 4;
  const sugarOk = sum.sugar <= sugarMax;
  return { ok: kcalOk && macrosOk && sugarOk, kcalOk, macrosOk, sugarOk, sugarMax, dk, dev, shares: sh };
}

/**
 * Ein Lösungslauf: Koordinatenabstieg mit Schranken auf einer quadratischen Zielfunktion.
 * Jede Abweichung wird in Vielfachen ihrer Toleranz gemessen: Kalorien in 5 %, Eiweiß in 3 Prozentpunkten,
 * Fett und Kohlenhydrate in 5 Prozentpunkten. Die Makroanteile sind linear in den Mengen:
 * Anteil_k = Ziel_k genau dann, wenn Summe_i x_i (e_ik - Ziel_k * E_i) = 0 (e = Energie des Makros, E = Summe).
 */
function fit(list, t, lambda, W, minShare = 0, extra = null) {
  const free = list.filter((p) => p.g == null && !p.off && p.f.n[0] > 5);
  const tol = PLAN.reference.tolerance;
  const tolK = [tol.kcalPercent, tol.proteinPoints ?? tol.macroPoints, tol.macroPoints, tol.macroPoints];
  const share = [t.ref.protein / 100, t.ref.fat / 100, t.ref.carbs / 100];
  // Zeile je Gramm: [kcal, Eiweißabweichung, Fettabweichung, KH-Abweichung (jeweils kcal), Zucker g]
  const row = (f) => {
    const e = [f.n[1] * 4 / 100, f.n[2] * 9 / 100, f.n[3] * 4 / 100];
    const E = e[0] + e[1] + e[2];
    return [f.n[0] / 100, e[0] - share[0] * E, e[1] - share[1] * E, e[2] - share[2] * E, f.n[4] / 100];
  };
  const T = [t.kcal, 0, 0, 0];
  // Skala je Zeile: eine Toleranz Abweichung ergibt 1
  const S = tolK.map((v) => t.kcal * v / 100);
  const SMAX = t.kcal * PLAN.reference.sugarMaxPercent / 100 / 4 * 0.98;
  const base = [0, 0, 0, 0, 0];
  if (extra) row({ n: [extra.kcal * 100, extra.protein * 100, extra.fat * 100, extra.carbs * 100, extra.sugar * 100] }).forEach((v, k) => (base[k] += v));
  for (const p of list) {
    if (free.includes(p)) continue;
    p.x = p.off ? 0 : p.g ?? (p.f.n[0] <= 5 ? typical(p.f) : 0);
    row(p.f).forEach((v, k) => (base[k] += v * p.x));
  }
  const A = free.map((p) => row(p.f));
  const tp = free.map((p) => typical(p.f));
  // Untergrenze: Wer ein Lebensmittel auswählt, soll es auch auf dem Teller sehen (minShare der üblichen Portion).
  const lo = tp.map((v, i) => Math.min(free[i].f.cap, v * minShare));
  const x = tp.slice();
  const sum = base.slice();
  A.forEach((a, i) => a.forEach((v, k) => (sum[k] += v * x[i])));
  for (let it = 0; it < 800; it++) {
    let moved = 0;
    for (let i = 0; i < free.length; i++) {
      // Zielfunktion in x_i: sum_k W_k ((Rest_k + a_ik x_i - T_k) / S_k)^2 + lambda ((x_i - tp_i) / tp_i)^2
      let num = lambda / tp[i], den = lambda / (tp[i] * tp[i]);
      for (let k = 0; k < 4; k++) {
        const a = A[i][k];
        if (!a) continue;
        const r = sum[k] - a * x[i] - T[k];
        num -= W[k] * a * r / (S[k] * S[k]);
        den += W[k] * a * a / (S[k] * S[k]);
      }
      // Zucker über der Grenze wird stark bestraft (einseitig, nur wenn die Grenze sonst überschritten wäre)
      const sa = A[i][4];
      if (sa) {
        const rs = sum[4] - sa * x[i];
        const cand = Math.min(free[i].f.cap, Math.max(lo[i], num / den));
        if (rs + sa * cand > SMAX) {
          const WS = 50, SS = SMAX * 0.05;
          num -= WS * sa * (rs - SMAX) / (SS * SS);
          den += WS * sa * sa / (SS * SS);
        }
      }
      const nx = Math.min(free[i].f.cap, Math.max(lo[i], num / den));
      const d = nx - x[i];
      if (d) { for (let k = 0; k < 5; k++) sum[k] += A[i][k] * d; x[i] = nx; moved += Math.abs(d); }
    }
    if (moved < 0.01) break;
  }
  free.forEach((p, i) => (p.x = x[i]));
  const items = list.map((p) => ({ name: p.name, g: roundG(p.f, p.x), fixed: p.g != null, cap: p.f.cap, light: p.f.light }));
  const sum2 = totals(items);
  if (extra) for (const k of Object.keys(sum2)) sum2[k] += extra[k] || 0;
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
  // Rote Lebensmittel plant der Rechner nie ein. Hat jemand sie schon gegessen (feste Menge), zählen sie mit.
  // opt.used: schon selbst eingetragene Mengen je Lebensmittel. Sie verkleinern die Obergrenze (z. B. Kürbis ca. 200 g am Tag).
  const used = opt.used || {};
  const list = picks.map((p) => { const f = BY_NAME[p.name]; return { ...p, f: f && used[p.name] ? { ...f, cap: Math.max(0, f.cap - used[p.name]) } : f }; })
    .filter((p) => p.f && (p.f.light !== 'r' || p.g != null));
  const W = opt.W || [1, 1, 1, 1];
  const extra = opt.extra || null;
  const lambdas = opt.lambda != null ? [opt.lambda] : [3, 1, 0.3, 0.1, 0.03];
  // Erst mit Mindestmengen (ein Drittel der üblichen Portion je gewähltem Lebensmittel) rechnen,
  // nur wenn das Longos Werte nicht trifft, dürfen einzelne Lebensmittel auf 0 g fallen.
  for (const lambda of lambdas) {
    list.forEach((p) => (p.off = false));
    const res = fit(list, t, lambda, W, 1 / 3, extra);
    if (res.verdict.ok) return res;
  }
  let res;
  for (const lambda of lambdas) {
    list.forEach((p) => (p.off = false));
    res = fit(list, t, lambda, W, 0, extra);
    // Mengen unter einem Viertel der üblichen Portion streichen und neu rechnen
    for (let round = 0; round < 3; round++) {
      const tiny = list.filter((p, i) => p.g == null && !p.off && p.f.n[0] > 5 && res.items[i].g < typical(p.f) / 4);
      if (!tiny.length) break;
      tiny.forEach((p) => (p.off = true));
      res = fit(list, t, lambda, W, 0, extra);
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

// Abstand eines Ergebnisses zu Longos Fenster in Toleranz-Einheiten (0 = alles genau getroffen).
const gap = (r) => {
  const v = r.verdict, tol = PLAN.reference.tolerance, tp = tol.proteinPoints ?? tol.macroPoints;
  const out = (d, t) => Math.max(0, Math.abs(d) - t) / t;
  return out(v.dk, tol.kcalPercent) * 2 + out(v.dev.protein, tp) + out(v.dev.fat, tol.macroPoints) + out(v.dev.carbs, tol.macroPoints)
    + Math.max(0, r.sum.sugar - v.sugarMax) / 2 + (Math.abs(v.dk) + Math.abs(v.dev.protein) + Math.abs(v.dev.fat) + Math.abs(v.dev.carbs)) / 100;
};

function poolFor(v) {
  const pool = [];
  if (v.dev.fat < -2) pool.push(...FIX.fat);
  if (v.dev.carbs < -2) pool.push(...FIX.carbs);
  if (v.dev.protein > 1) pool.push(...FIX.lessProtein);
  if (v.dk < -3) pool.push(...FIX.kcal);
  if (!v.sugarOk) pool.push(...FIX.lowSugar);
  return pool.length ? pool : [...FIX.fat, ...FIX.carbs];
}

/** Schlägt bis zu drei einzelne Lebensmittel vor, mit denen der Tag (besser) in Longos Fenster passt. */
export function suggestAdditions(picks, t, res = solve(picks, t), opt = {}) {
  if (res.verdict.ok) return [];
  const have = new Set(picks.map((p) => p.name));
  const base = gap(res);
  return [...new Set(poolFor(res.verdict))].filter((n) => !have.has(n))
    .map((n) => { const r = solve([...picks, { name: n }], t, opt); return { name: n, g: r.items.find((i) => i.name === n).g, ok: r.verdict.ok, gain: base - gap(r) }; })
    .filter((s) => s.gain > 0.05 && s.g > 0)
    .sort((a, b) => Number(b.ok) - Number(a.ok) || b.gain - a.gain)
    .slice(0, 3);
}

/**
 * Ergänzt den Tag Schritt für Schritt um bis zu max Lebensmittel (Tag 1 braucht mit seinen 56 % Fett oft Öl, Nüsse und etwas Sättigendes zugleich), bis er in Longos Fenster passt.
 * Reicht eine einzelne Zutat nicht (z. B. nur Gemüse ausgewählt), entsteht so ein kleines Paket aus Fett und Sättigendem.
 * Rückgabe: { add: [{name, g}], res, ok } oder null, wenn nichts hilft.
 */
export function completeDay(picks, t, max = 4, opt = {}) {
  let cur = [...picks];
  let res = solve(cur, t, opt);
  if (res.verdict.ok) return null;
  const added = [];
  for (let step = 0; step < max && !res.verdict.ok; step++) {
    const have = new Set(cur.map((p) => p.name));
    const base = gap(res);
    let best = null;
    for (const n of new Set(poolFor(res.verdict))) {
      if (have.has(n)) continue;
      const r = solve([...cur, { name: n }], t, opt);
      const gain = base - gap(r);
      if (gain > 0.05 && (!best || Number(r.verdict.ok) > Number(best.r.verdict.ok) || (r.verdict.ok === best.r.verdict.ok && gain > best.gain))) best = { n, r, gain };
    }
    if (!best) break;
    cur.push({ name: best.n }); added.push(best.n); res = best.r;
  }
  if (!added.length) return null;
  // Zutaten, die am Ende bei 0 g landen, gehören nicht ins Paket
  const add = added.map((n) => ({ name: n, g: res.items.find((i) => i.name === n).g })).filter((a) => a.g > 0);
  return add.length ? { add, res, ok: res.verdict.ok } : null;
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
// Flüssige Basis für Suppe und Soße
const LIQUID = new Set(['Gemüsebrühe', 'Kokosmilch (vollfett)', 'Kokosmilch (fettreduziert)', 'Tomaten, passiert', 'Sojakochcreme']);
const RAW = new Set(['Gurke', 'Tomaten', 'Kirschtomaten', 'Radieschen', 'Rettich', 'Kresse', 'Avocado', 'Rote Bete (vorgegart)',
  'Frühlingszwiebeln', 'Kohlrabi', 'Fenchel', 'Rote Paprika', 'Gelbe Paprika', 'Karotten', 'Rotkohl', 'Gewürzgurken', 'Sauerkraut']);
const SOUP = new Set(['Hokkaido-Kürbis', 'Gartenkürbis', 'Karotten', 'Lauch', 'Kartoffeln', 'Süßkartoffel', 'Blumenkohl', 'Brokkoli',
  'Knollensellerie', 'Pastinaken', 'Erbsen (TK)', 'Rote Linsen (gegart)', 'Linsen (gegart)', 'Tomaten, passiert', 'Staudensellerie',
  'Weiße Bohnen (gegart)', 'Kichererbsen (gegart)', 'Steckrübe', 'Rote Bete (vorgegart)', 'Kokosmilch (vollfett)', 'Zucchini']);
const OVEN = new Set(['Hokkaido-Kürbis', 'Gartenkürbis', 'Karotten', 'Kartoffeln', 'Süßkartoffel', 'Blumenkohl', 'Brokkoli', 'Rosenkohl',
  'Aubergine', 'Rote Paprika', 'Gelbe Paprika', 'Grüne Paprika', 'Zucchini', 'Pastinaken', 'Knollensellerie', 'Rote Zwiebel',
  'Fenchel', 'Rote Bete (vorgegart)', 'Kichererbsen (gegart)', 'Grünkohl', 'Tomaten', 'Kirschtomaten', 'Champignons', 'Steckrübe']);
// Saaten und Muse kommen in die Gerichte (bestreuen, Dressing), ganze Nüsse höchstens als Handvoll pur.
const SEEDS = new Set(['Leinsamen', 'Sesam', 'Kürbiskerne', 'Sonnenblumenkerne', 'Chiasamen', 'Hanfsamen', 'Mohn', 'Pinienkerne', 'Gemahlene Mandeln']);
const NUT_BUTTER = /mus$|Tahin|Streichcreme|Erdnussbutter/;
// Aufstriche und Dips kommen als Klecks ans Gericht
const SPREAD = /aufstrich|Pastete|Guacamole|Hummus|joghurt|quark|Frischkäse|Schlagcreme/i;
const HANDFUL = 20;

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
  fertig: { title: 'Fertig', kind: 'Fertig gekauft', min: 10, steps: (m) => [
    `${list(m.veg)} nach Packungsangabe erwärmen oder kalt genießen.`, 'Wirf vorher einen Blick auf die Zutatenliste: ohne Fleisch, Sahne und Zuckerzusatz passt es am besten.'] },
  snack: { title: 'Snack', kind: 'Snack', min: 5, steps: (m) => [
    `${list([...m.veg, ...m.top])} portionieren.`, 'Langsam essen, dazu ein großes Glas Wasser oder Kräutertee.'] },
};

const label = (it) => `${amount(it.name, it.g)} ${it.name.replace(/ \((gegart|vollfett|TK|vorgegart)\)/, '')}`;
const list = (items) => {
  const xs = items.map((x) => (typeof x === 'string' ? x : label(x)));
  return xs.length > 1 ? `${xs.slice(0, -1).join(', ')} und ${xs[xs.length - 1]}` : xs[0] || '';
};
/** Einheit für die Mengenangabe: Flüssiges in ml, alles andere in g. */
export function unit(name) {
  const f = BY_NAME[name];
  return f?.group === 'getraenk' || f?.group === 'drink' || name === 'Gemüsebrühe' || (f?.group === 'wuerze' && /saft|essig|Balsamico|Sojasauce|sauce$/i.test(name)) || /suppe|brühe$|Gazpacho|drink/i.test(name) ? 'ml' : 'g';
}
export function amount(name, g) {
  if (unit(name) === 'ml') return `${g >= 100 ? Math.round(g / 10) * 10 : Math.round(g)} ml`;
  return `${g < 2 && g > 0 ? Math.round(g * 2) / 2 : Math.round(g)} g`.replace('.', ',');
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
  const use = items.filter((i) => i.g > 0 && f(i).n[0] > 0).map((i) => ({ ...i }));
  // Snacks sind nur Lückenfüller: Nüsse, Saaten, Oliven und Obst wandern zuerst in die Gerichte.
  // Als Snack bleiben nur echte Snacks (Waffeln, Popcorn, eine Handvoll Nüsse) und Obst, wenn es keinen Salat gibt.
  const g = (i) => f(i).group;
  const drink = use.filter((i) => g(i) === 'getraenk');
  // Pflanzendrinks: in die Suppe oder als Snack. Säfte und Kokoswasser: zum Snack. Tee, Kaffee, Wasser gehören in keine Mahlzeit.
  const plantMilk = drink.filter((i) => f(i).n[0] > 5 && /drink/i.test(i.name));
  const sips = drink.filter((i) => f(i).n[0] > 5 && !plantMilk.includes(i));
  const crisp = use.filter((i) => g(i) === 'knusper');
  const fruit = use.filter((i) => g(i) === 'obst');
  const seeds = use.filter((i) => g(i) === 'nuss' && (SEEDS.has(i.name) || NUT_BUTTER.test(i.name)));
  const nuts = use.filter((i) => g(i) === 'nuss' && !seeds.includes(i));
  const toppers = use.filter((i) => g(i) === 'fettfrucht' && i.name !== 'Avocado' && !LIQUID.has(i.name) && !SPREAD.test(i.name));
  const spreads = use.filter((i) => SPREAD.test(i.name));
  // Fertige Suppen und Gerichte bleiben, was sie sind: ein eigenes Gericht zum Aufwärmen
  const ready = use.filter((i) => g(i) === 'suppe');
  const taken = new Set([...drink, ...crisp, ...fruit, ...seeds, ...nuts, ...toppers, ...spreads, ...ready]);
  const rest = use.filter((i) => !taken.has(i));
  // Pflanzliche Kochcremes (Gruppe pflanz, kein Joghurt oder Aufstrich) sind ebenfalls Flüssigkeit für Suppe und Soße
  const liquid = rest.filter((i) => LIQUID.has(i.name) || g(i) === 'pflanz');
  // Flüssiges (passierte Tomaten, Brühe, Kokosmilch) zählt nur als Flüssigkeit, sonst stünde es doppelt im Rezept
  const veg = rest.filter((i) => !liquid.includes(i) && (['gemuese', 'blatt', 'pilze', 'knolle'].includes(f(i).group) || i.name === 'Avocado'));
  const base = rest.filter((i) => ['huelsen', 'getreide', 'soja'].includes(f(i).group));
  const oil = rest.filter((i) => f(i).group === 'fett');
  const herb = rest.filter((i) => f(i).group === 'kraeuter');
  const acid = rest.filter((i) => f(i).group === 'wuerze' && /saft|essig|Balsamico/i.test(i.name));
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
  // Übrige Zutaten den Gerichten zuordnen, in denen sie üblich sind
  const at = (...tpls) => { for (const t of tpls) { const m = meals.find((x) => x.tpl === t); if (m) return m; } return meals[0]; };
  const snackItems = { veg: [...crisp, ...sips], top: [] };
  // Eine Handvoll Nüsse (höchstens 20 g, eine Sorte) bleibt Snack, der Rest kommt als Topping in die Gerichte
  const nutsSorted = [...nuts].sort((a, b) => b.g - a.g);
  if (nutsSorted.length && (meals.length === 0 || nutsSorted[0].g >= 8)) {
    const n0 = nutsSorted.shift();
    // Bis 30 g bleibt die ganze Menge eine Handvoll, darüber 20 g pur und der Rest als Topping
    const keep = meals.length && n0.g > 30 ? HANDFUL : n0.g;
    snackItems.top.push({ ...n0, g: keep });
    if (n0.g - keep >= 1) nutsSorted.unshift({ ...n0, g: n0.g - keep });
  }
  if (meals.length) {
    for (const i of nutsSorted) at('salat', 'ofen', 'pfanne', 'suppe').top.push(i);
    for (const i of seeds) {
      if (NUT_BUTTER.test(i.name)) at('salat', 'pfanne', 'ofen', 'suppe').acid.push(i);
      else at('salat', 'suppe', 'ofen', 'pfanne').top.push(i);
    }
    for (const i of toppers) at('salat', 'ofen', 'pfanne', 'suppe').top.push(i);
    for (const i of spreads) at('ofen', 'pfanne', 'salat', 'suppe').dip = [...(at('ofen', 'pfanne', 'salat', 'suppe').dip || []), i];
    const salad = meals.find((x) => x.tpl === 'salat');
    // Obst: in den Salat, sonst ein Stück als Snack und der Rest als Nachtisch zum letzten Gericht
    if (salad) salad.veg.push(...fruit);
    else if (fruit.length) {
      const [f0, ...more] = [...fruit].sort((a, b) => b.g - a.g);
      snackItems.veg.push(f0);
      if (more.length) meals[meals.length - 1].dessert = more;
    }
    const soup = meals.find((x) => x.tpl === 'suppe');
    if (soup) soup.liq.push(...plantMilk); else snackItems.veg.push(...plantMilk);
  } else {
    snackItems.top.push(...nutsSorted, ...seeds, ...toppers, ...spreads);
    snackItems.veg.push(...fruit, ...plantMilk);
  }
  if (snackItems.veg.length || snackItems.top.length) meals.push({ tpl: 'snack', ...snackItems, base: [], oils: [], herb: [], acid: [], aroma: [], liq: [] });
  // Fertige Suppen und Gerichte zuerst: Sie ersetzen eine Hauptmahlzeit
  for (const r of [...ready].reverse()) meals.unshift({ tpl: 'fertig', veg: [r], base: [], oils: [], herb: [], acid: [], aroma: [], liq: [], top: [] });

  // Geteilte Mengen auf ganze Gramm runden, sodass die Summe je Zutat genau der Tagesmenge entspricht
  // (größter Rest zuerst). Sonst würde z. B. 35 g Öl auf 2 × 18 g = 36 g und läge über der Obergrenze.
  const parts = new Map();
  for (const m of meals) for (const k of ['veg', 'base', 'oils', 'herb', 'acid', 'aroma', 'liq', 'top', 'dessert', 'dip']) for (const it of m[k] || []) {
    if (!parts.has(it.name)) parts.set(it.name, []);
    parts.get(it.name).push(it);
  }
  for (const [name, xs] of parts) {
    const total = Math.round(use.find((i) => i.name === name)?.g ?? xs.reduce((a, x) => a + x.g, 0));
    const fl = xs.map((x) => Math.floor(x.g + 1e-9));
    let left = total - fl.reduce((a, b) => a + b, 0);
    const order = xs.map((x, j) => [x.g - fl[j], j]).sort((a, b) => b[0] - a[0]);
    for (const [, j] of order) { if (left <= 0) break; fl[j]++; left--; }
    xs.forEach((x, j) => (x.g = fl[j]));
  }

  return meals.map((m, idx) => {
    const t = TEMPLATES[m.tpl];
    const big = (xs) => xs.filter((i) => Math.round(i.g) >= 1);
    const main = names([...m.veg].sort((a, b) => f(b).n[0] * b.g - f(a).n[0] * a.g || b.g - a.g)).slice(0, 3);
    const title = m.tpl === 'fertig' ? short(m.veg[0].name) : m.tpl === 'snack' ? `Snack mit ${list(names([...m.top, ...m.veg]))}`
      : `${t.title} mit ${list(main.length ? main : names(m.base))}`;
    const ctx = { veg: big(m.veg), base: big(m.base), oil: Math.round(m.oils.reduce((a, o) => a + o.g, 0)), acid: big(m.acid),
      aroma: big(m.aroma), herb: big(m.herb), top: big(m.top), liquid: big(m.liq).map(label).join(' und ') };
    const merged = mergeItems([...m.veg, ...m.base, ...m.oils, ...m.herb, ...m.acid, ...m.liq, ...m.aroma, ...m.top, ...(m.dessert || []), ...(m.dip || [])]);
    return { tpl: m.tpl, slot: m.tpl === 'snack' ? 'Snack' : idx === 0 ? 'Mittags' : 'Abends', kind: t.kind, minutes: t.min, title,
      items: merged, steps: [...t.steps(ctx), m.dip?.length ? `Dazu einen Klecks ${list(big(m.dip))}.` : null, m.dessert?.length ? `Als Nachtisch: ${list(big(m.dessert))}, in Spalten oder Stücke geschnitten.` : null].filter(Boolean), sum: totals(merged) };
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
