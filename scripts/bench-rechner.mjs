// Belastungstest: zufällige, realistische Einkaufskörbe. Zählt, wie oft der Rechner Longos Fenster trifft
// (direkt oder mit einer seiner Ergänzungen) und ob dabei Regeln verletzt werden.
import { FOODS, BY_NAME, solve, targets, profile, suggestAdditions, completeDay, buildMeals, totals } from '../src/lib/rechner.js';
let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const pickN = (arr, n) => { const a = [...arr]; const out = []; while (out.length < n && a.length) out.push(a.splice(Math.floor(rnd() * a.length), 1)[0]); return out; };
const by = (gs) => FOODS.filter((f) => f.light !== 'r' && gs.includes(f.group) && f.n[0] > 5).map((f) => f.name);
const VEG = by(['gemuese', 'blatt', 'pilze']), FAT = by(['fett', 'nuss', 'fettfrucht', 'pflanz']), STARCH = by(['knolle', 'huelsen', 'getreide', 'obst', 'soja', 'knusper']);
const N = +(process.argv[2] || 150);
const stat = { ok: 0, okAdd: 0, okPack: 0, fail: 0, capViol: 0, sugarViol: 0, mealLoss: 0 };
const fails = [];
for (let i = 0; i < N; i++) {
  const names = [...pickN(VEG, 2 + Math.floor(rnd() * 4)), ...pickN(FAT, 1 + Math.floor(rnd() * 2)), ...pickN(STARCH, Math.floor(rnd() * 3))];
  const p = profile({ sex: rnd() < 0.5 ? 'w' : 'm', age: 25 + Math.floor(rnd() * 45), h: 155 + Math.floor(rnd() * 35), w: 50 + Math.floor(rnd() * 50), pal: [1.4, 1.6, 1.8][Math.floor(rnd() * 3)] });
  const t = targets(rnd() < 0.3 ? 1 : 2, p.f);
  const picks = names.map((name) => ({ name }));
  const r = solve(picks, t);
  for (const it of r.items) if (it.g > BY_NAME[it.name].cap) stat.capViol++;
  if (r.verdict.ok && r.sum.sugar > r.verdict.sugarMax + 0.5) stat.sugarViol++;
  const back = totals(buildMeals(r.items).flatMap((m) => m.items));
  if (Math.abs(back.kcal - r.sum.kcal) > 15) stat.mealLoss++;
  if (r.verdict.ok) { stat.ok++; continue; }
  const add = suggestAdditions(picks, t, r);
  if (add.some((a) => a.ok)) stat.okAdd++; else if (completeDay(picks, t)?.ok) stat.okPack++; else { stat.fail++; if (fails.length < 8) fails.push(`${names.join(', ')} -> ${Math.round(r.sum.kcal)}/${Math.round(t.kcal)} kcal, E ${Math.round(r.verdict.shares.protein)} F ${Math.round(r.verdict.shares.fat)} KH ${Math.round(r.verdict.shares.carbs)}, Zucker ${Math.round(r.sum.sugar)}/${Math.round(r.verdict.sugarMax)}`); }
}
console.log(`${N} Körbe: direkt passend ${stat.ok}, mit einer Ergänzung passend ${stat.okAdd}, mit Ergänzungspaket passend ${stat.okPack}, ungelöst ${stat.fail}, Obergrenze verletzt ${stat.capViol}, Zucker falsch ${stat.sugarViol}, Mahlzeiten verlieren kcal ${stat.mealLoss}`);
fails.forEach((f) => console.log('  ', f));
// Schwellen: Regeln dürfen nie verletzt werden, und fast jeder Korb muss sich mit den Vorschlägen des Rechners lösen lassen.
const solved = (stat.ok + stat.okAdd + stat.okPack) / N;
const bad = stat.capViol + stat.sugarViol + stat.mealLoss;
if (bad || solved < 0.9) { console.log(`FEHLER: ${bad} Regelverletzungen, ${Math.round(solved * 100)} % lösbar (mindestens 90 % erwartet)`); process.exit(1); }
console.log(`Alles ok (${Math.round(solved * 100)} % lösbar)`);
