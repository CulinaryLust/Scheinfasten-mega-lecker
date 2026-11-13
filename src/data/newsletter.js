// Zyklus-Erinnerung per E-Mail (Brevo, Server in der EU, Double-Opt-in).
// Bleibt ausgeschaltet, bis Gewerbe, Impressum und Datenschutzerklärung stehen und das Brevo-Formular angelegt ist.
// Einrichtung: siehe README, Abschnitt „Zyklus-Erinnerung“.

/** true = Box auf Rechner und Planer anzeigen. Nur einschalten, wenn ACTION gesetzt ist. */
export const NEWSLETTER_ENABLED = false;

/** Formular-Adresse aus Brevo (Kontakte > Formulare > Einbetten > „action“ des HTML-Formulars),
 *  z. B. „https://xxxx.sibforms.com/serve/MUIF...“. */
export const NEWSLETTER_ACTION = '';

/** Name des Brevo-Kontaktattributs (Typ Datum) für den Start des nächsten Durchgangs. */
export const DATE_FIELD = 'ZYKLUS_START';

/** Brevo-Attribut (Typ Ja/Nein) für das freiwillige Newsletter-Häkchen. Getrennt von der Erinnerung (Kopplungsverbot). */
export const TIPS_FIELD = 'SF_TIPPS';

/** Brevo-Liste „Scheinfasten Erinnerung“ (Ordner „Scheinfasten“), am 13.11.2026 per API angelegt. */
export const LIST_ID = 5;

/** Datumsformat, das das Brevo-Formular erwartet (in Brevo beim Datumsfeld einstellbar). */
export const DATE_FORMAT = 'DD-MM-YYYY';

/** Anbieter für die Datenschutzerklärung. */
export const PROVIDER = 'Brevo (Sendinblue GmbH, Köpenicker Straße 126, 10179 Berlin)';
