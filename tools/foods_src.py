# Lebensmitteldatenbank für den Rechner.
# Nährwerte kommen aus dem Bundeslebensmittelschlüssel (BLS 4.0, Max Rubner-Institut, CC BY 4.0),
# siehe tools/bls_values.json (erzeugt mit tools/bls_import.py). Nur wenige Gewürze ohne BLS-Eintrag
# behalten die bisherigen USDA-angelehnten Richtwerte aus recipes_src.py (Feld bls = None).
#
# Ampel: g = passt gut, y = nur kleine Menge (Obergrenze cap in g pro Tag), r = passt nicht ins Scheinfasten.
# cap: Obergrenze pro Tag in Gramm, die der Rechner nie überschreitet. Die Werte sind Richtwerte dieser Seite,
# abgeleitet aus Longos Makroverteilung, keine Zahlen aus Longos Protokoll.
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
}

WHY = {
  'y': 'Eine kleine Menge passt prima, von mehr hält Longos Rezept nichts.',
  'tier': 'Longos Scheinfasten ist rein pflanzlich und eiweißarm. Pilze und Hülsenfrüchte übernehmen hier den herzhaften Part.',
  'milch': 'Scheinfasten ist rein pflanzlich, Milchprodukte machen deshalb Pause.',
  'suess': 'Longos Vorgabe heißt: wenig Zucker. Zucker würde sonst schnell das ganze Tagesbudget aufbrauchen.',
  'weissmehl': 'Kostet viele Kalorien und macht kaum satt. Gemüse bringt dir mehr auf den Teller.',
  'drink': 'Bringt Zucker oder Alkohol mit. Wasser und ungesüßter Tee sind in diesen Tagen die Basis.',
  'eiweiss': 'Fleischersatz besteht fast nur aus Eiweiß. Genau das hält Longo in diesen Tagen niedrig.',
  'knusper': 'Knusprig und leicht, aber fast reine Stärke. Ein, zwei Stück passen gut in den Tag, mehr verdrängt das Gemüse.',
}

ALTS = {
  'tier': ['Champignons', 'Austernpilze', 'Kichererbsen (gegart)', 'Walnusskerne'],
  'milch': ['Kokosmilch (vollfett)', 'Cashewkerne', 'Tahin', 'Mandeldrink ungesüßt'],
  'suess': ['Heidelbeeren', 'Apfel', 'Walnusskerne'],
  'weissmehl': ['Kartoffeln', 'Hirse (gegart)', 'Blumenkohl', 'Zucchini'],
  'drink': ['Kräutertee', 'Zitronensaft', 'Gemüsebrühe'],
  'eiweiss': ['Champignons', 'Austernpilze', 'Kichererbsen (gegart)'],
}

# name, BLS-Code, Gruppe, Ampel (None = Gruppe), cap (None = Gruppe), Suchbegriffe, Alternativen, Begründung, Stück (Bezeichnung, g)
F = []
def f(name, bls, group, light=None, cap=None, syn='', alts='', why='', piece=None, n=None):
    # n: nur für Einträge ohne BLS-Code, Richtwerte (kcal, Eiweiß, Fett, Kohlenhydrate gesamt, Zucker) je 100 g nach USDA FoodData Central
    F.append(dict(name=name, bls=bls, group=group, light=light, cap=cap, syn=[s.strip() for s in syn.split(',') if s.strip()],
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
f('Hokkaido-Kürbis', 'G581000', 'gemuese', syn='Kürbis, Hokkaido')
f('Gartenkürbis', 'G581100', 'gemuese', syn='Butternut, Muskatkürbis, Kürbis')
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
f('Olivenöl', 'Q120000', 'fett', syn='Öl')
f('Rapsöl', 'Q180000', 'fett', syn='Öl')
f('Leinöl', 'Q160000', 'fett', cap=15, syn='Öl')
f('Walnussöl', 'Q310000', 'fett', cap=15, syn='Öl')
f('Sesamöl', 'Q230000', 'fett', syn='Öl')
f('Kokosöl', 'Q550000', 'fett', light='y', cap=10, syn='Kokosfett', alts='Olivenöl; Rapsöl',
  why='Besteht überwiegend aus gesättigten Fettsäuren. Longo setzt auf Olivenöl und Nüsse.')

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
f('Mandeldrink ungesüßt', 'H800000', 'getraenk', cap=250, syn='Mandelmilch')

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
f('Tofu', 'H861000', 'soja', syn='Räuchertofu', alts='Austernpilze; Champignons',
  why='Pflanzlich, aber sehr eiweißreich. Longos Tage 2 bis 5 sehen nur etwa 9 % Eiweiß vor.')

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
  why='Eine dünne Scheibe passt an Tag 1. Für Brot sieht Longo sonst kaum Platz vor.')

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
f('Zucker', 'S111000', 'suess', syn='Haushaltszucker, Rohrzucker')
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
  why='Fisch ist tierisches Eiweiß. Omega-3 bekommst du im Scheinfasten aus Walnüssen und Leinöl.')
