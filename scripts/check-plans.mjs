// Prüft, ob der Standardplan an allen fünf Tagen in Longos Toleranzfenster liegt.
import { PLAN, dayTotal, check, fmt } from '../src/lib/nutrition.js';

let failed = false;
for (const day of [1, 2, 3, 4, 5]) {
  const n = dayTotal(PLAN.days[day]);
  const c = check(day, n);
  const s = c.shares;
  console.log(`Tag ${day}: ${fmt(n.kcal)} kcal, E ${fmt(s.protein)} %, F ${fmt(s.fat)} %, KH ${fmt(s.carbs)} % ${c.ok ? 'ok' : 'AUSSERHALB'}`);
  if (!c.ok) failed = true;
}
process.exit(failed ? 1 : 0);
