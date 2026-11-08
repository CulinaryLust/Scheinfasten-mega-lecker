// robots.txt. Wirkt nur an der Wurzel einer Domain, also erst mit eigener Domain (src/data/site.js).
export function GET({ site }) {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, '/');
  const body = `User-agent: *\nAllow: /\n\nSitemap: ${new URL(base + 'sitemap.xml', site).href}\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
