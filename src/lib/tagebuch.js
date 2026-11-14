// Tagesbilanz: zählt, was jemand an einem Fastentag schon gegessen hat, vergleicht es mit dem Tageslimit
// nach Longo und schlägt vor, wie sich der Rest des Tages passend füllen lässt.
// Läuft im Browser und in Node (Tests).
import { BY_NAME, FOODS, search, solve, totals, verdict, norm, unit } from './rechner.js';
import { RECIPES, BY_SLUG, PLAN, nutrition, shares } from './nutrition.js';

/** Eine kleine Tasse Kaffee in ml. Mehr als eine pro Tag ist nicht vorgesehen (Empfehlung des ProLon-Herstellers). */
export const CUP_ML = 150;
/** Kürbis an Tag 2 bis 5: höchstens ca. 200 g, sonst geht zu viel vom Zuckerbudget drauf. */
export const PUMPKIN_MAX = 200;
const PUMPKIN = ['Hokkaido-Kürbis', 'Gartenkürbis'];
const COFFEE = 'Kaffee';
const TEA_CUP = 200;

// Haushaltsmengen in Gramm (bzw. ml), damit niemand seine Avocado wiegen muss. Eigene Richtwerte.
const SEED = /Leinsamen|Chiasamen|Sesam|Hanfsamen|Mohn|Kürbiskerne|Sonnenblumenkerne|Pinienkerne|Gemahlene Mandeln/;
const BUTTER = /mus$|Tahin|Streichcreme|Erdnussbutter/;
const CUPLIKE = /joghurt|quark|Skyr/i;
const SPREADY = /aufstrich|Pastete|Guacamole|Hummus|Frischkäse|Ajvar|Senf|Tomatenmark|Misopaste|Currypaste|Meerrettich|Kochcreme|Schlagcreme|Kokosmilch|Sojakochcreme|Kokosmus|Margarine|Butter|Pflanzencreme|Schmand|Sahne|Crème|Mayonnaise|Ketchup|Marmelade|Nougat|Honig|Sirup|Dicksaft/i;
const POWDER = /pulver|Kurkuma|Kreuzkümmel|Zimt|Pfeffer|Salz|Chili|Muskat|Oregano/;
const FLAKES = /flocken|Müsli|kleie|Weizenkeime|Kokosraspeln|Kokoschips|mehl|Stärke|gepufft/i;
const PLURAL = { Tasse: 'Tassen', 'kleine Tasse': 'kleine Tassen', Glas: 'Gläser', Portion: 'Portionen', Waffel: 'Waffeln', Scheibe: 'Scheiben', Zehe: 'Zehen', Kern: 'Kerne', Knolle: 'Knollen', Blatt: 'Blätter', Olive: 'Oliven', Schale: 'Schalen', Kugel: 'Kugeln' };
/** Mehrzahl einer Einheit, z. B. „2 Scheiben“. EL, TL, Becher, Handvoll und Stück bleiben gleich. */
export const plural = (u, q) => (+q === 1 || +q < 1 ? u : PLURAL[u] || u);

