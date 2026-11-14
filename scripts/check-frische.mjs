// Meldet Angaben, die veralten können: ProLon-Preis älter als 90 Tage, Ratgeber-Artikel älter als ein Jahr.
// Läuft einmal im Monat automatisch (.github/workflows/wartung.yml). Schlägt etwas an, schickt GitHub eine E-Mail.
import { PROLON_CHECKED, PROLON_PRICE, PRODUCTS_CHECKED } from '../src/data/affiliate.js';
import { ARTIKEL } from '../src/data/ratgeber.js';

const tage = (d) => Math.floor((Date.now() - d.getTime()) / 86400000);
const offen = [];
const [t, m, j] = PROLON_CHECKED.split('.');
const p = tage(new Date(`${j}-${m}-${t}T12:00:00Z`));
if (p > 90) offen.push(`ProLon-Preis (${PROLON_PRICE} €) zuletzt vor ${p} Tagen geprüft: auf prolon.eu nachsehen und PROLON_PRICE und PROLON_CHECKED in src/data/affiliate.js anpassen.`);
const [pt, pm, pj] = PRODUCTS_CHECKED.split('.');
const pp = tage(new Date(`${pj}-${pm}-${pt}T12:00:00Z`));
if (pp > 180) offen.push(`Amazon-Produkte zuletzt vor ${pp} Tagen durchgesehen: neue Testergebnisse (ÖKO-TEST, Stiftung Warentest) prüfen, PRODUCTS in src/data/affiliate.js anpassen und PRODUCTS_CHECKED setzen.`);
for (const a of ARTIKEL) {
  const d = tage(new Date(`${a.stand}T12:00:00Z`));
  if (d > 365) offen.push(`Ratgeber „${a.title}“ zuletzt vor ${d} Tagen geprüft: Inhalt durchsehen und „stand“ in src/data/ratgeber.js anpassen.`);
}
console.log(offen.length ? 'Bitte aktualisieren:\n' + offen.map((o) => '- ' + o).join('\n') : 'frische: alles aktuell');
if (offen.length) process.exitCode = 1;
