// Affiliate-Konfiguration. Hier trägst Du Deine Partner-IDs ein, sobald die Konten stehen.
// Alle Links werden automatisch als „Anzeige“ gekennzeichnet und mit rel="sponsored" ausgegeben.
// Die Seite zu Krebs zeigt grundsätzlich keine Affiliate-Links und keine Werbung.

/** Amazon PartnerNet: Deine Tracking-ID, z. B. „scheinfasten-21“. Leer = Links ohne Provision. */
export const AMAZON_TAG = 'einfachleckerfasten-21';

/** ProLon (Partnerprogramm über Refersion oder Awin): Dein persönlicher Partnerlink. */
export const PROLON_LINK = 'https://prolon.eu/de/';

/** Preis laut Herstellerseite, zuletzt geprüft am 03.11.2026. Bitte bei Änderungen anpassen. */
export const PROLON_PRICE = 179;
export const PROLON_CHECKED = '03.11.2026';

/** Werbeanzeigen (z. B. AdSense). Erst einschalten, wenn ein Einwilligungsbanner eingebaut ist. */
export const ADS_ENABLED = false;

/** Link zu Amazon: Produktseite mit ASIN, sonst Amazon-Suche. Immer mit Tracking-ID. */
export function amazonUrl(p) {
  const tag = AMAZON_TAG ? `tag=${encodeURIComponent(AMAZON_TAG)}` : '';
  if (p.asin) return `https://www.amazon.de/dp/${p.asin}${tag ? '?' + tag : ''}`;
  return `https://www.amazon.de/s?k=${encodeURIComponent(p.search)}${tag ? '&' + tag : ''}`;
}

/** Datum der letzten Produktprüfung. Nach 180 Tagen meldet die monatliche Wartung, dass die Liste durchgesehen werden soll. */
export const PRODUCTS_CHECKED = '14.11.2026';

