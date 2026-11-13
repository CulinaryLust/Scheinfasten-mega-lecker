# Scheinfasten - einfach lecker fasten

Webseite mit pflanzlichen Rezepten und einem persönlichen 5-Tage-Planer, angelehnt an die Fasting Mimicking Diet nach Prof. Dr. Valter Longo.

Live: https://einfach-lecker-fasten.de (die alte Adresse auf github.io leitet dorthin weiter)

## Aufbau

- **Astro** erzeugt eine statische Seite, bei jedem Push auf `main` lädt `.github/workflows/deploy.yml` sie per FTP zu ALL-INKL hoch. GitHub Pages zeigt danach nur noch Weiterleitungen von der alten Adresse.
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

- `src/data/site.js`: eigene Domain in `DOMAIN`. Der Build setzt dann Adresse, Pfad, Sitemap, robots.txt und die `.htaccess` (HTTPS, www-Umleitung, 404, Cache).
- `src/data/betreiber.js`: Name, Anschrift, E-Mail für Impressum und Datenschutzerklärung.
- `src/data/affiliate.js`: Amazon-Tracking-ID und ProLon-Partnerlink.
- Werbeanzeigen erst mit Einwilligungsbanner einschalten (`ADS_ENABLED`).
- Nach dem Umzug: Domain in der Google Search Console und den Bing Webmaster Tools anmelden und `sitemap.xml` einreichen.

## Hosting bei ALL-INKL

Einmal einrichten, danach lädt jeder Push auf `main` die Seite automatisch hoch.

1. Im KAS unter Domain die Domain `einfach-lecker-fasten.de` bearbeiten: Ziel ist ein eigener Ordner, z. B. `/einfach-lecker-fasten/`. SSL unter Domain > SSL-Schutz mit Let's Encrypt einschalten. DNS nicht ändern, die Domain zeigt bei ALL-INKL von selbst auf den Webspace.
2. Im KAS unter FTP einen Zusatz-FTP-Benutzer anlegen, der nur diesen Ordner sieht.
3. In GitHub unter Settings > Secrets and variables > Actions drei Repository-Secrets anlegen: `ALLINKL_FTP_HOST` (Server aus der FTP-Übersicht, z. B. `w0123456.kasserver.com`), `ALLINKL_FTP_USER` und `ALLINKL_FTP_PASSWORD`.
4. In GitHub unter Actions den Lauf „Seite veröffentlichen“ neu starten. Ohne Secrets bricht er mit einer klaren Meldung ab und die alte Seite bleibt online.
5. Im KAS unter Tools > Auftragsverarbeitung den Vertrag zur Auftragsverarbeitung abschließen (Pflicht nach DSGVO).
6. Für `kontakt@einfach-lecker-fasten.de` im KAS unter E-Mail ein Postfach oder eine Weiterleitung anlegen. Die Adresse steht im Impressum.

## Was automatisch läuft

Ziel: möglichst keine wiederkehrende Handarbeit. Einmal einrichten, danach läuft es.

| Aufgabe | Automatik | Einmal einrichten |
| --- | --- | --- |
| Seite veröffentlichen | Jeder Merge auf `main` baut und veröffentlicht (`deploy.yml`) | erledigt |
| Rezepte und Pläne nachrechnen | Bei jedem Build; passt ein Tag nicht zu Longos Werten, wird nicht veröffentlicht | erledigt |
| Bilder verkleinern | `scripts/bilder.mjs` erzeugt WebP in passenden Größen | erledigt |
| Tote interne Links | `scripts/check-links.mjs` bricht den Build ab | erledigt |
| Änderungen vorab prüfen | `pruefen.yml` baut jeden Pull Request | erledigt |
| Pinterest-Grafiken | `scripts/pins.mjs` baut pro Rezept ein Hochformat-Bild nach `pins/` | erledigt |
| Pins veröffentlichen | Feed `pins.xml`, Pinterest holt alle 2 Tage ein neues Rezept ab | siehe „Pinterest automatisch“ |
| Externe Links, ProLon-Preis, Artikel-Alter | `wartung.yml` am 1. jedes Monats, bei Befund E-Mail von GitHub | GitHub-Benachrichtigungen für fehlgeschlagene Actions anlassen (Standard) |
| Einkaufsliste und „Tag für Tag“ im Ratgeber | Werden aus dem Standardplan berechnet, ändern sich mit dem Plan | erledigt |
| Sitemap für Google und Bing | Entsteht bei jedem Build, Suchmaschinen holen sie selbst ab | Sitemap einmal in Search Console und Bing eintragen |
| Erinnerungs-Mails | Brevo-Automationen, Texte in `docs/mails.md` | siehe „Zyklus-Erinnerung“ |
| Besucherzahlen | GoatCounter zählt Aufrufe und Klicks auf Partnerlinks | Code in `src/data/statistik.js` eintragen |
| Offene Punkte vor dem Start | `npm run check:launch`, steht auch in der Zusammenfassung jedes Deploys | erledigt |

