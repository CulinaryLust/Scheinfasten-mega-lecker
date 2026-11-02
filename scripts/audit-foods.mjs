// Prüft jedes einzelne Lebensmittel der Datenbank: Lässt es sich zusammen mit einer neutralen Basis
// (Olivenöl, Walnüsse, Oliven, Kartoffeln, Hirse, Zucchini, Blumenkohl, Tomaten) in Longos Tageswerte bringen, ohne eine Obergrenze zu reißen?
// Rote Lebensmittel dürfen nie eingerechnet werden und brauchen Begründung und passende Alternativen.
import { FOODS, BY_NAME, solve, targets, suggestAdditions } from '../src/lib/rechner.js';

const BASE = ['Olivenöl', 'Walnusskerne', 'Grüne Oliven', 'Kartoffeln', 'Hirse (gegart)', 'Zucchini', 'Blumenkohl', 'Tomaten'];
let failed = 0;
const bad = (msg) => { failed++; console.log('FEHLER:', msg); };
const rows = [];
for (const f of FOODS) {
  if (f.light === 'r') {
    if (!f.why) bad(`${f.name}: rot ohne Begründung`);
    if (!f.alts.length) bad(`${f.name}: rot ohne Alternative`);
    for (const a of f.alts) if (BY_NAME[a].light === 'r') bad(`${f.name}: Alternative ${a} ist selbst rot`);
    const r = solve([{ name: f.name }, ...BASE.map((name) => ({ name }))], targets(2));
    if (r.items.some((i) => i.name === f.name)) bad(`${f.name}: rot, aber eingerechnet`);
    continue;
  }
  for (const a of f.alts) if (BY_NAME[a].light === 'r') bad(`${f.name}: Alternative ${a} ist rot`);
  if (f.n[0] <= 5) continue; // Wasser, Tee, Brühe, Salz: ohne Kalorien, nichts zu verteilen
  for (const day of [1, 2]) {
    const t = targets(day);
    const picks = [{ name: f.name }, ...BASE.filter((n) => n !== f.name).map((name) => ({ name }))];
    let r = solve(picks, t);
    let via = '';
    if (!r.verdict.ok) {
      // Passt die Kombination nicht, muss der Rechner eine Ergänzung finden, mit der es passt.
      const add = suggestAdditions(picks, t, r).find((a) => a.ok);
      if (!add) { bad(`${f.name} Tag ${day === 1 ? 1 : '2-5'}: weder passend noch mit Ergänzung lösbar`); continue; }
      r = solve([...picks, { name: add.name }], t);
      via = add.name;
    }
    for (const i of r.items) if (i.g > BY_NAME[i.name].cap) bad(`${f.name}: ${i.name} ${i.g} g über Obergrenze ${BY_NAME[i.name].cap} g`);
    if (r.sum.sugar > r.verdict.sugarMax + 0.5) bad(`${f.name}: Zucker über Grenze`);
    if (day === 2) rows.push([f.name, r.items.find((i) => i.name === f.name).g, f.cap, f.capWhy, via]);
  }
}
const zero = rows.filter((r) => r[1] === 0);
console.log(`${FOODS.length} Lebensmittel geprüft, ${FOODS.filter((f) => f.light === 'r').length} rot.`);
console.log(`Tag 2-5 mit Basis: ${rows.length - zero.length} Lebensmittel werden eingeplant, ${zero.length} bleiben bei 0 g (der Rest des Tages reicht schon):`, zero.map((r) => r[0]).join(', ') || 'keine');
console.log(failed ? `${failed} Fehler` : 'Alle Lebensmittel ok');
process.exit(failed ? 1 : 0);
