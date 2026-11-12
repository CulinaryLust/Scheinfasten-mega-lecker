// Zentrale Adresse der Seite. Für den Umzug auf eine eigene Domain nur DOMAIN eintragen,
// z. B. 'einfach-lecker-fasten.de' (ohne https://, ohne www). Der Build setzt dann
// Adresse, Pfad, Sitemap, robots.txt und die CNAME-Datei für GitHub Pages automatisch.
// Danach in GitHub unter Settings > Pages die Domain eintragen und „Enforce HTTPS“ anhaken.

export const DOMAIN = '';

export const SITE = DOMAIN ? `https://${DOMAIN}` : 'https://culinarylust.github.io';
export const BASE = DOMAIN ? '/' : '/Scheinfasten-mega-lecker/';
export const SITE_NAME = 'Scheinfasten - einfach lecker fasten';

// Pinterest automatisch: Der Feed /pins.xml gibt ab diesem Datum alle PINS_ABSTAND Tage ein weiteres Rezept frei.
// Pinterest erstellt daraus selbst Pins (README, Abschnitt „Pinterest automatisch“). Leer = Feed bleibt leer.
// Datum im Format JJJJ-MM-TT eintragen, am besten der Tag, an dem du den Feed bei Pinterest einträgst.
export const PINS_START = '';
export const PINS_ABSTAND = 2;