Nicht automatisierbar: Domainkauf, Gewerbeanmeldung, Impressumsangaben, Anmeldung bei Partnerprogrammen, Brevo und Pinterest (jeweils einmalig).

## Pinterest automatisch

1. Pinterest-Unternehmenskonto anlegen und die eigene Domain bestätigen („Website beanspruchen“). Das geht erst mit eigener Domain.
2. In `src/data/site.js` bei `PINS_START` das heutige Datum eintragen (JJJJ-MM-TT) und mergen.
3. In Pinterest am Computer unter Einstellungen > Pins in großen Mengen erstellen > Automatisch veröffentlichen die Adresse `https://DOMAIN/pins.xml` eintragen und eine Pinnwand wählen.

Ab dann gibt der Feed alle `PINS_ABSTAND` Tage ein weiteres Rezept frei, Rezepte der aktuellen Jahreszeit zuerst. Die Seite baut sich dafür montags und donnerstags selbst neu. Bei 56 Rezepten reicht das für knapp vier Monate. Neue Rezepte hängen sich hinten an.

## Statistik (GoatCounter)

Kostenloses Konto auf goatcounter.com anlegen, den gewählten Code in `src/data/statistik.js` eintragen. Die Datenschutzerklärung ergänzt den Abschnitt dann selbst. Vor dem Einschalten bitte die Angaben dort einmal mit den aktuellen Datenschutzhinweisen von GoatCounter abgleichen. Klicks auf Partnerlinks erscheinen als Ereignisse `partner-amazon-…` und `partner-prolon`.

## Ratgeber

Artikel stehen in `src/pages/ratgeber/`, die Liste in `src/data/ratgeber.js`. Jeder Artikel trägt ein Prüfdatum (`stand`). Aussagen sind mit „Studie“, „Hersteller“ oder „Unser Tipp“ markiert.

## Stand sichern
Im Rechner erstellt „Link erstellen“ einen persönlichen Link mit QR-Code (`src/components/StandSichern.astro`, Logik `src/lib/sicherung.js`). Alle gespeicherten Daten (`smlTagebuch`, `smlProfil`, `smlPlaner`, `smlRechner`) stehen komprimiert im Teil hinter `#stand=`, der nie an den Server geht. Beim Öffnen fragt die Seite, ob der Stand übernommen werden soll. Test: `node scripts/check-sicherung.mjs`.

## Zyklus-Erinnerung (Brevo, vorerst aus)
Die Box `src/components/Erinnerung.astro` erscheint auf Rechner und Planer, sobald sie in `src/data/newsletter.js` eingeschaltet ist. Erst einschalten, wenn Gewerbe, Impressum und Datenschutzerklärung stehen, denn die Mails enthalten Affiliate-Links.

Per API schon erledigt (13.11.2026): Ordner „Scheinfasten“, Liste „Scheinfasten Erinnerung“ (ID 5), Attribute `ZYKLUS_START` (Datum) und `SF_TIPPS` (Ja/Nein). Der API-Schlüssel liegt nur in der Umgebung, nie im Code.

Im Brevo-Dashboard noch selbst zu tun:
1. Auftragsverarbeitungsvertrag in den Kontoeinstellungen annehmen.
2. Absender und Domain verifizieren (Einstellungen > Absender, Domains), z. B. `hallo@DOMAIN`. Der vorhandene Absender gehört zu einem anderen Projekt und darf hier nicht verwendet werden.
3. Unter Kontakte > Formulare ein Anmeldeformular anlegen: Liste „Scheinfasten Erinnerung“, Felder E-Mail, `ZYKLUS_START` (Datumsformat TT-MM-JJJJ), `SF_TIPPS` (Kontrollkästchen, nicht vorausgewählt) und das DSGVO-Feld `OPT_IN`. Double-Opt-in aktivieren, Bestätigungstext aus `docs/mails.md`.
4. Beim Einbetten die Adresse aus `action="…"` des HTML-Codes kopieren und in `NEWSLETTER_ACTION` eintragen, dann `NEWSLETTER_ENABLED = true`.
5. Automationen anlegen (Auslöser in `docs/mails.md`). Newsletter-Kampagnen nur an Kontakte mit `SF_TIPPS` = Ja schicken.
6. Einmal mit der eigenen Adresse testen, ob Datum und Häkchen in Brevo richtig ankommen.

Keine Amazon-Partnerlinks direkt in Mails, das verbieten die Teilnahmebedingungen. Stattdessen auf die eigene Seite `/ausstattung/` verlinken.

Die fertigen Mailtexte und die Auslöser für alle fünf Mails stehen in `docs/mails.md`.

Die Datenschutzerklärung zeigt den passenden Abschnitt automatisch, sobald die Box eingeschaltet ist. Ernährungseinträge werden nie an Brevo übertragen.
