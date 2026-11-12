// Sitemap für Google und Bing. Impressum und Datenschutz fehlen absichtlich (noindex).
import { RECIPES } from '../lib/nutrition.js';
import { ARTIKEL } from '../data/ratgeber.js';

const STATIC = ['', 'planer/', 'rechner/', 'rezepte/', 'wissen/', 'ausstattung/', 'prolon-oder-selbst-kochen/', 'fuer-wen-nicht/', 'krebs/', 'transparenz/', 'so-arbeiten-wir/', 'ratgeber/'];

export function GET({ site }) {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, '/');
  const paths = [...STATIC, ...ARTIKEL.map((a) => `ratgeber/${a.slug}/`), ...RECIPES.filter((r) => r.slot !== 'side').map((r) => `rezepte/${r.slug}/`)];
  const urls = paths.map((p) => `  <url><loc>${new URL(base + p, site).href}</loc></url>`).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
