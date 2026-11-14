// Prüft den Lebensmittel-Rechner mit typischen Kühlschrank-Inhalten.
import { solve, targets, profile, buildMeals, matchRecipes, suggestAdditions, completeDay, search, totals, unit, FOODS, BY_NAME } from '../src/lib/rechner.js';
import { shares, nutrition, RECIPES, BY_SLUG as BY_SLUG_R } from '../src/lib/nutrition.js';
import { mealCheck } from '../src/lib/tagebuch.js';
import { doneHtml } from '../src/lib/fortschritt.js';
import { ownMealsOf, ownDay } from '../src/lib/eigene.js';
import { planDay } from '../src/lib/plan.js';
import PLAN from '../src/data/plan.json' with { type: 'json' };

let failed = 0;
const must = (cond, msg) => { if (!cond) { failed++; console.log('FEHLER:', msg); } };
const fmt = (x) => Math.round(x);

// Datenbank
must(FOODS.length >= 700, `nur ${FOODS.length} Lebensmittel`);
for (const f of FOODS) {
  must(f.n.length === 6 && f.n.slice(0, 5).every((v) => typeof v === 'number' && v >= 0), `Nährwerte ${f.name}`);
  must(f.alts.every((a) => BY_NAME[a]), `Alternative fehlt bei ${f.name}`);
  if (f.light === 'r') must(f.alts.length >= 1 && f.why, `Rot ohne Alternative/Begründung: ${f.name}`);
}
// Suche
must(search('möhre')[0]?.name === 'Karotten', 'Suche Möhre');
must(search('Hack')[0]?.light === 'r', 'Suche Hack');
must(search('kurbis').some((f) => f.name === 'Hokkaido-Kürbis'), 'Suche ohne Umlaut');
must(search('maiscracker')[0]?.name === 'Maiswaffeln', 'Suche Maiscracker');
must(search('reiscracker')[0]?.name === 'Reiswaffeln', 'Suche Reiscracker');
must(search('hafermilch')[0]?.name === 'Haferdrink', 'Suche Hafermilch');
must(search('seitan')[0]?.light === 'r', 'Seitan rot');

