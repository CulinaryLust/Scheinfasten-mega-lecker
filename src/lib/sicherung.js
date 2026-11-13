// „Stand sichern“: packt alles, was Planer und Rechner im Browser gespeichert haben, in einen Link.
// Die Daten stehen nur im Teil hinter „#“. Diesen Teil schickt der Browser nie an einen Server,
// auch nicht an GitHub Pages. Kein Konto, keine Datenbank.

/** Schlüssel im localStorage, die mitgenommen werden. */
export const KEYS = ['smlTagebuch', 'smlProfil', 'smlPlaner', 'smlRechner'];
export const PARAM = 'stand';

const b64url = (bytes) => {
  let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
};
const unb64url = (str) => {
  const s = atob(str.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((str.length + 3) % 4));
  return Uint8Array.from(s, (c) => c.charCodeAt(0));
};
const canZip = () => typeof CompressionStream !== 'undefined' && typeof DecompressionStream !== 'undefined';
async function pipe(bytes, stream) {
  const out = new Response(new Blob([bytes]).stream().pipeThrough(stream));
  return new Uint8Array(await out.arrayBuffer());
}

/** Liest die gespeicherten Daten aus einem Storage-Objekt (localStorage oder Ersatz in Tests). */
export function collect(storage) {
  const data = {};
  for (const k of KEYS) {
    try { const v = storage.getItem(k); if (v) data[k] = JSON.parse(v); } catch {}
  }
  return data;
}

/** Verpackt die Daten als kurzen Text: „z.“ = komprimiert, „j.“ = nur kodiert (ältere Browser). */
export async function pack(data) {
  const bytes = new TextEncoder().encode(JSON.stringify(data));
  if (canZip()) return 'z.' + b64url(await pipe(bytes, new CompressionStream('deflate-raw')));
  return 'j.' + b64url(bytes);
}

/** Packt den Text wieder aus. Wirft einen Fehler, wenn der Link beschädigt ist. */
export async function unpack(text) {
  const [kind, body] = [text.slice(0, 2), text.slice(2)];
  let bytes = unb64url(body);
  if (kind === 'z.') {
    if (!canZip()) throw new Error('Dieser Browser kann den Link nicht öffnen.');
    bytes = await pipe(bytes, new DecompressionStream('deflate-raw'));
  } else if (kind !== 'j.') throw new Error('Unbekanntes Format');
  const data = JSON.parse(new TextDecoder().decode(bytes));
  if (!data || typeof data !== 'object') throw new Error('Leerer Stand');
  // Nur bekannte Schlüssel übernehmen
  return Object.fromEntries(Object.entries(data).filter(([k]) => KEYS.includes(k)));
}

/** Schreibt einen ausgepackten Stand in den Speicher. Ersetzt die bisherigen Daten dieser Schlüssel. */
export function restore(storage, data) {
  for (const k of KEYS) {
    if (data[k] != null) storage.setItem(k, JSON.stringify(data[k]));
    else storage.removeItem(k);
  }
}

/** Kurze Zusammenfassung für die Rückfrage vor dem Übernehmen. */
export function summary(data) {
  const logs = data.smlTagebuch?.logs || {};
  const days = Object.entries(logs).filter(([, es]) => es?.length).map(([d]) => d).sort();
  const parts = [];
  if (days.length) parts.push(`Einträge für Tag ${days.join(', ')}`);
  if (data.smlPlaner?.inputs?.start) parts.push(`Plan mit Start am ${new Date(data.smlPlaner.inputs.start + 'T12:00:00').toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' })}`);
  if (data.smlRechner?.picks?.length) parts.push(`${data.smlRechner.picks.length} Lebensmittel im Kühlschrank`);
  return parts.join(', ') || 'Deine Körperdaten';
}
