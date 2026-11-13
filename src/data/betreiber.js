// Angaben für Impressum und Datenschutzerklärung. Solange Pflichtfelder leer sind,
// zeigen beide Seiten einen gelben Hinweis und `npm run check:launch` meldet sie als offen.
// Ohne Gewerbe: Felder trotzdem mit deinen privaten Angaben füllen, das Impressum ist Pflicht,
// sobald die Seite Einnahmen erzielt (Affiliate-Links reichen dafür).

export const BETREIBER = {
  /** Vor- und Nachname (bei Einzelunternehmen der eigene Name, optional mit Zusatz). */
  name: 'Alexander Russo',
  /** Ladungsfähige Anschrift, kein Postfach. Wer die Privatadresse nicht zeigen will: Impressum-Service mit Geschäftsanschrift. */
  strasse: 'Am Herrnholz 3',
  plzOrt: '85630 Grasbrunn',
  /** E-Mail-Adresse, die du regelmäßig liest. */
  email: 'kontakt@einfach-lecker-fasten.de',
  /** Optional: Telefon. Nicht Pflicht, beschleunigt aber Anfragen.  */
  telefon: '',
  /** Optional: Umsatzsteuer-ID, nur wenn vorhanden. Als Kleinunternehmer ohne USt-ID leer lassen. */
  ustId: '',
  /** Optional: Wirtschafts-Identifikationsnummer, sobald zugeteilt. */
  wIdNr: '',
};

export const PFLICHT = ['name', 'strasse', 'plzOrt', 'email'];
export const fehlend = () => PFLICHT.filter((k) => !BETREIBER[k]);