const p = profile({ sex: 'w', age: 42, h: 168, w: 70, pal: 1.6 });
const cases = [
  ['Mediterran', ['Zucchini', 'Tomaten', 'Rote Paprika', 'Olivenöl', 'Grüne Oliven', 'Walnusskerne', 'Kartoffeln', 'Knoblauch']],
  ['Herbst', ['Hokkaido-Kürbis', 'Karotten', 'Lauch', 'Kokosmilch (vollfett)', 'Gemüsebrühe', 'Kürbiskerne', 'Olivenöl', 'Apfel']],
  ['Salat', ['Blattsalat', 'Gurke', 'Tomaten', 'Avocado', 'Walnusskerne', 'Olivenöl', 'Zitronensaft', 'Kichererbsen (gegart)']],
  ['Kohl', ['Brokkoli', 'Blumenkohl', 'Champignons', 'Olivenöl', 'Mandeln', 'Hirse (gegart)', 'Zwiebeln']],
];
for (const day of [1, 2]) {
  const t = targets(day, p.f);
  for (const [label, names] of cases) {
    const r = solve(names.map((name) => ({ name })), t);
    const v = r.verdict;
    console.log(`Tag ${day === 1 ? '1' : '2-5'} ${label}: ${fmt(r.sum.kcal)}/${fmt(t.kcal)} kcal, E ${fmt(v.shares.protein)} F ${fmt(v.shares.fat)} KH ${fmt(v.shares.carbs)}, Zucker ${fmt(r.sum.sugar)}/${fmt(v.sugarMax)} g ${v.ok ? 'ok' : 'AUSSERHALB'}`);
    must(r.sum.sugar <= v.sugarMax + 0.5 || !v.ok, `${label}: Zucker über Grenze, aber als passend markiert`);
    console.log('   ', r.items.map((i) => `${i.name} ${i.g}`).join(', '));
    if (!v.ok) {
      // Passt die Auswahl allein nicht, muss der Rechner eine Ergänzung vorschlagen, mit der es passt.
      const add = suggestAdditions(names.map((name) => ({ name })), t, r);
      console.log('    Vorschläge:', add.map((a) => `${a.name} ${a.g} g${a.ok ? ' (passt dann)' : ''}`).join(', ') || 'keine');
      must(add.length > 0, `${label} Tag ${day}: keine Ergänzung vorgeschlagen`);
    }
    for (const i of r.items) must(i.g <= BY_NAME[i.name].cap, `${i.name} über Obergrenze`);
    const meals = buildMeals(r.items);
    const back = totals(meals.flatMap((m) => m.items));
    must(Math.abs(back.kcal - r.sum.kcal) < 15, `Mahlzeiten ${label}: ${fmt(back.kcal)} statt ${fmt(r.sum.kcal)} kcal`);
    if (day === 2) for (const m of meals) console.log(`    ${m.slot}: ${m.title} (${fmt(m.sum.kcal)} kcal)`);
  }
}
// Kürbis-Fall: viel Kürbis darf die Zuckergrenze nicht sprengen
{
  const t = targets(2, p.f);
  const r = solve([{ name: 'Hokkaido-Kürbis' }, { name: 'Karotten' }, { name: 'Olivenöl' }, { name: 'Walnusskerne' }, { name: 'Zucchini' }], t);
  const k = r.items.find((i) => i.name === 'Hokkaido-Kürbis').g;
  console.log('Kürbis-Fall Tag 2-5:', r.items.map((i) => `${i.name} ${i.g}`).join(', '), `Zucker ${fmt(r.sum.sugar)} g`, r.verdict.ok ? 'ok' : 'AUSSERHALB');
  must(r.sum.sugar <= r.verdict.sugarMax + 0.5, 'Kürbis-Fall: Zucker über Grenze');
}
// Unvollständige Auswahl: nur Gemüse, kein Fett
const t2 = targets(2, p.f);
const thin = [{ name: 'Zucchini' }, { name: 'Brokkoli' }, { name: 'Karotten' }];
const rThin = solve(thin, t2);
must(!rThin.verdict.ok, 'Nur Gemüse darf nicht als passend gelten');
const add = suggestAdditions(thin, t2, rThin);
console.log('Nur Gemüse ->', fmt(rThin.sum.kcal), 'kcal, Vorschläge:', add.map((a) => `${a.name} ${a.g} g${a.ok ? ' (passt dann)' : ''}`).join(', '));
must(add.length && BY_NAME[add[0].name].group === 'fett' || add.some((a) => ['fett', 'nuss', 'fettfrucht'].includes(BY_NAME[a.name].group)), 'Fett-Ergänzung erwartet');
// Rote Lebensmittel werden nicht eingerechnet
const rRed = solve([{ name: 'Hähnchen' }, ...thin], t2);
must(!rRed.items.some((i) => i.name === 'Hähnchen'), 'Rotes Lebensmittel eingerechnet');
// Fest eingetragene Menge bleibt
const rFix = solve([{ name: 'Zucchini', g: 300 }, { name: 'Olivenöl' }, { name: 'Kartoffeln' }, { name: 'Walnusskerne' }], t2);
must(rFix.items.find((i) => i.name === 'Zucchini').g === 300, 'Feste Menge geändert');
// Rezeptabgleich
const m = matchRecipes(['Hokkaido-Kürbis', 'Ingwer', 'Kokosmilch (vollfett)']);
must(m[0]?.recipe.slug === 'kuerbissuppe', `Rezeptabgleich: ${m[0]?.recipe.slug}`);
// Snacks nur als Lückenfüller: Saaten, Oliven und Nüsse wandern in die Gerichte, pur bleibt höchstens eine Handvoll
{
  const t = targets(2, p.f);
  const many = ['Brokkoli', 'Mandeln', 'Haselnüsse', 'Apfel', 'Birne', 'Grünkohl', 'Leinsamen', 'Grüne Oliven', 'Olivenöl', 'Maiswaffeln', 'Kartoffeln'];
  const r = solve(many.map((name) => ({ name })), t);
  const meals = buildMeals(r.items);
  const snack = meals.find((m) => m.slot === 'Snack');
  const sn = snack ? snack.items.map((i) => BY_NAME[i.name]) : [];
  console.log('Snack:', snack ? snack.items.map((i) => `${i.name} ${i.g}`).join(', ') : 'keiner');
  must(sn.filter((f) => f.group === 'nuss').length <= 1, 'Mehr als eine Nusssorte als Snack');
  must(!sn.some((f) => ['Leinsamen', 'Grüne Oliven'].includes(f.name)), 'Saaten oder Oliven als Snack');
  must(sn.filter((f) => f.group === 'obst').length <= 1, 'Mehr als ein Obst als Snack');
  const back = totals(meals.flatMap((m) => m.items));
  must(Math.abs(back.kcal - r.sum.kcal) < 15, `Mahlzeiten verlieren Zutaten: ${fmt(back.kcal)} statt ${fmt(r.sum.kcal)} kcal`);
  // Nur Nüsse und Obst: dann ist alles ein Snack
  const only = buildMeals(solve([{ name: 'Walnusskerne' }, { name: 'Apfel' }], t).items);
  must(only.length === 1 && only[0].slot === 'Snack', 'Nur Snack-Zutaten');
}
// ---- Prüfungen vom 14.11.2026 ----
// Makroanteile ergeben zusammen 100 % (Kohlenhydrate inkl. Ballaststoffen mit 4 kcal/g wie in Longos US-Angaben)
{
  const sh = shares({ kcal: 700, protein: 16, fat: 34, carbs: 95 });
  must(Math.abs(sh.protein + sh.fat + sh.carbs - 100) < 1e-9, 'Makroanteile ergeben nicht 100 %');
  must(shares({ kcal: 0, protein: 0, fat: 0, carbs: 0 }).fat === 0, 'Leere Summe');
  // Longos Referenz selbst muss als passend gelten
  for (const day of [1, 2]) {
    const t = targets(day);
    const sum = { kcal: t.kcal, protein: t.kcal * t.ref.protein / 400, fat: t.kcal * t.ref.fat / 900, carbs: t.kcal * t.ref.carbs / 400, sugar: 10 };
    const sh2 = shares(sum);
    must(Math.abs(sh2.protein - t.ref.protein) < 0.01 && Math.abs(sh2.fat - t.ref.fat) < 0.01, `Referenz Tag ${day} wird nicht getroffen`);
  }
}
// Zielwerte und Skalierung: Tag 1 1.090 kcal, Tag 2 bis 5 725 kcal, Faktor 0,9 bis 1,15
{
  must(targets(1).kcal === 1090 && targets(2).kcal === 725, 'Zielkalorien');
  must(targets(2).ref.protein === 9 && targets(2).ref.fat === 44 && targets(2).ref.carbs === 47, 'Makros Tag 2 bis 5');
  must(targets(1).ref.protein === 10 && targets(1).ref.fat === 56 && targets(1).ref.carbs === 34, 'Makros Tag 1');
  const small = profile({ sex: 'w', age: 70, h: 150, w: 45, pal: 1.4 }), big = profile({ sex: 'm', age: 25, h: 200, w: 120, pal: 1.8 });
  must(small.f === 0.9 && big.f === 1.15, `Faktor-Grenzen ${small.f} ${big.f}`);
  const w = profile({ sex: 'w', age: 40, h: 170, w: 70, pal: 1.6 }), m = profile({ sex: 'm', age: 40, h: 170, w: 70, pal: 1.6 }), d = profile({ sex: 'd', age: 40, h: 170, w: 70, pal: 1.6 });
  must(w.tdee < d.tdee && d.tdee < m.tdee, 'Geschlecht in der Bedarfsformel');
  must(Math.abs(m.tdee - (10 * 70 + 6.25 * 170 - 5 * 40 + 5) * 1.6) < 1e-6, 'Mifflin-St Jeor');
  must(Math.abs(w.bmi - 70 / 1.7 / 1.7) < 1e-9, 'BMI');
}
// Suche: mehrere Wörter, Marken, keine Zufallstreffer mitten im Wort
must(search('tk brokkoli')[0]?.name === 'Brokkoli (TK)', 'Suche TK Brokkoli');
must(search('bohnen dose').some((f) => f.name === 'Weiße Bohnen (Dose)'), 'Suche Bohnen Dose');
must(search('oatly').length > 0 && search('alpro').length > 0, 'Markensuche');
must(search('nutella')[0]?.light === 'r' && search('snickers')[0]?.light === 'r', 'Marken rot');
must(!search('cola').some((f) => f.name === 'Pudding'), 'Zufallstreffer mitten im Wort');
must(search('brühe')[0]?.name === 'Gemüsebrühe', 'Suche Brühe');
must(search('saft').every((f) => f.light !== 'g'), 'Säfte sind nie grün');
// Typische Produkte und ihre Ampel
for (const [n, l] of [['Gemüsebrühe (Pulver)', 'g'], ['Hühnerbrühe', 'r'], ['Mayonnaise', 'r'], ['Cola Zero', 'r'], ['Apfelsaft', 'r'], ['Kräutertee', 'g'], ['Rooibostee', 'g'],
  ['Kaffee', 'y'], ['Espresso', 'y'], ['Cappuccino', 'r'], ['Mandeldrink ungesüßt', 'g'], ['Haferdrink (gesüßt)', 'r'], ['Tahin', 'g'], ['Erdnussbutter', 'y'], ['Grüne Oliven', 'g'],
  ['Kichererbsen (Dose)', 'y'], ['Brokkoli (TK)', 'g'], ['Rotkohl (Glas)', 'y'], ['Studentenfutter', 'r'], ['Bitterschokolade', 'r'], ['Proteinpulver', 'r'], ['Tofu', 'y'],
  ['Toastbrot', 'r'], ['Vollkornbrot', 'y'], ['Thunfisch in Öl', 'r'], ['Skyr', 'r'], ['Süßstoff', 'r'], ['Alkoholfreies Bier', 'r'], ['Gemüsesuppe (klar)', 'y'], ['Ajvar', 'g']]) {
  must(BY_NAME[n]?.light === l, `Ampel ${n}: ${BY_NAME[n]?.light} statt ${l}`);
}
for (const f of FOODS) {
  if (f.light !== 'g') must(!!f.why, `${f.name}: gelb oder rot ohne Begründung`);
  if (f.light === 'r') must(f.cap === 0 || f.cap >= 0, `${f.name}: Obergrenze`);
  if (f.light === 'y' && f.n[0] > 5) must(f.cap > 0, `${f.name}: gelb ohne Menge`);
  // Zucker kann nicht über den Kohlenhydraten liegen, Makros nicht über 100 g
  must(f.n[4] <= f.n[3] + 0.6, `${f.name}: Zucker ${f.n[4]} über Kohlenhydraten ${f.n[3]}`);
  must(f.n[1] + f.n[2] + f.n[3] <= 101, `${f.name}: Makros über 100 g`);
  // Obergrenze hält die Budgetregel ein: höchstens halbes Zucker- und Eiweißbudget von Tag 2 bis 5
  if (f.light !== 'r') must(f.n[4] * f.cap / 100 <= 13.7 && f.n[1] * f.cap / 100 <= 8.2, `${f.name}: Obergrenze ${f.cap} g sprengt Zucker- oder Eiweißbudget`);
}
// Kürbis: Richtwert ca. 200 g, gleiche Zahl wie im Tagebuch, und kein Rezept liegt auch bei Faktor 1,15 darüber
for (const k of ['Hokkaido-Kürbis', 'Gartenkürbis']) must(BY_NAME[k].cap === 200 && BY_NAME[k].capWhy === 'kuerbis', `Kürbis-Obergrenze ${k}`);
for (const r of RECIPES) must(r.ingredients.filter((i) => /Kürbis$/.test(i.name)).reduce((a, i) => a + i.amount, 0) * 1.15 <= 202, `Rezept ${r.slug}: zu viel Kürbis`);
// Einheiten: Flüssiges in ml
must(unit('Tomatensuppe') === 'ml' && unit('Sojadrink') === 'ml' && unit('Ananas (Dose, ungesüßt)') === 'g' && unit('Olivenöl') === 'g', 'Einheiten');
// Ergänzungspaket: nur Gemüse wird mit bis zu drei Zutaten passend
{
  const t = targets(2, p.f);
  for (const day of [1, 2]) {
    const td = targets(day, p.f);
    const pack = completeDay(thin, td, 4);
    console.log(`Paket Tag ${day === 1 ? 1 : '2-5'}:`, pack?.add.map((a) => `${a.name} ${a.g} g`).join(', '), pack?.ok ? 'passt' : 'passt NICHT');
    must(pack && pack.ok && pack.add.length <= 4, `Ergänzungspaket Tag ${day} löst „nur Gemüse“ nicht`);
    must(pack.add.every((a) => BY_NAME[a.name].light !== 'r' && a.g <= BY_NAME[a.name].cap), 'Paket mit roter Zutat oder über Obergrenze');
  }
  must(completeDay(cases[0][1].map((name) => ({ name })), t) === null, 'Passender Tag braucht kein Paket');
}
// Mahlzeiten: jede Zutat kommt genau mit ihrer Tagesmenge vor (keine Rundungsdrift, nichts doppelt, nichts verloren)
{
  const t = targets(2, p.f);
  const baskets = [
    ['Zucchini', 'Karotten', 'Tomaten, passiert', 'Olivenöl', 'Leinöl', 'Walnusskerne', 'Kartoffeln', 'Blattsalat', 'Gurke'],
    ['Tomatensuppe', 'Brokkoli (TK)', 'Olivenöl', 'Mandeln', 'Kartoffeln', 'Guacamole', 'Apfel', 'Haferdrink', 'Kokoswasser'],
    ['Kartoffelsalat (mit Brühe)', 'Blattsalat', 'Hummus', 'Grüne Oliven', 'Olivenöl', 'Karotten', 'Kichererbsen (Dose)'],
    ['Hokkaido-Kürbis', 'Kokosmilch (vollfett)', 'Gemüsebrühe', 'Ingwer', 'Kürbiskernöl', 'Kürbiskerne', 'Vollkornbrot'],
  ];
  for (const names of baskets) {
    const r = solve(names.map((name) => ({ name })), t);
    const meals = buildMeals(r.items);
    const back = new Map();
    for (const i of meals.flatMap((m) => m.items)) back.set(i.name, (back.get(i.name) || 0) + i.g);
    for (const it of r.items) {
      if (!(it.g > 0) || BY_NAME[it.name].n[0] === 0 || (BY_NAME[it.name].group === 'getraenk' && BY_NAME[it.name].n[0] <= 5)) continue;
      must((back.get(it.name) || 0) === it.g, `Mahlzeiten ${names[0]}: ${it.name} ${back.get(it.name) || 0} g statt ${it.g} g`);
      must(it.g <= BY_NAME[it.name].cap, `${it.name} über Obergrenze`);
    }
  }
  const soup = buildMeals(solve(baskets[1].map((name) => ({ name })), t).items);
  must(soup[0].tpl === 'fertig' && soup[0].title === 'Tomatensuppe', `Fertige Suppe ist kein eigenes Gericht: ${soup[0].title}`);
  must(!soup.some((m) => m.tpl === 'suppe' && m.items.some((i) => i.name === 'Kokoswasser')), 'Kokoswasser in der Suppe');
}
// Mit Frühstück: das Frühstück zählt fest mit, geprüft wird der ganze Tag
{
  const t = targets(2, p.f);
  const bf = RECIPES.find((x) => x.slot === 'breakfast');
  const extra = nutrition(bf, 0.8);
  const picks = cases[0][1].map((name) => ({ name }));
  const r = solve(picks, t, { extra });
  must(Math.abs(r.sum.kcal - (totals(r.items).kcal + extra.kcal)) < 1e-6, 'Frühstück fehlt in der Tagessumme');
  const pack = r.verdict.ok ? null : completeDay(picks, t, 4, { extra });
  console.log(`Mit Frühstück (${bf.slug}): ${fmt(r.sum.kcal)}/${fmt(t.kcal)} kcal`, r.verdict.ok ? 'ok' : `nicht direkt, Paket: ${pack?.add.map((a) => a.name).join(', ')} ${pack?.ok ? 'passt' : ''}`);
  must(r.verdict.ok || pack?.ok || suggestAdditions(picks, t, r, { extra }).some((a) => a.ok), 'Mit Frühstück weder passend noch ergänzbar');
  must(r.sum.kcal <= t.kcal * 1.05 + 1, 'Mit Frühstück über dem Kalorienziel');
}
// Feste Mengen: zu viel Gegessenes wird ehrlich als zu viel gemeldet, nicht schöngerechnet
{
  const t = targets(2, p.f);
  const r = solve([{ name: 'Walnusskerne', g: 40 }, { name: 'Olivenöl', g: 35 }, { name: 'Mandeln', g: 35 }, { name: 'Avocado', g: 120 }, { name: 'Zucchini' }], t);
  must(!r.verdict.ok && r.verdict.dk > 5, 'Zu viel Fett müsste über dem Ziel liegen');
  must(solve([], t).sum.kcal === 0 && !solve([], t).verdict.ok, 'Leere Auswahl');
  must(solve([{ name: 'Gibt es nicht' }, { name: 'Zucchini' }], t).items.length === 1, 'Unbekanntes Lebensmittel');
}
// Eine Rechenquelle: Tag-Knöpfe, „Dein Tag“, Gerichte, Abhak-Leiste und Mengentabelle zeigen dieselben Werte
{
  const K = ['kcal', 'protein', 'fat', 'carbs'];
  for (const day of [1, 2]) {
    const t = targets(day, p.f);
    const ref = day === 1 ? PLAN.reference.day1 : PLAN.reference.day2to5;
    must(Math.abs(Math.round(ref.kcal * p.f / 10) * 10 - t.kcal) <= 5, `Tag-Knopf ${day} weicht vom Ziel ab`);
    // Selbst eingetragenes Frühstück und ein Snack als feste Mengen, Rest aus den Lebensmitteln
    const owns = [
      mealCheck([{ type: 'food', name: 'Sojajoghurt', qty: 150, unit: 'g' }, { type: 'food', name: 'Heidelbeeren', qty: 80, unit: 'g' }], t, day, true),
      mealCheck([{ type: 'food', name: 'Walnusskerne', qty: 20, unit: 'g' }], t, day, false),
    ];
    const extra = Object.fromEntries([...K, 'sugar'].map((k) => [k, owns.reduce((a, c) => a + (c.sum[k] || 0), 0)]));
    for (const [name, list] of cases.slice(0, 6)) {
      const r = solve(list.map((n) => ({ name: n })), t, { extra, used: {} });
      const meals = buildMeals(r.items);
      for (const k of K) {
        const viaMeals = meals.reduce((a, m) => a + m.sum[k], 0) + extra[k];
        must(Math.abs(viaMeals - r.sum[k]) < 0.5, `${name} Tag ${day}: Gerichte + Eingetragenes (${fmt(viaMeals)}) ≠ Tag (${fmt(r.sum[k])}) bei ${k}`);
        const viaTable = totals(r.items)[k] + extra[k];
        must(Math.abs(viaTable - r.sum[k]) < 0.5, `${name} Tag ${day}: Tabelle ≠ Tag bei ${k}`);
      }
      const html = doneHtml(extra, t, fmt, '', r.sum);
      must(html.includes(`eingeplant ${fmt(r.sum.kcal)} kcal`) && html.includes(`<b>${fmt(extra.kcal)}</b> von ${fmt(t.kcal)} kcal`), `${name}: Abhak-Leiste zeigt andere Werte`);
      must(!/<b>\d+ %<\/b>/.test(html), 'Abhak-Leiste zeigt wieder verwechselbare Makro-Prozente');
    }
  }
}
// Eigene Mahlzeiten: Rechner und Planer lesen dieselben Einträge und Nährwerte
{
  const t = targets(2, p.f);
  const snack = RECIPES.find((r) => r.slot === 'snack');
  const main = RECIPES.find((r) => r.slot === 'main');
  const o = { d: '2026-11-14', mode: { bf: 'selbst', mi: 'rezept', ab: '', zA: 'rezept' }, items: { bf: [{ type: 'food', name: 'Sojajoghurt', qty: 150, unit: 'g' }], mi: [], ab: [] },
    rec: { mi: { slug: main.slug, qty: 1 }, zA: { slug: snack.slug, qty: 0.5 } }, fin: {}, zw: [{ id: 'zA', pos: 2, items: [] }, { id: 'zB', pos: 3, items: [{ type: 'food', name: 'Walnusskerne', qty: 20, unit: 'g' }] }] };
  const ms = ownMealsOf(o);
  must(ms.map((m) => m.key).join() === 'own-bf,own-mi,own-zA,own-zB', `Eigene Mahlzeiten falsch erkannt: ${ms.map((m) => m.key)}`);
  must(ms.find((m) => m.key === 'own-zA')?.recipe?.slug === snack.slug, 'Rezept bei der Zwischenmahlzeit fehlt');
  must(!ms.some((m) => m.key === 'own-ab'), 'Offene Mahlzeit zählt mit');
  for (const m of ownDay(o, t, 2)) {
    for (const k of ['kcal', 'protein', 'fat', 'carbs']) must(Math.abs(m.n[k] - m.c.sum[k]) <= Math.max(1, m.c.sum[k] * 0.02), `${m.key}: Planer (${fmt(m.n[k])}) und Rechner (${fmt(m.c.sum[k])}) rechnen ${k} verschieden`);
  }
  const r1 = ownMealsOf({ ...o, mode: { ...o.mode, mi: '' } });
  must(!r1.some((m) => m.key === 'own-mi'), 'Abgewähltes Rezept zählt weiter');
}
// Vorlieben aus der Suche (f:Name) tauschen Gerichte genauso wie die festen Gruppen
{
  const has = (st, n) => [1, 2, 3, 4, 5].flatMap((d) => planDay(st, d)).filter((it) => it.type === 'main' && BY_SLUG_R[it.recipe].ingredients.some((i) => i.name === n)).length;
  const before = has({}, 'Zucchini'), after = has({ prefs: { like: [], no: ['f:Zucchini'] } }, 'Zucchini');
  must(before > 0 && after < before, `Vorliebe „lieber nicht Zucchini“ wirkt nicht (${before} -> ${after})`);
}
console.log(failed ? `${failed} Fehler` : 'Alles ok');
process.exit(failed ? 1 : 0);

