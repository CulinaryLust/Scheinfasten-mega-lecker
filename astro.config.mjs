import { defineConfig } from 'astro/config';
import { writeFileSync } from 'node:fs';
import { DOMAIN, SITE, BASE } from './src/data/site.js';

// Adresse und Pfad kommen aus src/data/site.js. Bei eigener Domain schreibt der Build die CNAME-Datei für GitHub Pages.
const cname = {
  name: 'cname',
  hooks: {
    'astro:build:done': ({ dir }) => { if (DOMAIN) writeFileSync(new URL('CNAME', dir), DOMAIN + '\n'); },
  },
};

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: 'ignore',
  integrations: [cname],
});
