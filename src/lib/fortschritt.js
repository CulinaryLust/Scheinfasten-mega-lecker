// Fortschritt beim Abhaken: Kalorien und Eiweiß, Fett, Kohlenhydrate des Gegessenen im Verhältnis zum Tagesziel.
// Gemeinsam für den fertigen Plan und den DIY-Plan.

const MAC = [
  ['protein', 'Eiweiß', 4, 'p'],
  ['fat', 'Fett', 9, 'f'],
  ['carbs', 'Kohlenhydrate', 4, 'c'],
];
const r0 = (x) => Math.round(x);

/**
 * eaten, target: { kcal, protein, fat, carbs } (Gramm bzw. kcal).
 * planned (optional): alles, was für heute eingeplant ist, inklusive Gegessenem. Erscheint hell im Balken.
 * fmt: Zahlenformat der Seite. Liefert Balken (Gegessenes nach Nährstoffen eingefärbt, Eingeplantes hell)
 * und drei Kennzahlen in Gramm. Prozente nur bei den Kalorien, damit sie nicht mit Makroanteilen verwechselt werden.
 */
export function doneHtml(eaten, target, fmt, extra = '', planned = null) {
  const kcalPct = target.kcal ? r0((eaten.kcal / target.kcal) * 100) : 0;
  const targetE = MAC.reduce((a, [k, , f]) => a + target[k] * f, 0);
  const eatenE = MAC.reduce((a, [k, , f]) => a + eaten[k] * f, 0);
  const info = MAC.map(([k, label, f, cls]) => {
    const pct = target[k] ? r0((eaten[k] / target[k]) * 100) : 0;
    const width = targetE ? Math.min(100, (eaten[k] * f / targetE) * 100) : 0;
    const plan = planned ? ` Eingeplant: ${fmt(planned[k])} g.` : '';
    const tip = `${label}: ${fmt(eaten[k])} g gegessen, Tagesziel ${fmt(target[k])} g (${pct} % davon).${plan}`;
    return { k, label, cls, width, tip };
  });
  const used = info.reduce((a, m) => a + m.width, 0);
  const planW = planned && targetE ? Math.max(0, Math.min(100 - used, ((MAC.reduce((a, [k, , f]) => a + planned[k] * f, 0) - eatenE) / targetE) * 100)) : 0;
  const planTxt = planned ? ` · eingeplant ${fmt(planned.kcal)} kcal` : '';
  return `<div class="donebar">
    <div class="bar stacked" role="img" aria-label="${kcalPct} % der Tageskalorien gegessen${planTxt}">${info.map((m) => `<i class="${m.cls}" style="width:${m.width}%" title="${m.tip}"></i>`).join('')}${planW ? `<i class="pl" style="width:${planW}%" title="Eingeplant, noch nicht abgehakt"></i>` : ''}</div>
    <span><b>${fmt(eaten.kcal)}</b> von ${fmt(target.kcal)} kcal gegessen (${kcalPct} %)${planTxt}${extra}</span>
    <div class="donemac">${info.map((m) => `<span class="dm ${m.k}" tabindex="0" data-tip="${m.tip}"><i class="dot"></i>${m.label} <b>${fmt(eaten[m.k])}</b> von ${fmt(target[m.k])} g</span>`).join('')}</div>
  </div>`;
}