// Produktbreite: Varianten von Joghurt, Pflanzendrinks, Kochcremes und Ölen sind einzeln auffindbar und richtig eingestuft
{
  const find = (q, name) => must(search(q, 10).some((f) => f.name === name), `Suche "${q}" findet ${name} nicht`);
  find('Kokosjoghurt', 'Kokosjoghurt'); find('Cashewmilch', 'Cashewdrink ungesüßt'); find('Mandelmilch', 'Mandeldrink ungesüßt');
  find('Hafer Cuisine', 'Haferkochcreme'); find('Oatly Barista', 'Haferdrink Barista'); find('griechischer Joghurt', 'Griechischer Joghurt');
  find('Avocadoöl', 'Avocadoöl'); find('Ghee', 'Butterschmalz'); find('Harvest Moon', 'Kokosjoghurt'); find('Kokosmilch light', 'Kokosmilch (fettreduziert)');
  for (const n of ['Kokosjoghurt', 'Mandeljoghurt', 'Cashewjoghurt', 'Haferjoghurt', 'Lupinenjoghurt', 'Sojaquark', 'Haferkochcreme']) must(BY_NAME[n].light === 'y' && BY_NAME[n].cap <= 100 && BY_NAME[n].src.db === 'Hersteller', `${n}: Ampel, Grenze oder Quelle`);
  for (const n of ['Griechischer Joghurt', 'Laktosefreie Milch', 'Butterschmalz', 'Emmentaler', 'Pflanzenjoghurt (gesüßt)', 'Kokosblütenzucker', 'Mandelmehl (entölt)']) must(BY_NAME[n].light === 'r', `${n} muss rot sein`);
  for (const n of ['Avocadoöl', 'Arganöl', 'Mandelöl', 'Bratöl']) must(BY_NAME[n].light === 'g' && BY_NAME[n].n[2] === 100, `${n}: Öl`);
  must(unit('Cashewdrink ungesüßt') === 'ml' && unit('Kokosjoghurt') === 'g', 'Einheiten der neuen Produkte');
  // Mahlzeiten: Joghurt wird ein Klecks zum Gericht, Kochcreme Flüssigkeit, nichts geht verloren oder zählt doppelt
  const t = targets(2, 1);
  const r = solve(['Zucchini', 'Karotten', 'Kartoffeln', 'Olivenöl', 'Kokosjoghurt', 'Haferkochcreme', 'Cashewdrink ungesüßt', 'Sojajoghurt', 'Gemahlene Mandeln'].map((name) => ({ name })), t);
  const meals = buildMeals(r.items);
  const got = {};
  for (const m of meals) for (const k of ['veg', 'base', 'oils', 'herb', 'acid', 'aroma', 'liq', 'top', 'dessert', 'dip']) for (const it of m[k] || []) got[it.name] = (got[it.name] || 0) + it.g;
  for (const it of r.items) if (it.g > 0 && BY_NAME[it.name].n[0] > 0) must(got[it.name] === it.g, `Mahlzeiten: ${it.name} ${got[it.name]} statt ${it.g} g`);
  must(meals.some((m) => (m.dip || []).some((i) => i.name === 'Kokosjoghurt')) || !r.items.find((i) => i.name === 'Kokosjoghurt').g, 'Kokosjoghurt sollte als Klecks zum Gericht kommen');
}
