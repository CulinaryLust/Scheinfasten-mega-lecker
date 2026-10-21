const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';

/** Pfad relativ zur Startseite, funktioniert mit und ohne base. */
export const u = (path = '') => base + String(path).replace(/^\//, '');
