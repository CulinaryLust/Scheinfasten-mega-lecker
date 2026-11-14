// Prüft die Amazon-Produkte in src/data/affiliate.js. Läuft bei jedem Build (ohne Netz):
// Tracking-ID gesetzt, jede ASIN gültig und eindeutig, Symbolbild vorhanden, Gruppe bekannt.
// Mit --live (monatlich in .github/workflows/wartung.yml): ruft jede Produktseite einmal ab.
// 404 = Produkt gelöscht, dann schlägt der Lauf fehl und GitHub schickt eine E-Mail.
// Amazon blockt automatische Abrufe oft (503). Solche Produkte werden nur gelistet, nicht als Fehler gezählt.
import { access } from 'node:fs/promises';
import { AMAZON_TAG, PRODUCTS, GROUPS, PRODUCTS_CHECKED } from '../src/data/affiliate.js';

const live = process.argv.includes('--live');
const IMG = new URL('../public/img/produkte/', import.meta.url).pathname;
const fehler = [];
if (!/^[a-z0-9-]+-21$/.test(AMAZON_TAG)) fehler.push(`AMAZON_TAG „${AMAZON_TAG}“ sieht nicht wie eine Amazon.de-Tracking-ID aus (…-21).`);
const gruppen = new Set(GROUPS.map((g) => g.key));
const asins = new Map();
for (const [key, p] of Object.entries(PRODUCTS)) {
  if (!gruppen.has(p.group)) fehler.push(`${key}: unbekannte Gruppe „${p.group}“.`);
  if (!p.title || !p.why) fehler.push(`${key}: title oder why fehlt.`);
  if (p.asin) {
    if (!/^[A-Z0-9]{10}$/.test(p.asin)) fehler.push(`${key}: ASIN „${p.asin}“ ist ungültig (10 Zeichen, A-Z und 0-9).`);
    if (asins.has(p.asin)) fehler.push(`${key}: ASIN doppelt (auch bei ${asins.get(p.asin)}).`);
    asins.set(p.asin, key);
  } else if (!p.search) fehler.push(`${key}: weder asin noch search.`);
  try { await access(IMG + (p.img || key) + '.jpg'); } catch { fehler.push(`${key}: Bild img/produkte/${p.img || key}.jpg fehlt.`); }
}
console.log(`partner: ${Object.keys(PRODUCTS).length} Produkte, ${asins.size} mit ASIN, Stand ${PRODUCTS_CHECKED}, ${fehler.length} Fehler`);
fehler.forEach((f) => console.log('  ✗ ' + f));
if (fehler.length) process.exitCode = 1;

if (live) {
  const weg = [], unklar = [], aus = [];
  for (const [key, p] of Object.entries(PRODUCTS)) {
    if (!p.asin) continue;
    const url = `https://www.amazon.de/dp/${p.asin}`;
    let status = 0, text = '';
    try {
      const r = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(20000), headers: { 'user-agent': 'einfach-lecker-fasten.de Linkpruefung', 'accept-language': 'de-DE' } });
      status = r.status; if (status === 200) text = await r.text();
    } catch { status = 0; }
    if (status === 404 || status === 410) weg.push(`${key} (${p.title}): ${url}`);
    else if (status === 200 && /Derzeit nicht verfügbar|Currently unavailable/i.test(text)) aus.push(`${key} (${p.title}): ${url}`);
    else if (status !== 200) unklar.push(`${key}: ${status || 'keine Antwort'}`);
    console.log(`  ${status === 404 || status === 410 ? '✗' : status === 200 ? '✓' : '?'} ${status || '-'} ${key}`);
    await new Promise((r) => setTimeout(r, 1500));
  }
  if (aus.length) console.log('\nDerzeit nicht lieferbar (bitte Ersatz wählen, wenn das länger anhält):\n' + aus.map((a) => '- ' + a).join('\n'));
  if (unklar.length) console.log(`\n${unklar.length} Produktseiten hat Amazon für die automatische Prüfung blockiert. Kein Fehler, nur nicht prüfbar.`);
  if (weg.length) { console.log('\nNicht mehr bei Amazon (Produkt in src/data/affiliate.js ersetzen):\n' + weg.map((w) => '- ' + w).join('\n')); process.exitCode = 1; }
}
