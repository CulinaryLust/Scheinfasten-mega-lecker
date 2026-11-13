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
 * fmt: Zahlenformat der Seite. Liefert Balken (nach Nährstoffen eingefärbt) und drei Kennzahlen mit Tooltip.
 */
export function doneHtml(eaten, target, fmt, extra = '') {
  const kcalPct = target.kcal ? r0((eaten.kcal / target.kcal) * 100) : 0;
  const eatenE = MAC.reduce((a, [k, , f]) => a + eaten[k] * f, 0);
  const targetE = MAC.reduce((a, [k, , f]) => a + target[k] * f, 0);
  const info = MAC.map(([k, label, f, cls]) => {
    const pct = target[k] ? r0((eaten[k] / target[k]) * 100) : 0;
    const share = eatenE ? r0((eaten[k] * f / eatenE) * 100) : 0;
    const ref = targetE ? r0((target[k] * f / targetE) * 100) : 0;
    const width = target.kcal ? Math.min(100, (eaten[k] * f / targetE) * 100) : 0;
    const tip = eatenE
      ? `${label}: ${fmt(eaten[k])} von ${fmt(target[k])} g, ${pct} % des Tagesbedarfs. Anteil an den gegessenen Kalorien: ${share} % (Vorgabe ${ref} %).`
      : `${label}: noch nichts abgehakt. Vorgabe ${ref} % der Kalorien.`;
    return { k, label, cls, pct, share, ref, width, tip };
  });
  return `<div class="donebar">
    <div class="bar stacked" role="img" aria-label="${kcalPct} % der Tageskalorien abgehakt">${info.map((m) => `<i class="${m.cls}" style="width:${m.width}%" title="${m.tip}"></i>`).join('')}</div>
    <span><b>${fmt(eaten.kcal)}</b> von ${fmt(target.kcal)} kcal abgehakt · ${kcalPct} %${extra}</span>
    <div class="donemac">${info.map((m) => `<span class="dm ${m.k}" tabindex="0" data-tip="${m.tip}"><i class="dot"></i>${m.label} <b>${fmt(eaten[m.k])}</b>/${fmt(target[m.k])} g · <b>${m.pct} %</b></span>`).join('')}</div>
  </div>`;
}
