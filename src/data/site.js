// Zentrale Adresse der Seite. Für den Umzug auf eine eigene Domain nur DOMAIN eintragen,
// z. B. 'scheinfasten-mega-lecker.de' (ohne https://, ohne www). Der Build setzt dann
// Adresse, Pfad, Sitemap, robots.txt und die CNAME-Datei für GitHub Pages automatisch.
// Danach in GitHub unter Settings > Pages die Domain eintragen und „Enforce HTTPS“ anhaken.

export const DOMAIN = '';

export const SITE = DOMAIN ? `https://${DOMAIN}` : 'https://culinarylust.github.io';
export const BASE = DOMAIN ? '/' : '/Scheinfasten-mega-lecker/';
export const SITE_NAME = 'Scheinfasten mega lecker';
