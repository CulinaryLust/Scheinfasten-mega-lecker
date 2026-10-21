# Scheinfasten mega lecker

Webseite mit pflanzlichen Rezepten und einem persönlichen 5-Tage-Planer, angelehnt an die Fasting Mimicking Diet nach Prof. Dr. Valter Longo.

Live: https://culinarylust.github.io/Scheinfasten-mega-lecker/

## Aufbau

- **Astro** erzeugt eine statische Seite, GitHub Pages veröffentlicht sie bei jedem Push auf `main` (`.github/workflows/deploy.yml`).
- `src/data/` enthält Nährwerte, Rezepte und den Standardplan als JSON. Diese Dateien werden aus `tools/recipes_src.py` erzeugt.
- `src/lib/nutrition.js` rechnet Nährwerte und prüft Tage gegen Longos Referenz (Tag 1: 1.090 kcal, 10/56/34 %; Tage 2 bis 5: 725 kcal, 9/44/47 %; Toleranz ±5 % kcal, ±5 Prozentpunkte je Makro).
- Der Planer (`src/pages/planer.astro`) rechnet komplett im Browser. Eingaben bleiben im localStorage.

## Ein Rezept hinzufügen

1. In `tools/recipes_src.py` einen `r(...)`-Aufruf ergänzen. Neue Zutaten mit Nährwerten je 100 g in `N` eintragen.
2. Foto als `public/img/rezepte/<bildname>.jpg` ablegen (4:3, etwa 900 × 675 px).
3. `cd tools && python3 export.py` ausführen. Das Skript bricht ab, wenn der Standardplan Longos Toleranz verlässt.
4. `npm run build` und committen.

## Lokal starten

```bash
npm install
npm run dev
```

## Offene Punkte vor dem Start

- Impressum und Datenschutzerklärung ausfüllen.
- Nährwerte mit dem Bundeslebensmittelschlüssel (BLS) gegenrechnen.
- Eigene Rezeptfotos statt Unsplash-Symbolbildern.
- Shop-Anbindung für das E-Book.