f('Thunfisch', 'T121902', 'tier', syn='Fisch, Thunfischdose', alts='Kichererbsen (gegart); Walnusskerne')
f('Garnelen', 'T753100', 'tier', syn='Shrimps, Krabben, Scampi', alts='Austernpilze; Champignons')
f('Eier', 'E111100', 'tier', syn='Ei, Hühnerei, Spiegelei, Rührei', alts='Kichererbsen (gegart); Champignons; Avocado')
f('Milch', 'M111300', 'milch', syn='Kuhmilch, Vollmilch, Cappuccino, Latte, Milchkaffee', alts='Mandeldrink ungesüßt')
f('Joghurt', 'M141300', 'milch', syn='Naturjoghurt, Skyr', alts='Kokosmilch (vollfett); Cashewkerne')
f('Quark', 'M713100', 'milch', syn='Magerquark, Topfen', alts='Tahin; Cashewkerne')
f('Käse', 'M402600', 'milch', syn='Gouda, Bergkäse, Emmentaler, Cheddar', alts='Cashewkerne; Grüne Oliven; Tahin')
f('Mozzarella', 'M032100', 'milch', syn='Burrata', alts='Avocado; Cashewkerne')
f('Feta', 'M012200', 'milch', syn='Schafskäse, Hirtenkäse', alts='Grüne Oliven; Kapern; Cashewkerne')
f('Butter', 'Q611000', 'milch', syn='Butterschmalz, Ghee', alts='Olivenöl; Rapsöl')
f('Sahne', 'M173800', 'milch', syn='Schlagsahne, Rahm, Creme fraiche', alts='Kokosmilch (vollfett); Cashewkerne')
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
f('Weinessig', 'R121000', 'wuerze', cap=30, syn='Weißweinessig, Rotweinessig, Branntweinessig, Kräuteressig')
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
f('Margarine', 'Q4A4000', 'fett', light='y', cap=10, syn='vegane Margarine, Pflanzenmargarine, Streichfett', alts='Olivenöl; Rapsöl',
  why='Pflanzlich, aber stark verarbeitet. Longo setzt auf Olivenöl und Nüsse.')