// Produkte. Ausgewählt nach unabhängigen Tests und Bewertungen (Belege im Feld „beleg“, nur intern, nicht auf der Seite).
// Lebensmittel überwiegend Bio. Texte ohne Gesundheitsversprechen (HWG, Health-Claims-Verordnung), keine Preise
// und keine Sterne (Amazon erlaubt beides nur live über die Product Advertising API).
// asin: Amazon-Artikelnummer (steht in der Produkt-URL nach /dp/). search: Rückfall, wenn kein konkretes Produkt passt.
// img: Symbolbild aus public/img/produkte/, sonst der Schlüssel selbst.
export const PRODUCTS = {
  // Küche
  waage: { group: 'kueche', icon: 'scale', asin: 'B003VELZQU', title: 'Tanita Küchenwaage KD-321 mit 0,1-g-Feinteilung', why: 'Bis 300 g auf 0,1 g genau, darüber bis 3 kg. Damit stimmen Öl und Nüsse aus dem Planer aufs Gramm.', beleg: 'Japanischer Waagenspezialist, 0,1 g bis 300 g; Gefu Preziso verworfen (schwache Bewertungen zur Feinteilung).' },
  stab: { group: 'kueche', icon: 'pot', asin: 'B086HX9LB6', title: 'Braun MultiQuick 5 Vario Stabmixer', why: 'Für cremige Suppen, Pesto und Kräuteröl ohne Sahne. Mit Mix- und Messbecher.', beleg: 'Stiftung Warentest 7/2021: MultiQuick 5 Vario Testsieger Stabmixer (laut desired.de).' },
  stab_bosch: { group: 'kueche', img: 'stab', icon: 'pot', asin: 'B0BBH5WK6Y', title: 'Bosch ErgoMaster Serie 6 Stabmixer', why: 'Kräftiger Stabmixer mit vier Klingen. Püriert auch Suppen mit Hülsenfrüchten in Sekunden.', beleg: 'Mittelklasse bis Premium, verschleißfreie Keramik-Kupplung, je nach Variante 10 Jahre Motorgarantie.' },
  spirale: { group: 'kueche', icon: 'leaf', asin: 'B00UL5XP4C', title: 'GEFU Spiralschneider Spirelli 2.0', why: 'Macht aus Zucchini, Karotten und Gurke in einer Minute Gemüsenudeln.', beleg: 'Marktführer im Handspiralschneider-Segment, Der Standard 4/6 Punkten; kein Stiftung-Warentest-Test vorhanden.' },
  hobel: { group: 'kueche', icon: 'leaf', asin: 'B0116XZF18', title: 'Börner V5 Gemüsehobel PowerLine (Plus-Set)', why: 'Scheiben, Stifte und Würfel für Ofengemüse und Rohkost, schnell und gleichmäßig. Mit Fingerschutz.', beleg: 'SRF Kassensturz: Testsieger „gut“ bei Gemüsehobeln/Raffeln, Made in Germany.' },
  messer: { group: 'kueche', icon: 'leaf', asin: 'B085V653KM', title: 'WÜSTHOF Classic Kochmesser 20 cm', why: 'Ein scharfes Kochmesser macht das viele Gemüseschneiden zum Vergnügen statt zur Pflicht.', beleg: 'Geschmiedet in Solingen; Wüsthof bei Stiftung Warentest (Santoku) und dTest 2018 (Classic Ikon) vorn.' },
  dosen: { group: 'kueche', icon: 'pot', asin: 'B09C917KZ1', title: 'Emsa Clip & Close Glasdosen, 3er-Set', why: 'Suppen und Salate für zwei Tage vorkochen und portioniert in den Kühlschrank stellen. Ofen- und spülmaschinenfest.', beleg: 'Glas schlägt Plastik (test.de über Saldo-Test); Emsa Clip & Close etablierter Standard, 100 % dicht laut Hersteller.' },
  daempfer: { group: 'kueche', icon: 'pot', asin: 'B002QF38PG', title: 'WMF Dämpfeinsatz 20 cm aus Edelstahl', why: 'Gemüse schonend dämpfen, passt in viele 20-cm-Töpfe. Kein Extragerät nötig.', beleg: 'Cromargan 18/10, passt laut Bewertungen auch in Töpfe anderer Marken.' },
  thermo: { group: 'kueche', icon: 'cup', asin: 'B08MXGR35T', title: 'alfi Isolierkanne Skyline 1 Liter', why: 'Kräutertee für den ganzen Tag, morgens einmal aufgießen und bis abends warm.', beleg: 'alfi Testsieger beim dänischen Partner Forbrugerrådet Tænk (über test.de); Glaseinsatz, 12 h heiß.' },
  thermo_helena: { group: 'kueche', img: 'thermo', icon: 'cup', asin: 'B07GLBW7WQ', title: 'alfi Isolierkanne Helena 1 Liter', why: 'Klassische Edelstahlkanne mit Glaseinsatz, Made in Germany. Hält Tee bis zu 12 Stunden heiß.', beleg: 'Premium-Variante von alfi.' },
  teebereiter: { group: 'kueche', img: 'tee', icon: 'cup', asin: 'B006IBNJ1C', title: 'Bodum Assam Teebereiter 1 Liter', why: 'Für losen Kräutertee: Stempel runter, und der Tee zieht nicht nach.', beleg: 'Klassiker, Borosilikatglas, Edelstahlfilter.' },
  // Vorrat
  oel: { group: 'vorrat', icon: 'oil', asin: 'B07D49D3NR', title: 'Rapunzel Bio-Olivenöl fruchtig, nativ extra', why: 'Die wichtigste Fettquelle in fast jedem unserer Rezepte. Ein gutes Öl schmeckt man sofort.', beleg: 'ÖKO-TEST 05/2026: Rapunzel Olivenöl nativ extra „sehr gut“ (eines von zwei). Sorte im Test nicht frei einsehbar.' },
  oel_manira: { group: 'vorrat', img: 'oel', icon: 'oil', asin: 'B005PM1TMG', title: 'Rapunzel Bio-Olivenöl Manira, nativ extra', why: 'Griechisches Öl aus Koroneiki-Oliven, kräftig und grün. Ideal für Salate und zum Beträufeln.', beleg: 'Rapunzel (ÖKO-TEST 05/2026 „sehr gut“ für Rapunzel-Öl), 4,9 Sterne bei kleiner Bewertungszahl.' },
  bruehe: { group: 'vorrat', icon: 'pot', asin: 'B0BTMC19HJ', title: 'Knorr Bio Gemüse-Bouillon', why: 'Basis für alle Suppen. Ohne Zuckerzusatz und ohne Geschmacksverstärker.', beleg: 'ÖKO-TEST 10/2026: „sehr gut“, keine Pestizide, kein Aroma.' },
  nuesse: { group: 'vorrat', icon: 'nut', asin: 'B07DM9BMH3', title: 'Rapunzel Bio-Walnusskerne, halbe', why: 'Für Nussmix, Pesto und Toppings. In zehn unserer Rezepte dabei.', beleg: 'ÖKO-TEST Walnüsse: alle Bio-Walnüsse bei Inhaltsstoffen „sehr gut“.' },
  kuerbiskerne: { group: 'vorrat', img: 'nuesse', icon: 'nut', asin: 'B0078GBPUS', title: 'Davert Bio Knabber-Kürbiskerne', why: 'Knusprig über Suppe und Salat. Kleine Menge, viel Biss.', beleg: 'Davert Bio-Marke, schalenlos gewachsen.' },
  oliven: { group: 'vorrat', icon: 'leaf', asin: 'B07ZVVB35G', title: 'Rapunzel Bio-Oliven mit Kräutern, ohne Stein', why: 'Unser liebster Snack zwischendurch: viel Geschmack, wenig Zucker.', beleg: 'Bio, griechische Handernte, Kräuter und Olivenöl.' },
  leinsamen: { group: 'vorrat', icon: 'herb', asin: 'B013DO9UT6', title: 'Rapunzel Bio-Leinsaat braun', why: 'Für die knusprigen Leinsamen-Cracker und als Topping.', beleg: 'Bio, Herkunft Deutschland.' },
  tahin: { group: 'vorrat', icon: 'oil', asin: 'B0038GWBPA', title: 'Rapunzel Bio-Tahin', why: 'Für Hummus-Bowl und Dressings. Nur Sesam, sonst nichts.', beleg: 'Bio, 100 % Sesam; kein unabhängiger Tahin-Test vorhanden.' },
  miso: { group: 'vorrat', icon: 'pot', asin: 'B00HS1O2V2', title: 'Arche Bio Shiro Miso (hell)', why: 'Gibt Brühen in Sekunden einen tiefen, herzhaften Geschmack.', beleg: 'Bio, milde Reis-Miso, traditionelle Naturkostmarke.' },
  kokos: { group: 'vorrat', icon: 'pot', asin: 'B009RENX5E', title: 'Morgenland Bio-Kokosmilch, 60 % Kokos', why: 'Für Curry und cremige Suppen. Nur Kokos und Wasser, ohne Verdickungsmittel.', beleg: 'ÖKO-TEST Kokosmilch: Morgenland Kokosmilch extra „sehr gut“.' },
  hirse: { group: 'vorrat', icon: 'herb', asin: 'B0078GBUQC', title: 'Davert Bio-Hirse', why: 'Mild und schnell gegart. In fünf unserer Rezepte die sättigende Beilage.', beleg: 'Bio, Davert Naturkostmarke.' },
  gewuerze: { group: 'vorrat', icon: 'herb', asin: 'B007QTZ9EU', title: 'Sonnentor Bio-Gewürze, Probierset mit 10 Sorten', why: 'Wenn Salz und Fett knapp sind, machen Gewürze den Unterschied. Zum Ausprobieren ohne große Vorräte.', beleg: 'Sonnentor Bio, Einzelgewürze à 5 g.' },
  gewuerze_italia: { group: 'vorrat', img: 'gewuerze', icon: 'herb', asin: 'B07R4GV62J', title: 'Sonnentor Bio-Kräuter All’Italiana', why: 'Für Tomatensuppe, Ofengemüse und Dressing. Eine Prise reicht.', beleg: 'Sonnentor Bio.' },
  tee: { group: 'vorrat', icon: 'cup', asin: 'B00OYBENWC', title: 'Lebensbaum Bio-Kräutertee Wiesenkräuter', why: 'Kräutertee ist während der fünf Tage erlaubt. Mild, ohne Aroma und ohne Koffein.', beleg: 'Lebensbaum-Kräutertee bei ÖKO-TEST mehrfach „sehr gut“ (auch PA-Prüfung).' },
  tee_minze: { group: 'vorrat', img: 'tee', icon: 'cup', asin: 'B076B8D2VM', title: 'Lebensbaum Bio-Tee Minze, Minze & Minze', why: 'Frisch und kräftig, hilft durch den Nachmittag.', beleg: 'Lebensbaum Bio, ohne Aroma.' },
  tee_lose: { group: 'vorrat', img: 'tee', icon: 'cup', asin: 'B007FBCCJE', title: 'Lebensbaum Bio-Kräutertee Morgengruß, lose', why: 'Fenchel, Minze und Ysop für die Teekanne. Lose Kräuter sind ergiebiger als Beutel.', beleg: 'Lebensbaum Bio, lose 100 g.' },
  // Bücher
  buch_longo: { group: 'buch', img: 'buch', icon: 'book', asin: '3442177146', title: 'Prof. Dr. Valter Longo: Iss dich jung', why: 'Das Buch des Erfinders. Erklärt die Forschung hinter dem Scheinfasten aus erster Hand.', beleg: 'Goldmann, Taschenbuch.' },
  buch_michalsen: { group: 'buch', img: 'buch', icon: 'book', asin: '3965845101', title: 'Andreas Michalsen: Scheinfasten, mein Masterplan', why: 'Der Berliner Fastenmediziner mit Plänen für mehrere Kuren.', beleg: 'SPIEGEL-Bestseller.' },
  buch_gu: { group: 'buch', img: 'buch', icon: 'book', title: 'GU: Scheinfasten, Das Rezeptbuch', why: 'Weitere vegane Rezepte, drei pro Tag, wenn Du Abwechslung suchst.', search: 'Scheinfasten Das Rezeptbuch GU', beleg: 'ASIN noch nicht ermittelt, daher Suche.' },
};

