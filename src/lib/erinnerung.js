// Start des nächsten Fastendurchgangs aus den Planer-Eingaben (start, cyc, gap), für die Zyklus-Erinnerung.

/** ISO-Datum (JJJJ-MM-TT) des nächsten Durchgangs ab heute, sonst null. */
export function nextCycle(inputs, today = new Date()) {
  if (!inputs?.start) return null;
  const s = new Date(`${inputs.start}T12:00:00`);
  if (Number.isNaN(s.getTime())) return null;
  const t = new Date(today); t.setHours(12, 0, 0, 0);
  const cyc = Math.max(1, +inputs.cyc || 1), gap = Math.max(1, +inputs.gap || 1);
  for (let c = 0; c < cyc; c++) {
    const d = new Date(s); d.setMonth(d.getMonth() + c * gap);
    if (d.getTime() >= t.getTime()) return d.toISOString().slice(0, 10);
  }
  return null;
}

/** Wandelt JJJJ-MM-TT in das Format des Brevo-Formulars. */
export function formatDate(iso, fmt = 'DD-MM-YYYY') {
  const [y, m, d] = iso.split('-');
  return fmt.replace('YYYY', y).replace('MM', m).replace('DD', d);
}
