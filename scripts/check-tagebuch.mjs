// Prüft die Tagesbilanz (Reiter „Was habe ich gegessen?“) mit typischen Tagen.
import { status, fillFoods, fillRecipes, expand, grams, qtyLabel, searchAll, dayFromStart, defaultAmount, PUMPKIN_MAX } from '../src/lib/tagebuch.js';
import { targets, profile, BY_NAME } from '../src/lib/rechner.js';

let failed = 0;
const must = (cond, msg) => { if (!cond) { failed++; console.log('FEHLER:', msg); } };
const r = Math.round;
const p = profile({ sex: 'w', age: 42, h: 168, w: 70, pal: 1.6 });
const t1 = targets(1, p.f), t2 = targets(2, p.f);
const food = (name, qty, unit = 'g') => ({ type: 'food', name, qty, unit });
const rec = (slug, qty = 1) => ({ type: 'recipe', slug, qty, unit: 'portion' });

// Einheiten
must(grams(food('Zucchini', 1, 'piece')) === 200, 'Stück Zucchini');
must(grams(food('Kaffee', 1, 'cup')) === 150, 'Tasse Kaffee');
must(qtyLabel(food('Zucchini', 1, 'piece')).includes('200 g'), `Label ${qtyLabel(food('Zucchini', 1, 'piece'))}`);
must(defaultAmount({ type: 'food', name: 'Olivenöl' }).qty === 10, 'Standardmenge Öl');
// Suche findet Rezepte und Lebensmittel
must(searchAll('minestrone')[0]?.type === 'recipe', 'Suche Rezept');
must(searchAll('möhre').some((h) => h.name === 'Karotten'), 'Suche Lebensmittel');
must(searchAll('walnu')[0]?.name === 'Walnusskerne', `Suche Walnuss: ${searchAll('walnu')[0]?.label}`);
// Rezept wird in Zutaten zerlegt
const ex = expand([rec('minestrone', 2)]);
must(r(ex.find((i) => i.name === 'Zucchini').g) === 200, 'Rezept zerlegt, Portionen');

// Leerer Tag: alles offen
const s0 = status([], t2, 2);
must(s0.bars[0].eaten === 0 && !s0.done, 'Leerer Tag');
// Halber Tag 2: Minestrone mittags
const half = [rec('minestrone'), food('Walnusskerne', 10)];
const s1 = status(half, t2, 2);
console.log(`Tag 2 halb: ${r(s1.sum.kcal)}/${r(t2.kcal)} kcal`, s1.bars.map((b) => `${b.key} ${r(b.pct)} %`).join(', '));
must(s1.bars[0].state === 'open', 'Halber Tag offen');
const ff = fillFoods(half, t2);
console.log('  Auffüllen:', ff.add.map((i) => `${i.name} ${i.g}`).join(', '), `=> ${r(ff.sum.kcal)} kcal`, ff.verdict.ok ? 'ok' : 'AUSSERHALB');
must(ff.verdict.ok, 'Auffüllen trifft Longo nicht');
const fr = fillRecipes(half, t2);
console.log('  Rezepte:', fr.map((x) => `${x.recipe.slug} ×${x.portion} -> ${r(x.sum.kcal)} kcal${x.ok ? ' ok' : ''}`).join(', '));
must(fr.length > 0, 'Keine Rezeptvorschläge');
for (const x of fr) must(x.sum.kcal <= t2.kcal * 1.05 + 1, `${x.recipe.slug} sprengt Kalorien`);
// Kaffee und Kürbis
const s2 = status([food('Kaffee', 2, 'cup'), food('Hokkaido-Kürbis', 250)], t2, 3);
must(s2.notes.some((n) => n.key === 'kaffee'), 'Kaffee-Hinweis fehlt');
must(s2.notes.some((n) => n.key === 'kuerbis'), 'Kürbis-Hinweis fehlt');
must(!status([food('Hokkaido-Kürbis', 250)], t1, 1).notes.some((n) => n.key === 'kuerbis'), 'Kürbis-Hinweis an Tag 1');
must(!status([food('Kaffee', 1, 'cup')], t2, 2).notes.length, 'Eine Tasse ist ok');
must(status([food('Hokkaido-Kürbis', PUMPKIN_MAX)], t2, 2).notes.length === 0, 'Genau 200 g Kürbis ist ok');
// Rotes Lebensmittel zählt mit und bekommt Hinweis
const red = Object.values(BY_NAME).find((f) => f.light === 'r');
const s3 = status([food(red.name, 100)], t2, 2);
must(s3.sum.kcal > 0 && s3.notes.some((n) => n.key === 'rot'), 'Rotes Lebensmittel');
const ffr = fillFoods([food(red.name, 50)], t2);
must(ffr.sum.kcal >= s3.sum.kcal / 2 - 1, 'Rotes Gegessenes beim Auffüllen vergessen');
// Überschritten
const s4 = status([food('Olivenöl', 80), food('Walnusskerne', 40)], t2, 2);
must(s4.over && fillRecipes([food('Olivenöl', 80), food('Walnusskerne', 40)], t2).length === 0, 'Überschritten ohne Vorschläge');
// Zyklustag aus dem Startdatum
must(dayFromStart('2026-11-02', new Date('2026-11-04T09:00:00')) === 3, 'Tag aus Start');
must(dayFromStart('2026-11-02', new Date('2026-11-10T09:00:00')) === null, 'Außerhalb des Zyklus');
console.log(failed ? `${failed} Fehler` : 'Alles ok');
process.exit(failed ? 1 : 0);
