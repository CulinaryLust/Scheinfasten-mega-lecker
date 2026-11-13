import { defineConfig } from 'astro/config';
import { writeFileSync, readdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { DOMAIN, SITE, BASE } from './src/data/site.js';

// Adresse und Pfad kommen aus src/data/site.js. Bei eigener Domain schreibt der Build die .htaccess für ALL-INKL (Apache):
// HTTPS erzwingen, www auf die Domain ohne www umleiten, eigene 404-Seite, Cache (Bilder 7 Tage; ersetzte Fotos lädt der Browser trotzdem sofort neu, weil jede Bildadresse ?v=<Version> trägt).
const htaccess = (d) => `# Wird beim Build aus src/data/site.js erzeugt, nicht von Hand ändern.
ErrorDocument 404 /404.html
Options -Indexes
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^${d.replace(/\./g, '\\.')}$ [NC]
RewriteRule ^ https://${d}%{REQUEST_URI} [L,R=301]
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 7 days"
  ExpiresByType image/jpeg "access plus 7 days"
  ExpiresByType image/png "access plus 7 days"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/html "access plus 0 seconds"
</IfModule>
`;
const hosting = {
  name: 'hosting',
  hooks: {
    'astro:build:done': ({ dir }) => { if (DOMAIN) writeFileSync(new URL('.htaccess', dir), htaccess(DOMAIN)); },
  },
};

// Bildversion: Prüfsumme über alle Fotos in public/img. Ändert sich ein Foto, ändert sich die Adresse (?v=…),
// und Browser laden es neu statt eine alte Fassung aus dem Zwischenspeicher zu zeigen.
const imgVersion = (() => {
  const h = createHash('md5');
  const walk = (d) => { for (const e of readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) { const p = join(d, e.name); if (e.isDirectory()) walk(p); else { h.update(p); h.update(readFileSync(p)); } } };
  walk(new URL('./public/img', import.meta.url).pathname);
  return h.digest('hex').slice(0, 8);
})();

export default defineConfig({
  vite: { define: { 'import.meta.env.IMG_V': JSON.stringify(imgVersion) } },
  site: SITE,
  base: BASE,
  trailingSlash: 'ignore',
  integrations: [hosting],
});