# Nüsse, Saaten, Kokos
f('Pinienkerne', 'H320100', 'nuss', syn='Pinienkern')
f('Hanfsamen', None, 'nuss', syn='Hanfsamen geschält, Hanfherzen', n=(553, 31.6, 48.8, 8.7, 1.5))
f('Mohn', 'H450100', 'nuss', cap=10, syn='Mohnsamen')
f('Cashewmus', 'F960800', 'nuss', cap=30, syn='Cashewkernmus, Cashewbutter')
f('Haselnussmus', 'H130800', 'nuss', cap=30, syn='Haselnussbutter')
f('Kokosraspeln', 'H150400', 'fettfrucht', light='y', cap=15, syn='Kokosflocken, Kokoschips', alts='Walnusskerne; Mandeln',
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
f('Sojajoghurt', 'H844000', 'soja', cap=100, syn='Joghurtalternative, Sojaghurt, veganer Joghurt', alts='Kokosmilch (vollfett); Avocado',
  why='Ungesüßt eine gute Basis für Dressings. Viel davon bringt zu viel Eiweiß.')
f('Sojadrink', 'H841100', 'soja', cap=200, syn='Sojamilch', alts='Mandeldrink ungesüßt; Haferdrink',
  why='Ungesüßt okay, aber eiweißreicher als Mandel- oder Haferdrink.')
f('Tempeh', None, 'eiweiss', syn='Tempe', n=(192, 20.3, 10.8, 7.6, 0))
f('Seitan', 'C558000', 'eiweiss', syn='Weizeneiweiß, Weizengluten')
f('Sojagranulat', 'H765000', 'eiweiss', syn='Sojaschnetzel, Sojahack, Sojafleisch, texturiertes Soja')
f('Veggie-Wurst', 'H930000', 'eiweiss', syn='vegane Wurst, vegetarische Wurst, Wurstalternative, Fleischersatz, Veggie-Aufschnitt')
f('Veggie-Burger', 'H910300', 'eiweiss', syn='vegetarische Bratwurst, Veggie-Bratwurst, Burger-Patty vegan, Veggie-Frikadelle')

# Pflanzendrinks und Getränke
f('Haferdrink', 'C660000', 'getraenk', light='y', cap=200, syn='Hafermilch, Haferdrink ungesüßt', alts='Mandeldrink ungesüßt',
  why='Der Hafer bringt natürlichen Zucker mit. Ein Schuss im Tee passt, Mandeldrink ist zuckerärmer.')
f('Reisdrink', 'C650000', 'getraenk', light='y', cap=100, syn='Reismilch', alts='Mandeldrink ungesüßt',
  why='Schmeckt süß, weil die Stärke beim Herstellen zu Zucker wird. Mandeldrink ist die bessere Wahl.')
f('Kokoswasser', 'H151000', 'getraenk', light='y', cap=200, alts='Wasser; Kräutertee',
  why='Leicht süß. Ein Glas ist okay, Wasser und Kräutertee sind die Basis.')
f('Gemüsesaft', 'G090600', 'getraenk', light='y', cap=200, syn='Tomatensaft, Möhrensaft, Karottensaft, Rote-Bete-Saft', alts='Gemüsebrühe; Kräutertee',
  why='Ein Glas passt, im Saft fehlt aber die Sättigung vom ganzen Gemüse.')
f('Wasser', 'N110000', 'getraenk', cap=3000, syn='Trinkwasser, Leitungswasser')
f('Mineralwasser', 'N128000', 'getraenk', cap=3000, syn='Sprudel, Sprudelwasser, stilles Wasser')
# Schwarzer und grüner Tee: Longos Buch nennt laut Sekundärquellen ungesüßten Tee ohne Einschränkung auf Kräutertee.
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
  why='Eine dünne Scheibe passt an Tag 1. Für Brot sieht Longo sonst kaum Platz vor.')
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
f('Frischkäse', 'M710800', 'milch', syn='Doppelrahmfrischkäse, Philadelphia, Mascarpone', alts='Hummus; Cashewmus')
f('Parmesan', 'M306400', 'milch', syn='Grana Padano, Pecorino, Hartkäse', alts='Hefeflocken; Cashewkerne')
f('Hüttenkäse', 'M711100', 'milch', syn='körniger Frischkäse, Cottage Cheese', alts='Sojajoghurt; Avocado')
f('Kefir', 'M130300', 'milch', syn='Ayran, Dickmilch', alts='Mandeldrink ungesüßt; Sojajoghurt')
f('Buttermilch', 'M150000', 'milch', syn='Molke', alts='Mandeldrink ungesüßt')


# Obergrenze je Lebensmittel und Tag (eigene Regel der Seite, Longo nennt keine Mengen pro Lebensmittel):
# Ein einzelnes Lebensmittel darf höchstens die Hälfte des Zucker- bzw. Eiweißbudgets von Tag 2 bis 5 belegen,
# damit für den Rest des Tages Platz bleibt. Budget Tag 2 bis 5: 725 kcal, davon 9 % Eiweiß (Longo) und
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
    Kohlenhydrate gesamt = verfügbare Kohlenhydrate + Ballaststoffe, wie in den bisherigen Daten und in Longos US-Quellen."""
    import json, os
    b = json.load(open(os.path.join(os.path.dirname(__file__), 'bls_values.json')))
    out = {}
    for x in F:
        if x['bls']:
            e = b[x['bls']]
            out[x['name']] = (e['kcal'], e['protein'], e['fat'], round(e['cho'] + e['fiber'], 2), e['sugar'], e['fiber'])
    return out
