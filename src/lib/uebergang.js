// Übergangstag (Tag 6) und „Wie geht es weiter?“: gemeinsam für den fertigen Plan und den DIY-Plan.

/** Gerichte, die gut zum Übergang passen (normale Portion). */
export const TRANSITION_SLUGS = ['minestrone', 'kuerbissuppe', 'spinat-dal'];

/** Wahl der Durchgänge: [Schlüssel, Durchgänge, Abstand in Monaten, Text]. */
export const CYCLE_OPTS = [
  ['once', 1, 1, 'Erst mal nur dieser Durchgang'],
  ['study', 3, 1, '3 Durchgänge, einmal im Monat (wie in der Studie)'],
  ['quarter', 4, 3, 'Alle 3 Monate'],
  ['half', 2, 6, 'Zweimal im Jahr'],
];

const WD = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
export const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
export const addMonths = (d, n) => { const x = new Date(d); x.setMonth(x.getMonth() + n); return x; };
export const dsl = (d) => `${WD[d.getDay()]}, ${d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' })}`;

/**
 * Hinweise für den Übergangstag mit Rezeptvorschlägen.
 * recipes: [{ href, img, title, minutes }]
 */
export function transitionHtml(date, recipes, esc) {
  return `<h3>Übergangstag${date ? ` am ${dsl(date)}` : ''}</h3><ul>
    <li>Nicht direkt zu großen Portionen zurückkehren.</li><li>Gut geeignet: Suppen, gedünstetes Gemüse, Reis, Haferbrei, kleine Mengen Eiweiß.</li>
    <li>Ab dem nächsten Tag wieder normal und ausgewogen essen.</li></ul>
    <p><b>Passt gut zum Übergang</b> <span class="muted small">(normale Portion, dazu Reis, Brot oder Haferbrei)</span></p>
    <div class="stack" style="gap:8px">${recipes.map((r) => `<a class="alt" href="${r.href}"><img src="${r.img}" alt="" loading="lazy"><span><b>${esc(r.title)}</b><small>${r.minutes} Minuten</small></span><span></span></a>`).join('')}</div>`;
}

/** „Wie geht es weiter?“ mit Auswahl der Durchgänge und den Folgeterminen ab start (erster Fastentag). */
export function nextCycleHtml(start, cyc, gap, icon = '') {
  const curKey = (CYCLE_OPTS.find((o) => o[1] === cyc && o[2] === gap) || CYCLE_OPTS[0])[0];
  let li = '';
  for (let c = 1; c < cyc; c++) { const s1 = addMonths(start, c * gap); li += `<li><b>${c + 1}. Durchgang:</b> ${dsl(s1)} bis ${dsl(addDays(s1, 4))} <span class="muted">(Vorbereitung ${dsl(addDays(s1, -1))})</span></li>`; }
  return `<h3>${icon} Wie geht es weiter?</h3>
    <p class="small muted">Gerichte und Mengen bleiben in jedem Durchgang gleich, es ändern sich nur die Termine. In der wichtigsten Studie gab es drei Durchgänge im Abstand von einem Monat. Wer gesund und normalgewichtig ist, kommt laut Prof. Dr. Longo mit etwa zwei Durchgängen im Jahr aus. Entscheide nach diesem ersten Durchgang, wie es Dir ging.</p>
    <div class="cycopts">${CYCLE_OPTS.map(([key, c, g, l]) => `<label><input type="radio" name="nextcyc" value="${key}" data-cyc="${c}" data-gap="${g}" ${key === curKey ? 'checked' : ''}><span>${l}</span></label>`).join('')}</div>
    ${cyc > 1 ? `<p><b>Dein nächster Scheinfastenzyklus beginnt am ${dsl(addMonths(start, gap))}.</b></p><ul>${li}</ul>` : ''}`;
}