function household(f) {
  const n = f.name, g = f.group, out = [];
  const push = (key, label, grams) => { if (!out.some((x) => x[0] === key)) out.push([key, label, grams]); };
  if (CUPLIKE.test(n) && !/Trinkjoghurt/.test(n)) { push('becher', 'Becher', 150); push('el', 'EL', 15); }
  if (n === 'Kaffee' || n === 'Espresso' || n === 'Kaffee (entkoffeiniert)') push('cup', 'kleine Tasse', n === 'Espresso' ? 40 : CUP_ML);
  else if (g === 'getraenk' || g === 'drink' || /drink|milch$|Milch$|Kefir|Buttermilch|Ayran|Trinkjoghurt|saft$/i.test(n) && !/Kokosmilch/.test(n)) {
    if (/tee|Kaffee|Cappuccino/i.test(n)) push('cup', 'Tasse', TEA_CUP); else push('glas', 'Glas', 200);
  }
  if (g === 'suppe' || g === 'fertig') { push('teller', 'Teller', 300); push('schale', 'Schale', 200); }
  if (f.piece) push('piece', f.piece[0], f.piece[1]);
  if (g === 'fett') { push('tl', 'TL', 5); push('el', 'EL', 10); }
  else if (g === 'nuss') {
    if (BUTTER.test(n)) { push('tl', 'TL', 7); push('el', 'EL', 15); }
    else if (SEED.test(n)) { push('tl', 'TL', 4); push('el', 'EL', 10); }
    else { push('hand', 'Handvoll', 25); push('el', 'EL', 10); }
  } else if (/Oliven|Oliven mit/.test(n)) { push('olive', 'Olive', 4); push('el', 'EL', 15); }
  else if (n === 'Falafel') push('piece', 'Stück', 20);
  else if (SPREADY.test(n)) { push('tl', 'TL', 5); push('el', 'EL', 15); }
  else if (FLAKES.test(n)) { push('el', 'EL', 8); if (/flocken|Müsli/i.test(n)) push('portion', 'Portion', 40); }
  else if (g === 'wuerze') { if (POWDER.test(n)) push('tl', 'TL', 2); else if (!f.piece) { push('tl', 'TL', 5); push('el', 'EL', 15); } }
  else if (g === 'kraeuter') { push('el', 'EL', 3); push('hand', 'Handvoll', 10); }
  else if (g === 'blatt') { push('hand', 'Handvoll', 25); push('portion', 'Portion', 60); }
  else if (['gemuese', 'pilze', 'knolle'].includes(g)) {
    if (/Kirschtomaten|Radieschen|Champignons$/.test(n)) push('stk', 'Stück', n === 'Champignons' ? 20 : 15);
    push('hand', 'Handvoll', 60); push('portion', 'Portion', 150);
  } else if (g === 'obst') { if (!f.piece) push('hand', 'Handvoll', 80); push('portion', 'Portion', 125); }
  else if (['huelsen', 'getreide'].includes(g)) { push('el', 'EL', 20); push('portion', 'Portion', 150); }
  else if (g === 'soja') { if (/Tofu/.test(n)) push('portion', 'Portion', 100); else if (n === 'Edamame') push('hand', 'Handvoll', 50); }
  else if (g === 'knusper' && !f.piece) push('hand', 'Handvoll', 10);
  else if (/Käse|Emmentaler|Edamer|Cheddar|Tilsiter|Gouda/.test(n)) push('scheibe', 'Scheibe', 20);
  else if (['suess', 'weissmehl', 'tier', 'milch', 'eiweiss'].includes(g) && !out.length) push('portion', 'Portion', 100);
  return out;
}

/** Einheiten, in denen sich ein Lebensmittel oder Rezept eintragen lässt: [Schlüssel, Bezeichnung, Gramm je Einheit]. */
export function units(entry) {
  if (entry.type === 'recipe') return [['portion', 'Portion', 1]];
  const f = BY_NAME[entry.name];
  const fluid = unit(f.name) === 'ml' || /saft|essig|Balsamico|Sojasauce/i.test(f.name);
  return [[fluid ? 'ml' : 'g', fluid ? 'ml' : 'g', 1], ...household(f)];
}

/** Vorschlag für die Menge, wenn jemand ein Lebensmittel neu einträgt: die erste Haushaltsmenge, sonst übliche Gramm. */
export function defaultAmount(entry) {
  if (entry.type === 'recipe') return { qty: 1, unit: 'portion' };
  const f = BY_NAME[entry.name];
  const u = units(entry);
  // Haushaltsmenge statt Gramm, aber keine Winzlinge wie „1 Mandel“ als Startwert
  const hh = u.slice(1).filter((x) => x[2] >= 4 && !(x[0] === 'piece' && x[2] < 8));
  const pref = hh.find((x) => ['becher', 'cup', 'glas', 'teller'].includes(x[0])) || (f.light !== 'r' || hh.length ? hh[0] : null);
  if (pref) return { qty: 1, unit: pref[0] };
  const g = { fett: 10, nuss: 15, kraeuter: 5, wuerze: 5, fettfrucht: 20, pflanz: 50 }[f.group] ?? 100;
  return { qty: g, unit: u[0][0] };
}

