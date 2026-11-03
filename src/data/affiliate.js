// Affiliate-Konfiguration. Hier trägst du deine Partner-IDs ein, sobald die Konten stehen.
// Alle Links werden automatisch als „Anzeige“ gekennzeichnet und mit rel="sponsored" ausgegeben.
// Die Seite zu Krebs zeigt grundsätzlich keine Affiliate-Links und keine Werbung.

/** Amazon PartnerNet: deine Tracking-ID, z. B. „scheinfasten-21“. Leer = Links ohne Provision. */
export const AMAZON_TAG = '';

/** ProLon (Partnerprogramm über Refersion oder Awin): dein persönlicher Partnerlink. */
export const PROLON_LINK = 'https://prolon.eu/de/';

/** Preis laut Herstellerseite, zuletzt geprüft am 03.11.2026. Bitte bei Änderungen anpassen. */
export const PROLON_PRICE = 179;
export const PROLON_CHECKED = '03.11.2026';

/** Werbeanzeigen (z. B. AdSense). Erst einschalten, wenn ein Einwilligungsbanner eingebaut ist. */
export const ADS_ENABLED = false;

/** Link zu Amazon: Produktseite, wenn eine ASIN bekannt ist, sonst Amazon-Suche. */
export function amazonUrl(p) {
  const tag = AMAZON_TAG ? `tag=${encodeURIComponent(AMAZON_TAG)}` : '';
  if (p.asin) return `https://www.amazon.de/dp/${p.asin}${tag ? '?' + tag : ''}`;
  return `https://www.amazon.de/s?k=${encodeURIComponent(p.search)}${tag ? '&' + tag : ''}`;
}

