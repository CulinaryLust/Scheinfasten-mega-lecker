// Baut aus dist/ einen Ordner dist-weiterleitung/ für GitHub Pages: Jede Seite der alten Adresse
// culinarylust.github.io/Scheinfasten-mega-lecker/... leitet auf dieselbe Seite der eigenen Domain weiter.
// So gehen alte Links und Pins nicht verloren. Läuft nur, wenn DOMAIN gesetzt ist.
import { readdirSync, mkdirSync, writeFileSync, statSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { DOMAIN } from '../src/data/site.js';

if (!DOMAIN) { console.log('weiterleitung: keine DOMAIN, nichts zu tun'); process.exit(0); }
const src = 'dist', out = 'dist-weiterleitung';
const ziel = `https://${DOMAIN}/`;
const seite = (url) => `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Umgezogen</title>
<link rel="canonical" href="${url}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=${url}"></head>
<body><p>Diese Seite ist umgezogen: <a href="${url}">${url}</a></p></body></html>\n`;

let n = 0;
const walk = (d) => readdirSync(d).forEach((f) => {
  const p = join(d, f);
  if (statSync(p).isDirectory()) return walk(p);
  if (!f.endsWith('.html')) return;
  const rel = relative(src, p).replace(/\\/g, '/');
  const pfad = rel === '404.html' ? '' : rel.replace(/index\.html$/, '');
  mkdirSync(dirname(join(out, rel)), { recursive: true });
  writeFileSync(join(out, rel), seite(ziel + pfad));
  n++;
});
walk(src);
// Unbekannte alte Adressen: 404-Seite leitet per Skript auf denselben Pfad der Domain
writeFileSync(join(out, '404.html'), `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Umgezogen</title><meta name="robots" content="noindex">
<script>location.replace(${JSON.stringify(ziel)} + location.pathname.replace(/^\\/Scheinfasten-mega-lecker\\/?/i, '') + location.search + location.hash);</script>
</head><body><p>Diese Seite ist umgezogen: <a href="${ziel}">${ziel}</a></p></body></html>\n`);
console.log(`weiterleitung: ${n} Seiten leiten auf ${ziel} weiter`);
