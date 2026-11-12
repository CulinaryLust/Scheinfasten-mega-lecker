# Scheinfasten - einfach lecker fasten

Webseite mit pflanzlichen Rezepten und einem persönlichen 5-Tage-Planer, angelehnt an die Fasting Mimicking Diet nach Prof. Dr. Valter Longo.

Live: https://culinarylust.github.io/Scheinfasten-mega-lecker/

## Aufbau

- **Astro** erzeugt eine statische Seite, GitHub Pages veröffentlicht sie bei jedem Push auf `main` (`.github/workflows/deploy.yml`).
- `src/data/` enthält Nährwerte, Rezepte und den Standardplan als JSON. Diese Dateien werden aus `tools/recipes_src.py` erzeugt.
- `src/lib/nutrition.js` rechnet Nährwerte und prüft Tage gegen Longos Referenz (Tag 1: 1.090 kcal, 10/56/34 % nach Brandhorst 2015; Tage 2 bis 5: 725 kcal, 9/44/47 %; Toleranz ±5 % kcal, ±5 Prozentpunkte je Makro; Zucker höchstens 15 % der kcal als eigene Regel).
- Der Planer (`src/pages/planer.astro`) rechnet komplett im Browser. Eingaben bleiben im localStorage.
- Der Lebensmittel-Rechner (`src/pages/rechner.astro`, Logik in `src/lib/rechner.js`) verteilt Longos Tagesbudget auf eingegebene Lebensmittel, zeigt Alternativen für ungeeignete und baut Gerichte daraus. Test: `npm run check:rechner`.
- Die Tagesbilanz (Reiter „Was habe ich gegessen?“, `src/components/Tagebuch.astro`, Logik in `src/lib/tagebuch.js`) zählt Gegessenes je Zyklustag gegen das Tageslimit und füllt den Rest mit Rezepten oder Zutaten auf. Einträge bleiben im localStorage (`smlTagebuch`, Körperdaten `smlProfil`). Test: `npm run check:rechner`.
- Nährwerte: BLS 4.0 (Max Rubner-Institut, CC BY 4.0). Die Lebensmittelliste mit Ampel, Obergrenzen und Alternativen steht in `tools/foods_src.py`. `tools/bls_import.py <BLS_4_0_Daten_2025_DE.xlsx>` aktualisiert `tools/bls_values.json` (Download unter https://blsdb.de).

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

## Start-Checkliste

`npm run check:launch` zeigt, was noch fehlt. Alle Angaben stehen in je einer Datei:

- `src/data/site.js`: eigene Domain in `DOMAIN` eintragen. Der Build setzt dann Adresse, Pfad, Sitemap, robots.txt und die CNAME-Datei. Danach in GitHub unter Settings > Pages die Domain eintragen und „Enforce HTTPS“ anhaken. Beim Domainanbieter: für die Hauptdomain A-Records auf 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 und für `www` einen CNAME auf `culinarylust.github.io`.
- DNS bei ALL-INKL: Im KAS unter Tools > DNS-Einstellungen die Domain wählen. Die vorhandenen A-Records für die Domain ohne Präfix löschen und vier neue anlegen (Ziel je eine der vier GitHub-IPs oben). Für `www` den A-Record löschen und einen CNAME auf `culinarylust.github.io.` anlegen. Erst danach `DOMAIN` setzen und in GitHub die Domain eintragen. Bis das Zertifikat da ist, können bis zu 24 Stunden vergehen.
- `src/data/betreiber.js`: Name, Anschrift, E-Mail für Impressum und Datenschutzerklärung.
- `src/data/affiliate.js`: Amazon-Tracking-ID und ProLon-Partnerlink.
- Werbeanzeigen erst mit Einwilligungsbanner einschalten (`ADS_ENABLED`).
- Nach dem Umzug: Domain in der Google Search Console und den Bing Webmaster Tools anmelden und `sitemap.xml` einreichen.

## Stand sichern
Im Rechner erstellt „Link erstellen“ einen persönlichen Link mit QR-Code (`src/components/StandSichern.astro`, Logik `src/lib/sicherung.js`). Alle gespeicherten Daten (`smlTagebuch`, `smlProfil`, `smlPlaner`, `smlRechner`) stehen komprimiert im Teil hinter `#stand=`, der nie an den Server geht. Beim Öffnen fragt die Seite, ob der Stand übernommen werden soll. Test: `node scripts/check-sicherung.mjs`.

## Zyklus-Erinnerung (Brevo, vorerst aus)
Die Box `src/components/Erinnerung.astro` erscheint auf Rechner und Planer, sobald sie in `src/data/newsletter.js` eingeschaltet ist. Erst einschalten, wenn Gewerbe, Impressum und Datenschutzerklärung stehen, denn die Mails enthalten Affiliate-Links.

1. Konto bei Brevo anlegen (kostenloser Tarif reicht für den Anfang) und den Auftragsverarbeitungsvertrag in den Kontoeinstellungen annehmen.
2. Unter Kontakte > Einstellungen ein Attribut `ZYKLUS_START` vom Typ Datum anlegen.
3. Unter Kontakte > Formulare ein Anmeldeformular mit den Feldern E-Mail und `ZYKLUS_START` anlegen, Double-Opt-in aktivieren, Datumsformat TT-MM-JJJJ.
4. Beim Einbetten die Adresse aus `action="…"` des HTML-Codes kopieren und in `NEWSLETTER_ACTION` eintragen, dann `NEWSLETTER_ENABLED = true`.
5. Unter Automationen einen Ablauf „Datum eines Attributs“ mit `ZYKLUS_START` minus 3 Tage anlegen: Erinnerung mit Link zum Planer, Einkaufsliste und Ausstattungs-Empfehlungen.
6. Einmal mit der eigenen Adresse testen, ob das Datum in Brevo richtig ankommt.

Die Datenschutzerklärung zeigt den passenden Abschnitt automatisch, sobald die Box eingeschaltet ist. Ernährungseinträge werden nie an Brevo übertragen.
