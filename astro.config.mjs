import { defineConfig } from 'astro/config';

// GitHub Pages: https://culinarylust.github.io/Scheinfasten-mega-lecker/
// Bei eigener Domain: site anpassen und base auf '/' setzen.
export default defineConfig({
  site: 'https://culinarylust.github.io',
  base: '/Scheinfasten-mega-lecker/',
  trailingSlash: 'ignore',
});
