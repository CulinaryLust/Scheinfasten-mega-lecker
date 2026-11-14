# Lebensmitteldatenbank für den Rechner.
# Nährwerte kommen aus dem Bundeslebensmittelschlüssel (BLS 4.0, Max Rubner-Institut, CC BY 4.0),
# siehe tools/bls_values.json (erzeugt mit tools/bls_import.py). Nur wenige Gewürze ohne BLS-Eintrag
# behalten die bisherigen USDA-angelehnten Richtwerte aus recipes_src.py (Feld bls = None).
#
# Ampel: g = passt gut, y = nur kleine Menge (Obergrenze cap in g pro Tag), r = passt nicht ins Scheinfasten.
# cap: Obergrenze pro Tag in Gramm, die der Rechner nie überschreitet. Die Werte sind Richtwerte dieser Seite,
# abgeleitet aus Prof. Dr. Longos Makroverteilung, keine Zahlen aus Prof. Dr. Longos Protokoll.
# alts: bessere Alternativen (Namen aus dieser Liste). syn: Suchbegriffe.

GROUPS = {
  'gemuese': ('Gemüse', 'g', 400), 'blatt': ('Salat und Blattgemüse', 'g', 250), 'pilze': ('Pilze', 'g', 300),
  'kraeuter': ('Kräuter', 'g', 30), 'wuerze': ('Würzen', 'g', 30), 'fett': ('Öle', 'g', 35),
  'nuss': ('Nüsse und Saaten', 'g', 40), 'fettfrucht': ('Oliven, Avocado, Kokos', 'g', 80),
  'knolle': ('Kartoffeln und Stärkegemüse', 'y', 200), 'huelsen': ('Hülsenfrüchte', 'y', 80),
  'getreide': ('Getreide', 'y', 120), 'obst': ('Obst', 'y', 150), 'soja': ('Soja', 'y', 60),
  'getraenk': ('Getränke', 'g', 1000),
  'tier': ('Fleisch, Fisch und Ei', 'r', 0), 'milch': ('Milchprodukte', 'r', 0), 'suess': ('Zucker und Süßes', 'r', 0),
  'weissmehl': ('Weißmehl und Snacks', 'r', 0), 'drink': ('Alkohol, Säfte, Softdrinks', 'r', 0),
  'eiweiss': ('Fleischersatz und Eiweißprodukte', 'r', 0), 'knusper': ('Cracker und Waffeln', 'y', 20),
  'suppe': ('Suppen und fertige Gerichte', 'y', 300), 'fertig': ('Fertiggerichte', 'r', 0),
  'pflanz': ('Pflanzliche Joghurts und Cremes', 'y', 100),
}

WHY = {
  'y': 'Eine kleine Menge passt prima, von mehr hält Prof. Dr. Longos Rezept nichts.',
  'tier': 'Prof. Dr. Longos Scheinfasten ist rein pflanzlich und eiweißarm. Pilze und Hülsenfrüchte übernehmen hier den herzhaften Part.',
  'milch': 'Scheinfasten ist rein pflanzlich, Milchprodukte machen deshalb Pause.',
  'suess': 'Prof. Dr. Longos Vorgabe heißt: wenig Zucker. Zucker würde sonst schnell das ganze Tagesbudget aufbrauchen.',
  'weissmehl': 'Kostet viele Kalorien und macht kaum satt. Gemüse bringt Dir mehr auf den Teller.',
  'drink': 'Bringt Zucker oder Alkohol mit. Wasser und ungesüßter Tee sind in diesen Tagen die Basis.',
  'eiweiss': 'Fleischersatz besteht fast nur aus Eiweiß. Genau das hält Prof. Dr. Longo in diesen Tagen niedrig.',
  'fertig': 'Enthält Fleisch, Fisch, Ei, Milchprodukte oder viel Weißmehl. Selbst gekocht hast Du in der Hand, was drin ist.',
  'pflanz': 'Pflanzlich und ungesüßt in Ordnung, aber verarbeitet. Ein paar Löffel reichen.',
  'knusper': 'Knusprig und leicht, aber fast reine Stärke. Ein, zwei Stück passen gut in den Tag, mehr verdrängt das Gemüse.',
}

ALTS = {
  'tier': ['Champignons', 'Austernpilze', 'Kichererbsen (gegart)', 'Walnusskerne'],
  'milch': ['Kokosmilch (vollfett)', 'Cashewkerne', 'Tahin', 'Mandeldrink ungesüßt'],
  'suess': ['Heidelbeeren', 'Apfel', 'Walnusskerne'],
  'weissmehl': ['Kartoffeln', 'Hirse (gegart)', 'Blumenkohl', 'Zucchini'],
  'drink': ['Kräutertee', 'Zitronensaft', 'Gemüsebrühe'],
  'eiweiss': ['Champignons', 'Austernpilze', 'Kichererbsen (gegart)'],
  'fertig': ['Gemüsebrühe', 'Champignons', 'Zucchini'],
}

# name, BLS-Code, Gruppe, Ampel (None = Gruppe), cap (None = Gruppe), Suchbegriffe, Alternativen, Begründung, Stück (Bezeichnung, g)
F = []
# Kürbis: Richtwert ca. 200 g am Tag (Tag 2 bis 5), gleiche Zahl wie PUMPKIN_MAX in src/lib/tagebuch.js.
# Rezepte bleiben bei 175 g, damit auch die größte Portion (Faktor 1,15) darunter liegt.
PUMPKIN_MAX = 200
PUMPKIN = ('Hokkaido-Kürbis', 'Gartenkürbis')
def f(name, bls, group, light=None, cap=None, syn='', alts='', why='', piece=None, n=None, db=None):
    # n: nur für Einträge ohne BLS-Code, Richtwerte (kcal, Eiweiß, Fett, Kohlenhydrate gesamt, Zucker) je 100 g nach USDA FoodData Central
    # db: Quelle der n-Werte, 'Hersteller' = Richtwert aus typischen Nährwertangaben auf den Packungen (Mittel mehrerer Marken)
    F.append(dict(db=db, name=name, bls=bls, group=group, light=light, cap=cap, syn=[s.strip() for s in syn.split(',') if s.strip()],
                  alts=[a.strip() for a in alts.split(';') if a.strip()], why=why, piece=piece, n=n))

# Gemüse
f('Zucchini', 'G582100', 'gemuese', syn='Zucchetti', piece=('Stück', 200))
f('Tomaten', 'G561100', 'gemuese', syn='Tomate', piece=('Stück', 100))
f('Kirschtomaten', 'G561100', 'gemuese', syn='Cocktailtomaten, Cherrytomaten')
f('Tomaten, passiert', 'R161200', 'gemuese', cap=300, syn='Passata, Tomatenpüree')
f('Tomatenmark', 'R160000', 'wuerze', cap=40)
f('Karotten', 'G620100', 'gemuese', syn='Karotte, Möhre, Möhren, Rüebli', piece=('Stück', 80))
f('Staudensellerie', 'G220100', 'gemuese', syn='Stangensellerie, Bleichsellerie')
f('Knollensellerie', 'G660100', 'gemuese', syn='Sellerie, Sellerieknolle')
f('Zwiebeln', 'G480100', 'gemuese', cap=150, syn='Zwiebel, Speisezwiebel', piece=('Stück', 80))
f('Rote Zwiebel', 'G480100', 'gemuese', cap=150, syn='rote Zwiebeln')
f('Frühlingszwiebeln', 'G482100', 'gemuese', cap=150, syn='Lauchzwiebel, Frühlingszwiebel')
f('Schalotten', 'G485100', 'gemuese', cap=100, syn='Schalotte')
f('Lauch', 'G470100', 'gemuese', syn='Porree')
f('Hokkaido-Kürbis', 'G581000', 'gemuese', cap=PUMPKIN_MAX, syn='Kürbis, Hokkaido')
f('Gartenkürbis', 'G581100', 'gemuese', cap=PUMPKIN_MAX, syn='Butternut, Muskatkürbis, Kürbis')
f('Blumenkohl', 'G311100', 'gemuese', syn='Karfiol')
f('Brokkoli', 'G312100', 'gemuese', syn='Broccoli')
f('Rosenkohl', 'G332100', 'gemuese', syn='Kohlsprossen')
f('Weißkohl', 'G342100', 'gemuese', syn='Weisskohl, Kraut, Spitzkohl')
f('Rotkohl', 'G341100', 'gemuese', syn='Blaukraut, Rotkraut')
f('Wirsing', 'G343100', 'gemuese')
f('Chinakohl', 'G321100', 'gemuese')
f('Pak Choi', 'G324100', 'gemuese', syn='Pak Choy, Bok Choy')
f('Grünkohl', 'G322100', 'gemuese', syn='Federkohl, Kale')
f('Kohlrabi', 'G331100', 'gemuese', piece=('Stück', 250))
f('Fenchel', 'G431100', 'gemuese', piece=('Knolle', 250))
f('Rote Paprika', 'G543100', 'gemuese', syn='Paprika, Paprikaschote', piece=('Stück', 150))
f('Gelbe Paprika', 'G542100', 'gemuese', syn='Paprika', piece=('Stück', 150))
f('Grüne Paprika', 'G541100', 'gemuese', syn='Paprika', piece=('Stück', 150))
f('Aubergine', 'G510100', 'gemuese', syn='Melanzani, Auberginen', piece=('Stück', 300))
f('Gurke', 'G520100', 'gemuese', syn='Salatgurke, Gurken', piece=('Stück', 400))
f('Gewürzgurken', 'G520802', 'gemuese', cap=100, syn='Essiggurken, saure Gurken')
f('Sauerkraut', 'G345902', 'gemuese', cap=200)
f('Rote Bete (vorgegart)', 'G613152', 'gemuese', cap=250, syn='Rote Bete, Rote Rübe, Randen')
f('Radieschen', 'G691100', 'gemuese')
f('Rettich', 'G680100', 'gemuese')
f('Steckrübe', 'G611100', 'gemuese', syn='Kohlrübe')
f('Pastinaken', 'G640100', 'gemuese', cap=200, syn='Pastinake')
f('Spargel', 'G450100', 'gemuese', syn='Spargel grün, Spargel weiß')
f('Grüne Bohnen', 'G710100', 'gemuese', syn='Bohnen grün, Brechbohnen, Fisolen, Prinzessbohnen')
f('Zuckerschoten', 'G761100', 'gemuese', syn='Zuckererbsen, Kaiserschoten')
f('Erbsen (TK)', 'G760200', 'huelsen', cap=120, syn='Erbsen, grüne Erbsen', alts='Zuckerschoten; Brokkoli')
f('Okra', 'G530100', 'gemuese')
f('Artischocken', 'G410100', 'gemuese', syn='Artischocke')
f('Mais', 'G570902', 'knolle', cap=80, syn='Zuckermais, Maiskörner', alts='Rote Paprika; Erbsen (TK)')

# Salat und Blattgemüse
f('Babyspinat', 'G211100', 'blatt', syn='Spinat, Blattspinat')
f('Mangold', 'G230100', 'blatt')
f('Rucola', 'G130100', 'blatt', syn='Rauke')
f('Feldsalat', 'G104100', 'blatt', syn='Rapunzel, Nüsslisalat')
f('Blattsalat', 'G105100', 'blatt', syn='Kopfsalat, Salat, Pflücksalat')
f('Romanasalat', 'G107100', 'blatt', syn='Römersalat, Romana')
f('Eisbergsalat', 'G103100', 'blatt', syn='Eisberg')
f('Radicchio', 'G106100', 'blatt')
f('Chicorée', 'G101100', 'blatt', syn='Chicoree')
f('Endiviensalat', 'G102100', 'blatt', syn='Endivie, Escariol')
f('Kresse', 'G280100', 'kraeuter', syn='Gartenkresse')

# Pilze
f('Champignons', 'K701100', 'pilze', syn='Champignon, Pilze')
f('Austernpilze', 'K740100', 'pilze', syn='Austernseitling, Seitlinge, Pilze')
f('Shiitake', 'K724100', 'pilze', syn='Shiitakepilze, Pilze')
f('Pfifferlinge', 'K713100', 'pilze', syn='Eierschwammerl, Pilze')

# Kräuter und Würzen
f('Basilikum', 'G061000', 'kraeuter')
f('Petersilie', 'G250100', 'kraeuter')
f('Schnittlauch', 'G081100', 'kraeuter')
f('Dill', None, 'kraeuter')
f('Minze', None, 'kraeuter', syn='Pfefferminze')
f('Knoblauch', 'G490100', 'wuerze', cap=15, syn='Knoblauchzehe', piece=('Zehe', 3))
f('Ingwer', 'R211200', 'wuerze', cap=20)
f('Meerrettich', 'G630100', 'wuerze', cap=20, syn='Kren')
f('Kapern', 'G012902', 'wuerze', cap=20)
f('Zitronensaft', 'F601600', 'wuerze', cap=40, syn='Zitrone, Zitronen')
f('Limettensaft', 'F602600', 'wuerze', cap=40, syn='Limette, Limetten')
f('Balsamico', 'R125000', 'wuerze', cap=15, syn='Balsamicoessig, Aceto balsamico')
f('Apfelessig', 'R123100', 'wuerze', cap=30, syn='Essig')
f('Helle Misopaste', 'H862200', 'wuerze', cap=15, syn='Miso')
f('Rote Currypaste', None, 'wuerze', cap=15, syn='Currypaste, Curry')
f('Paprikapulver, geräuchert', None, 'wuerze', cap=5, syn='Paprikapulver, Pimentón')
f('Gemüsebrühe', 'X416243', 'wuerze', cap=600, syn='Brühe, Gemüsefond')

# Öle
f('Olivenöl', 'Q120000', 'fett', syn='Öl, natives Olivenöl extra, extra vergine, kaltgepresstes Olivenöl, Bertolli')
f('Rapsöl', 'Q180000', 'fett', syn='Öl, Rapskernöl, kaltgepresstes Rapsöl, Rapsöl mit Buttergeschmack, Albaöl, Rapso')
f('Leinöl', 'Q160000', 'fett', cap=15, syn='Öl')
f('Walnussöl', 'Q310000', 'fett', cap=15, syn='Öl')
f('Sesamöl', 'Q230000', 'fett', syn='Öl')
f('Kokosöl', 'Q550000', 'fett', light='y', cap=10, syn='Kokosfett', alts='Olivenöl; Rapsöl',
  why='Besteht überwiegend aus gesättigten Fettsäuren. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')

# Nüsse und Saaten
f('Walnusskerne', 'H120100', 'nuss', syn='Walnüsse, Walnuss', piece=('Kern', 5))
f('Mandeln', 'H210100', 'nuss', syn='Mandel', piece=('Stück', 1.2))
f('Haselnüsse', 'H130100', 'nuss', syn='Haselnuss, Haselnusskerne')
f('Pekannüsse', 'H160100', 'nuss', syn='Pekannuss')
f('Macadamia', 'H190100', 'nuss', syn='Macadamianüsse')
f('Paranüsse', 'H180100', 'nuss', cap=10, syn='Paranuss', why='Sehr selenreich, deshalb höchstens zwei Stück am Tag.')
f('Pistazien', 'H250100', 'nuss', syn='Pistazie')
f('Cashewkerne', 'H170100', 'nuss', syn='Cashew, Cashews')
f('Erdnüsse', 'H110600', 'nuss', light='y', cap=20, syn='Erdnuss', alts='Mandeln; Walnusskerne',
  why='Botanisch eine Hülsenfrucht mit viel Eiweiß. Eine Handvoll ist okay, Walnüsse und Mandeln passen besser.')
f('Kürbiskerne', 'H310100', 'nuss')
f('Sonnenblumenkerne', 'H430100', 'nuss')
f('Sesam', 'H420100', 'nuss')
f('Leinsamen', 'H410100', 'nuss', cap=20)
f('Chiasamen', 'H480100', 'nuss', cap=20, syn='Chia')
f('Tahin', 'Q901000', 'nuss', cap=30, syn='Sesammus, Tahini')
f('Mandelmus', 'H212800', 'nuss', cap=30)
f('Erdnussmus', 'H110800', 'nuss', light='y', cap=15, syn='Erdnussbutter', alts='Mandelmus; Tahin',
  why='Viel Eiweiß für wenig Menge. Mandelmus oder Tahin passen besser.')

# Oliven, Avocado, Kokos
f('Grüne Oliven', 'H510802', 'fettfrucht', syn='Oliven, Olive')
f('Schwarze Oliven', 'H520800', 'fettfrucht', syn='Oliven, Kalamata')
f('Avocado', 'F502100', 'fettfrucht', cap=120, piece=('Stück', 150))
f('Kokosmilch (vollfett)', 'H154000', 'fettfrucht', cap=100, syn='Kokosmilch')
f('Mandeldrink ungesüßt', 'H800000', 'getraenk', cap=250, syn='Mandelmilch, Mandelmilch ungesüßt, Alpro Mandel ungesüßt, Mandeldrink natur, Provamel Mandel, Reis-Mandel-Drink')

# Kartoffeln und Stärkegemüse (gelb)
f('Kartoffeln', 'K110100', 'knolle', syn='Kartoffel, Erdäpfel', alts='Blumenkohl; Knollensellerie', piece=('Stück', 100))
f('Süßkartoffel', 'K420100', 'knolle', cap=150, syn='Süßkartoffeln, Batate', alts='Hokkaido-Kürbis; Karotten')

# Hülsenfrüchte (gelb)
f('Weiße Bohnen (gegart)', 'H740132', 'huelsen', syn='weiße Bohnen, Cannellini', alts='Zucchini; Champignons')
f('Kichererbsen (gegart)', 'G770432', 'huelsen', syn='Kichererbsen', alts='Blumenkohl; Champignons')
f('Rote Linsen (gegart)', 'H730032', 'huelsen', syn='rote Linsen, Linsen', alts='Hokkaido-Kürbis; Karotten')
f('Linsen (gegart)', 'H730132', 'huelsen', syn='Linsen, Tellerlinsen, Berglinsen')
f('Kidneybohnen (gegart)', 'H742902', 'huelsen', syn='Kidneybohnen, rote Bohnen', alts='Rote Paprika; Aubergine')
f('Edamame', 'G750100', 'soja', syn='Sojabohnen', alts='Zuckerschoten; Erbsen (TK)')
f('Tofu', 'H861000', 'soja', syn='Tofu natur, Naturtofu, fester Tofu', alts='Austernpilze; Champignons',
  why='Pflanzlich, aber sehr eiweißreich. Prof. Dr. Longos Tage 2 bis 5 sehen nur etwa 9 % Eiweiß vor.')

