import { defineConfig } from 'astro/config';
import { writeFileSync } from 'node:fs';
import { DOMAIN, SITE, BASE } from './src/data/site.js';

// Adresse und Pfad kommen aus src/data/site.js. Bei eigener Domain schreibt der Build die .htaccess für ALL-INKL (Apache):
// HTTPS erzwingen, www auf die Domain ohne www umleiten, eigene 404-Seite, Cache (Bilder 7 Tage, weil ihre Namen gleich bleiben).
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

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: 'ignore',
  integrations: [hosting],
});