// Produkte. Texte bewusst ohne Gesundheitsversprechen (HWG, Health-Claims-Verordnung).
// asin: optional, wenn du ein konkretes Produkt empfehlen willst. search: Suchbegriff als Fallback.
export const PRODUCTS = {
  waage: { group: 'kueche', icon: 'scale', title: 'Digitale Küchenwaage auf 0,1 g', why: 'Beim Scheinfasten zählt jedes Gramm Öl und Nuss. Eine Feinwaage macht die Mengen aus dem Planer exakt.', search: 'Küchenwaage 0,1 g digital' },
  loeffel: { group: 'kueche', icon: 'oil', title: 'Messlöffel-Set', why: 'Für Öl, Tahin und Gewürze, wenn die Waage gerade nicht griffbereit ist.', search: 'Messlöffel Set Edelstahl' },
  dosen: { group: 'kueche', icon: 'pot', title: 'Meal-Prep-Glasdosen', why: 'Suppen und Salate für zwei Tage vorkochen und portioniert in den Kühlschrank stellen.', search: 'Meal Prep Glasbehälter Deckel' },
  stab: { group: 'kueche', icon: 'pot', title: 'Stabmixer', why: 'Für cremige Suppen, Pesto und Kräuteröl ohne Sahne.', search: 'Stabmixer Edelstahl' },
  spirale: { group: 'kueche', icon: 'leaf', title: 'Spiralschneider', why: 'Macht aus Zucchini in einer Minute Gemüsenudeln.', search: 'Spiralschneider Gemüse' },
  thermo: { group: 'kueche', icon: 'cup', title: 'Thermoskanne', why: 'Kräutertee für den ganzen Tag, auch unterwegs und im Büro.', search: 'Thermoskanne 1 Liter Tee' },
  tee: { group: 'vorrat', icon: 'cup', title: 'Kräutertee ohne Zucker', why: 'Tee ist während der fünf Tage ausdrücklich erlaubt. Abwechslung hilft durch den Nachmittag.', search: 'Kräutertee Bio ungesüßt' },
  oel: { group: 'vorrat', icon: 'oil', title: 'Natives Olivenöl extra', why: 'Die wichtigste Fettquelle in fast jedem unserer Rezepte. Ein gutes Öl schmeckt man sofort.', search: 'Olivenöl nativ extra Bio' },
  bruehe: { group: 'vorrat', icon: 'pot', title: 'Gemüsebrühe ohne Zuckerzusatz', why: 'Basis für alle Suppen. Achte auf eine Brühe ohne Zucker und mit wenig Salz.', search: 'Gemüsebrühe ohne Zucker Bio' },
  nuesse: { group: 'vorrat', icon: 'nut', title: 'Walnüsse und Mandeln', why: 'Für Nussmix, Pesto und Toppings. Größere Packungen sind deutlich günstiger.', search: 'Walnusskerne Bio 500 g' },
  oliven: { group: 'vorrat', icon: 'leaf', title: 'Grüne Oliven', why: 'Unser liebster Snack zwischendurch: viel Geschmack, wenig Zucker.', search: 'grüne Oliven Bio Glas' },
  leinsamen: { group: 'vorrat', icon: 'herb', title: 'Leinsamen', why: 'Für die knusprigen Leinsamen-Cracker.', search: 'Leinsamen Bio' },
  tahin: { group: 'vorrat', icon: 'oil', title: 'Tahin', why: 'Für Hummus-Bowl und Dressings.', search: 'Tahin Bio' },
  miso: { group: 'vorrat', icon: 'pot', title: 'Helle Misopaste', why: 'Gibt Brühen in Sekunden einen tiefen, herzhaften Geschmack.', search: 'helle Misopaste Bio' },
  buch_longo: { group: 'buch', icon: 'book', title: 'Prof. Dr. Valter Longo: Iss dich jung', why: 'Das Buch des Erfinders. Erklärt die Forschung hinter dem Scheinfasten aus erster Hand.', search: 'Valter Longo Iss dich jung' },
  buch_michalsen: { group: 'buch', icon: 'book', title: 'Andreas Michalsen: Scheinfasten, mein Masterplan', why: 'Der Berliner Fastenmediziner mit Plänen für mehrere Kuren.', search: 'Michalsen Scheinfasten mein Masterplan' },
  buch_gu: { group: 'buch', icon: 'book', title: 'GU: Scheinfasten, Das Rezeptbuch', why: 'Weitere vegane Rezepte, drei pro Tag, wenn du Abwechslung suchst.', search: 'Scheinfasten Das Rezeptbuch GU' },
};

export const GROUPS = [
  { key: 'kueche', title: 'Für die Küche', lead: 'Einmal gekauft, für jede Fastenwoche.' },
  { key: 'vorrat', title: 'Für den Vorrat', lead: 'Was in fast jedem Rezept vorkommt und sich gut lagern lässt.' },
  { key: 'buch', title: 'Zum Weiterlesen', lead: 'Bücher rund um das Scheinfasten.' },
];

/** Passende Produkte zu einem Rezept: Waage immer, dazu was zu Zutaten und Kategorie passt. */
export function productsForRecipe(r) {
  const names = r.ingredients.map((i) => i.name);
  const has = (s) => names.some((n) => n.includes(s));
  const keys = ['waage'];
  if (r.category === 'Suppe') keys.push('stab', 'bruehe');
  if (r.slug.includes('zucchini-nudeln')) keys.push('spirale');
  if (has('Misopaste')) keys.push('miso');
  if (has('Leinsamen')) keys.push('leinsamen');
  if (has('Tahin')) keys.push('tahin');
  if (has('Oliven')) keys.push('oliven');
  if (has('Walnuss') || has('Mandeln') || has('Cashew')) keys.push('nuesse');
  if (has('Olivenöl')) keys.push('oel');
  keys.push('dosen');
  return [...new Set(keys)].slice(0, 3).map((k) => ({ key: k, ...PRODUCTS[k] }));
}

export const pick = (...keys) => keys.map((k) => ({ key: k, ...PRODUCTS[k] }));