# Getreide (gelb)
f('Hirse (gegart)', 'C334032', 'getreide', syn='Hirse', alts='Blumenkohl; Knollensellerie')
f('Quinoa (gegart)', 'C118032', 'getreide', syn='Quinoa', alts='Blumenkohl; Hirse (gegart)')
f('Buchweizen (gegart)', 'C320032', 'getreide', syn='Buchweizen', alts='Blumenkohl; Hirse (gegart)')
f('Vollkornreis (gegart)', 'C351032', 'getreide', syn='Reis, Naturreis, Vollkornreis', alts='Blumenkohl; Hirse (gegart)')
f('Reis (gegart)', 'C352032', 'getreide', cap=80, syn='Reis, weißer Reis, Basmati, Jasminreis', alts='Blumenkohl; Hirse (gegart)')
f('Bulgur (gegart)', 'C119132', 'getreide', cap=80, syn='Bulgur', alts='Hirse (gegart); Blumenkohl')
f('Couscous (gegart)', 'C119232', 'getreide', cap=80, syn='Couscous', alts='Hirse (gegart); Blumenkohl')
f('Haferflocken', 'C133000', 'getreide', cap=30, syn='Hafer, Porridge', alts='Leinsamen; Walnusskerne')
f('Vollkornbrot', 'B121000', 'getreide', cap=40, syn='Brot, Roggenbrot, Dinkelbrot, Vollkorntoast', alts='Gurke; Kohlrabi',
  why='Eine dünne Scheibe passt an Tag 1. Für Brot sieht Prof. Dr. Longo sonst kaum Platz vor.')

# Obst (gelb)
f('Apfel', 'F110100', 'obst', syn='Äpfel', alts='Heidelbeeren; Gurke', piece=('Stück', 150))
f('Birne', 'F130100', 'obst', syn='Birnen', alts='Apfel; Heidelbeeren', piece=('Stück', 160))
f('Orange', 'F603100', 'obst', syn='Orangen, Apfelsine', alts='Zitronensaft; Heidelbeeren', piece=('Stück', 150))
f('Mandarine', 'F606100', 'obst', syn='Mandarinen, Clementine', alts='Orange; Heidelbeeren', piece=('Stück', 70))
f('Grapefruit', 'F604100', 'obst', alts='Orange; Heidelbeeren')
f('Heidelbeeren', 'F304100', 'obst', cap=100, syn='Blaubeeren, Beeren')
f('Himbeeren', 'F302100', 'obst', cap=100, syn='Beeren')
f('Erdbeeren', 'F301100', 'obst', cap=150, syn='Beeren')
f('Kiwi', 'F514100', 'obst', alts='Erdbeeren; Heidelbeeren', piece=('Stück', 75))
f('Banane', 'F503100', 'obst', cap=60, syn='Bananen', alts='Heidelbeeren; Apfel', piece=('Stück', 120),
  why='Viel Zucker und Stärke. Eine halbe kleine Banane passt, Beeren passen besser.')
f('Mango', 'F516100', 'obst', cap=80, alts='Erdbeeren; Orange')

