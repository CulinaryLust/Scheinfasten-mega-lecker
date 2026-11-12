// Prüft nach dem Build jeden internen Link und jedes Bild in dist/: Zeigt etwas ins Leere, bricht der Build ab.
// Mit --extern zusätzlich: prüft alle externen Adressen (Quellen, Partner) und meldet tote Links (404, 410, 5xx, nicht erreichbar).
// Antworten wie 403 oder 429 gelten als erreichbar, weil viele Seiten automatische Abfragen blockieren.
import { readdir, readFile, access } from 'node:fs/promises';
import { join } from 'node:path';
import { BASE, SITE } from '../src/data/site.js';

const DIST = new URL('../dist/', import.meta.url).pathname;
const extern = process.argv.includes('--extern');

async function* files(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* files(p); else if (/\.(html|xml)$/.test(e.name)) yield p;
  }
}
const exists = (p) => access(p).then(() => true, () => false);

const bad = [], ext = new Map();
let n = 0;
for await (const file of files(DIST)) {
  const html = await readFile(file, 'utf8');
  const refs = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1])
    .concat([...html.matchAll(/srcset="([^"]+)"/g)].flatMap((m) => m[1].split(',').map((s) => s.trim().split(/\s+/)[0])));
  for (const raw of refs) {
    const ref = raw.replace(/&amp;/g, '&');
    if (/^https?:\/\//.test(ref)) { if (!ext.has(ref)) ext.set(ref, file.slice(DIST.length)); continue; }
    if (!ref.startsWith(BASE)) continue; // mailto:, #anker, data:, //cdn
    n++;
    const path = decodeURIComponent(ref.slice(BASE.length).split(/[?#]/)[0]);
    const target = join(DIST, path);
    if (!(await exists(path === '' || path.endsWith('/') ? join(target, 'index.html') : target))) bad.push(`${file.slice(DIST.length)} → ${ref}`);
  }
}
console.log(`links: ${n} interne Verweise geprüft, ${bad.length} defekt`);
bad.forEach((b) => console.log('  ✗ ' + b));

if (extern) {
  const dead = [];
  // Eigene Adressen deckt die interne Prüfung ab. Amazon und Pinterest-Teilen-Links blockieren Abfragen: nicht prüfen
  const urls = [...ext.keys()].filter((x) => !/amazon\.de|pinterest\.com\/pin\/create|schema\.org|w3\.org|sitemaps\.org|search\.yahoo\.com/.test(x) && !x.startsWith(SITE));
  for (const url of urls) {
    let status = 0;
    for (let i = 0; i < 2 && !status; i++) {
      try { const r = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(20000), headers: { 'user-agent': 'Mozilla/5.0 (link check)' } }); status = r.status; } catch { status = 0; }
    }
    const tot = status === 0 || status === 404 || status === 410 || status >= 500;
    console.log(`  ${tot ? '✗' : '✓'} ${status || 'keine Antwort'} ${url}`);
    if (tot) dead.push(`${url} (${status || 'keine Antwort'}, verlinkt in ${ext.get(url)})`);
  }
  console.log(`links: ${urls.length} externe Adressen geprüft, ${dead.length} tot`);
  if (dead.length) { console.log('\nTote externe Links:\n' + dead.map((d) => '- ' + d).join('\n')); process.exitCode = 1; }
}
if (bad.length) process.exitCode = 1;
