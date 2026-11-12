// Erzeugt nach dem Build WebP-Varianten aller Fotos in dist/img (kleiner, schneller als JPG).
// Rezeptfotos (900 px): 400 und 900 px breit. Große Fotos (1800 px): 800 und 1800 px breit.
// Die JPGs bleiben als Rückfall für alte Browser. Läuft automatisch mit `npm run build`.
import { readdir } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const ROOT = new URL('../dist/img/', import.meta.url).pathname;
export const BREITEN = { rezepte: [400, 900], gross: [800, 1800] };

async function* jpgs(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* jpgs(p);
    else if (e.name.endsWith('.jpg')) yield p;
  }
}

let n = 0;
for await (const file of jpgs(ROOT)) {
  const breiten = file.includes('/rezepte/') ? BREITEN.rezepte : BREITEN.gross;
  for (const w of breiten) {
    await sharp(file).resize({ width: w, withoutEnlargement: true }).webp({ quality: 72 }).toFile(file.replace(/\.jpg$/, `-${w}.webp`));
    n++;
  }
}
console.log(`bilder: ${n} WebP-Dateien erzeugt`);
