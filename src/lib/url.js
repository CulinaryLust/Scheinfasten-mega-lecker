const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';

/** Version aller Fotos (aus astro.config.mjs); hängt an Bildadressen, damit ersetzte Fotos sofort neu geladen werden. */
const V = import.meta.env.IMG_V || '';
const ver = (url) => (V ? `${url}?v=${V}` : url);

/** Pfad relativ zur Startseite, funktioniert mit und ohne base. Bilder unter img/ bekommen die Version angehängt. */
export const u = (path = '') => {
  const url = base + String(path).replace(/^\//, '');
  return /^\/?img\/.*\.(jpe?g|png|webp)$/.test(String(path)) ? ver(url) : url;
};

/**
 * WebP-Quellen zu einem Foto aus public/img (erzeugt von scripts/bilder.mjs nach dem Build).
 * Rezeptfotos gibt es in 400 und 900 px, große Fotos in 800 und 1800 px.
 */
export const webp = (path) => {
  if (import.meta.env.DEV) return '';
  const stem = (base + String(path).replace(/^\//, '')).replace(/\.jpg$/, '');
  const ws = /(rezepte|menschen|rechner|diy)\//.test(path) ? [400, 900] : [800, 1800];
  return ws.map((w) => `${ver(`${stem}-${w}.webp`)} ${w}w`).join(', ');
};
/** Kleines Vorschaubild (400 px WebP) für Listen im Planer und Rechner. */
export const thumb = (base, image) => ver(`${base}img/rezepte/${image}${import.meta.env.DEV ? '.jpg' : '-400.webp'}`);
/** Wie thumb, aber für einen anderen Bildordner (z. B. diy). */
export const thumbIn = (base, dir, image) => ver(`${base}img/${dir}/${image}${import.meta.env.DEV ? '.jpg' : '-400.webp'}`);
