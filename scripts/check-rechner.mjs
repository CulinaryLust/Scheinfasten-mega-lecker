// Prüft den Lebensmittel-Rechner mit typischen Kühlschrank-Inhalten.
import { solve, targets, profile, buildMeals, matchRecipes, suggestAdditions, search, totals, FOODS, BY_NAME } from '../src/lib/rechner.js';

let failed = 0;
const must = (cond, msg) => { if (!cond) { failed++; console.log('FEHLER:', msg); } };
const fmt = (x) => Math.round(x);

// Datenbank
must(FOODS.length >= 150, `nur ${FOODS.length} Lebensmittel`);
for (const f of FOODS) {
  must(f.n.length === 6 && f.n.slice(0, 5).every((v) => typeof v === 'number' && v >= 0), `Nährwerte ${f.name}`);
  must(f.alts.every((a) => BY_NAME[a]), `Alternative fehlt bei ${f.name}`);
  if (f.light === 'r') must(f.alts.length >= 1 && f.why, `Rot ohne Alternative/Begründung: ${f.name}`);
}
// Suche
must(search('möhre')[0]?.name === 'Karotten', 'Suche Möhre');
must(search('Hack')[0]?.light === 'r', 'Suche Hack');
must(search('kurbis').some((f) => f.name === 'Hokkaido-Kürbis'), 'Suche ohne Umlaut');

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
    console.log(`Tag ${day === 1 ? '1' : '2-5'} ${label}: ${fmt(r.sum.kcal)}/${fmt(t.kcal)} kcal, E ${fmt(v.shares.protein)} F ${fmt(v.shares.fat)} KH ${fmt(v.shares.carbs)} ${v.ok ? 'ok' : 'AUSSERHALB'}`);
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
console.log(failed ? `${failed} Fehler` : 'Alles ok');
process.exit(failed ? 1 : 0);
