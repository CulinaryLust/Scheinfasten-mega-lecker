// Angaben für Impressum und Datenschutzerklärung. Solange Pflichtfelder leer sind,
// zeigen beide Seiten einen gelben Hinweis und `npm run check:launch` meldet sie als offen.
// Ohne Gewerbe: Felder trotzdem mit Deinen privaten Angaben füllen, das Impressum ist Pflicht,
// sobald die Seite Einnahmen erzielt (Affiliate-Links reichen dafür).

export const BETREIBER = {
  /** Vor- und Nachname (bei Einzelunternehmen der eigene Name, optional mit Zusatz). */
  name: '',
  /** Ladungsfähige Anschrift, kein Postfach. Wer die Privatadresse nicht zeigen will: Impressum-Service mit Geschäftsanschrift. */
  strasse: '',
  plzOrt: '',
  /** E-Mail-Adresse, die Du regelmäßig liest. */
  email: '',
  /** Optional: Telefon. Nicht Pflicht, beschleunigt aber Anfragen.  */
  telefon: '',
  /** Optional: Umsatzsteuer-ID, nur wenn vorhanden. Als Kleinunternehmer ohne USt-ID leer lassen. */
  ustId: '',
  /** Optional: Wirtschafts-Identifikationsnummer, sobald zugeteilt. */
  wIdNr: '',
};

export const PFLICHT = ['name', 'strasse', 'plzOrt', 'email'];
export const fehlend = () => PFLICHT.filter((k) => !BETREIBER[k]);