# Passt nicht (rot)
f('Datteln', 'F504400', 'suess', syn='Dattel, Trockenobst', alts='Apfel; Heidelbeeren',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Zucker', 'S111000', 'suess', syn='Haushaltszucker, Rohrzucker, Raffinade, Puderzucker, Gelierzucker, Vanillezucker')
f('Honig', 'S120000', 'suess', syn='Ahornsirup, Sirup')
f('Schokolade', 'S530000', 'suess', syn='Milchschokolade, Süßigkeiten, Riegel', alts='Walnusskerne; Heidelbeeren; Mandeln')
f('Kuchen', 'D422600', 'suess', syn='Rührkuchen, Gebäck, Torte', alts='Apfel; Walnusskerne')
f('Weißbrot', 'B311000', 'weissmehl', syn='Toast, Brötchen, Semmel, Baguette')
f('Nudeln', 'X432142', 'weissmehl', syn='Pasta, Spaghetti, Teigwaren', alts='Zucchini; Kartoffeln; Hirse (gegart)',
  why='Viel Stärke auf kleinem Raum. Zucchini-Nudeln oder eine kleine Portion Kartoffeln passen besser.')
f('Croissant', 'D771600', 'weissmehl', syn='Gebäck, Plunder')
f('Kartoffelchips', 'K280100', 'weissmehl', syn='Chips', alts='Grünkohl; Kichererbsen (gegart)',
  why='Frittiert, gesalzen, wenig Gemüse. Grünkohl-Chips aus dem Ofen liefern das Knuspern ohne den Ballast.')
f('Pommes frites', 'K130492', 'weissmehl', syn='Pommes', alts='Süßkartoffel; Kartoffeln')
f('Hähnchen', 'V416100', 'tier', syn='Huhn, Hühnchen, Hähnchenbrust, Chicken, Pute, Geflügel')
f('Rindfleisch', 'U010100', 'tier', syn='Rind, Hackfleisch, Hack, Steak')
f('Schweinefleisch', 'U541100', 'tier', syn='Schwein, Schnitzel')
f('Salami', 'W140000', 'tier', syn='Wurst, Aufschnitt')
f('Kochschinken', 'W424000', 'tier', syn='Schinken')
f('Lachs', 'T410100', 'tier', syn='Fisch, Räucherlachs', alts='Walnusskerne; Leinöl; Leinsamen',
  why='Fisch ist tierisches Eiweiß. Omega-3 bekommst Du im Scheinfasten aus Walnüssen und Leinöl.')
f('Thunfisch', 'T121902', 'tier', syn='Fisch, Thunfischdose', alts='Kichererbsen (gegart); Walnusskerne')
f('Garnelen', 'T753100', 'tier', syn='Shrimps, Krabben, Scampi', alts='Austernpilze; Champignons')
f('Eier', 'E111100', 'tier', syn='Ei, Hühnerei, Spiegelei, Rührei', alts='Kichererbsen (gegart); Champignons; Avocado')
f('Milch', 'M111300', 'milch', syn='Kuhmilch, Vollmilch, Frischmilch, Weidemilch, Heumilch, Bio-Milch', alts='Mandeldrink ungesüßt')
f('Joghurt', 'M141300', 'milch', syn='Naturjoghurt, Joghurt 3,5 %, Vollmilchjoghurt, Bio-Joghurt', alts='Kokosmilch (vollfett); Cashewkerne')
f('Quark', 'M713100', 'milch', syn='Magerquark, Topfen, Speisequark', alts='Tahin; Cashewkerne')
f('Käse', 'M402600', 'milch', syn='Gouda, Schnittkäse, Scheibenkäse, Reibekäse, Leerdammer, Maasdamer', alts='Cashewkerne; Grüne Oliven; Tahin')
f('Mozzarella', 'M032100', 'milch', syn='Burrata', alts='Avocado; Cashewkerne')
f('Feta', 'M012200', 'milch', syn='Schafskäse, Hirtenkäse', alts='Grüne Oliven; Kapern; Cashewkerne')
f('Butter', 'Q611000', 'milch', syn='Süßrahmbutter, Sauerrahmbutter, gesalzene Butter, Kerrygold, Weidebutter', alts='Olivenöl; Rapsöl')
f('Sahne', 'M173800', 'milch', syn='Schlagsahne, Rahm, Kochsahne, Sahne zum Kochen, Cremefine, Sprühsahne', alts='Kokosmilch (vollfett); Cashewkerne')
# Kaffee: Die Studien (Brandhorst 2015, Wei 2017) sagen nichts dazu. ProLon-Hilfecenter (L-Nutra): außer Wasser nichts zusätzlich,
# wenn nötig höchstens eine kleine Tasse Kaffee pro Tag ohne Zucker oder Zusätze. Kleine Tasse = 150 ml (unsere Annahme).
f('Kaffee', 'N410100', 'getraenk', light='y', cap=150, syn='Espresso, Filterkaffee, schwarzer Kaffee', alts='Kräutertee',
  why='Wenn es ohne nicht geht: eine kleine Tasse schwarz am Tag, ohne Milch und Zucker. So empfiehlt es der Hersteller des Fertigprodukts ProLon.')
f('Bier', 'P163000', 'drink', syn='Pils, Alkohol')
f('Wein', 'P2A3000', 'drink', syn='Rotwein, Weißwein, Sekt, Alkohol')
f('Orangensaft', 'F603600', 'drink', syn='Saft, Fruchtsaft, Apfelsaft', alts='Orange; Kräutertee')
f('Cola', 'N330000', 'drink', syn='Limonade, Softdrink, Eistee, Energydrink')
f('Kräutertee', 'N720100', 'getraenk', syn='Tee, Pfefferminztee, Kamillentee, Früchtetee')


# ---- Erweiterung November 2026 ----
# Gemüse, Sprossen, Pilze
f('Spitzkohl', 'G344100', 'gemuese')
f('Romanesco', 'G350100', 'gemuese')
f('Schwarzwurzeln', 'G650100', 'gemuese', syn='Schwarzwurzel')
f('Topinambur', 'K430100', 'gemuese', syn='Erdartischocke')
f('Petersilienwurzel', 'G670100', 'gemuese', syn='Wurzelpetersilie')
f('Weiße Rübe', 'G614100', 'gemuese', syn='Mairübe, Teltower Rübchen, Navet')
f('Rote Bete (roh)', 'G613100', 'gemuese', syn='Rote Bete roh, Rote Rübe roh')
f('Spinat (TK)', 'G211200', 'blatt', syn='Rahmspinat, Tiefkühlspinat, Spinat tiefgekühlt')
f('Rhabarber', 'F081100', 'gemuese')
f('Löwenzahn', 'G262100', 'blatt', syn='Löwenzahnblätter')
f('Portulak', 'G460100', 'blatt', syn='Postelein, Winterportulak')
f('Bambussprossen', 'H610902', 'gemuese', syn='Bambus')
f('Mungbohnensprossen', 'H650100', 'gemuese', syn='Sprossen, Keimlinge, Sojasprossen aus Mungbohnen')
f('Sojasprossen', 'H620100', 'gemuese', syn='Sprossen, Keimlinge')
f('Alfalfasprossen', 'H640100', 'gemuese', cap=50, syn='Sprossen, Keimlinge, Luzerne')
f('Chili', 'G554100', 'wuerze', cap=20, syn='Chilischote, Peperoncini, Pfefferschote, Jalapeño')
f('Peperoni (eingelegt)', 'G550802', 'gemuese', cap=50, syn='Peperoni, Pfefferoni, Pfefferschoten eingelegt')
f('Salzgurken', 'G890702', 'gemuese', cap=100, syn='Salzdillgurke, Dillgurke, fermentierte Gurken')
f('Tomaten (Dose)', 'G568900', 'gemuese', cap=300, syn='geschälte Tomaten, Dosentomaten, gehackte Tomaten, Pelati')
f('Getrocknete Tomaten', 'G560400', 'gemuese', light='y', cap=15, syn='Tomaten getrocknet, sonnengetrocknete Tomaten',
  alts='Tomaten; Tomatenmark', why='Konzentriert: drei, vier Stück bringen schon so viel Zucker wie eine ganze Schale frischer Tomaten.')
f('Champignons (Dose)', 'K701902', 'pilze', syn='Champignons Glas, Pilze Dose')
f('Steinpilze', 'K718100', 'pilze', syn='Herrenpilz, Pilze')
f('Nori', 'G995000', 'wuerze', cap=5, syn='Algen, Seetang, Noriblatt, Sushi-Algen', piece=('Blatt', 3))
f('Bärlauch', 'G492100', 'kraeuter', syn='wilder Knoblauch')
f('Koriander', None, 'kraeuter', syn='Koriandergrün, Cilantro', n=(23, 2.1, 0.5, 3.7, 0.9))
f('Thymian', None, 'kraeuter', cap=10, n=(101, 5.6, 1.7, 24.5, 0))
f('Rosmarin', None, 'kraeuter', cap=10, n=(131, 3.3, 5.9, 20.7, 0))
f('Oregano (getrocknet)', None, 'wuerze', cap=5, syn='Oregano, Majoran, Kräuter der Provence, italienische Kräuter', n=(265, 9.0, 4.3, 68.9, 4.1))
f('Kurkuma', None, 'wuerze', cap=5, syn='Gelbwurz, Curcuma', n=(312, 9.7, 3.3, 67.1, 3.2))
f('Kreuzkümmel', None, 'wuerze', cap=5, syn='Cumin, Kumin', n=(375, 17.8, 22.3, 44.2, 2.3))
f('Currypulver', None, 'wuerze', cap=5, syn='Curry, Garam Masala', n=(325, 14.3, 14.0, 55.8, 2.8))
f('Zimt', None, 'wuerze', cap=5, syn='Zimtpulver, Ceylon-Zimt', n=(247, 4.0, 1.2, 80.6, 2.2))
f('Chiliflocken', None, 'wuerze', cap=3, syn='Cayennepfeffer, Chilipulver, Pul Biber', n=(318, 12.0, 17.3, 56.6, 10.3))
f('Muskatnuss', None, 'wuerze', cap=2, syn='Muskat', n=(525, 5.8, 36.3, 49.3, 28.5))
f('Pfeffer', 'R258100', 'wuerze', cap=5, syn='schwarzer Pfeffer, Pfefferkörner')
f('Salz', 'R114000', 'wuerze', cap=6, syn='Jodsalz, Meersalz, Speisesalz',
  why='Etwas Salz ist okay, die Brühe bringt schon welches mit. Mehr als ein Teelöffel am Tag sollte es nicht werden.')
f('Senf', 'R132000', 'wuerze', cap=15, syn='Dijonsenf, Senf mittelscharf')
f('Sojasauce', 'R143000', 'wuerze', cap=15, syn='Sojasoße, Tamari, Shoyu')
f('Hefeflocken', None, 'wuerze', cap=10, syn='Edelhefeflocken, Nährhefe',
  why='Schmecken käsig und würzig, sind aber zur Hälfte Eiweiß. Ein Esslöffel reicht.', n=(400, 50.0, 5.0, 33.0, 0))
f('Weinessig', 'R121000', 'wuerze', cap=30, syn='Weißweinessig, Rotweinessig, Branntweinessig, Kräuteressig, Sherryessig, Himbeeressig, Tafelessig, Essigessenz')
f('Zitrone', 'F601100', 'wuerze', cap=60, syn='Zitronen, Zitronenschale', piece=('Stück', 60))
f('Limette', 'F602100', 'wuerze', cap=60, syn='Limetten', piece=('Stück', 45))
f('Ketchup', 'R141100', 'suess', syn='Tomatenketchup, Curryketchup, BBQ-Sauce', alts='Tomatenmark; Tomaten, passiert',
  why='Ein Fünftel Ketchup ist Zucker. Tomatenmark mit etwas Essig und Gewürzen schmeckt ähnlich.')
f('Pesto', 'X372012', 'milch', syn='Pesto verde, Basilikumpesto, Pesto Genovese', alts='Basilikum; Olivenöl; Pinienkerne',
  why='Klassisches Pesto enthält Parmesan. Basilikum mit Olivenöl und ein paar Pinienkernen gemixt passt.')

# Öle
f('Kürbiskernöl', 'Q250000', 'fett', cap=15, syn='Öl')
f('Hanföl', 'Q170000', 'fett', cap=15, syn='Öl')
f('Sonnenblumenöl', 'Q320000', 'fett', syn='Öl')
f('Erdnussöl', 'Q210000', 'fett', syn='Öl')
f('Traubenkernöl', 'Q330000', 'fett', syn='Öl')
f('Margarine', 'Q4A4000', 'fett', light='y', cap=10, syn='vegane Margarine, Pflanzenmargarine, Streichfett, Rama, Sonnenblumenmargarine, Deli Reform, Becel', alts='Olivenöl; Rapsöl',
  why='Pflanzlich, aber stark verarbeitet. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')

# Nüsse, Saaten, Kokos
f('Pinienkerne', 'H320100', 'nuss', syn='Pinienkern')
f('Hanfsamen', None, 'nuss', syn='Hanfsamen geschält, Hanfherzen', n=(553, 31.6, 48.8, 8.7, 1.5))
f('Mohn', 'H450100', 'nuss', cap=10, syn='Mohnsamen')
f('Cashewmus', 'F960800', 'nuss', cap=30, syn='Cashewkernmus, Cashewbutter')
f('Haselnussmus', 'H130800', 'nuss', cap=30, syn='Haselnussbutter')
f('Kokosraspeln', 'H150400', 'fettfrucht', light='y', cap=15, syn='Kokosflocken, Kokosraspel', alts='Walnusskerne; Mandeln',
  why='Viel gesättigtes Fett wie beim Kokosöl. Als Topping okay, Nüsse passen besser.')
f('Kokosnuss (frisch)', 'H150100', 'fettfrucht', light='y', cap=30, syn='Kokosnuss, Kokos', alts='Avocado; Walnusskerne',
  why='Viel gesättigtes Fett wie beim Kokosöl. Ein kleines Stück ist okay.')

# Hülsenfrüchte, Soja, Fleischersatz
f('Kichererbsen (Dose)', 'H720902', 'huelsen', syn='Kichererbsen Konserve, Kichererbsen abgetropft', alts='Blumenkohl; Champignons')
f('Mungbohnen (gegart)', 'H770132', 'huelsen', syn='Mungbohnen, Mungobohnen', alts='Zuckerschoten; Champignons')
f('Trockenerbsen (gegart)', 'G760432', 'huelsen', syn='Schälerbsen, gelbe Erbsen, Erbsensuppe', alts='Zucchini; Kartoffeln')
f('Hummus', 'H960000', 'huelsen', cap=50, syn='Humus, Kichererbsenmus, Kichererbsendip', alts='Tahin; Avocado',
  why='Kichererbsen mit Tahin und Öl: lecker, aber gehaltvoll. Zwei Esslöffel passen gut.')
f('Falafel', 'Y9A1050', 'huelsen', light='r', syn='Kichererbsenbällchen', alts='Kichererbsen (gegart); Hummus',
  why='Frittiert. Ofen-Kichererbsen oder Hummus liefern den Geschmack ohne Fettbad.')
f('Seidentofu', 'H861100', 'soja', cap=100, syn='Silken Tofu', alts='Kokosmilch (vollfett); Avocado')
f('Sojajoghurt', 'H844000', 'soja', cap=100, syn='Joghurtalternative, Sojaghurt, Sojagurt, veganer Joghurt, Alpro Natur, Soja-Joghurtalternative ungesüßt, Sojade, Provamel', alts='Kokosmilch (vollfett); Avocado',
  why='Ungesüßt eine gute Basis für Dressings. Viel davon bringt zu viel Eiweiß.')
f('Sojadrink', 'H841100', 'soja', cap=200, syn='Sojamilch, Sojamilch ungesüßt, Alpro Soja ungesüßt, Provamel, Sojadrink natur', alts='Mandeldrink ungesüßt; Haferdrink',
  why='Ungesüßt okay, aber eiweißreicher als Mandel- oder Haferdrink.')
f('Tempeh', None, 'eiweiss', syn='Tempe', n=(192, 20.3, 10.8, 7.6, 0))
f('Seitan', 'C558000', 'eiweiss', syn='Weizeneiweiß, Weizengluten')
f('Sojagranulat', 'H765000', 'eiweiss', syn='Sojaschnetzel, Sojahack, Sojafleisch, texturiertes Soja')
f('Veggie-Wurst', 'H930000', 'eiweiss', syn='vegane Wurst, vegetarische Wurst, Wurstalternative, Fleischersatz, Veggie-Aufschnitt')
f('Veggie-Burger', 'H910300', 'eiweiss', syn='vegetarische Bratwurst, Veggie-Bratwurst, Burger-Patty vegan, Veggie-Frikadelle')

# Pflanzendrinks und Getränke
f('Haferdrink', 'C660000', 'getraenk', light='y', cap=200, syn='Hafermilch, Haferdrink ungesüßt, Oatly, Kölln Haferdrink, Haferdrink natur, Hafer ohne Zucker', alts='Mandeldrink ungesüßt',
  why='Der Hafer bringt natürlichen Zucker mit. Ein Schuss im Tee passt, Mandeldrink ist zuckerärmer.')
f('Reisdrink', 'C650000', 'getraenk', light='y', cap=100, syn='Reismilch', alts='Mandeldrink ungesüßt',
  why='Schmeckt süß, weil die Stärke beim Herstellen zu Zucker wird. Mandeldrink ist die bessere Wahl.')
f('Kokoswasser', 'H151000', 'getraenk', light='y', cap=200, alts='Wasser; Kräutertee',
  why='Leicht süß. Ein Glas ist okay, Wasser und Kräutertee sind die Basis.')
f('Gemüsesaft', 'G090600', 'getraenk', light='y', cap=200, syn='Tomatensaft, Möhrensaft, Karottensaft, Rote-Bete-Saft', alts='Gemüsebrühe; Kräutertee',
  why='Ein Glas passt, im Saft fehlt aber die Sättigung vom ganzen Gemüse.')
f('Wasser', 'N110000', 'getraenk', cap=3000, syn='Trinkwasser, Leitungswasser')
f('Mineralwasser', 'N128000', 'getraenk', cap=3000, syn='Sprudel, Sprudelwasser, stilles Wasser')
# Schwarzer und grüner Tee: Prof. Dr. Longos Buch nennt laut Sekundärquellen ungesüßten Tee ohne Einschränkung auf Kräutertee.
# Die Koffeingrenze wie bei Kaffee ist unsere Ableitung.
f('Grüner Tee', 'N610100', 'getraenk', light='y', cap=250, syn='Grüntee, Matcha', alts='Kräutertee',
  why='Ungesüßt passt eine Tasse. Enthält Koffein, deshalb am selben Tag lieber Tee oder Kaffee, nicht beides.')
f('Schwarzer Tee', 'N630000', 'getraenk', light='y', cap=250, syn='Schwarztee, Earl Grey', alts='Kräutertee',
  why='Ungesüßt passt eine Tasse. Enthält Koffein, deshalb am selben Tag lieber Tee oder Kaffee, nicht beides.')
f('Smoothie', 'F032600', 'drink', syn='Fruchtsmoothie, grüner Smoothie', alts='Heidelbeeren; Gurke',
  why='Püriertes Obst ist schnell getrunkener Zucker. Ganze Beeren machen satter.')

# Cracker, Waffeln, Brot, Getreide
f('Maiswaffeln', 'C533100', 'knusper', syn='Maiscracker, Maiswaffel, Mais-Cracker, Maiskekse', piece=('Waffel', 8))
f('Reiswaffeln', 'C532700', 'knusper', syn='Reiscracker, Reiswaffel, Puffreis, Reis-Cracker', piece=('Waffel', 8))
f('Knäckebrot', 'B6A2100', 'knusper', syn='Roggenknäcke, Vollkornknäckebrot, Knäcke', piece=('Scheibe', 10))
f('Knäckebrot mit Saaten', 'B6A5100', 'knusper', syn='Dinkelknäcke, Saatenknäcke, Körnerknäcke', piece=('Scheibe', 12))
f('Popcorn', 'C533000', 'knusper', cap=15, syn='Popcorn ungesüßt, Puffmais',
  why='Ungesüßt und selbst gepoppt ein guter Knabberersatz. Eine kleine Schale reicht.')
f('Pumpernickel', 'B780500', 'getreide', cap=40, syn='Schwarzbrot', alts='Knäckebrot; Gurke',
  why='Eine dünne Scheibe passt an Tag 1. Für Brot sieht Prof. Dr. Longo sonst kaum Platz vor.')
f('Amaranth (gegart)', 'C335032', 'getreide', syn='Amaranth', alts='Hirse (gegart); Blumenkohl')
f('Grünkern (gegart)', 'C311032', 'getreide', syn='Grünkern', alts='Hirse (gegart); Blumenkohl')
f('Dinkel (gegart)', 'C236032', 'getreide', syn='Dinkel, Dinkelreis, Ebly', alts='Hirse (gegart); Blumenkohl')
f('Graupen (gegart)', 'C148032', 'getreide', syn='Gerste, Perlgraupen, Rollgerste', alts='Hirse (gegart); Blumenkohl')
f('Polenta (gegart)', 'C526000', 'getreide', syn='Polenta, Maisgrieß, Maisbrei', alts='Hirse (gegart); Kartoffeln')
f('Vollkornnudeln (gegart)', 'E500032', 'getreide', cap=80, syn='Vollkornnudeln, Vollkornpasta, Dinkelnudeln', alts='Zucchini; Hirse (gegart)',
  why='Eine kleine Portion passt. Zucchini-Nudeln strecken sie auf einen vollen Teller.')
f('Reisnudeln (gegart)', 'C559032', 'getreide', cap=80, syn='Reisnudeln, Reisbandnudeln', alts='Zucchini; Glasnudeln (gegart)')
f('Glasnudeln (gegart)', 'H030432', 'getreide', cap=80, syn='Glasnudeln, Mungbohnennudeln', alts='Zucchini; Mungbohnensprossen')
f('Apfelmus ungesüßt', 'F923900', 'obst', cap=100, syn='Apfelmus, Apfelmark, Apfelkompott', alts='Apfel; Heidelbeeren')

# Obst
f('Wassermelone', 'F535100', 'obst', syn='Melone', alts='Erdbeeren; Gurke')
f('Honigmelone', 'F532100', 'obst', syn='Melone, Cantaloupe, Netzmelone, Zuckermelone', alts='Erdbeeren; Gurke')
f('Ananas', 'F501100', 'obst', cap=100, alts='Erdbeeren; Orange')
f('Weintrauben', 'F310100', 'obst', cap=80, syn='Trauben, Weintraube', alts='Heidelbeeren; Erdbeeren')
f('Pfirsich', 'F203100', 'obst', syn='Pfirsiche', alts='Erdbeeren; Himbeeren', piece=('Stück', 130))
f('Nektarine', 'F202100', 'obst', syn='Nektarinen', alts='Erdbeeren; Himbeeren', piece=('Stück', 130))
f('Pflaumen', 'F220100', 'obst', syn='Pflaume, Zwetschgen, Zwetschken', alts='Heidelbeeren; Himbeeren', piece=('Stück', 35))
f('Kirschen', 'F211100', 'obst', cap=80, syn='Süßkirschen, Kirsche', alts='Himbeeren; Heidelbeeren')
f('Sauerkirschen', 'F212100', 'obst', cap=80, syn='Weichseln', alts='Himbeeren; Johannisbeeren')
f('Aprikose', 'F201100', 'obst', syn='Aprikosen, Marille, Marillen', alts='Erdbeeren; Himbeeren', piece=('Stück', 40))
f('Johannisbeeren', 'F321100', 'obst', syn='Ribisel, Beeren')
f('Brombeeren', 'F303100', 'obst', syn='Beeren')
f('Stachelbeeren', 'F305100', 'obst', syn='Beeren')
f('Granatapfel', 'F506100', 'obst', cap=60, syn='Granatapfelkerne', alts='Himbeeren; Johannisbeeren')
f('Feigen (frisch)', 'F505100', 'obst', cap=80, syn='Feige, Feigen', alts='Himbeeren; Brombeeren')
f('Papaya', 'F517100', 'obst', cap=100, alts='Erdbeeren; Orange')
f('Physalis', 'F552100', 'obst', cap=50, syn='Kapstachelbeere, Andenbeere', alts='Himbeeren; Erdbeeren')

# Passt nicht (rot)
f('Rosinen', 'F840100', 'suess', syn='Sultaninen, Korinthen', alts='Heidelbeeren; Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Getrocknete Aprikosen', 'F201400', 'suess', syn='Trockenaprikosen, Trockenobst, Trockenfrüchte', alts='Aprikose; Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Cranberries (getrocknet)', 'F414400', 'suess', syn='Cranberries, Moosbeeren, Goji', alts='Himbeeren; Johannisbeeren',
  why='Getrocknet und meist zusätzlich gezuckert.')
f('Müsli', 'C512300', 'suess', syn='Früchtemüsli, Bircher Müsli', alts='Haferflocken; Heidelbeeren; Walnusskerne',
  why='Die Trockenfrüchte machen ein Fünftel Zucker. Ein paar Haferflocken mit frischen Beeren und Nüssen passen.')
f('Knuspermüsli', 'C514200', 'suess', syn='Granola, Crunchy Müsli, Schokomüsli', alts='Haferflocken; Walnusskerne')
f('Cornflakes', 'C515000', 'weissmehl', syn='Frühstücksflocken, Choco Pops, Frosties', alts='Haferflocken; Heidelbeeren')
f('Müsliriegel', 'S830000', 'suess', syn='Riegel, Fitnessriegel, Proteinriegel, Energieriegel', alts='Walnusskerne; Mandeln; Apfel')
f('Gummibärchen', 'S361000', 'suess', syn='Fruchtgummi, Weingummi, Bonbons, Lakritz', alts='Heidelbeeren; Erdbeeren')
f('Kekse', 'D630400', 'suess', syn='Butterkekse, Plätzchen, Cookies', alts='Maiswaffeln; Walnusskerne')
f('Marmelade', 'S132000', 'suess', syn='Konfitüre, Gelee, Fruchtaufstrich', alts='Himbeeren; Apfelmus ungesüßt')
f('Nuss-Nougat-Creme', 'S145000', 'suess', syn='Nutella, Schokoaufstrich', alts='Mandelmus; Haselnussmus')
f('Speiseeis', 'S243000', 'suess', syn='Eis, Eiscreme, Softeis', alts='Heidelbeeren; Kokosmilch (vollfett)')
f('Cracker', 'D050000', 'weissmehl', syn='Kräcker, Butterkräcker, TUC, Salzcracker', alts='Maiswaffeln; Knäckebrot; Reiswaffeln',
  why='Weißmehl plus viel Fett. Mais- oder Reiswaffeln knuspern leichter.')
f('Salzstangen', 'D064000', 'weissmehl', syn='Salzbrezeln, Brezeln, Laugengebäck', alts='Maiswaffeln; Grünkohl')
f('Tortilla-Chips', 'C546000', 'weissmehl', syn='Nachos, Tortillachips, Maischips', alts='Maiswaffeln; Grünkohl',
  why='Frittiert und gesalzen. Maiswaffeln oder Grünkohl-Chips aus dem Ofen knuspern ohne Fettbad.')
f('Wraps', 'B783012', 'weissmehl', syn='Tortilla, Weizentortilla, Wrap, Fladenbrot', alts='Romanasalat; Chinakohl',
  why='Weißmehlfladen. Große Salat- oder Chinakohlblätter sind die Wraps fürs Scheinfasten.')
f('Pizza', 'X912033', 'weissmehl', syn='Pizza Margherita, Flammkuchen', alts='Zucchini; Tomaten; Champignons')
f('Mischbrot', 'B271000', 'weissmehl', syn='Graubrot, Bauernbrot, Sauerteigbrot', alts='Knäckebrot; Vollkornbrot')
f('Burger', 'Y911260', 'tier', syn='Hamburger, Cheeseburger, Fast Food', alts='Champignons; Kichererbsen (gegart); Avocado')
f('Döner', 'V422072', 'tier', syn='Kebab, Gyros, Dürüm', alts='Champignons; Kichererbsen (gegart)')
f('Bratwurst', 'Y021312', 'tier', syn='Würstchen, Wiener, Currywurst, Grillwurst', alts='Champignons; Austernpilze')
f('Speck', 'W411300', 'tier', syn='Bacon, Schinkenspeck, Pancetta', alts='Paprikapulver, geräuchert; Champignons')
f('Leberwurst', 'W880100', 'tier', syn='Streichwurst, Teewurst, Mettwurst', alts='Hummus; Tahin')
f('Fischstäbchen', 'T930100', 'tier', syn='Backfisch, Fisch paniert', alts='Kichererbsen (gegart); Champignons')
f('Frischkäse', 'M710800', 'milch', syn='Doppelrahmfrischkäse, Philadelphia, Exquisa, Kräuterfrischkäse', alts='Hummus; Cashewmus')
f('Parmesan', 'M306400', 'milch', syn='Grana Padano, Pecorino, Hartkäse', alts='Hefeflocken; Cashewkerne')
f('Hüttenkäse', 'M711100', 'milch', syn='körniger Frischkäse, Cottage Cheese', alts='Sojajoghurt; Avocado')
f('Kefir', 'M130300', 'milch', syn='Milchkefir, Kalinka', alts='Mandeldrink ungesüßt; Sojajoghurt')
f('Buttermilch', 'M150000', 'milch', syn='Molke', alts='Mandeldrink ungesüßt')


# ---- Erweiterung Produkte (14.11.2026): Tiefkühlware, Konserven, Fertigprodukte, Getränke, Aufstriche, Tabu-Produkte ----
# Markennamen stehen nur als Suchbegriffe in syn. Angezeigt und gerechnet wird immer das allgemeine Produkt mit BLS-Werten.
TK = 'tiefgekühlt, Tiefkühl, TK, gefroren'
DO = 'Konserve, Dose, Glas'

# Tiefkühlgemüse
f('Brokkoli (TK)', 'G312200', 'gemuese', syn=f'Broccoli {TK}, Iglo, Frosta')
f('Blumenkohl (TK)', 'G311200', 'gemuese', syn=f'Karfiol {TK}')
f('Rosenkohl (TK)', 'G332200', 'gemuese', syn=f'Kohlsprossen {TK}')
f('Grüne Bohnen (TK)', 'G710200', 'gemuese', syn=f'Bohnen {TK}, Brechbohnen, Prinzessbohnen')
f('Grünkohl (TK)', 'G322200', 'gemuese', syn=f'Kale {TK}')
f('Karotten (TK)', 'G620200', 'gemuese', syn=f'Möhren {TK}, Karotten gefroren')
f('Lauch (TK)', 'G470200', 'gemuese', syn=f'Porree {TK}')
f('Spargel (TK)', 'G450200', 'gemuese', syn=TK)
f('Zuckerschoten (TK)', 'G761200', 'gemuese', syn=f'Kaiserschoten {TK}')
f('Zwiebeln (TK)', 'G480200', 'gemuese', cap=150, syn=f'Zwiebelwürfel {TK}')
f('Mais (TK)', 'G570200', 'knolle', cap=80, syn=f'Zuckermais {TK}', alts='Rote Paprika; Erbsen (TK)')
f('Dicke Bohnen (TK)', 'G730200', 'huelsen', syn=f'Saubohnen, Ackerbohnen, Favabohnen {TK}', alts='Grüne Bohnen (TK); Zuckerschoten')
f('Suppengemüse (TK)', 'G093200', 'gemuese', syn=f'Suppengrün, Suppenkraut {TK}')
f('Kaisergemüse (TK)', 'G090200', 'gemuese', syn=f'Buttergemüse, Gemüsemischung, Mischgemüse {TK}')
f('Asia-Gemüse (TK)', 'G994200', 'gemuese', syn=f'Wokgemüse, Pfannengemüse, Gemüsemischung asiatisch, Chop Suey {TK}')
f('Erbsen und Möhren (TK)', 'G992200', 'gemuese', light='y', cap=200, syn=f'Erbsen-Karotten, Gemüsemischung {TK}', alts='Kaisergemüse (TK); Brokkoli (TK)',
  why='Die Erbsen bringen Eiweiß mit. Eine Portion passt gut.')
f('Mexiko-Gemüse (TK)', 'G993200', 'gemuese', light='y', cap=200, syn=f'Gemüsemischung mexikanisch, Mexikopfanne {TK}', alts='Kaisergemüse (TK); Asia-Gemüse (TK)',
  why='Mais und Bohnen bringen Stärke und Eiweiß mit. Eine Portion passt gut.')
f('Leipziger Allerlei (TK)', 'G920200', 'gemuese', light='y', cap=200, syn=f'Gemüsemischung, Mischgemüse {TK}', alts='Kaisergemüse (TK); Brokkoli (TK)',
  why='Die Erbsen bringen Eiweiß mit. Eine Portion passt gut.')
f('Champignons (TK)', 'K701200', 'pilze', syn=f'Pilze {TK}')
f('Mischpilze (TK)', 'K750200', 'pilze', syn=f'Pilzmischung, Waldpilze, Pilze {TK}')
f('Petersilie (TK)', 'G250200', 'kraeuter', syn=f'Kräuter {TK}, TK-Kräuter, 8-Kräuter')
f('Beerenmischung (TK)', 'F092100', 'obst', cap=100, syn=f'Beeren {TK}, Waldbeeren, Beerenmix, Tiefkühlbeeren, Beerenfrüchte')

# Gemüse aus Dose und Glas
f('Grüne Bohnen (Dose)', 'G710902', 'gemuese', syn=f'Bohnen, Brechbohnen {DO}, Bonduelle')
f('Erbsen (Dose)', 'G760902', 'huelsen', cap=120, syn=f'Erbsen {DO}, junge Erbsen', alts='Zuckerschoten; Brokkoli')
f('Erbsen und Möhren (Dose)', 'G992902', 'gemuese', light='y', cap=200, syn=f'Erbsen-Karotten, Mischgemüse {DO}', alts='Karotten; Brokkoli',
  why='Die Erbsen bringen Eiweiß mit. Eine Portion passt gut.')
f('Karotten (Dose)', 'G620902', 'gemuese', syn=f'Möhren {DO}, Pariser Karotten')
f('Spargel (Glas)', 'G450902', 'gemuese', syn=f'Spargel {DO}, Stangenspargel')
f('Artischockenherzen (Dose)', 'G410902', 'gemuese', syn=f'Artischocken {DO}, Artischockenböden')
f('Artischocken in Öl', 'G410702', 'fettfrucht', syn='Artischockenherzen in Öl, Antipasti, eingelegte Artischocken')
f('Palmherzen', 'G440902', 'gemuese', syn=f'Palmenherzen, Palmito {DO}')
f('Sojasprossen (Glas)', 'H620902', 'gemuese', syn=f'Sojabohnenkeimlinge {DO}')
f('Mungbohnensprossen (Glas)', 'H650902', 'gemuese', syn=f'Mungbohnenkeimlinge, Sprossen {DO}')
f('Sauerkraut (frisch)', 'G345100', 'gemuese', cap=200, syn='Weinsauerkraut, rohes Sauerkraut, Frischkost')
f('Rotkohl (Glas)', 'G341900', 'gemuese', light='y', syn=f'Rotkraut, Blaukraut, Apfelrotkohl {DO}, Kühne, Hengstenberg', alts='Rotkohl; Weißkohl',
  why='Fertiger Rotkohl ist gezuckert. Frischer Rotkohl mit etwas Apfel und Essig schmeckt ähnlich und spart den Zucker.')
f('Rote Bete (Glas)', 'G613802', 'gemuese', light='y', syn=f'Rote Bete eingelegt, Rote-Bete-Salat, Rote Rüben {DO}', alts='Rote Bete (vorgegart); Rote Bete (roh)',
  why='Eingelegte Rote Bete ist gezuckert. Vorgegarte aus dem Kühlregal kommt ohne Zucker aus.')
f('Mixed Pickles', 'G880602', 'gemuese', light='y', cap=100, syn='eingelegtes Gemüse, Essiggemüse, Pickles', alts='Gewürzgurken; Salzgurken',
  why='Im Sud steckt etwas Zucker. Als kleine Beilage passt es.')
f('Cornichons', 'G890902', 'gemuese', cap=100, syn='Gürkchen, kleine Gewürzgurken, Essiggurken')
f('Silberzwiebeln', 'G488802', 'gemuese', cap=50, syn='Perlzwiebeln, eingelegte Zwiebeln')
f('Paprika (Glas)', 'G543802', 'gemuese', cap=150, syn=f'geröstete Paprika, eingelegte Paprika, Tomatenpaprika, Antipasti {DO}')
f('Honiggurken', 'G891102', 'gemuese', light='y', syn='Gurkensticks süß, süße Gurken, dänische Gurken', alts='Salzgurken; Gewürzgurken',
  why='Im Sud steckt Honig oder Zucker. Salz- und Gewürzgurken sind die bessere Wahl.')
f('Senfgurken', 'G891202', 'gemuese', light='y', cap=100, syn='Schälgurken eingelegt', alts='Salzgurken; Gewürzgurken',
  why='Im Sud steckt etwas Zucker. Als kleine Beilage passt es.')
f('Kürbis süß-sauer (Glas)', 'G581802', 'gemuese', light='y', syn='eingelegter Kürbis, Kürbis im Glas', alts='Hokkaido-Kürbis; Gewürzgurken',
  why='Fast ein Viertel davon ist Zucker. Ein, zwei Stücke sind okay, frischer Kürbis passt besser.')
f('Puszta-Salat', 'G090802', 'gemuese', light='y', cap=100, syn='Pusztasalat, Paprikasalat Glas', alts='Rote Paprika; Gewürzgurken',
  why='Im Sud steckt etwas Zucker. Als kleine Beilage passt es.')
f('Getrocknete Tomaten in Öl', 'G567702', 'gemuese', light='y', cap=20, syn='Tomaten in Öl, eingelegte Tomaten, Antipasti', alts='Tomaten; Tomatenmark',
  why='Konzentriert und ölig: ein paar Stücke geben viel Geschmack, mehr kostet schnell Zucker- und Fettbudget.')
f('Knoblauch (eingelegt)', 'G491802', 'wuerze', cap=20, syn='Knoblauchzehen eingelegt, Knoblauch Glas')
f('Kimchi', None, 'gemuese', cap=150, syn='fermentierter Chinakohl, Kimchee', n=(15, 1.1, 0.5, 2.4, 1.1))
f('Pfifferlinge (Glas)', 'K713902', 'pilze', syn=f'Eierschwammerl, Pilze {DO}')
f('Mischpilze (Dose)', 'K750902', 'pilze', syn=f'Pilzmischung, Pilze {DO}')
f('Steinpilze (getrocknet)', 'K718400', 'pilze', cap=15, syn='Trockenpilze, getrocknete Pilze, Herrenpilze getrocknet',
  why='Getrocknet sehr konzentriert, eine kleine Handvoll reicht für ein ganzes Gericht.')
f('Mischpilze (getrocknet)', 'K750400', 'pilze', cap=15, syn='Trockenpilze, getrocknete Pilze, Waldpilze getrocknet',
  why='Getrocknet sehr konzentriert, eine kleine Handvoll reicht für ein ganzes Gericht.')
f('Röstzwiebeln', 'G860192', 'weissmehl', syn='Danish Onions, Zwiebeln geröstet, frittierte Zwiebeln', alts='Zwiebeln; Frühlingszwiebeln',
  why='Frittiert und in Mehl gewendet. Frisch angebratene Zwiebeln geben das gleiche Aroma.')

# Hülsenfrüchte aus Dose und Glas
f('Linsen (Dose)', 'H730902', 'huelsen', syn=f'Linsen {DO}, Tellerlinsen Dose', alts='Hokkaido-Kürbis; Karotten')
f('Weiße Bohnen (Dose)', 'H740902', 'huelsen', syn=f'Cannellini, Riesenbohnen, Bohnen weiß {DO}', alts='Zucchini; Champignons')
f('Baked Beans', 'H900900', 'huelsen', light='y', cap=80, syn='Bohnen in Tomatensoße, weiße Bohnen in Tomatensauce, Heinz Beanz', alts='Weiße Bohnen (Dose); Tomaten (Dose)',
  why='Die Soße ist gezuckert. Weiße Bohnen mit Dosentomaten und Gewürzen schmecken ähnlich.')
f('Sojabohnen (gegart)', 'G750432', 'soja', cap=40, syn='Sojabohnen, Sojakerne gekocht', alts='Kichererbsen (gegart); Zuckerschoten')
f('Limabohnen (gegart)', 'G780432', 'huelsen', syn='Butterbohnen, Mondbohnen, Limabohnen', alts='Zucchini; Champignons')
f('Erbsen (frisch)', 'G760100', 'huelsen', cap=120, syn='Erbsen frisch, Palerbsen, Schotenerbsen', alts='Zuckerschoten; Brokkoli')
f('Wachsbohnen', 'G720100', 'gemuese', syn='gelbe Bohnen, Butterbohnen gelb')
f('Maiskolben', 'G570100', 'knolle', cap=100, syn='Zuckermais frisch, Mais frisch', alts='Rote Paprika; Zucchini', piece=('Kolben', 200))

# Knollen, Kartoffelprodukte
f('Pellkartoffeln', 'K120134', 'knolle', syn='Kartoffeln gekocht mit Schale, Salzkartoffeln, gekochte Kartoffeln', alts='Blumenkohl; Knollensellerie', piece=('Stück', 100))
f('Kartoffelpüree (mit Wasser)', 'X638012', 'knolle', cap=200, syn='Kartoffelbrei, Püree, Stampfkartoffeln, Kartoffelpüree Pulver, Pfanni', alts='Kartoffeln; Blumenkohl',
  why='Mit Wasser statt Milch und Butter angerührt passt eine Portion.')
f('Kartoffelsalat (mit Brühe)', 'X1A2010', 'suppe', cap=150, syn='Kartoffelsalat schwäbisch, Kartoffelsalat Essig und Öl, Kartoffelsalat ohne Mayo', alts='Kartoffeln; Gurke',
  why='Mit Brühe, Essig und Öl angemacht passt eine kleine Portion. Fertige Salate enthalten oft Zucker.')
f('Maniok', 'K410100', 'knolle', cap=100, syn='Cassava, Yuca, Kassava', alts='Kartoffeln; Süßkartoffel')
f('Kochbanane', 'F545100', 'knolle', cap=80, syn='Plantain, Gemüsebanane', alts='Kartoffeln; Süßkartoffel')
f('Maronen', 'H230100', 'knolle', cap=60, syn='Esskastanien, Edelkastanien, Maroni, gegarte Maronen', alts='Kartoffeln; Hokkaido-Kürbis',
  why='Stärkereich und süßlich. Eine kleine Handvoll passt gut in Suppe oder Ofengemüse.')
f('Gnocchi', 'K270032', 'weissmehl', syn='Kartoffelnocken, Gnocchi Kühlregal', alts='Kartoffeln; Zucchini',
  why='Kartoffelteig mit viel Weißmehl. Eine kleine Portion Kartoffeln passt besser.')
f('Kartoffelklöße', 'K241232', 'weissmehl', syn='Knödel, Klöße, Kartoffelknödel, Semmelknödel, Pfanni', alts='Kartoffeln; Knollensellerie',
  why='Viel Stärke auf kleinem Raum. Eine kleine Portion Kartoffeln passt besser.')
f('Rösti', 'K391200', 'weissmehl', syn='Kartoffelrösti, Röstinchen, Hash Browns, Reibekuchen, Kartoffelpuffer', alts='Kartoffeln; Zucchini',
  why='In Fett vorgebacken. Selbst geriebene Kartoffeln mit Zucchini aus der Pfanne kommen mit wenig Öl aus.')
f('Kroketten', 'K282200', 'weissmehl', syn='Kartoffelkroketten, Herzoginkartoffeln, Kartoffelecken, Wedges', alts='Kartoffeln; Süßkartoffel',
  why='Paniert und in Fett vorgebacken. Ofenkartoffeln mit etwas Olivenöl passen besser.')

# Brühen, Würzmittel, Soßen
f('Gemüsebrühe (Pulver)', 'R821000', 'wuerze', cap=10, syn='Brühwürfel, gekörnte Brühe, Instantbrühe, Brühpulver, Bouillon, Suppenwürfel, Maggi, Knorr', piece=('Teelöffel', 5))
f('Hühnerbrühe', 'X411243', 'tier', syn='Hühnerfond, Geflügelbrühe, Geflügelfond, Hühnersuppe klar', alts='Gemüsebrühe; Helle Misopaste',
  why='Aus Huhn gekocht. Scheinfasten ist rein pflanzlich, Gemüsebrühe ist der direkte Ersatz.')
f('Rinderbrühe', 'Y183013', 'tier', syn='Fleischbrühe, Rinderfond, Kraftbrühe, Knochenbrühe, Bone Broth, Fleischfond', alts='Gemüsebrühe; Helle Misopaste',
  why='Aus Fleisch und Knochen gekocht. Scheinfasten ist rein pflanzlich, Gemüsebrühe ist der direkte Ersatz.')
f('Ajvar', 'G898400', 'wuerze', cap=50, syn='Paprikamus, Paprikapaste, Ajwar')
f('Sambal Oelek', 'R146100', 'wuerze', cap=10, syn='Chilipaste, Harissa, Chilisauce scharf')
f('Wasabi', 'R913000', 'wuerze', cap=10, syn='Wasabipaste, japanischer Meerrettich')
f('Meerrettich (Glas)', 'G898300', 'wuerze', cap=20, syn='Tafelmeerrettich, Kren Glas')
f('Sushi-Ingwer', 'R912000', 'wuerze', light='y', cap=20, syn='Gari, eingelegter Ingwer', alts='Ingwer',
  why='In gesüßtem Essig eingelegt. Ein paar Scheiben sind okay, frischer Ingwer kommt ohne Zucker aus.')
f('Süßer Senf', 'R135000', 'wuerze', light='y', cap=10, syn='Weißwurstsenf, bayerischer Senf, Honigsenf', alts='Senf',
  why='Ein Viertel davon ist Zucker. Ein Teelöffel geht, mittelscharfer Senf passt besser.')
f('Kakaopulver (ungesüßt)', 'S711000', 'wuerze', cap=10, syn='Backkakao, Kakao ungesüßt, Kakao',
  why='Ungesüßt ein Teelöffel für Geschmack. Trinkkakao mit Zucker gehört nicht dazu.')
f('Sriracha', None, 'wuerze', light='y', cap=10, syn='Chilisauce, Chilisoße, Hot Sauce, Tabasco', alts='Chiliflocken; Sambal Oelek',
  why='Scharf, aber gezuckert. Ein paar Spritzer sind okay.', n=(93, 1.9, 0.9, 19.2, 15.1))
f('Worcestersauce', None, 'wuerze', light='y', cap=10, syn='Worcestershire, Worcestersoße, Maggi Würze', alts='Sojasauce; Balsamico',
  why='Enthält meist Sardellen und Zucker. Ein paar Spritzer fallen kaum ins Gewicht, Sojasauce ist die pflanzliche Wahl.', n=(78, 0, 0, 19.5, 10.0))
f('Teriyakisauce', None, 'suess', syn='Teriyaki, Teriyakisoße, Yakitori', alts='Sojasauce; Ingwer',
  why='Sojasauce mit viel Zucker. Sojasauce mit frischem Ingwer und Knoblauch schmeckt ähnlich.', n=(89, 5.9, 0, 15.6, 14.1))
f('Hoisinsauce', None, 'suess', syn='Hoisin, Hoi Sin, Süß-Sauer-Sauce, Sweet Chili, süße Chilisauce, Pflaumensauce', alts='Sojasauce; Helle Misopaste',
  why='Mehr als ein Viertel davon ist Zucker. Miso und Sojasauce bringen die Würze ohne Zucker.', n=(220, 3.3, 3.4, 44.1, 27.3))
f('Fischsauce', None, 'tier', syn='Fischsoße, Nam Pla, Austernsauce, Austernsoße', alts='Sojasauce; Nori',
  why='Aus Fisch vergoren. Sojasauce mit etwas Nori bringt den gleichen herzhaften Geschmack.', n=(35, 5.1, 0, 3.6, 3.6))
f('Grillsauce', 'R148200', 'suess', syn='BBQ-Sauce, Barbecuesauce, Zigeunersauce, Schaschliksauce, Cocktailsauce, Burgersauce', alts='Tomatenmark; Ajvar',
  why='Ein Fünftel davon ist Zucker. Ajvar oder Tomatenmark mit Gewürzen geben Würze ohne Zucker.')
f('Chutney', 'R144100', 'suess', syn='Mango-Chutney, Fruchtchutney, Relish', alts='Apfelmus ungesüßt; Ajvar',
  why='Eingekochtes Obst mit sehr viel Zucker.')
f('Mayonnaise', 'Q991000', 'tier', syn='Mayo, Majo, Aioli, Hellmanns, Thomy', alts='Avocado; Tahin; Senf',
  why='Mit Eigelb gemacht. Zerdrückte Avocado oder Tahin mit Zitrone machen Salate genauso cremig.')
f('Remoulade', 'Q999000', 'tier', syn='Remouladensauce, Tartarsauce, Sauce Tartare', alts='Avocado; Senf; Kapern',
  why='Mayonnaise mit Ei. Avocado mit Kapern und Senf schmeckt ähnlich.')
f('Salatcreme', 'Q998000', 'tier', syn='Miracel Whip, Salatmayonnaise, Sandwichcreme, Joghurt-Salatcreme', alts='Tahin; Avocado; Zitronensaft',
  why='Enthält Ei und Zucker. Tahin mit Zitronensaft und Wasser ergibt ein cremiges Dressing.')
f('Joghurt-Dressing', 'X357340', 'milch', syn='Salatdressing, Fertigdressing, Sylter Dressing, Caesar Dressing, French Dressing, Kräuterdressing, Salatsoße', alts='Olivenöl; Zitronensaft; Tahin',
  why='Fertige Dressings enthalten Milchprodukte, Ei oder Zucker. Öl mit Zitrone oder Essig ist in einer Minute angerührt.')
f('Bratensoße', 'R910032', 'tier', syn='Bratensauce, Soßenbinder, Jägersoße, Rahmsoße, dunkle Soße', alts='Tomaten, passiert; Sojasauce',
  why='Fertigsoßen basieren auf Fleischextrakt, Fett und Stärke. Passierte Tomaten mit Sojasauce geben eine herzhafte Soße.')
f('Sauce Hollandaise', 'X371043', 'milch', syn='Hollandaise, Sauce Bearnaise, Buttersoße', alts='Olivenöl; Zitronensaft',
  why='Butter und Eigelb. Zum Spargel passt Olivenöl mit Zitrone.')
f('Pesto rosso', 'X3A7010', 'milch', syn='rotes Pesto, Tomatenpesto, Barilla Pesto', alts='Getrocknete Tomaten; Olivenöl; Pinienkerne',
  why='Fertiges Pesto enthält Käse. Getrocknete Tomaten mit Olivenöl und Pinienkernen gemixt passen.')
f('Gelatine', 'R468000', 'tier', syn='Blattgelatine, Speisegelatine, Götterspeise, Wackelpudding', alts='Chiasamen; Leinsamen',
  why='Tierisches Eiweiß. Chiasamen binden Flüssigkeit ganz ähnlich.')
f('Weizenmehl', 'C214100', 'weissmehl', syn='Mehl, Weißmehl, Type 405, Type 550, Auszugsmehl, Dinkelmehl', alts='Kartoffeln; Hirse (gegart)',
  why='Reine Stärke, die kaum satt macht. Zum Binden reicht ein Löffel püriertes Gemüse oder Kartoffel.')
f('Vollkornmehl', 'C211000', 'getreide', cap=30, syn='Weizenvollkornmehl, Dinkelvollkornmehl, Roggenvollkornmehl', alts='Haferflocken; Hirse (gegart)',
  why='Ein Esslöffel zum Binden oder für einen kleinen Fladen passt.')
f('Kichererbsenmehl', 'H720400', 'huelsen', cap=30, syn='Besan, Gram-Mehl', alts='Kichererbsen (gegart)',
  why='Eiweißreich. Ein, zwei Esslöffel zum Binden oder für einen dünnen Pfannkuchen passen.')
f('Speisestärke', 'C446000', 'getreide', cap=10, syn='Maisstärke, Stärke, Mondamin, Kartoffelstärke, Kartoffelmehl, Tapioka', alts='Kartoffeln',
  why='Ein Teelöffel zum Binden ist okay.')

# Aufstriche und Dips
f('Guacamole', 'X389000', 'fettfrucht', cap=80, syn='Avocadocreme, Avocado-Dip, Avocadoaufstrich')
f('Sonnenblumenkernaufstrich', 'H880100', 'fettfrucht', light='y', cap=30, syn='veganer Brotaufstrich, pflanzlicher Aufstrich, Streich, Zwergenwiese, Brotaufstrich vegan', alts='Hummus; Tahin; Avocado',
  why='Pflanzlich, aber mit zugesetztem Öl und etwas Zucker. Ein, zwei Esslöffel passen.')
f('Gemüseaufstrich', 'G940100', 'fettfrucht', light='y', cap=30, syn='veganer Brotaufstrich, Paprikaaufstrich, Tomatenaufstrich, Bruschetta-Aufstrich, Gemüsecreme', alts='Ajvar; Hummus; Avocado',
  why='Pflanzlich, aber mit zugesetztem Öl und etwas Zucker. Ein, zwei Esslöffel passen.')
f('Vegetarische Pastete', 'K820000', 'fettfrucht', light='y', cap=30, syn='Hefepastete, Tartex, vegane Pastete, Brotaufstrich Hefe', alts='Hummus; Tahin',
  why='Pflanzlich, aber stark verarbeitet und fettreich. Ein, zwei Esslöffel passen.')
f('Mandel-Streichcreme', 'H882100', 'nuss', cap=40, syn='veganer Frischkäse, Frischkäsealternative, Streichcreme Mandel, Simply V Streichgenuss, vegane Frischecreme')
f('Erdnussbutter', 'H880200', 'nuss', light='y', cap=15, syn='Erdnusscreme, Peanut Butter, Erdnussbutter crunchy', alts='Mandelmus; Tahin',
  why='Meist mit Zucker und Palmfett. Reines Mandelmus oder Tahin passen besser.')
f('Oliven mit Paprika gefüllt', 'H510900', 'fettfrucht', syn='gefüllte Oliven, Oliven gefüllt, Antipasti')
f('Oliven mit Mandeln gefüllt', 'H511900', 'fettfrucht', syn='gefüllte Oliven, Mandeloliven, Antipasti')

# Öle und Fette
f('Maiskeimöl', 'Q260000', 'fett', syn='Öl, Keimöl, Mazola')
f('Sojaöl', 'Q270000', 'fett', syn='Öl, Pflanzenöl, Speiseöl')
f('Distelöl', 'Q340000', 'fett', syn='Öl, Safloröl')
f('Haselnussöl', 'Q140000', 'fett', cap=15, syn='Öl, Nussöl')
f('Weizenkeimöl', 'Q220000', 'fett', cap=15, syn='Öl')
f('Kokosfett (gehärtet)', 'Q550200', 'fett', light='y', cap=10, syn='Palmin, Plattenfett, Palmfett, Frittierfett', alts='Olivenöl; Rapsöl',
  why='Fast nur gesättigte Fettsäuren. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')
f('Kräuterbutter', 'Q656000', 'milch', syn='Knoblauchbutter, Grillbutter', alts='Olivenöl; Knoblauch; Petersilie')
f('Schmalz', 'Q860000', 'tier', syn='Schweineschmalz, Griebenschmalz, Gänseschmalz, Butterschmalz', alts='Olivenöl; Rapsöl',
  why='Tierisches Fett. Zum Braten passen Oliven- oder Rapsöl.')

# Nüsse und Knabbereien
f('Mandeln (geröstet, gesalzen)', 'H210710', 'nuss', light='y', cap=20, syn='Salzmandeln, Rauchmandeln, geröstete Mandeln', alts='Mandeln; Walnusskerne',
  why='In Fett geröstet und gesalzen. Eine kleine Handvoll ist okay, naturbelassene Nüsse passen besser.')
f('Cashewkerne (geröstet, gesalzen)', 'H170700', 'nuss', light='y', cap=20, syn='Cashews gesalzen, geröstete Cashews', alts='Cashewkerne; Walnusskerne',
  why='In Fett geröstet und gesalzen. Eine kleine Handvoll ist okay, naturbelassene Nüsse passen besser.')
f('Pistazien (geröstet, gesalzen)', 'H250700', 'nuss', light='y', cap=20, syn='Pistazien gesalzen, Pistazien in Schale', alts='Pistazien; Walnusskerne',
  why='Gesalzen. Eine kleine Handvoll ist okay, naturbelassene Nüsse passen besser.')
f('Macadamia (geröstet, gesalzen)', 'H190700', 'nuss', light='y', cap=20, syn='Macadamianüsse gesalzen', alts='Macadamia; Walnusskerne',
  why='Gesalzen. Eine kleine Handvoll ist okay, naturbelassene Nüsse passen besser.')
f('Erdnüsse (gesalzen)', 'H110700', 'nuss', light='y', cap=15, syn='Salzerdnüsse, geröstete Erdnüsse gesalzen, Ültje, Partynüsse, Nussmischung gesalzen', alts='Mandeln; Walnusskerne',
  why='Viel Eiweiß und Salz. Ein paar Stück sind okay, Walnüsse und Mandeln passen besser.')
f('Studentenfutter', 'H810000', 'suess', syn='Nuss-Frucht-Mischung, Trail Mix, Nussmix mit Rosinen, Seeberger', alts='Walnusskerne; Mandeln; Heidelbeeren',
  why='Die Rosinen machen fast ein Drittel Zucker aus. Nüsse pur mit ein paar frischen Beeren passen.')
f('Erdnüsse im Teigmantel', 'H810100', 'weissmehl', syn='NicNacs, Teignüsse, Wasabi-Nüsse, Erdnusslocken', alts='Mandeln; Walnusskerne')
f('Erdnussflips', 'D041000', 'weissmehl', syn='Flips, Erdnusslocken, Maisflips', alts='Popcorn; Maiswaffeln')
f('Kartoffelsticks', 'K280200', 'weissmehl', syn='Sticks, Pombär, Chipsletten, Pringles, Stapelchips', alts='Grünkohl; Maiswaffeln')
f('Popcorn (süß)', 'C519000', 'suess', syn='Kinopopcorn, karamellisiertes Popcorn, Popcorn gezuckert', alts='Popcorn; Maiswaffeln')
f('Reiswaffeln mit Schokolade', 'C532900', 'suess', syn='Schoko-Reiswaffeln, schokolierte Reiswaffeln', alts='Reiswaffeln; Maiswaffeln')
f('Gebrannte Mandeln', 'S465000', 'suess', syn='gebrannte Nüsse, Krokant, kandierte Nüsse', alts='Mandeln; Walnusskerne')
f('Amaranth (gepufft)', 'C530100', 'knusper', cap=15, syn='Amaranth-Pops, gepoppter Amaranth')
f('Quinoa (gepufft)', 'C530200', 'knusper', cap=15, syn='Quinoa-Pops, gepoppter Quinoa')
f('Dinkel (gepufft)', 'C531000', 'knusper', cap=15, syn='Weizen gepufft, Dinkelpops ungesüßt, Puffweizen')

# Getreideprodukte, Brot
f('Wildreis (gegart)', 'C353132', 'getreide', syn='Wildreis, Wildreismischung', alts='Blumenkohl; Hirse (gegart)')
f('Parboiled Reis (gegart)', 'C359032', 'getreide', cap=80, syn='Langkornreis, Kochbeutelreis, Uncle Bens, Parboiled, Risottoreis', alts='Blumenkohl; Hirse (gegart)')
f('Sushi-Reis', 'X8A1100', 'getreide', cap=80, syn='Klebreis, Sushireis gewürzt', alts='Blumenkohl; Hirse (gegart)',
  why='Mit Zucker und Essig gewürzt. Eine kleine Portion passt.')
f('Haferbrei (mit Wasser)', 'X9A2120', 'getreide', cap=200, syn='Porridge, Oatmeal, Haferschleim, Overnight Oats mit Wasser', alts='Leinsamen; Heidelbeeren',
  why='Mit Wasser gekocht und ungesüßt passt eine kleine Schale, am besten an Tag 1.')
f('Haferkleie', 'C138000', 'getreide', cap=20, syn='Kleie, Haferkleieflocken', alts='Leinsamen; Chiasamen')
f('Weizenkleie', 'C217000', 'getreide', cap=15, syn='Kleie, Speisekleie, Dinkelkleie', alts='Leinsamen; Chiasamen')
f('Weizenkeime', 'C114000', 'getreide', cap=10, syn='Keime', alts='Leinsamen; Sesam',
  why='Sehr eiweißreich. Ein Teelöffel als Topping reicht.')
f('Hirseflocken', 'C333100', 'getreide', cap=30, syn='Hirse Flocken, Braunhirse', alts='Leinsamen; Walnusskerne')
f('Dinkelflocken', 'C236100', 'getreide', cap=30, syn='Dinkel Flocken, Mehrkornflocken, Getreideflocken, Roggenflocken', alts='Leinsamen; Walnusskerne')
f('Müsli (ungesüßt)', 'C512600', 'getreide', cap=30, syn='Basismüsli, Bircher Müsli ungesüßt, Müsli ohne Zucker, Seitenbacher', alts='Haferflocken; Walnusskerne',
  why='Auch ungesüßt bringen Trockenfrüchte Zucker mit. Zwei Esslöffel passen, Haferflocken mit frischen Beeren sind besser.')
f('Vollkornbrötchen', 'B401000', 'getreide', cap=30, syn='Körnerbrötchen, Vollkornsemmel, Mehrkornbrötchen', alts='Knäckebrot; Gurke', piece=('Stück', 60),
  why='Ein halbes passt an Tag 1. Für Brot sieht Prof. Dr. Longo sonst kaum Platz vor.')
f('Roggenbrot', 'B221000', 'getreide', cap=40, syn='Roggenschrotbrot, Kommissbrot, Landbrot', alts='Knäckebrot; Gurke', piece=('Scheibe', 45),
  why='Eine dünne Scheibe passt an Tag 1. Für Brot sieht Prof. Dr. Longo sonst kaum Platz vor.')
f('Toastbrot', 'B314000', 'weissmehl', syn='Toast, Buttertoast, Sandwichtoast, Golden Toast, Weizentoast', alts='Knäckebrot; Vollkornbrot', piece=('Scheibe', 25))
f('Brötchen', 'B511000', 'weissmehl', syn='Semmel, Schrippe, Weck, Weizenbrötchen, Aufbackbrötchen', alts='Knäckebrot; Vollkornbrot', piece=('Stück', 50))
f('Baguette', 'B781200', 'weissmehl', syn='Stangenweißbrot, Ciabatta, Kräuterbaguette', alts='Knäckebrot; Vollkornbrot')
f('Fladenbrot', 'B782100', 'weissmehl', syn='Pide, Pita, Naan, Dönerbrot', alts='Romanasalat; Knäckebrot')
f('Laugenbrezel', 'B723000', 'weissmehl', syn='Brezel, Breze, Laugenstange, Laugenbrötchen, Laugengebäck', alts='Knäckebrot; Maiswaffeln', piece=('Stück', 80))
f('Eiweißbrot', 'B881100', 'eiweiss', syn='Proteinbrot, Low-Carb-Brot, Eiweißbrötchen', alts='Knäckebrot; Vollkornbrot',
  why='Fast ein Viertel davon ist Eiweiß. Genau das hält Prof. Dr. Longo in diesen Tagen niedrig.')
f('Glutenfreies Brot', 'B309000', 'weissmehl', syn='Brot glutenfrei, Schär, Toast glutenfrei', alts='Maiswaffeln; Reiswaffeln',
  why='Meist aus Stärke und Fett. Mais- oder Reiswaffeln sind die glutenfreie Wahl mit weniger Kalorien.')
f('Zwieback', 'D038000', 'weissmehl', syn='Brandt Zwieback, Vollkornzwieback', alts='Knäckebrot; Maiswaffeln',
  why='Weißmehl mit Zucker. Knäckebrot knuspert ohne Zucker.')
f('Blätterteig', 'D072000', 'weissmehl', syn='Strudelteig, Pizzateig, Fertigteig, Mürbeteig, Tante Fanny', alts='Zucchini; Aubergine')
f('Eiernudeln', 'E432032', 'weissmehl', syn='Eierteigwaren, Bandnudeln, Spätzle, Tagliatelle, Schupfnudeln, Barilla', alts='Zucchini; Vollkornnudeln (gegart)')
f('Ravioli (Dose)', 'E911000', 'weissmehl', syn='Ravioli in Tomatensoße, Dosenravioli, Tortellini, Maultaschen, Maggi Ravioli', alts='Zucchini; Tomaten (Dose)')

# Suppen und fertige Gerichte, die passen können (gelb: Portion im Blick behalten)
SUP = 'Eine Portion kann ein ganzes Gericht ersetzen. Fertigprodukte unterscheiden sich stark, schau bei Zucker, Sahne und Fleisch auf die Zutatenliste.'
f('Gemüsesuppe (klar)', 'X416713', 'suppe', syn='Gemüsesuppe, Gemüsebrühe mit Einlage, Dosensuppe, Fertigsuppe', alts='Gemüsebrühe; Suppengemüse (TK)', why=SUP)
f('Gemüsecremesuppe', 'X416913', 'suppe', syn='Cremesuppe, pürierte Gemüsesuppe, Brokkolicremesuppe, Spargelcremesuppe', alts='Gemüsebrühe; Blumenkohl', why=SUP)
f('Minestrone (fertig)', 'X425163', 'suppe', syn='Minestrone Dose, italienische Gemüsesuppe', alts='Gemüsebrühe; Suppengemüse (TK)', why=SUP)
f('Tomatensuppe', 'X4A6020', 'suppe', syn='Tomatencremesuppe, Tomatensuppe Dose, Tomatensuppe Tüte', alts='Tomaten, passiert; Gemüsebrühe', why=SUP)
f('Kürbissuppe (mit Kokosmilch)', 'X4A3010', 'suppe', syn='Kürbiscremesuppe, Kürbissuppe fertig, Hokkaidosuppe', alts='Hokkaido-Kürbis; Kokosmilch (vollfett)', why=SUP)
f('Kartoffelsuppe', 'X449023', 'suppe', syn='Kartoffelcremesuppe, Kartoffelsuppe Dose', alts='Kartoffeln; Gemüsebrühe', why=SUP)
f('Linsensuppe', 'X462513', 'suppe', cap=200, syn='Linseneintopf, Linsensuppe Dose, Erasco', alts='Linsen (Dose); Gemüsebrühe',
  why='Linsen bringen viel Eiweiß mit, deshalb nur eine kleine Portion. Achte darauf, dass kein Speck oder Würstchen drin ist.')
f('Erbsensuppe', 'X4A8020', 'suppe', cap=200, syn='Erbseneintopf, Erbsensuppe Dose', alts='Erbsen (TK); Gemüsebrühe',
  why='Erbsen bringen viel Eiweiß mit, deshalb nur eine kleine Portion. Achte darauf, dass kein Speck oder Würstchen drin ist.')
f('Gazpacho', 'X469460', 'suppe', syn='kalte Gemüsesuppe, kalte Tomatensuppe', alts='Tomaten; Gurke', why=SUP)
f('Misosuppe', 'X4A8060', 'suppe', cap=500, syn='Miso-Suppe, Instant-Miso', alts='Helle Misopaste; Gemüsebrühe', why='Leicht und würzig. Ohne Fisch-Dashi ist sie rein pflanzlich.')
f('Tütensuppe (Gemüse)', 'G850132', 'suppe', syn='Instantsuppe, Tassensuppe, 5-Minuten-Terrine, Suppe aus Pulver, Heiße Tasse', alts='Gemüsebrühe; Suppengemüse (TK)',
  why='Stärke, Zucker und Aromen statt Gemüse. Eine Tasse ist okay, eine Brühe mit TK-Gemüse ist genauso schnell und besser.')
f('Chili sin Carne', 'X4A8000', 'suppe', cap=200, syn='veganes Chili, Bohnenchili, Chili vegetarisch', alts='Kidneybohnen (gegart); Tomaten (Dose)',
  why='Bohnen bringen viel Eiweiß mit, deshalb nur eine kleine Portion.')
f('Ratatouille (fertig)', 'X518543', 'suppe', syn='Ratatouille, Schmorgemüse, Gemüsepfanne fertig, Letscho', alts='Zucchini; Aubergine; Tomaten', why=SUP)
f('Sushi (vegan)', 'X8A1090', 'suppe', cap=150, syn='Gemüsesushi, Maki Gurke, Avocado-Maki, Kappa Maki', alts='Gurke; Avocado; Nori',
  why='Gurke- oder Avocado-Maki sind pflanzlich. Der Reis ist gezuckert, deshalb nur ein paar Stück.')

# Fertiggerichte, die nicht passen
f('Chili con Carne', 'X469753', 'fertig', syn='Chili mit Hackfleisch, Chili Dose', alts='Chili sin Carne; Kidneybohnen (gegart)')
f('Gulaschsuppe', 'X456143', 'fertig', syn='Gulasch, Gulaschsuppe Dose, Soljanka', alts='Tomatensuppe; Champignons')
f('Hühnersuppe', 'X4A1020', 'fertig', syn='Hühnernudelsuppe, Nudelsuppe, Hühnerfrikassee', alts='Gemüsesuppe (klar); Gemüsebrühe')
f('Paella', 'X890933', 'fertig', syn='Reispfanne, Nasi Goreng, Bami Goreng, gebratener Reis', alts='Vollkornreis (gegart); Rote Paprika')
f('Risotto', 'X850133', 'fertig', syn='Risotto mit Parmesan, Pilzrisotto', alts='Vollkornreis (gegart); Champignons',
  why='Mit Butter und Parmesan gekocht. Vollkornreis mit Pilzen und Olivenöl ist die Scheinfasten-Variante.')
f('Kartoffelsalat (Mayonnaise)', 'X1A2020', 'fertig', syn='Kartoffelsalat mit Mayo, Nudelsalat, Fleischsalat, Eiersalat, Farmersalat', alts='Kartoffelsalat (mit Brühe); Kartoffeln')
f('Sushi (mit Fisch)', 'Y627112', 'fertig', syn='Sushi, Lachs-Nigiri, Maki Lachs, Sashimi, California Roll', alts='Sushi (vegan); Gurke; Avocado')
f('Frikadelle', 'Y912030', 'fertig', syn='Bulette, Fleischpflanzerl, Fleischküchle, Hackbällchen, Köttbullar, Cevapcici', alts='Champignons; Kichererbsen (gegart)')
f('Bolognese', 'Y038213', 'fertig', syn='Bolognese-Soße, Hackfleischsoße, Spaghetti Bolognese, Lasagne, Fertiggericht, Tiefkühlgericht, Mikrowellengericht, Fertigessen', alts='Tomaten, passiert; Linsen (gegart); Champignons',
  why='Hackfleischsoße, oft mit Käse überbacken. Passierte Tomaten mit Linsen oder Pilzen geben eine herzhafte pflanzliche Soße.')

# Fisch, Fleisch, Wurst, Ei
f('Räucherlachs', 'T410600', 'tier', syn='geräucherter Lachs, Graved Lachs, Stremellachs', alts='Avocado; Walnusskerne; Nori')
f('Thunfisch in Öl', 'T121702', 'tier', syn='Thunfisch Dose Öl, Thunfischsalat', alts='Kichererbsen (gegart); Walnusskerne')
f('Sardinen in Öl', 'T105702', 'tier', syn='Ölsardinen, Sardinen Dose, Sardellen, Anchovis', alts='Grüne Oliven; Kapern')
f('Hering', 'T820802', 'tier', syn='Bismarckhering, Matjes, Rollmops, Brathering, Heringssalat, Heringsfilet', alts='Gewürzgurken; Rote Bete (vorgegart)')
f('Makrele (geräuchert)', 'T107600', 'tier', syn='Räuchermakrele, Räucherfisch, geräucherte Forelle, Forellenfilet', alts='Walnusskerne; Leinöl')
f('Kabeljau', 'T204100', 'tier', syn='Dorsch, Seelachs, Alaska-Seelachs, Pangasius, Weißfisch, Fischfilet, Zander, Forelle', alts='Blumenkohl; Champignons')
f('Muscheln', 'T792100', 'tier', syn='Miesmuscheln, Meeresfrüchte, Jakobsmuscheln, Austern', alts='Austernpilze; Champignons')
f('Tintenfisch', 'T020100', 'tier', syn='Calamari, Calamares, Oktopus, Pulpo, Sepia', alts='Austernpilze; Champignons')
f('Surimi', 'T890100', 'tier', syn='Krebsfleischimitat, Krabbenstäbchen, Crab Sticks', alts='Palmherzen; Austernpilze')
f('Putenbrust', 'V486100', 'tier', syn='Pute, Truthahn, Putenschnitzel, Putenfilet', alts='Champignons; Austernpilze')
f('Ente', 'V464100', 'tier', syn='Entenbrust, Gans, Gänsebraten, Entenkeule', alts='Champignons; Maronen')
f('Lammfleisch', 'U817100', 'tier', syn='Lamm, Lammkeule, Lammkotelett, Ziege, Hammel', alts='Aubergine; Kichererbsen (gegart)')
f('Fleischwurst', 'W234000', 'tier', syn='Lyoner, Mortadella, Bierschinken, Aufschnitt, Geflügelwurst, Jagdwurst', alts='Hummus; Avocado')
f('Leberkäse', 'W256100', 'tier', syn='Fleischkäse, Leberkäs', alts='Champignons; Kartoffeln')
f('Wiener Würstchen', 'W211200', 'tier', syn='Wiener, Frankfurter, Bockwurst, Hot Dog, Saitenwürstchen', alts='Champignons; Austernpilze')
f('Putenbrust-Aufschnitt', 'W561000', 'tier', syn='Putenaufschnitt, Hähnchenbrust-Aufschnitt, Geflügelaufschnitt, Truthahnbrust', alts='Hummus; Avocado; Gurke')
f('Rohschinken', 'W441000', 'tier', syn='Parmaschinken, Serrano, Schwarzwälder Schinken, Lachsschinken, Prosciutto', alts='Getrocknete Tomaten; Grüne Oliven')
f('Kasseler', 'W510000', 'tier', syn='Kassler, Rauchfleisch, Pökelfleisch, Eisbein', alts='Champignons; Sauerkraut')
f('Eiklar', 'E113100', 'tier', syn='Eiweiß vom Ei, Eischnee, flüssiges Eiklar', alts='Kichererbsen (gegart); Seidentofu')

# Milchprodukte
f('Fettarme Milch', 'M111200', 'milch', syn='Milch 1,5 %, fettarme H-Milch, teilentrahmte Milch', alts='Mandeldrink ungesüßt; Haferdrink')
f('Fruchtjoghurt', 'M241300', 'milch', syn='Joghurt mit Frucht, Erdbeerjoghurt, Activia, Danone, Müller, Froop, Landliebe, Joghurt mit der Ecke', alts='Sojajoghurt; Heidelbeeren')
f('Skyr', 'M710100', 'milch', syn='isländischer Joghurt, Proteinjoghurt, High-Protein-Joghurt, Arla Skyr', alts='Sojajoghurt; Seidentofu')
f('Camembert', 'M602600', 'milch', syn='Brie, Weichkäse, Weißschimmelkäse, Ziegenkäse', alts='Avocado; Cashewkerne')
f('Gorgonzola', 'M5B1600', 'milch', syn='Blauschimmelkäse, Roquefort, Edelpilzkäse', alts='Walnusskerne; Grüne Oliven')
f('Halloumi', 'M524500', 'milch', syn='Grillkäse, Backcamembert', alts='Aubergine; Austernpilze')
f('Ricotta', 'M741600', 'milch', syn='Molkenkäse', alts='Seidentofu; Cashewmus')
f('Schmelzkäse', 'M810600', 'milch', syn='Scheibletten, Toastkäse, Kochkäse, Babybel, Streichkäse', alts='Hummus; Avocado')
f('Harzer Käse', 'M730100', 'milch', syn='Harzer, Handkäse, Sauermilchkäse, Mainzer', alts='Champignons; Hummus')
f('Schmand', 'M172700', 'milch', syn='Sauerrahm 24 %', alts='Kokosmilch (vollfett); Sojajoghurt')
f('Kondensmilch', 'M182500', 'milch', syn='Kaffeemilch, Dosenmilch, Bärenmarke', alts='Mandeldrink ungesüßt; Haferdrink')
f('Milchreis', 'X810033', 'milch', syn='Reisbrei, Grießbrei, Grießpudding, Müller Milchreis', alts='Haferbrei (mit Wasser); Heidelbeeren')
f('Pudding', 'R481132', 'milch', syn='Vanillepudding, Schokopudding, Dessert, Mousse au Chocolat, Dr. Oetker', alts='Chiasamen; Kokosmilch (vollfett); Heidelbeeren')
f('Milchshake', 'M2H2300', 'milch', syn='Shake, Erdbeermilch, Vanillemilch, Bananenmilch', alts='Mandeldrink ungesüßt; Heidelbeeren')

# Pflanzliche Alternativen
f('Sojadrink (gesüßt)', 'H842400', 'drink', syn='Sojamilch gesüßt, Alpro Soja Original, Sojadrink Vanille, Sojadrink Schoko, Sojadrink Barista', alts='Mandeldrink ungesüßt; Sojadrink',
  why='Gesüßt und aromatisiert. Nimm die ungesüßte Variante.')
f('Haferdrink (gesüßt)', 'C660300', 'drink', syn='Hafermilch gesüßt, Hafer Schoko, Hafer Vanille, Oatly Schoko', alts='Mandeldrink ungesüßt; Haferdrink',
  why='Gesüßt und aromatisiert. Nimm die ungesüßte Variante oder Mandeldrink.')
f('Mandeldrink (gesüßt)', 'H800200', 'getraenk', light='y', cap=200, syn='Mandelmilch gesüßt, Alpro Mandel Original, Mandeldrink Barista, Mandel Vanille', alts='Mandeldrink ungesüßt',
  why='Leicht gesüßt. Ein Schuss geht, die ungesüßte Variante passt besser.')
f('Sojajoghurt (gesüßt)', 'H844400', 'suess', syn='Sojajoghurt Frucht, Alpro Joghurt Erdbeere, veganer Fruchtjoghurt, Sojajoghurt Vanille', alts='Sojajoghurt; Heidelbeeren',
  why='Gesüßt und aromatisiert. Ungesüßter Sojajoghurt mit frischen Beeren passt.')
f('Sojakochcreme', 'H845000', 'fettfrucht', light='y', cap=50, syn='Soja Cuisine, Pflanzensahne, vegane Sahne, Kochcreme, Alpro Cuisine, Sojasahne', alts='Kokosmilch (vollfett); Cashewmus',
  why='Pflanzlich, aber verarbeitet. Ein Schuss für die Soße passt.')
f('Veganer Pudding', 'H843200', 'suess', syn='Sojapudding, Alpro Dessert, pflanzlicher Pudding, Sojadessert', alts='Chiasamen; Kokosmilch (vollfett); Heidelbeeren')
f('Veganer Käse (Kokosöl)', 'Q590000', 'fettfrucht', light='y', cap=30, syn='Käsealternative, veganer Reibekäse, vegane Scheiben, Violife, Simply V, Pflanzenkäse', alts='Hefeflocken; Cashewkerne; Avocado',
  why='Kokosfett und Stärke. Eine Scheibe ist okay, Hefeflocken geben den Käsegeschmack leichter.')
f('Veganer Käse (Cashew)', 'H882000', 'nuss', light='y', cap=30, syn='Cashewkäse, Käsealternative Cashew, fermentierter Cashew, veganer Camembert', alts='Cashewkerne; Hefeflocken',
  why='Aus Cashewkernen, aber recht eiweißreich. Eine kleine Portion passt.')
f('Veganes Schnitzel', 'H910400', 'eiweiss', syn='Veggie-Schnitzel, vegane Nuggets, Rügenwalder, Like Meat, vegetarisches Schnitzel, veganes Hack, Beyond Meat')
f('Vegane Würstchen', 'H910500', 'eiweiss', syn='vegetarische Wiener, Veggie-Würstchen, Tofuwürstchen, vegane Bratwurst')
f('Proteinpulver', 'H011000', 'eiweiss', syn='Eiweißpulver, Whey, Sojaprotein, Erbsenprotein, Proteinshake, Eiweißshake', alts='Mandeldrink ungesüßt; Walnusskerne',
  why='Fast reines Eiweiß. Genau das hält Prof. Dr. Longo in diesen Tagen niedrig.')
f('Lupinenmehl', 'H731400', 'eiweiss', syn='Lupine, Süßlupine, Lupinenschrot, Sojamehl', alts='Kichererbsenmehl; Vollkornmehl')
f('Sojakerne (geröstet)', 'H760600', 'eiweiss', syn='Sojanüsse, geröstete Sojabohnen, Edamame geröstet', alts='Mandeln; Kürbiskerne')

# Obst frisch
f('Clementine', 'F607100', 'obst', syn='Clementinen, Satsuma, Tangerine', alts='Orange; Heidelbeeren', piece=('Stück', 60))
f('Pomelo', 'F605100', 'obst', syn='Pampelmuse', alts='Orange; Heidelbeeren')
f('Kaki', 'F507100', 'obst', cap=80, syn='Sharon, Persimone, Sharonfrucht', alts='Apfel; Orange')
f('Maracuja', 'F508100', 'obst', cap=80, syn='Passionsfrucht', alts='Himbeeren; Orange', piece=('Stück', 20))
f('Litschi', 'F515100', 'obst', cap=60, syn='Lychee, Litschis', alts='Erdbeeren; Himbeeren')
f('Mirabellen', 'F224100', 'obst', cap=80, syn='Mirabelle, Reineclauden', alts='Himbeeren; Heidelbeeren')
f('Quitte', 'F140100', 'obst', syn='Quitten', alts='Apfel; Birne')
f('Preiselbeeren (frisch)', 'F401100', 'obst', cap=100, syn='Preiselbeeren, Cranberries frisch, Moosbeeren frisch')
f('Schwarze Johannisbeeren', 'F323100', 'obst', cap=100, syn='Cassis, schwarze Ribisel, Beeren')
f('Guave', 'F513100', 'obst', syn='Guava', alts='Erdbeeren; Orange')
f('Sternfrucht', 'F553100', 'obst', syn='Karambole')
f('Jackfrucht', 'F549100', 'obst', cap=80, syn='Jackfruit, Jackfrucht reif', alts='Mango; Champignons')

# Obst aus Dose und Glas
f('Fruchtcocktail (ungesüßt)', 'F093902', 'obst', cap=100, syn=f'Obstsalat, Fruchtmischung im eigenen Saft {DO}', alts='Erdbeeren; Apfel')
f('Ananas (Dose, ungesüßt)', 'F5A1902', 'obst', cap=100, syn=f'Ananas im eigenen Saft, Ananasscheiben {DO}', alts='Erdbeeren; Orange')
f('Pfirsiche (Dose, ungesüßt)', 'F208902', 'obst', cap=150, syn=f'Pfirsiche ohne Zucker {DO}', alts='Erdbeeren; Himbeeren')
f('Sauerkirschen (Glas, ungesüßt)', 'F213902', 'obst', cap=100, syn=f'Schattenmorellen ungesüßt {DO}', alts='Himbeeren; Johannisbeeren')
f('Pfirsiche (Dose, gezuckert)', 'F203902', 'suess', syn=f'Dosenpfirsiche, Pfirsiche in Sirup, Aprikosen Dose {DO}', alts='Pfirsich; Erdbeeren',
  why='In Zuckersirup eingelegt. Frisches Obst oder ungesüßte Konserven passen.')
f('Ananas (Dose, gezuckert)', 'F501902', 'suess', syn=f'Ananas in Sirup {DO}', alts='Ananas; Erdbeeren',
  why='In Zuckersirup eingelegt. Frisches Obst oder ungesüßte Konserven passen.')
f('Mandarinen (Dose)', 'F606902', 'suess', syn=f'Mandarin-Orangen, Dosenmandarinen {DO}', alts='Mandarine; Orange',
  why='In Zuckersirup eingelegt. Frische Mandarinen passen.')
f('Schattenmorellen (Glas)', 'F212902', 'suess', syn=f'Sauerkirschen gezuckert, Kirschen {DO}', alts='Sauerkirschen; Himbeeren',
  why='Gezuckert. Frische oder ungesüßte Kirschen passen.')
f('Apfelmus (gezuckert)', 'F921900', 'suess', syn='Apfelkompott gezuckert, Apfelmus Glas', alts='Apfelmus ungesüßt; Apfel',
  why='Ein Fünftel davon ist Zucker. Ungesüßtes Apfelmark passt.')
f('Preiselbeeren (Glas)', 'F4A1900', 'suess', syn='Wildpreiselbeeren, Preiselbeerkompott, Cranberrysauce', alts='Preiselbeeren (frisch); Himbeeren')
f('Rote Grütze', 'Y855053', 'suess', syn='Grütze, Kompott, Fruchtgrütze, Götterspeise', alts='Beerenmischung (TK); Himbeeren')
f('Pflaumenmus', 'S161000', 'suess', syn='Powidl, Apfelkraut, Birnenkraut, Zwetschgenmus', alts='Apfelmus ungesüßt; Pflaumen')

# Trockenobst
f('Getrocknete Pflaumen', 'F220400', 'suess', syn='Trockenpflaumen, Backpflaumen, Dörrpflaumen, Trockenobst', alts='Pflaumen; Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Getrocknete Feigen', 'F505400', 'suess', syn='Trockenfeigen, Feigen getrocknet, Trockenobst', alts='Feigen (frisch); Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Apfelringe', 'F110400', 'suess', syn='getrocknete Äpfel, Apfelchips, Trockenobst', alts='Apfel; Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Bananenchips', 'F503400', 'suess', syn='getrocknete Banane, Trockenobst', alts='Banane; Walnusskerne',
  why='Getrocknetes Obst ist konzentrierter Zucker, oft zusätzlich frittiert.')
f('Getrocknete Mango', 'F516400', 'suess', syn='Mangostreifen, Trockenmango, getrocknete Ananas, getrocknete Papaya, Trockenobst', alts='Mango; Orange',
  why='Getrocknetes Obst ist konzentrierter Zucker.')
f('Fruchtschnitte', 'F820000', 'suess', syn='Fruchtriegel, Dattelriegel, Rohkostriegel, Energy Balls', alts='Apfel; Walnusskerne',
  why='Gepresstes Trockenobst ist konzentrierter Zucker.')

# Zucker, Sirup, Süßes
f('Brauner Zucker', 'S112000', 'suess', syn='Rohrzucker, Rohzucker, Kandis, Kokosblütenzucker, Vollrohrzucker, Puderzucker, Vanillezucker')
f('Traubenzucker', 'S115100', 'suess', syn='Dextrose, Dextro Energy, Glukose, Fruchtzucker')
f('Ahornsirup', 'S151100', 'suess', syn='Maple Syrup, Sirup, Reissirup, Dattelsirup')
f('Agavendicksaft', None, 'suess', syn='Agavensirup, Dicksaft, Apfeldicksaft, Birnendicksaft', n=(310, 0.1, 0.5, 76.0, 68.0))
f('Zuckerrübensirup', 'S152000', 'suess', syn='Melasse, Rübenkraut, Grafschafter Goldsaft')
f('Xylit', 'S163000', 'suess', syn='Birkenzucker, Xylitol, Erythrit, Zuckeralkohol, Sorbit', alts='Zimt; Heidelbeeren',
  why='Zuckerersatz kommt in Prof. Dr. Longos Protokoll nicht vor. Wir raten, die fünf Tage ohne Süßes auszukommen, dann lässt auch die Lust darauf nach.')
f('Süßstoff', 'S170000', 'suess', syn='Stevia, Saccharin, Aspartam, Sucralose, Süßstofftabletten, Flüssigsüße, Canderel', alts='Zimt; Zitronensaft',
  why='Kalorienfrei, kommt aber in Prof. Dr. Longos Protokoll nicht vor. Wir raten, die fünf Tage ohne Süßes auszukommen.')
f('Zartbitterschokolade', 'S560000', 'suess', syn='Halbbitterschokolade, dunkle Schokolade, Herrenschokolade, Kuvertüre', alts='Walnusskerne; Kakaopulver (ungesüßt); Heidelbeeren')
f('Bitterschokolade', 'S570000', 'suess', syn='Schokolade 70 %, Schokolade 85 %, Edelbitter, Lindt Excellence, Kakaonibs', alts='Walnusskerne; Kakaopulver (ungesüßt); Mandeln',
  why='Auch dunkle Schokolade besteht zu rund einem Drittel aus Zucker. Nüsse mit einem Hauch ungesüßtem Kakao helfen über die Lust hinweg.')
f('Weiße Schokolade', 'S580000', 'suess', syn='Milka, Ritter Sport, Kinderschokolade, Vollmilchschokolade')
f('Schokoriegel', 'S581100', 'suess', syn='Snickers, Mars, Twix, Bounty, KitKat, Duplo, Kinderriegel, Hanuta, Knoppers', alts='Walnusskerne; Mandeln; Apfel')
f('Pralinen', 'S610000', 'suess', syn='Konfekt, Trüffel, Ferrero Rocher, Mon Cheri, Toffifee, Raffaello', alts='Walnusskerne; Mandeln')
f('Schokokuss', 'S582200', 'suess', syn='Schaumkuss, Dickmanns, Marshmallows, Mäusespeck', alts='Heidelbeeren; Erdbeeren')
f('Marzipan', 'S420000', 'suess', syn='Marzipankartoffeln, Mozartkugeln, Nougat, Persipan', alts='Mandeln; Mandelmus')
f('Bonbons', 'S311000', 'suess', syn='Hustenbonbons, Lutscher, Karamell, Toffee, Kaugummi, Werthers, Nimm2', alts='Kräutertee; Minze')
f('Kandierter Ingwer', 'S478100', 'suess', syn='Ingwerstäbchen, kandierte Früchte, Zitronat, Orangeat', alts='Ingwer')
f('Vanilleeis', 'S241000', 'suess', syn='Milcheis, Schokoladeneis, Eis am Stiel, Magnum, Cornetto, Ben & Jerrys, Häagen-Dazs, Sahneeis', alts='Heidelbeeren; Kokosmilch (vollfett)')
f('Sorbet', 'S201000', 'suess', syn='Fruchteis, Wassereis, Zitronensorbet, Frozen Yogurt', alts='Beerenmischung (TK); Himbeeren',
  why='Kein Fett, dafür viel Zucker. Angetaute TK-Beeren sind fast wie Sorbet.')
f('Kakaogetränkepulver', 'S723000', 'suess', syn='Trinkkakao, Kaba, Nesquik, Ovomaltine, Trinkschokolade, Instantkakao', alts='Kakaopulver (ungesüßt); Mandeldrink ungesüßt',
  why='Besteht zu drei Vierteln aus Zucker. Ein Teelöffel ungesüßter Kakao in warmem Mandeldrink passt.')

# Gebäck und Kuchen
f('Brownies', 'D4A2000', 'suess', syn='Schokokuchen, Schokoladenkuchen, Muffin, Schokomuffin', alts='Walnusskerne; Kakaopulver (ungesüßt)')
f('Donut', 'D741600', 'suess', syn='Berliner, Krapfen, Kreppel, Quarkbällchen', alts='Apfel; Walnusskerne')
f('Waffeln', 'D621000', 'suess', syn='Waffel, Pfannkuchen, Crêpe, Pancakes, Kaiserschmarrn', alts='Haferbrei (mit Wasser); Apfelmus ungesüßt')
f('Apfelstrudel', 'D4A1000', 'suess', syn='Apfelkuchen, Apfeltasche, Strudel', alts='Apfel; Zimt; Walnusskerne')
f('Käsekuchen', 'D461200', 'suess', syn='Quarkkuchen, Cheesecake, Sahnetorte, Torte', alts='Sojajoghurt; Heidelbeeren')
f('Marmorkuchen', 'D431100', 'suess', syn='Rührkuchen, Sandkuchen, Napfkuchen, Gugelhupf, Zitronenkuchen', alts='Apfel; Walnusskerne')
f('Streuselkuchen', 'D461500', 'suess', syn='Butterkuchen, Blechkuchen, Hefekuchen, Bienenstich, Zimtschnecke, Franzbrötchen, Rosinenbrötchen, Hefezopf', alts='Apfel; Walnusskerne')
f('Lebkuchen', 'D650600', 'suess', syn='Pfefferkuchen, Printen, Spekulatius, Dominosteine, Stollen, Weihnachtsgebäck, Zimtsterne', alts='Mandeln; Zimt; Mandarine')

# Säfte und Getränke
f('Apfelsaft', 'F110600', 'drink', syn='Saft, Direktsaft, naturtrüb', alts='Apfel; Kräutertee',
  why='Ein Glas enthält so viel Zucker wie drei Äpfel, aber sättigt nicht.')
f('Apfelschorle', 'N256000', 'drink', syn='Saftschorle, Schorle, Rhabarberschorle, Johannisbeerschorle', alts='Mineralwasser; Zitronensaft; Kräutertee',
  why='Auch verdünnt bleibt es Zuckerwasser. Wasser mit einem Spritzer Zitrone erfrischt genauso.')
f('Traubensaft', 'F310600', 'drink', syn='Saft, Kirschsaft, Johannisbeersaft, Granatapfelsaft, Hohes C', alts='Weintrauben; Kräutertee')
f('Multivitaminsaft', 'F010600', 'drink', syn='Mehrfruchtsaft, Saft, Capri-Sun, Punica, Fruchtsaftgetränk, Nektar, ACE-Saft, Valensina', alts='Orange; Kräutertee')
f('Ananassaft', 'F501600', 'drink', syn='Saft, Mangosaft, Maracujasaft, Grapefruitsaft', alts='Ananas; Kräutertee')
f('Tomatensaft', 'G560600', 'getraenk', light='y', cap=200, syn='Gemüsesaft Tomate', alts='Gemüsebrühe; Tomaten',
  why='Ein Glas passt. Im Saft fehlt aber die Sättigung von ganzen Tomaten.')
f('Karottensaft', 'G620600', 'getraenk', light='y', cap=200, syn='Möhrensaft, Gemüsesaft Karotte', alts='Karotten; Gemüsebrühe',
  why='Ein Glas passt. Im Saft fehlt aber die Sättigung vom ganzen Gemüse.')
f('Rote-Bete-Saft', 'G613600', 'getraenk', light='y', cap=150, syn='Rote Bete Saft, Randensaft', alts='Rote Bete (vorgegart); Gemüsebrühe',
  why='Recht süß. Ein kleines Glas passt.')
f('Sauerkrautsaft', 'G345600', 'getraenk', cap=300, syn='Sauerkraut-Saft, Krautsaft')
# Kombucha: kein USDA-Standardeintrag, Richtwert aus typischen Herstellerangaben (ca. 15 bis 20 kcal, 3 bis 4 g Zucker je 100 ml)
f('Kombucha', None, 'drink', syn='Wasserkefir, Teepilz, fermentierter Tee', alts='Kräutertee; Grüner Tee',
  why='Fermentierter, gezuckerter Tee mit etwas Restzucker und Spuren von Alkohol. Ungesüßter Tee ist die Basis in diesen Tagen.', n=(17, 0, 0, 4.0, 3.6))
f('Eistee', 'N019000', 'drink', syn='Ice Tea, Lipton, Pfanner, Volvic Tee, Eistee Pfirsich', alts='Kräutertee; Früchtetee')
f('Zitronenlimonade', 'N310400', 'drink', syn='Limo, Sprite, 7up, Zitronenlimo, Bionade, Almdudler, Brause', alts='Mineralwasser; Zitronensaft')
f('Orangenlimonade', 'N310300', 'drink', syn='Fanta, Orangina, Limo, Mezzo Mix, Spezi', alts='Mineralwasser; Orange')
f('Tonic Water', 'N314000', 'drink', syn='Bitter Lemon, Ginger Ale, Ginger Beer, Schweppes', alts='Mineralwasser; Limettensaft')
f('Cola Zero', 'N331000', 'drink', syn='Cola light, Coke Zero, Pepsi Max, zuckerfreie Cola, Diät-Cola', alts='Mineralwasser; Kräutertee',
  why='Kalorienfrei, aber mit Süßstoff und Koffein. Beides kommt in Prof. Dr. Longos Protokoll nicht vor.')
f('Limonade ohne Zucker', 'N311000', 'drink', syn='Light-Limonade, Zero-Limo, Sprite Zero, Fanta Zero, zuckerfreie Limonade, Red Bull Sugarfree, Energy Zero', alts='Mineralwasser; Zitronensaft',
  why='Kalorienfrei, aber mit Süßstoff. Der kommt in Prof. Dr. Longos Protokoll nicht vor. Wasser mit Zitrone erfrischt genauso.')
f('Wasser mit Geschmack (ungesüßt)', 'N001000', 'getraenk', cap=1500, syn='aromatisiertes Wasser, Near Water, Infused Water, Wasser mit Zitrone, Wasser mit Minze')
f('Malzbier', 'P122000', 'drink', syn='Malztrunk, Vitamalz, Karamalz', alts='Mineralwasser; Kräutertee')
f('Alkoholfreies Bier', 'P163100', 'drink', syn='Bier alkoholfrei, Pils alkoholfrei, Weizen alkoholfrei, 0,0', alts='Mineralwasser; Kräutertee',
  why='Ohne Alkohol, aber mit Malzzucker. Nach den fünf Tagen schmeckt es umso besser.')
f('Radler', 'P192000', 'drink', syn='Alsterwasser, Biermischgetränk, Russ, Weizenbier, Hefeweizen', alts='Mineralwasser; Zitronensaft')
f('Sekt', 'P2A6000', 'drink', syn='Prosecco, Champagner, Schaumwein, Aperol Spritz, Hugo', alts='Mineralwasser; Limettensaft')
f('Spirituosen', 'P712000', 'drink', syn='Wodka, Gin, Whisky, Rum, Schnaps, Korn, Likör, Tequila, Obstbrand, Cocktail, Longdrink', alts='Mineralwasser; Kräutertee')
f('Glühwein', 'P281000', 'drink', syn='Punsch, Feuerzangenbowle, Kinderpunsch', alts='Früchtetee; Zimt')
f('Rooibostee', 'N601000', 'getraenk', syn='Rotbuschtee, Roibusch, Rooibos')
f('Früchtetee', 'N710000', 'getraenk', syn='Hagebuttentee, Hibiskustee, Malventee, Apfeltee, Teekanne, Meßmer')
f('Pfefferminztee', 'N721000', 'getraenk', syn='Minztee, Kamillentee, Fencheltee, Ingwertee, Salbeitee, Melissentee')
f('Mate-Tee', 'N611000', 'getraenk', light='y', cap=250, syn='Mate, Yerba Mate', alts='Kräutertee; Rooibostee',
  why='Ungesüßt passt eine Tasse. Enthält Koffein, deshalb am selben Tag lieber Tee oder Kaffee, nicht beides. Gesüßte Mate-Limonade gehört nicht dazu.')
f('Espresso', 'N411100', 'getraenk', light='y', cap=60, syn='Mokka, türkischer Kaffee, Ristretto, Nespresso', alts='Kräutertee; Getreidekaffee',
  why='Wenn es ohne nicht geht: ein Espresso am Tag, schwarz und ohne Zucker. So empfiehlt es der Hersteller des Fertigprodukts ProLon für Kaffee.')
f('Kaffee (entkoffeiniert)', 'N415000', 'getraenk', light='y', cap=150, syn='Decaf, koffeinfreier Kaffee, entkoffeiniert', alts='Kräutertee; Getreidekaffee',
  why='Die Herstellerempfehlung „höchstens eine kleine Tasse“ unterscheidet nicht nach Koffein. Wir behandeln entkoffeinierten Kaffee deshalb genauso.')
f('Getreidekaffee', 'N500100', 'getraenk', cap=500, syn='Malzkaffee, Caro Kaffee, Kaffeeersatz, Zichorienkaffee, Lupinenkaffee, Muckefuck')
f('Kaffee mit Haferdrink', 'N4A0000', 'getraenk', light='y', cap=150, syn='Kaffee mit Hafermilch, Kaffee mit Mandeldrink, Kaffee mit Sojadrink, Hafer-Cappuccino klein', alts='Kräutertee; Getreidekaffee',
  why='Eine kleine Tasse mit einem Schuss ungesüßtem Pflanzendrink ist okay. Der Hersteller von ProLon rät zu Kaffee ohne Zusätze.')
f('Kaffee mit Milch', 'N410200', 'milch', syn='Milchkaffee, Kaffee weiß, Kaffee mit Kaffeesahne', alts='Kaffee; Kaffee mit Haferdrink',
  why='Milch macht in diesen Tagen Pause. Wenn Kaffee, dann eine kleine Tasse schwarz.')
f('Cappuccino', 'N414000', 'milch', syn='Latte macchiato, Flat White, Caffè Latte, Starbucks, Eiskaffee, Instant-Cappuccino', alts='Kaffee; Kaffee mit Haferdrink',
  why='Besteht vor allem aus Milch. Wenn Kaffee, dann eine kleine Tasse schwarz.')


# Obergrenze je Lebensmittel und Tag (eigene Regel der Seite, Prof. Dr. Longo nennt keine Mengen pro Lebensmittel):
# Ein einzelnes Lebensmittel darf höchstens die Hälfte des Zucker- bzw. Eiweißbudgets von Tag 2 bis 5 belegen,
# damit für den Rest des Tages Platz bleibt. Budget Tag 2 bis 5: 725 kcal, davon 9 % Eiweiß (Prof. Dr. Longo) und
# höchstens 15 % Zucker (eigene Regel). Dazu kommt die Portionsgrenze der Gruppe bzw. des Eintrags (cap).
DAY_KCAL = 725
PROTEIN_BUDGET = DAY_KCAL * 0.09 / 4   # 16,3 g
SUGAR_BUDGET = DAY_KCAL * 0.15 / 4     # 27,2 g
SHARE = 0.5

def _floor(g):
    step = 10 if g >= 100 else 5 if g >= 30 else 1
    return int(g // step * step)

def limit(cap, n):
    """Liefert (Obergrenze in g, Grund). n = (kcal, Eiweiß, Fett, Kohlenhydrate, Zucker) je 100 g.
    Grund: 'portion' (übliche Portion), 'zucker' oder 'eiweiss' (Budgetregel)."""
    out, why = cap, 'portion'
    if n[4] > 0:
        g = _floor(SHARE * SUGAR_BUDGET / n[4] * 100)
        if g < out: out, why = g, 'zucker'
    if n[1] > 0:
        g = _floor(SHARE * PROTEIN_BUDGET / n[1] * 100)
        if g < out: out, why = g, 'eiweiss'
    return out, why


def bls_table():
    """Nährwerte je 100 g als (kcal, Eiweiß, Fett, Kohlenhydrate gesamt, Zucker, Ballaststoffe) für alle Einträge mit BLS-Code.
    Kohlenhydrate gesamt = verfügbare Kohlenhydrate + Ballaststoffe, wie in den bisherigen Daten und in Prof. Dr. Longos US-Quellen."""
    import json, os
    b = json.load(open(os.path.join(os.path.dirname(__file__), 'bls_values.json')))
    out = {}
    for x in F:
        if x['bls']:
            e = b[x['bls']]
            out[x['name']] = (e['kcal'], e['protein'], e['fat'], round(e['cho'] + e['fiber'], 2), e['sugar'], e['fiber'])
    return out


# ---------------------------------------------------------------------------------------------
# Erweiterung Produktbreite (14.11.2026): Varianten von Joghurt, Pflanzendrinks, Kochcremes, Ölen,
# Milchprodukten, Essig, Mehl und Süßungsmitteln. Wo der BLS keinen Eintrag hat (fast alle pflanzlichen
# Alternativen), stehen Richtwerte aus typischen Herstellerangaben (Mittel mehrerer Marken laut Open Food Facts,
# Abruf 14.11.2026). Kohlenhydrate wie überall inklusive Ballaststoffe. Marken stehen nur als Suchbegriffe da.
# ---------------------------------------------------------------------------------------------
# Pflanzendrinks
f('Cashewdrink ungesüßt', None, 'getraenk', cap=250, syn='Cashewmilch, Cashewdrink, Cashew Drink natur, Provamel Cashew, Alpro Cashew, Nussdrink, Nussmilch', n=(38, 1.2, 3.0, 1.5, 0.4), db='Hersteller')
f('Kokosdrink ungesüßt', None, 'getraenk', cap=250, syn='Kokosmilch zum Trinken, Kokosnussdrink, Alpro Kokosnuss ungesüßt, Kokos Drink natur, Koko', n=(20, 0.3, 1.8, 1.0, 0.6), db='Hersteller')
f('Macadamiadrink ungesüßt', None, 'getraenk', cap=250, syn='Macadamiamilch, Macadamia Drink, Milkadamia, Walnussdrink, Pistaziendrink', n=(28, 0.4, 2.7, 0.8, 0.1), db='Hersteller')
f('Hanfdrink ungesüßt', None, 'getraenk', cap=250, syn='Hanfmilch, Hanf Drink, Good Hemp', n=(24, 0.8, 2.0, 0.8, 0.3), db='Hersteller')
f('Haselnussdrink', None, 'getraenk', light='y', cap=200, syn='Haselnussmilch, Alpro Haselnuss, Haselnuss Drink', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt',
  why='Fast immer leicht gesüßt. Ein Schuss passt, die ungesüßten Nussdrinks sind die bessere Wahl.', n=(29, 0.4, 1.6, 3.5, 3.2), db='Hersteller')
f('Erbsendrink ungesüßt', None, 'getraenk', light='y', cap=200, syn='Erbsenmilch, Erbsenproteindrink, vly, Happea, Sproud, Lupinendrink, Lupinenmilch', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt',
  why='Ungesüßt okay, aber eiweißreicher als Mandel- oder Cashewdrink.', n=(40, 3.4, 2.0, 2.0, 0.1), db='Hersteller')
f('Dinkeldrink', None, 'getraenk', light='y', cap=150, syn='Dinkelmilch, Dinkel Drink natur, Natumi Dinkel', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt',
  why='Die Stärke aus dem Dinkel wird beim Herstellen zu Zucker. Ein Schuss passt, Mandeldrink ist zuckerärmer.', n=(44, 0.8, 1.1, 8.2, 6.0), db='Hersteller')
f('Reis-Kokos-Drink', None, 'getraenk', light='y', cap=150, syn='Reis Kokos Drink, Kokos-Reis-Drink, Alpro Kokosnuss Original, Kokosdrink mit Reis', alts='Kokosdrink ungesüßt; Mandeldrink ungesüßt',
  why='Der Reisanteil bringt Zucker mit. Der ungesüßte Kokosdrink ohne Reis passt besser.', n=(45, 0.4, 1.1, 8.5, 4.5), db='Hersteller')
f('Haferdrink Barista', None, 'getraenk', light='y', cap=100, syn='Hafer Barista, Oatly Barista, Barista Hafer, Hafermilch Barista, Alpro Barista Hafer', alts='Mandeldrink ungesüßt; Haferdrink',
  why='Mehr Fett und etwas Zucker aus dem Hafer, damit er schäumt. Ein Schuss in den Kaffee passt.', n=(58, 1.0, 2.6, 7.8, 3.8), db='Hersteller')

# Pflanzliche Joghurts (ungesüßt)
f('Kokosjoghurt', None, 'pflanz', cap=100, syn='Kokosjoghurt natur, Kokos-Joghurtalternative, Kokosghurt, Harvest Moon, Alpro Kokosnuss Joghurt, Coconut Collaborative, veganer Joghurt', alts='Kokosmilch (vollfett); Avocado',
  why='Ungesüßt passt er mit seinem Fett gut in den Tag. Ein kleiner Becher reicht.', n=(110, 0.8, 9.5, 5.5, 0.8), db='Hersteller')
f('Mandeljoghurt', None, 'pflanz', cap=100, syn='Mandeljoghurt natur, Mandel-Joghurtalternative, Mandelghurt, Mandel natur, veganer Joghurt', alts='Kokosjoghurt; Mandeln', n=(55, 0.8, 3.2, 5.3, 0.5), db='Hersteller')
f('Cashewjoghurt', None, 'pflanz', cap=100, syn='Cashewjoghurt natur, Cashew-Joghurtalternative, Cashew natur, veganer Joghurt', alts='Kokosjoghurt; Cashewkerne', n=(89, 2.1, 6.6, 5.7, 0.9), db='Hersteller')
f('Haferjoghurt', None, 'pflanz', cap=80, syn='Haferjoghurt natur, Hafer-Joghurtalternative, Hafergurt, Oatly Hafergurt, veganer Joghurt', alts='Kokosjoghurt; Mandeljoghurt',
  why='Der Hafer bringt natürlichen Zucker mit. Ein paar Löffel passen, Kokos- oder Mandeljoghurt sind zuckerärmer.', n=(83, 0.7, 4.5, 10.0, 5.8), db='Hersteller')
f('Lupinenjoghurt', None, 'pflanz', cap=100, syn='Lupinenjoghurt natur, Lupinen-Joghurtalternative, Made with Luve, Luve, veganer Joghurt', alts='Kokosjoghurt; Mandeljoghurt', n=(101, 1.8, 6.0, 10.0, 1.5), db='Hersteller')
f('Sojaquark', None, 'pflanz', cap=60, syn='Skyr-Alternative, Soja-Skyr, Alpro Skyr Style, veganer Quark, veganer Skyr, Quarkalternative, Sojade Skyr', alts='Kokosjoghurt; Mandeljoghurt',
  why='Pflanzlich, aber eiweißreich wie Tofu. Ein paar Löffel passen, mehr kostet zu viel vom Eiweißbudget.', n=(62, 6.0, 3.2, 2.5, 1.0), db='Hersteller')
f('Pflanzenjoghurt (gesüßt)', None, 'suess', syn='Kokosjoghurt Mango, Kokosjoghurt Frucht, Haferjoghurt Frucht, Mandeljoghurt Vanille, veganer Fruchtjoghurt, Joghurtalternative Heidelbeere', alts='Kokosjoghurt; Heidelbeeren',
  why='Gesüßt und aromatisiert. Die ungesüßte Variante mit frischen Beeren passt.', n=(100, 0.6, 5.0, 14.0, 10.5), db='Hersteller')

# Pflanzliche Kochcremes, Frischkäse, Kokosprodukte
f('Haferkochcreme', None, 'pflanz', cap=50, syn='Hafer Cuisine, Hafercreme, Hafersahne, Oatly Cuisine, Oatly iMat, Reis Cuisine, Dinkel Cuisine, vegane Sahne, Pflanzensahne', alts='Kokosmilch (vollfett); Cashewmus',
  why='Pflanzlich, aber verarbeitet. Ein Schuss für die Soße passt.', n=(110, 0.7, 9.0, 6.2, 2.5), db='Hersteller')
f('Kokoskochcreme', None, 'pflanz', cap=60, syn='Kokos Cuisine, Kokossahne, Kokoscreme zum Kochen, vegane Sahne', alts='Kokosmilch (vollfett); Cashewmus',
  why='Pflanzlich, aber verarbeitet. Ein Schuss für die Soße passt.', n=(130, 1.1, 13.0, 2.6, 1.4), db='Hersteller')
f('Mandelkochcreme', None, 'pflanz', cap=60, syn='Mandel Cuisine, Mandelsahne, Mandelcreme zum Kochen, vegane Sahne', alts='Kokosmilch (vollfett); Mandelmus',
  why='Pflanzlich, aber verarbeitet. Ein Schuss für die Soße passt.', n=(85, 0.9, 8.7, 0.9, 0.3), db='Hersteller')
f('Vegane Schlagcreme', None, 'pflanz', cap=30, syn='Schlagfix, vegane Schlagsahne, Schlagcreme, Soyatoo, Pflanzencreme zum Aufschlagen, Rama Schlagcreme', alts='Kokosmilch (vollfett); Cashewmus',
  why='Gehärtetes Pflanzenfett, oft leicht gesüßt. Ein Klecks ist okay.', n=(200, 0.5, 19.0, 6.0, 3.0), db='Hersteller')
f('Veganer Frischkäse', None, 'pflanz', cap=30, syn='Frischkäsealternative, Simply V Streichgenuss, Oatly Aufstrich, veganer Streichkäse, Mandel-Frischkäse, Philadelphia vegan, Bedda', alts='Hummus; Cashewmus',
  why='Meist aus Mandeln oder Hafer mit Kokosfett. Dünn gestrichen passt er.', n=(245, 3.5, 23.0, 6.0, 1.0), db='Hersteller')
f('Kokosmilch (fettreduziert)', None, 'fettfrucht', cap=150, syn='Kokosmilch light, leichte Kokosmilch, Kokosmilch fettarm', n=(110, 1.0, 11.0, 1.8, 0.8), db='Hersteller')
f('Kokosmus', None, 'fettfrucht', light='y', cap=15, syn='Kokosbutter, Kokosmanna, Kokoscreme, Creamed Coconut', alts='Mandelmus; Tahin',
  why='Viel gesättigtes Fett wie beim Kokosöl. Ein Teelöffel ist okay.', n=(690, 7.0, 66.0, 19.0, 7.0), db='Hersteller')
f('Kokoschips', None, 'fettfrucht', light='y', cap=15, syn='Kokoschips ungesüßt, Kokosstreifen, Kokosnusschips', alts='Walnusskerne; Mandeln',
  why='Viel gesättigtes Fett wie beim Kokosöl. Als Topping okay, Nüsse passen besser.', n=(680, 7.3, 65.0, 20.0, 6.8), db='Hersteller')
f('Kokosmehl', None, 'fettfrucht', light='y', cap=15, syn='Kokosnussmehl', alts='Kichererbsenmehl; Vollkornmehl',
  why='Entölt und deshalb zu einem Fünftel Eiweiß und fast ebenso viel Zucker. Ein Esslöffel zum Binden passt.', n=(360, 20.0, 13.0, 56.0, 18.0), db='Hersteller')

# Öle und Fette
f('Avocadoöl', None, 'fett', syn='Öl, Avocado-Öl', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Arganöl', None, 'fett', cap=15, syn='Öl, Argan-Öl', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Schwarzkümmelöl', None, 'fett', cap=10, syn='Öl, Schwarzkümmel', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Leindotteröl', None, 'fett', cap=15, syn='Öl, Camelinaöl', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Macadamiaöl', None, 'fett', cap=15, syn='Öl, Macadamianussöl, Aprikosenkernöl, Pistazienöl', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Mandelöl', 'Q190000', 'fett', cap=15, syn='Öl')
f('Mohnöl', 'Q350000', 'fett', cap=15, syn='Öl')
f('Würzöl', None, 'fett', cap=15, syn='Öl, Chiliöl, Knoblauchöl, Trüffelöl, Zitronenöl, Kräuteröl, Basilikumöl, aromatisiertes Olivenöl', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Bratöl', 'Q940000', 'fett', syn='Öl, Frittieröl, Pflanzenöl, Speiseöl, Reisöl, Reiskeimöl, High-Oleic-Öl, Mazola, Thomy, Bellasan')
f('MCT-Öl', None, 'fett', light='y', cap=10, syn='Öl, MCT, Kokosöl MCT, C8-Öl', alts='Olivenöl; Rapsöl',
  why='Konzentriertes Fett aus Kokosöl. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.', n=(900, 0, 100, 0, 0), db='Hersteller')
f('Palmöl', 'Q150000', 'fett', light='y', cap=10, syn='Öl, Palmfett, Palmkernfett, Frittierfett', alts='Olivenöl; Rapsöl',
  why='Besteht zur Hälfte aus gesättigten Fettsäuren. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')
f('Vegane Butter', None, 'fett', light='y', cap=10, syn='Butteralternative, veganer Block, Naturli, Alsan, Flora Plant, pflanzliche Butter, Violife Block', alts='Olivenöl; Rapsöl',
  why='Pflanzlich, aber stark verarbeitet und oft aus Kokos- oder Sheafett. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.', n=(700, 0.5, 78.0, 0.3, 0.3), db='Hersteller')
f('Halbfettmargarine', 'Q440000', 'fett', light='y', cap=15, syn='Lätta, Halvarine, Diätmargarine, Becel light, Margarine light', alts='Olivenöl; Rapsöl',
  why='Pflanzlich, aber stark verarbeitet. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')
f('Pflanzencreme (zum Braten)', 'Q4B1000', 'fett', light='y', cap=10, syn='Rama Culinesse, Bratcreme, flüssige Margarine, Pflanzencreme', alts='Olivenöl; Rapsöl',
  why='Pflanzlich, aber stark verarbeitet. Prof. Dr. Longo setzt auf Olivenöl und Nüsse.')
f('Butterschmalz', 'Q683000', 'milch', syn='Ghee, Butterfett, Butaris, geklärte Butter', alts='Olivenöl; Rapsöl')
f('Halbfettbutter', 'Q640000', 'milch', syn='Butter leicht, Joghurtbutter, Streichzart, Kerrygold extra, Mischstreichfett', alts='Olivenöl; Avocado')

# Milch, Joghurt, Quark, Sahne, Käse (alles rot: Scheinfasten ist rein pflanzlich)
f('H-Milch', 'M113300', 'milch', syn='haltbare Milch, H-Vollmilch, Weihenstephan', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt')
f('Laktosefreie Milch', 'M114300', 'milch', syn='Milch laktosefrei, MinusL, LAC', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt')
f('Magermilch', 'M111100', 'milch', syn='entrahmte Milch, Milch 0,1 %, Milch 0,3 %', alts='Mandeldrink ungesüßt; Kokosdrink ungesüßt')
f('Ziegenmilch', 'M021000', 'milch', syn='Schafmilch, Schafsmilch', alts='Mandeldrink ungesüßt; Cashewdrink ungesüßt')
f('Schokomilch', 'M206300', 'milch', syn='Kakao, Trinkschokolade, Müllermilch, Kakaomilch, heiße Schokolade', alts='Mandeldrink ungesüßt; Kakaopulver (ungesüßt)')
f('Fettarmer Joghurt', 'M141200', 'milch', syn='Joghurt 1,5 %, Joghurt fettarm', alts='Kokosjoghurt; Mandeljoghurt')
f('Magerjoghurt', 'M141100', 'milch', syn='Joghurt 0,1 %, Joghurt entrahmt', alts='Kokosjoghurt; Mandeljoghurt')
f('Griechischer Joghurt', 'M141500', 'milch', syn='Sahnejoghurt, Joghurt griechischer Art, Joghurt 10 %, türkischer Joghurt, Total, Süzme', alts='Kokosjoghurt; Cashewjoghurt')
f('Laktosefreier Joghurt', 'M1E3300', 'milch', syn='Joghurt laktosefrei, MinusL Joghurt', alts='Kokosjoghurt; Mandeljoghurt')
f('Schafjoghurt', 'M149500', 'milch', syn='Schafsjoghurt, Ziegenjoghurt, Schafmilchjoghurt', alts='Kokosjoghurt; Mandeljoghurt')
f('Trinkjoghurt', 'M2L2300', 'milch', syn='Joghurtdrink, Actimel, Yakult, Müller Froop Drink, Joghurt zum Trinken', alts='Mandeldrink ungesüßt; Heidelbeeren')
f('Ayran', 'M2S8300', 'milch', syn='Lassi, Joghurtgetränk, Dugh', alts='Mineralwasser; Mandeldrink ungesüßt')
f('Dickmilch', 'M121300', 'milch', syn='Sauermilch, Schwedenmilch, Setzmilch', alts='Kokosjoghurt; Mandeljoghurt')
f('Quark (20 % Fett)', 'M713300', 'milch', syn='Halbfettquark, Speisequark 20 %', alts='Kokosjoghurt; Cashewmus')
f('Sahnequark', 'M713500', 'milch', syn='Quark 40 %, Speisequark Fettstufe', alts='Kokosjoghurt; Cashewmus')
f('Kräuterquark', 'M8A5000', 'milch', syn='Quark mit Kräutern, Zaziki, Tzatziki, Quarkdip', alts='Hummus; Guacamole')
f('Saure Sahne', 'M172500', 'milch', syn='Sauerrahm, Sauerrahm 10 %', alts='Kokosjoghurt; Cashewmus')
f('Crème fraîche', 'M176800', 'milch', syn='Creme fraiche, Crème légère, Creme double', alts='Kokosmilch (vollfett); Cashewmus')
f('Kaffeesahne', 'M171500', 'milch', syn='Kaffeesahne 10 %, Kaffeeweißer, Kaffeerahm', alts='Mandeldrink ungesüßt; Haferdrink')
f('Mascarpone', 'M7A6800', 'milch', alts='Kokosmilch (vollfett); Cashewmus')
f('Emmentaler', 'M304600', 'milch', syn='Allgäuer Emmentaler, Schweizer Käse', alts='Cashewkerne; Grüne Oliven')
f('Edamer', 'M401500', 'milch', alts='Cashewkerne; Grüne Oliven')
f('Cheddar', 'M303700', 'milch', syn='Chester', alts='Cashewkerne; Hefeflocken')
f('Tilsiter', 'M403600', 'milch', alts='Cashewkerne; Grüne Oliven')
f('Bergkäse', 'M302600', 'milch', syn='Gruyère, Greyerzer, Appenzeller, Comté, Alpkäse', alts='Cashewkerne; Hefeflocken')
f('Butterkäse', 'M501600', 'milch', alts='Cashewkerne; Avocado')
f('Raclettekäse', 'M307700', 'milch', syn='Raclette, Fonduekäse', alts='Champignons; Cashewkerne')
f('Brie', 'M601700', 'milch', alts='Avocado; Cashewkerne')
f('Ziegenkäse', 'M6A9600', 'milch', syn='Ziegenweichkäse, Ziegenrolle, Chèvre', alts='Avocado; Walnusskerne')
f('Ziegenfrischkäse', 'M7A1600', 'milch', syn='Ziegenfrischkäse natur, Schaffrischkäse', alts='Hummus; Cashewmus')
f('Obazda', 'M863000', 'milch', syn='Obatzter, Käsecreme', alts='Hummus; Guacamole')

# Tofu, Essig, Nussmus
f('Räuchertofu', None, 'soja', cap=50, syn='geräucherter Tofu, Tofu geräuchert, Tofu mariniert', alts='Austernpilze; Champignons',
  why='Pflanzlich, aber sehr eiweißreich. Prof. Dr. Longos Tage 2 bis 5 sehen nur etwa 9 % Eiweiß vor.', n=(150, 15.5, 8.8, 1.9, 0.6), db='Hersteller')
f('Reisessig', None, 'wuerze', cap=30, syn='Essig, Sushi-Essig ungesüßt, Genmai Su', n=(18, 0.3, 0, 0.5, 0.3), db='Hersteller')
f('Balsamico bianco', None, 'wuerze', cap=15, syn='Condimento bianco, weißer Balsamico, heller Balsamico', n=(110, 0.3, 0, 23.3, 21.7), db='Hersteller')
f('Crema di Balsamico', None, 'wuerze', light='y', cap=10, syn='Balsamicocreme, Balsamico-Creme, Balsamico-Glasur', alts='Balsamico; Zitronensaft',
  why='Eingekochter Balsamico mit viel Zucker. Ein paar Tropfen zum Verzieren sind okay.', n=(240, 1.0, 0, 59.0, 43.0), db='Hersteller')
f('Pistazienmus', None, 'nuss', cap=30, syn='Pistaziencreme ungesüßt', n=(645, 23.0, 56.0, 16.0, 5.5), db='Hersteller')
f('Sonnenblumenkernmus', None, 'nuss', cap=30, syn='Sonnenblumenmus', n=(687, 18.0, 64.0, 13.0, 1.6), db='Hersteller')
f('Gemahlene Mandeln', 'H210400', 'nuss', cap=35, syn='Mandeln gemahlen, Mandelgrieß, Mandelmehl nicht entölt')

# Mehl und Süßungsmittel
f('Dinkelvollkornmehl', 'C235000', 'getreide', cap=30, syn='Dinkelmehl Vollkorn')
f('Roggenvollkornmehl', 'C221000', 'getreide', cap=30, syn='Roggenmehl Vollkorn, Roggenschrot')
f('Buchweizenmehl', 'C421000', 'getreide', cap=30)
f('Hafermehl', 'C233000', 'getreide', cap=30, syn='gemahlene Haferflocken')
f('Reismehl', 'C453000', 'getreide', cap=30, syn='Reis gemahlen')
f('Mandelmehl (entölt)', None, 'eiweiss', syn='Mandelmehl, Mandelprotein, Low-Carb-Mehl', alts='Mandeln; Vollkornmehl',
  why='Entöltes Mandelmehl ist zur Hälfte Eiweiß. Genau das hält Prof. Dr. Longo in diesen Tagen niedrig.', n=(380, 52.0, 12.0, 23.0, 7.0), db='Hersteller')
f('Kokosblütenzucker', None, 'suess', syn='Kokoszucker, Palmzucker, Kokosblütensirup', n=(383, 1.4, 0.5, 94.0, 88.0), db='Hersteller')
f('Reissirup', None, 'suess', syn='Reismalz, Gerstenmalz, Malzsirup', n=(316, 0.5, 0.5, 79.0, 53.0), db='Hersteller')
f('Dattelsirup', None, 'suess', syn='Dattelsüße, Dattelzucker', alts='Heidelbeeren; Apfel; Zimt', n=(285, 1.5, 0.5, 71.0, 67.0), db='Hersteller')
