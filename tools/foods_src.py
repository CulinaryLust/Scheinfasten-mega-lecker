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
  'getreide': ('Getreide', 'y', 100), 'obst': ('Obst', 'y', 150), 'soja': ('Soja', 'y', 60),
  'getraenk': ('Getränke', 'g', 1000),
  'tier': ('Fleisch, Fisch und Ei', 'r', 0), 'milch': ('Milchprodukte', 'r', 0), 'suess': ('Zucker und Süßes', 'r', 0),
  'weissmehl': ('Weißmehl und Snacks', 'r', 0), 'drink': ('Kaffee, Alkohol, Softdrinks', 'r', 0),
}

WHY = {
  'y': 'Liefert viel Stärke, Zucker oder Eiweiß. Eine kleine Menge passt, mehr würde Longos Verteilung kippen.',
  'tier': 'Tierisches Eiweiß hält den Wachstumsfaktor IGF-1 hoch. Genau den will das Scheinfasten senken, deshalb ist das Protokoll rein pflanzlich.',
  'milch': 'Milchprodukte liefern tierisches Eiweiß und Milchzucker. Longos Protokoll ist rein pflanzlich.',
  'suess': 'Zucker treibt Blutzucker und Insulin hoch und hebt den Fastenstoffwechsel auf.',
  'weissmehl': 'Viel schnell verfügbare Stärke und wenig Gemüse. Das kostet Kalorienbudget, ohne satt zu machen.',
  'drink': 'Im Protokoll sind Wasser und ungesüßte Kräutertees vorgesehen. Kaffee, Alkohol und Säfte gehören nicht dazu.',
}

ALTS = {
  'tier': ['Champignons', 'Austernpilze', 'Kichererbsen (gegart)', 'Walnusskerne'],
  'milch': ['Kokosmilch (vollfett)', 'Cashewkerne', 'Tahin', 'Mandeldrink ungesüßt'],
  'suess': ['Heidelbeeren', 'Apfel', 'Walnusskerne'],
  'weissmehl': ['Kartoffeln', 'Hirse (gegart)', 'Blumenkohl', 'Zucchini'],
  'drink': ['Kräutertee', 'Zitronensaft', 'Gemüsebrühe'],
}

# name, BLS-Code, Gruppe, Ampel (None = Gruppe), cap (None = Gruppe), Suchbegriffe, Alternativen, Begründung, Stück (Bezeichnung, g)
F = []
def f(name, bls, group, light=None, cap=None, syn='', alts='', why='', piece=None):
    F.append(dict(name=name, bls=bls, group=group, light=light, cap=cap, syn=[s.strip() for s in syn.split(',') if s.strip()],
                  alts=[a.strip() for a in alts.split(';') if a.strip()], why=why, piece=piece))

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
f('Erbsen (TK)', 'G760200', 'huelsen', cap=100, syn='Erbsen, grüne Erbsen', alts='Zuckerschoten; Brokkoli')
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
f('Vollkornbrot', 'B121000', 'getreide', cap=40, syn='Brot, Roggenbrot, Schwarzbrot', alts='Gurke; Kohlrabi',
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
f('Kuchen', 'D422600', 'suess', syn='Rührkuchen, Gebäck, Kekse', alts='Apfel; Walnusskerne')
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
f('Milch', 'M111300', 'milch', syn='Kuhmilch, Vollmilch', alts='Mandeldrink ungesüßt')
f('Joghurt', 'M141300', 'milch', syn='Naturjoghurt, Skyr', alts='Kokosmilch (vollfett); Cashewkerne')
f('Quark', 'M713100', 'milch', syn='Magerquark, Topfen', alts='Tahin; Cashewkerne')
f('Käse', 'M402600', 'milch', syn='Gouda, Bergkäse, Parmesan, Emmentaler', alts='Cashewkerne; Grüne Oliven; Tahin')
f('Mozzarella', 'M032100', 'milch', syn='Burrata', alts='Avocado; Cashewkerne')
f('Feta', 'M012200', 'milch', syn='Schafskäse, Hirtenkäse', alts='Grüne Oliven; Kapern; Cashewkerne')
f('Butter', 'Q611000', 'milch', syn='Margarine', alts='Olivenöl; Rapsöl')
f('Sahne', 'M173800', 'milch', syn='Schlagsahne, Rahm, Creme fraiche', alts='Kokosmilch (vollfett); Cashewkerne')
f('Kaffee', 'N410100', 'drink', syn='Espresso, Cappuccino, Latte')
f('Bier', 'P163000', 'drink', syn='Pils, Alkohol')
f('Wein', 'P2A3000', 'drink', syn='Rotwein, Weißwein, Sekt, Alkohol')
f('Orangensaft', 'F603600', 'drink', syn='Saft, Fruchtsaft, Apfelsaft', alts='Orange; Kräutertee')
f('Cola', 'N330000', 'drink', syn='Limonade, Softdrink, Eistee')
f('Kräutertee', 'N720100', 'getraenk', syn='Tee, Pfefferminztee, Kamillentee, Früchtetee')


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
