// Erzeugt nach dem Build zu jedem Rezept eine Pinterest-Grafik im Hochformat (1000 × 1500 px) in dist/pins/.
// Foto oben, darunter Titel, Kalorien und der Name der Seite. Der Feed /pins.xml verweist auf diese Bilder,
// Pinterest kann daraus automatisch Pins erstellen (README, Abschnitt „Pinterest automatisch“).
import { mkdir, readFile } from 'node:fs/promises';
import sharp from 'sharp';
import { nutrition } from '../src/lib/nutrition.js';

const RECIPES = JSON.parse(await readFile(new URL('../src/data/recipes.json', import.meta.url)));
const DIST = new URL('../dist/', import.meta.url).pathname;
// Young Serif (SIL Open Font License), als TTF aus @fontsource umgewandelt, damit die Grafiken auf jedem Rechner gleich aussehen
const FONT = new URL('../tools/fonts/YoungSerif-latin.ttf', import.meta.url).pathname;
const W = 1000, H = 1500, PHOTO = 940, PAD = 70;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

async function text(markup, width, opts = {}) {
  return sharp({ text: { text: markup, font: 'Young Serif', fontfile: FONT, width, rgba: true, dpi: 72, wrap: 'word', ...opts } }).png().toBuffer({ resolveWithObject: true });
}

await mkdir(DIST + 'pins', { recursive: true });
let n = 0;
for (const r of RECIPES.filter((x) => x.slot !== 'side')) {
  const kcal = Math.round(nutrition(r).kcal);
  const photo = await sharp(`${DIST}img/rezepte/${r.image}.jpg`).resize(W, PHOTO, { fit: 'cover' }).toBuffer();
  // Titel so groß wie möglich, aber höchstens 4 Zeilen (ca. 300 px)
  let title;
  for (const size of [78, 70, 62, 54, 48]) {
    title = await text(`<span foreground="#1e2a1c" size="${size}pt">${esc(r.title)}</span>`, W - 2 * PAD, { spacing: 6 });
    if (title.info.height <= 300) break;
  }
  const meta = await text(`<span foreground="#cf4520" size="34pt">${kcal} kcal · ${r.minutes} Min. · 100 % pflanzlich</span>`, W - 2 * PAD);
  const brand = await text(`<span foreground="#ffffff" size="32pt">Scheinfasten · einfach lecker fasten</span>`, W - 2 * PAD);
  const kick = await text(`<span foreground="#5e6b5a" size="28pt">Scheinfasten-Rezept nach Longos Werten berechnet</span>`, W - 2 * PAD);
  const bar = 96;
  const top = PHOTO + 44;
  await sharp({ create: { width: W, height: H, channels: 3, background: '#fffdf8' } })
    .composite([
      { input: photo, left: 0, top: 0 },
      { input: kick.data, left: PAD, top },
      { input: title.data, left: PAD, top: top + kick.info.height + 22 },
      { input: meta.data, left: PAD, top: H - bar - meta.info.height - 34 },
      { input: { create: { width: W, height: bar, channels: 3, background: '#2a5a1f' } }, left: 0, top: H - bar },
      { input: brand.data, left: PAD, top: H - bar + Math.round((bar - brand.info.height) / 2) },
    ])
    .jpeg({ quality: 82, mozjpeg: true })
    .toFile(`${DIST}pins/${r.slug}.jpg`);
  n++;
}
console.log(`pins: ${n} Pinterest-Grafiken erzeugt`);
