// Einordnung von Lebensmitteln für Listen: Einkaufskategorie und Hauptnährstoff.
// Bewusst ohne Import der Lebensmitteldatenbank, damit der Planer sie nicht mitladen muss.

/** Einkaufskategorien in Anzeigereihenfolge: [Schlüssel, Überschrift, Icon, Gruppen aus tools/foods_src.py]. */
export const CATS = [
  ['gemuese', 'Gemüse, Salat und Pilze', 'leaf', ['gemuese', 'blatt', 'pilze', 'knolle']],
  ['saettig', 'Hülsenfrüchte, Getreide, Soja und Suppen', 'pot', ['huelsen', 'getreide', 'soja', 'knusper', 'suppe']],
  ['nuss', 'Nüsse, Saaten und Oliven', 'nut', ['nuss', 'fettfrucht']],
  ['oel', 'Öle', 'oil', ['fett']],
  ['obst', 'Obst', 'apple', ['obst']],
  ['wuerze', 'Kräuter und Würzen', 'herb', ['kraeuter', 'wuerze']],
  ['trinken', 'Getränke', 'cup', ['getraenk']],
  ['tauschen', 'Lieber tauschen', 'ban', ['tier', 'milch', 'suess', 'weissmehl', 'drink', 'eiweiss', 'fertig']],
];
const CAT_OF_GROUP = Object.fromEntries(CATS.flatMap(([k, , , gs]) => gs.map((g) => [g, k])));

/** Kategorie-Schlüssel eines Lebensmittels (Objekt mit group). */
export const catOf = (f) => CAT_OF_GROUP[f?.group] || 'gemuese';

/** Sortiert eine Liste in Kategorien. get(item) liefert das Lebensmittel-Objekt. Leere Kategorien fallen weg. */
export function groupByCat(items, get) {
  const out = CATS.map(([key, label, icon]) => ({ key, label, icon, items: [] }));
  const idx = Object.fromEntries(out.map((c, i) => [c.key, i]));
  for (const it of items) out[idx[catOf(get(it))]].items.push(it);
  return out.filter((c) => c.items.length);
}

export const MACROS = { carbs: 'Kohlenhydrate', protein: 'Eiweiß', fat: 'Fett' };

/**
 * Hauptnährstoff eines Lebensmittels: der Makronährstoff mit dem größten Anteil an den Kalorien.
 * n = [kcal, Eiweiß, Fett, Kohlenhydrate, ...] je 100 g. Kräuter, Würzen und fast kalorienfreie
 * Lebensmittel bekommen kein Symbol, weil sie in üblichen Mengen kaum etwas beitragen.
 * Rückgabe: { key, share } oder null.
 */
export function macroOf(f) {
  if (!f?.n || ['kraeuter', 'wuerze'].includes(f.group)) return null;
  const [, p, fa, c] = f.n;
  const e = { carbs: c * 4, protein: p * 4, fat: fa * 9 };
  const t = e.carbs + e.protein + e.fat;
  if (t < 10) return null;
  const [key, v] = Object.entries(e).sort((a, b) => b[1] - a[1])[0];
  return { key, share: Math.round((v / t) * 100) };
}
