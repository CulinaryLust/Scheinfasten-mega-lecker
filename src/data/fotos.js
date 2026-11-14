// Fotopools für die wechselnden Fotos (Rotator, FotoStreifen). Alle Fotos von Unsplash, IDs in tools/images.txt.
// Jede Seite bekommt eine breite Auswahl passender Fotos; das Startfoto wählt der Rotator zufällig.
const f = (dir, names) => names.map((n) => `img/${dir}${n}.jpg`);

export const POOLS = {
  // Großformat (1800 px) für den Hintergrund der Startseite
  hero: [...f('', ['hero']), ...f('hero/', ['gemueseplatte', 'gemuesesuppe', 'schneidebrett', 'gemuese-brett', 'wurzelgemuese']), ...f('', ['karotten', 'oel'])],
  essen: [...f('', ['hero']), ...f('hero/', ['gemueseplatte', 'gemuesesuppe', 'schneidebrett', 'gemuese-brett', 'wurzelgemuese']), ...f('diy/', ['ofen', 'pfanne', 'salat', 'snack', 'suppe']), ...f('rechner/', ['gemuese', 'kraeuter'])],
  rezepte: f('rezepte/', ['aubergine', 'baba-ganoush', 'baerlauchsuppe', 'blumenkohl', 'bowl', 'briam', 'chiapudding', 'curry', 'dal', 'escalivada', 'gazpacho', 'harissa-karotten', 'kaltschale', 'karottensuppe', 'kichererbsen', 'kuerbissalat', 'kuerbissuppe', 'minestrone', 'miso-aubergine', 'muhammara', 'ofengemuese', 'pakchoi', 'pilzpfanne', 'ratatouille', 'roesti', 'rote-bete-suppe', 'salat-bunt', 'spargel', 'suesskartoffel', 'tajine', 'wirsing', 'zoodles']),
  menschen: [...f('menschen/', ['freunde-tisch', 'kueche-zusammen', 'genuss-kuechentisch', 'lachen-essen', 'paar-kocht', 'schale-gemuese']), ...f('szenen/', ['runde-salat', 'schalen-reichen', 'grosser-tisch', 'anstossen', 'freundinnen-teller', 'familie-essen', 'familie-tisch', 'abendessen', 'mama-tochter', 'oma-enkelin-salat', 'oma-enkelin', 'salat-lachen', 'picknick'])],
  markt: [...f('', ['markt', 'karotten']), ...f('szenen/', ['markt-stand', 'markt-paprika', 'markt-kuerbis', 'markt-menge', 'markt-platz', 'markt-fahrrad', 'korb-gemuese', 'kuerbisse', 'zutaten'])],
  kueche: [...f('szenen/', ['kochen-kueche', 'paar-kueche', 'blaue-kueche', 'spargel-kochen', 'salat-schuessel', 'zutaten']), ...f('menschen/', ['paar-kocht', 'kueche-zusammen']), ...f('', ['oel'])],
  draussen: f('szenen/', ['waldweg', 'picknick', 'markt-fahrrad']),
};

/**
 * Fotoliste für eine Seite: das erste Foto mit Alt-Text (bleibt beim Bauen der Seite vorn),
 * danach passende Fotos aus den genannten Pools, ohne Doppelte, höchstens max Stück.
 * Jedes n-te Foto eines Pools (step) sorgt dafür, dass Seiten mit demselben Pool verschiedene Fotos zeigen.
 */
export function fotos(first, pools, { max = 12, step = 1, offset = 0 } = {}) {
  const out = [first];
  const seen = new Set([first.src]);
  const lists = pools.map((p) => POOLS[p] || []);
  // Pools abwechselnd mischen, damit nicht erst alle Fotos einer Sorte kommen
  for (let i = 0; out.length < max && lists.some((l) => i * step + offset < l.length); i++) {
    for (const l of lists) {
      const src = l[(i * step + offset) % l.length];
      if (i * step + offset < l.length && src && !seen.has(src) && out.length < max) { out.push({ src, alt: '' }); seen.add(src); }
    }
  }
  return out;
}
