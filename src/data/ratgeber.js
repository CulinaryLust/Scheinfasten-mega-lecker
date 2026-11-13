// Ratgeber-Artikel in Anzeigereihenfolge. Jeder Eintrag braucht eine Seite unter src/pages/ratgeber/<slug>.astro.
// stand = Datum der letzten inhaltlichen Prüfung (JJJJ-MM-TT). `npm run check:frische` meldet Artikel, die älter als ein Jahr sind.
export const ARTIKEL = [
  { slug: 'einkaufsliste', title: 'Scheinfasten-Einkaufsliste für 5 Tage', teaser: 'Alles, was Du für einen Durchgang brauchst, grammgenau aus unserem Standardplan berechnet.', icon: 'cart', stand: '2026-11-12' },
  { slug: 'tag-fuer-tag', title: 'Scheinfasten Tag für Tag: Ablauf von Tag 1 bis 5', teaser: 'Was Du an welchem Tag isst, wie viel es ist und womit viele an den einzelnen Tagen rechnen.', icon: 'calendar', stand: '2026-11-12' },
  { slug: 'nach-dem-scheinfasten', title: 'Was essen nach dem Scheinfasten? Tag 6 und danach', teaser: 'Wie Du nach fünf Tagen wieder einsteigst, ohne Dich zu überessen.', icon: 'pot', stand: '2026-11-12' },
  { slug: 'sport-und-alltag', title: 'Scheinfasten, Sport und Arbeit: Was geht in den 5 Tagen?', teaser: 'Was die Studien dazu sagen (wenig) und wie Du die Woche realistisch planst.', icon: 'pulse', stand: '2026-11-12' },
];
export const BY_SLUG = Object.fromEntries(ARTIKEL.map((a) => [a.slug, a]));
export const datum = (iso) => { const [y, m, d] = iso.split('-'); return `${d}.${m}.${y}`; };
