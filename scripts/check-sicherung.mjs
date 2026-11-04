// Prüft „Stand sichern“ (Link hin und zurück) und das Datum der Zyklus-Erinnerung.
import { collect, pack, unpack, restore, summary } from '../src/lib/sicherung.js';
import { nextCycle, formatDate } from '../src/lib/erinnerung.js';

let failed = 0;
const must = (c, m) => { if (!c) { failed++; console.log('FEHLER:', m); } };
const mem = (init = {}) => { const m = new Map(Object.entries(init)); return { getItem: (k) => m.get(k) ?? null, setItem: (k, v) => m.set(k, String(v)), removeItem: (k) => m.delete(k), m }; };

const logs = { 1: [{ type: 'recipe', slug: 'minestrone', qty: 1, unit: 'portion' }, { type: 'food', name: 'Walnusskerne', qty: 15, unit: 'g' }], 2: [{ type: 'food', name: 'Kürbis', qty: 1, unit: 'piece' }] };
const a = mem({ smlTagebuch: JSON.stringify({ logs }), smlProfil: JSON.stringify({ inputs: { sex: 'w', age: '42', h: '168', w: '70', pal: '1.6' }, day: '2' }), smlPlaner: JSON.stringify({ inputs: { start: '2026-11-02', cyc: '3', gap: '3' } }), fremd: 'x' });
const data = collect(a);
must(!('fremd' in data), 'Fremder Schlüssel mitgenommen');
const text = await pack(data);
console.log('Linklänge:', text.length, 'Zeichen');
must(text.startsWith('z.') && text.length < 1200, `Link zu lang (${text.length})`);
must(/^[A-Za-z0-9._-]+$/.test(text), 'Link enthält Sonderzeichen');
const back = await unpack(text);
must(JSON.stringify(back) === JSON.stringify(data), 'Rundreise verändert Daten');
const b = mem({ smlRechner: '{"picks":[]}' });
restore(b, back);
must(b.getItem('smlTagebuch') === a.getItem('smlTagebuch') && b.getItem('smlRechner') === null, 'Übernahme');
must(summary(back).includes('Tag 1, 2') && summary(back).includes('02.11.2026'), `Zusammenfassung: ${summary(back)}`);
let threw = false; try { await unpack(text.slice(0, 20)); } catch { threw = true; }
must(threw, 'Beschädigter Link nicht erkannt');
// Nächster Durchgang
const inp = { start: '2026-11-02', cyc: '3', gap: '3' };
must(nextCycle(inp, new Date('2026-11-04')) === '2027-02-02', `nächster Zyklus ${nextCycle(inp, new Date('2026-11-04'))}`);
must(nextCycle(inp, new Date('2026-11-01')) === '2026-11-02', 'Start in der Zukunft');
must(nextCycle(inp, new Date('2027-06-01')) === null, 'Nach dem letzten Durchgang');
must(formatDate('2027-02-02') === '02-02-2027', 'Datumsformat');
console.log(failed ? `${failed} Fehler` : 'Alles ok');
process.exit(failed ? 1 : 0);
