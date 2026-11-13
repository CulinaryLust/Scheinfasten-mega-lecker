# Mailtexte für die Zyklus-Erinnerung (Brevo)

Einmal in Brevo anlegen, danach läuft alles automatisch. `{{ contact.ZYKLUS_START }}` setzt Brevo selbst ein.
`DOMAIN` durch die eigene Adresse ersetzen. Partnerlinks in Mails immer mit „Anzeige“ kennzeichnen, keine Amazon-Links direkt in Mails (nur auf `/ausstattung/` verweisen).
Newsletter (neue Rezepte, Tipps) nur an Kontakte mit `SF_TIPPS` = Ja, die Erinnerungsmails 1 bis 5 an alle bestätigten Kontakte der Liste.
Kein Heilversprechen in Betreff oder Text (HWG).

| Mail | Auslöser in Brevo | Zweck |
| --- | --- | --- |
| 1 Bestätigung | Double-Opt-in-Vorlage des Formulars | Einwilligung nachweisen |
| 2 Willkommen | Automation: Kontakt zur Liste hinzugefügt | Plan-Link, Erwartung setzen |
| 3 Erinnerung | Automation: Datum `ZYKLUS_START` minus 3 Tage | Einkaufen und vorkochen |
| 4 Halbzeit | Automation: Datum `ZYKLUS_START` plus 2 Tage | Durchhalten an Tag 3 |
| 5 Danach | Automation: Datum `ZYKLUS_START` plus 5 Tage | Übergang, nächsten Termin eintragen |

## 1 Bestätigung (Double-Opt-in)

**Betreff:** Bitte bestätige Deine Erinnerung

Hallo,

Du hast auf einfach lecker fasten eine Erinnerung für Deinen nächsten Scheinfasten-Durchgang bestellt. Bitte bestätige kurz, dass die Adresse stimmt:

[Ja, Erinnerung schicken] (Bestätigungslink von Brevo)

Warst Du das nicht, ignoriere diese Mail einfach. Dann bekommst Du nichts weiter von uns.

## 2 Willkommen

**Betreff:** Deine Erinnerung steht

Hallo,

alles eingerichtet. Drei Tage vor Deinem Start am {{ contact.ZYKLUS_START }} melden wir uns mit der Einkaufsliste.

Bis dahin:

- Dein Plan: https://DOMAIN/planer/ (bleibt auf Deinem Gerät gespeichert)
- Einkaufsliste für fünf Tage: https://DOMAIN/ratgeber/einkaufsliste/
- So läuft die Woche ab: https://DOMAIN/ratgeber/tag-fuer-tag/

Wenn Du schwanger bist, stillst, Medikamente nimmst oder eine ernste Erkrankung hast, sprich vorher mit Deiner Ärztin oder Deinem Arzt.

Abmelden geht jederzeit über den Link unten.

## 3 Erinnerung (3 Tage vorher)

**Betreff:** In 3 Tagen geht es los: Zeit zum Einkaufen

Hallo,

am {{ contact.ZYKLUS_START }} startet Dein Durchgang. Das steht jetzt an:

1. **Einkaufen.** Die Liste für alle fünf Tage: https://DOMAIN/ratgeber/einkaufsliste/ Im Planer bekommst Du sie passend zu Deinen Mengen: https://DOMAIN/planer/
2. **Vorkochen.** Die Gerichte für Tag 1 und 2 am Vorabend kochen, den Nussmix für fünf Tage abwiegen.
3. **Kaffee reduzieren.** In den fünf Tagen ist höchstens eine kleine Tasse schwarz vorgesehen.
4. **Kalender prüfen.** Tag 2 und 3 empfinden viele als die zähesten. Plane dort wenig ein.

Was das Abwiegen leichter macht (Anzeige): eine Küchenwaage auf 0,1 g und Glasdosen zum Vorkochen. Unsere Auswahl: https://DOMAIN/ausstattung/

Guten Start!

## 4 Halbzeit (Tag 3)

**Betreff:** Halbzeit: Tag 3 von 5

Hallo,

Du bist mittendrin. Zwei Dinge, die heute helfen:

- **Hunger am Nachmittag** ist normal. Kräutertee, Wasser und die Oliven aus dem Plan sind dafür da.
- **Etwas schmeckt Dir nicht?** Im Planer tauschst Du jedes Gericht, die Werte rechnen sich neu: https://DOMAIN/planer/

Wie viel heute noch geht, zeigt Dir der Rechner: https://DOMAIN/rechner/

Wird Dir schwindelig, rast Dein Herz oder fühlst Du Dich sehr schwach, iss normal weiter. Ein abgebrochener Durchgang ist kein Problem.

## 5 Danach (Tag 6)

**Betreff:** Geschafft. So steigst Du wieder ein

Hallo,

fünf Tage sind um. Heute gilt: langsam wieder einsteigen, mit Suppe beginnen, abends eine normale, nicht üppige Mahlzeit. Die Details: https://DOMAIN/ratgeber/nach-dem-scheinfasten/

**Nächster Durchgang?** Trag das neue Startdatum hier ein, dann erinnern wir Dich wieder rechtzeitig: https://DOMAIN/planer/#remind

Hat Dir etwas gefehlt oder nicht geschmeckt? Antworte einfach auf diese Mail.