export const GROUPS = [
  { key: 'kueche', title: 'Für die Küche', lead: 'Einmal gekauft, für jede Fastenwoche.' },
  { key: 'vorrat', title: 'Für den Vorrat', lead: 'Was in fast jedem Rezept vorkommt und sich gut lagern lässt. Wo möglich in Bio-Qualität.' },
  { key: 'buch', title: 'Zum Weiterlesen', lead: 'Bücher rund um das Scheinfasten.' },
];

/** Passende Produkte zu einem Rezept: bis zu 7, die Box zeigt davon zufällig 3. */
export function productsForRecipe(r) {
  const names = r.ingredients.map((i) => i.name);
  const has = (s) => names.some((n) => n.includes(s));
  const keys = ['waage'];
  if (r.category === 'Suppe' || r.category === 'Eintopf') keys.push('stab', 'bruehe');
  if (r.slug.includes('zucchini-nudeln')) keys.push('spirale');
  if (has('Misopaste')) keys.push('miso');
  if (has('Leinsamen')) keys.push('leinsamen');
  if (has('Tahin')) keys.push('tahin');
  if (has('Grüne Oliven')) keys.push('oliven');
  if (has('Kokosmilch')) keys.push('kokos');
  if (has('Hirse')) keys.push('hirse');
  if (has('Kürbiskerne')) keys.push('kuerbiskerne');
  if (has('Walnuss') || has('Mandeln') || has('Cashew')) keys.push('nuesse');
  if (has('Olivenöl')) keys.push('oel');
  if (r.category === 'Ofengericht' || r.category === 'Salat' || r.category === 'Pfanne') keys.push('hobel', 'messer');
  if (has('Oregano') || has('Paprikapulver') || has('Kreuzkümmel')) keys.push('gewuerze');
  keys.push('dosen');
  return [...new Set(keys)].slice(0, 7).map((k) => ({ key: k, ...PRODUCTS[k] }));
}

export const pick = (...keys) => keys.map((k) => {
  if (!PRODUCTS[k]) throw new Error(`Unbekanntes Produkt „${k}“ in pick()`);
  return { key: k, ...PRODUCTS[k] };
});
