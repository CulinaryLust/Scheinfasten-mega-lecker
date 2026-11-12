// Zeigt, was vor dem offiziellen Start noch fehlt. Bricht nichts ab, läuft nicht im Deploy.
// Aufruf: npm run check:launch
import { DOMAIN } from '../src/data/site.js';
import { fehlend } from '../src/data/betreiber.js';
import { AMAZON_TAG, PROLON_LINK, ADS_ENABLED } from '../src/data/affiliate.js';
import { NEWSLETTER_ENABLED, NEWSLETTER_ACTION } from '../src/data/newsletter.js';
import { GOATCOUNTER_CODE } from '../src/data/statistik.js';

const rows = [
  ['Eigene Domain (src/data/site.js)', !!DOMAIN, DOMAIN || 'noch github.io, robots.txt wirkt dort nicht'],
  ['Impressum und Datenschutz (src/data/betreiber.js)', fehlend().length === 0, fehlend().length ? 'fehlt: ' + fehlend().join(', ') : 'vollständig'],
  ['Amazon-Tracking-ID (src/data/affiliate.js)', !!AMAZON_TAG, AMAZON_TAG || 'leer, Klicks bringen keine Provision'],
  ['ProLon-Partnerlink (src/data/affiliate.js)', !/^https:\/\/prolon\.eu\/de\/?$/.test(PROLON_LINK), PROLON_LINK],
  ['Zyklus-Erinnerung (src/data/newsletter.js)', NEWSLETTER_ENABLED && !!NEWSLETTER_ACTION, NEWSLETTER_ENABLED ? 'an' : 'aus, Brevo-Formular eintragen (README)'],
  ['Statistik ohne Cookies (src/data/statistik.js)', !!GOATCOUNTER_CODE, GOATCOUNTER_CODE || 'leer, keine Besucherzahlen'],
  ['Werbeanzeigen bleiben aus', !ADS_ENABLED, ADS_ENABLED ? 'AN, Einwilligungsbanner nötig!' : 'aus'],
];
let open = 0;
for (const [label, ok, info] of rows) { if (!ok) open++; console.log(`${ok ? '✓' : '○'} ${label}: ${info}`); }
console.log(open ? `\n${open} Punkt(e) offen.` : '\nAlles bereit für den Start.');
