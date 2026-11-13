// RSS-Feed für Pinterest („Pins automatisch veröffentlichen“). Jedes Rezept ist ein Eintrag mit Hochformat-Grafik
// aus scripts/pins.mjs. Ab PINS_START wird alle PINS_ABSTAND Tage ein weiteres Rezept freigegeben; der geplante
// Neuaufbau der Seite (deploy.yml, zweimal pro Woche) schaltet die fälligen Einträge frei.
import { RECIPES, nutrition } from '../lib/nutrition.js';
import { SITE_NAME, PINS_START, PINS_ABSTAND } from '../data/site.js';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const MONATE = { Frühling: [2, 3, 4], Sommer: [5, 6, 7], Herbst: [8, 9, 10], Winter: [11, 0, 1] };

/** Reihenfolge: Rezepte, die zur Jahreszeit des Starts passen, zuerst; sonst wie in der Sammlung. */
export function reihenfolge(recipes, start) {
  const m = start.getMonth();
  const passt = (r) => !r.season?.length || r.season.some((s) => MONATE[s]?.includes(m));
  return [...recipes.filter(passt), ...recipes.filter((r) => !passt(r))];
}

export function GET({ site }) {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, '/');
  const abs = (p) => new URL(base + p, site).href;
  const start = PINS_START ? new Date(`${PINS_START}T06:00:00Z`) : null;
  const now = Date.now();
  const items = !start || Number.isNaN(start.getTime()) ? [] : reihenfolge(RECIPES.filter((r) => r.slot !== 'side'), start)
    .map((r, i) => ({ r, date: new Date(start.getTime() + i * PINS_ABSTAND * 86400000) }))
    .filter((x) => x.date.getTime() <= now)
    .reverse();
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
  <title>${esc(SITE_NAME)}: Rezepte</title>
  <link>${abs('rezepte/')}</link>
  <description>Pflanzliche Scheinfasten-Rezepte, nach den Werten von Longo berechnet.</description>
  <language>de-DE</language>
${items.map(({ r, date }) => {
    const kcal = Math.round(nutrition(r).kcal), link = abs(`rezepte/${r.slug}/`), img = abs(`pins/${r.slug}.jpg`);
    return `  <item>
    <title>${esc(r.title)}</title>
    <link>${link}</link>
    <guid isPermaLink="true">${link}</guid>
    <pubDate>${date.toUTCString()}</pubDate>
    <description>${esc(`${r.teaser} ${kcal} kcal pro Portion, ${r.minutes} Minuten, 100 % pflanzlich. Scheinfasten-Rezept mit Nährwerten.`)}</description>
    <enclosure url="${img}" type="image/jpeg" length="0" />
    <media:content url="${img}" medium="image" type="image/jpeg" width="1000" height="1500" />
  </item>`;
  }).join('\n')}
</channel>
</rss>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
