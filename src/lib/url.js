const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';

/** Pfad relativ zur Startseite, funktioniert mit und ohne base. */
export const u = (path = '') => base + String(path).replace(/^\//, '');

/**
 * WebP-Quellen zu einem Foto aus public/img (erzeugt von scripts/bilder.mjs nach dem Build).
 * Rezeptfotos gibt es in 400 und 900 px, große Fotos in 800 und 1800 px.
 */
export const webp = (path) => {
  if (import.meta.env.DEV) return '';
  const stem = u(path).replace(/\.jpg$/, '');
  const ws = /(rezepte|menschen|rechner)\//.test(path) ? [400, 900] : [800, 1800];
  return ws.map((w) => `${stem}-${w}.webp ${w}w`).join(', ');
};
/** Kleines Vorschaubild (400 px WebP) für Listen im Planer und Rechner. */
export const thumb = (base, image) => `${base}img/rezepte/${image}${import.meta.env.DEV ? '.jpg' : '-400.webp'}`;