/** Gramm eines Eintrags (bei Rezepten: Portionen). */
export function grams(entry) {
  const u = units(entry).find((x) => x[0] === entry.unit) || units(entry)[0];
  return Math.max(0, +entry.qty || 0) * u[2];
}

/** Text für die Menge eines Eintrags, z. B. „1 Stück (200 g)“, „2 EL (20 g)“ oder „1,5 Portionen“. */
export function qtyLabel(entry) {
  const q = Number(entry.qty).toLocaleString('de-DE', { maximumFractionDigits: 1 });
  if (entry.type === 'recipe') return `${q} ${+entry.qty === 1 ? 'Portion' : 'Portionen'}`;
  const all = units(entry);
  const u = all.find((x) => x[0] === entry.unit) || all[0];
  if (u[2] === 1) return `${q} ${u[1]}`;
  return `${q} ${plural(u[1], entry.qty)} (${Math.round(grams(entry))} ${all[0][1]})`;
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

/**
 * Ampel für eine selbst eingetragene Mahlzeit, gemessen an Prof. Dr. Longos Tagesvorgaben.
 * entries: wie bei status(), t: Zielwerte, day: 1 bis 5, main: Haupt- oder Zwischenmahlzeit.
 * Fett und Kohlenhydrate einer einzelnen Mahlzeit bewerten wir nicht: Die gleicht der Rest des Tages aus.
 * Rückgabe: { light: 'g' | 'y' | 'r', notes: [Text], sum, shares, items }
 */
export function mealCheck(entries, t, day, main = true) {
  const items = expand(entries);
  const sum = totals(items);
  const sh = shares(sum);
  const tolP = PLAN.reference.tolerance.proteinPoints ?? PLAN.reference.tolerance.macroPoints;
  const sugarMax = t.kcal * PLAN.reference.sugarMaxPercent / 100 / 4;
  const red = [], yellow = [];
  for (const i of items) {
    const f = BY_NAME[i.name];
    if (f.light === 'r') red.push(`${f.name} passt nicht ins Scheinfasten. ${f.why}`);
    else if (f.cap && i.g > f.cap + 0.5 && f.n[0] > 5) yellow.push(`Mehr ${f.name}, als wir für einen ganzen Tag empfehlen (höchstens ${Math.round(f.cap)} ${unit(f.name)}).`);
  }
  if (sum.kcal > t.kcal * 1.05) red.push(`Allein diese Mahlzeit hat mehr Kalorien als Dein ganzer Fastentag (Ziel ${Math.round(t.kcal)} kcal).`);
  else if (sum.kcal > t.kcal * (main ? 0.5 : 0.3)) yellow.push(`Eine große Mahlzeit: ${Math.round(sum.kcal / t.kcal * 100)} % Deines Tagesziels. Für den Rest des Tages bleibt nur noch wenig.`);
  if (sum.kcal >= 40 && sh.protein > t.ref.protein + tolP) yellow.push(`Viel Eiweiß: ${Math.round(sh.protein)} % der Kalorien, Prof. Dr. Longo sieht ca. ${t.ref.protein} % vor. Beim Scheinfasten bleibt Eiweiß bewusst knapp.`);
  if (sum.sugar > sugarMax * 0.5) yellow.push(`Viel Zucker: ${Math.round(sum.sugar)} g, am ganzen Tag sind höchstens ${Math.round(sugarMax)} g vorgesehen.`);
  const g = (n) => items.filter((i) => n.includes(i.name)).reduce((a, i) => a + i.g, 0);
  if (day >= 2 && g(PUMPKIN) > PUMPKIN_MAX) yellow.push(`${Math.round(g(PUMPKIN))} g Kürbis. An Tag 2 bis 5 sind ca. ${PUMPKIN_MAX} g am Tag genug.`);
  if (g([COFFEE]) > CUP_ML + 1) yellow.push('Mehr als eine kleine Tasse Kaffee. Mehr ist beim Scheinfasten nicht vorgesehen.');
  const light = red.length ? 'r' : yellow.length ? 'y' : 'g';
  return { light, notes: [...red, ...yellow], sum, shares: sh, items };
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
