# Quelle der Rezeptdaten. Erzeugt src/data/*.json. Nährwerte je 100 g:
# kcal, Eiweiß, Fett, Kohlenhydrate, davon Zucker. Das sind nur noch Rückfallwerte (an USDA angelehnt):
# build_data.py ersetzt sie durch BLS-4.0-Werte, wo foods_src.py einen BLS-Code hat. Ohne BLS bleiben Dill, Minze, Paprikapulver und Currypaste.
N={
'Olivenöl':(884,0,100,0,0),'Sesamöl':(884,0,100,0,0),'Zucchini':(17,1.2,0.3,3.1,2.5),'Tomaten':(18,0.9,0.2,3.9,2.6),
'Kirschtomaten':(18,0.9,0.2,3.9,2.6),'Tomaten, passiert':(30,1.4,0.2,5.5,4),'Karotten':(41,0.9,0.2,9.6,4.7),
'Staudensellerie':(16,0.7,0.2,3,1.3),'Zwiebeln':(40,1.1,0.1,9.3,4.2),'Rote Zwiebel':(40,1.1,0.1,9.3,4.2),'Knoblauch':(149,6.4,0.5,33,1),
'Hokkaido-Kürbis':(34,1,0.1,8,3),'Kokosmilch (vollfett)':(197,2,21,2.8,2),'Kürbiskerne':(559,30,49,11,1.4),
'Blumenkohl':(25,1.9,0.3,5,1.9),'Babyspinat':(23,2.9,0.4,3.6,0.4),'Grünkohl':(49,4.3,0.9,8.8,2.3),
'Grüne Oliven':(145,1,15,3.8,0.5),'Walnusskerne':(654,15,65,14,2.6),'Mandeln':(579,21,50,22,4.4),
'Zitronensaft':(22,0.4,0.2,6.9,2.5),'Limettensaft':(25,0.4,0.1,8.4,1.7),'Basilikum':(23,3.2,0.6,2.7,0.3),
'Kartoffeln':(77,2,0.1,17,0.8),'Gemüsebrühe':(5,0.2,0.1,0.8,0.5),'Weiße Bohnen (gegart)':(139,9.7,0.4,25,0.3),
'Tahin':(595,17,54,21,0.5),'Ingwer':(80,1.8,0.8,18,1.7),'Petersilie':(36,3,0.8,6.3,0.9),'Kapern':(23,2.4,0.9,4.9,0.4),
'Süßkartoffel':(86,1.6,0.1,20,4.2),'Lauch':(61,1.5,0.3,14,3.9),'Champignons':(22,3.1,0.3,3.3,2),
'Rote Bete (vorgegart)':(43,1.6,0.2,9.6,6.8),'Rucola':(25,2.6,0.7,3.7,2),'Gurke':(15,0.7,0.1,3.6,1.7),
'Hirse (gegart)':(119,3.5,1,23.7,0.1),'Paprikapulver, geräuchert':(282,14,13,54,10),'Helle Misopaste':(199,12,6,26,6),
'Blattsalat':(15,1.4,0.2,2.9,0.8),'Orange':(47,0.9,0.1,11.8,9.4),'Fenchel':(31,1.2,0.2,7.3,3.9),'Rote Paprika':(31,1,0.3,6,4.2),
'Pak Choi':(13,1.5,0.2,2.2,1.2),'Rote Currypaste':(100,2,4,14,5),'Brokkoli':(34,2.8,0.4,6.6,1.7),'Rotkohl':(31,1.4,0.2,7.4,3.8),
'Apfel':(52,0.3,0.2,14,10),'Sonnenblumenkerne':(584,21,51,20,2.6),'Kichererbsen (gegart)':(164,8.9,2.6,27,4.8),
'Dill':(43,3.5,1.1,7,0),'Cashewkerne':(553,18,44,30,6),'Aubergine':(25,1,0.2,5.9,3.5),'Rote Linsen (gegart)':(116,9,0.4,20,1.8),
'Erbsen (TK)':(77,5.2,0.4,13.6,4.9),'Sesam':(573,18,50,23,0.3),'Meerrettich':(48,1.2,0.7,11,8),'Feldsalat':(21,2,0.4,3.6,0.4),
'Balsamico':(88,0.5,0,17,15),'Apfelessig':(21,0,0,0.9,0.4),'Leinsamen':(534,18,42,29,1.6),'Avocado':(160,2,15,8.5,0.7),
'Minze':(70,3.8,0.9,15,0),
}
# Rezept: slug, Titel, Kurzname, Kategorie, Slot, Minuten, Bild, Teaser, Zutaten[(Name, Menge, Notiz)], Schritte, Tipp
R=[]
def r(slug,title,short,cat,slot,mins,img,teaser,ing,steps,tip,diet=None):
    R.append(dict(slug=slug,title=title,short=short,category=cat,slot=slot,minutes=mins,image=img,teaser=teaser,
      ingredients=[dict(name=n,amount=a,note=t) for n,a,t in ing],steps=steps,tip=tip,own=False))
r('minestrone','Toskanische Minestrone mit Basilikumöl','Minestrone','Suppe','main',35,'minestrone',
 'Die Basis jeder Fastenwoche: viel Gemüse, wenig Bohnen, ein Löffel grünes Öl obendrauf. Schmeckt am zweiten Tag noch besser.',
 [('Olivenöl',8,'für den Topf'),('Zwiebeln',50,'fein gewürfelt'),('Knoblauch',3,'1 Zehe'),('Karotten',60,'gewürfelt'),('Staudensellerie',50,'in Scheiben'),
  ('Kartoffeln',80,'gewürfelt'),('Zucchini',100,'gewürfelt'),('Tomaten, passiert',150,''),('Gemüsebrühe',300,'salzarm'),
  ('Weiße Bohnen (gegart)',30,'aus der Dose, abgespült'),('Olivenöl',8,'für das Basilikumöl'),('Basilikum',10,'für das Basilikumöl')],
 ['Öl in einem Topf erhitzen. Zwiebel, Karotte und Sellerie 5 Minuten glasig dünsten.','Knoblauch und Kartoffeln zugeben, kurz mitrösten. Brühe und passierte Tomaten angießen.',
  '15 Minuten leise köcheln lassen. Zucchini und Bohnen zugeben, weitere 8 Minuten garen.','Basilikum mit Öl und einer Prise Salz fein pürieren.','Suppe mit Pfeffer, Salz und Oregano abschmecken, Basilikumöl in Klecksen daraufgeben.'],
 'Gleich die vierfache Menge kochen. Ohne Basilikumöl hält die Suppe 3 Tage im Kühlschrank.')
r('kuerbissuppe','Hokkaido-Kokos-Suppe mit Ingwer und gerösteten Kürbiskernen','Kürbissuppe','Suppe','main',30,'kuerbissuppe',
 'Samtig, leicht scharf und richtig sättigend. Die Kokosmilch liefert genau die Fette, die das Konzept vorsieht.',
 [('Hokkaido-Kürbis',175,'mit Schale gewürfelt'),('Karotten',70,'in Scheiben'),('Zwiebeln',40,''),('Ingwer',5,'frisch gerieben'),('Olivenöl',3,''),('Gemüsebrühe',250,''),('Kokosmilch (vollfett)',40,''),('Kürbiskerne',8,'1 EL')],
 ['Zwiebel im Öl 3 Minuten anschwitzen, Ingwer, Kürbis und Karotten kurz mitrösten.','Brühe angießen und zugedeckt 15 Minuten weich kochen.','Kokosmilch einrühren (1 TL zum Garnieren zurückbehalten) und fein pürieren.','Kürbiskerne ohne Fett rösten, bis sie knacken.','Mit Salz, Pfeffer und Limette abschmecken und mit Kernen servieren.'],
 'Eine Messerspitze Kurkuma und Kreuzkümmel machen die Suppe noch runder.')
r('ofen-blumenkohl','Ofen-Blumenkohl und Süßkartoffel mit Tahin-Zitronen-Sauce','Ofen-Blumenkohl','Ofengericht','main',35,'blumenkohl',
 'Röstaromen statt Verzicht. Die Tahin-Sauce macht alles cremig, ganz ohne Milchprodukte.',
 [('Blumenkohl',200,'in Röschen'),('Süßkartoffel',150,'in Spalten'),('Olivenöl',6,''),('Paprikapulver, geräuchert',1,'½ TL'),('Tahin',10,'2 TL'),('Zitronensaft',15,''),('Knoblauch',2,'gerieben'),('Petersilie',5,'gehackt')],
 ['Ofen auf 220 °C Umluft vorheizen.','Gemüse mit Öl, Paprika und Salz mischen und auf ein Blech geben.','25 Minuten rösten, nach der Hälfte wenden, bis die Ränder braun sind.','Tahin mit Zitronensaft, Knoblauch und 2 bis 3 EL warmem Wasser glatt rühren.','Gemüse anrichten, Sauce darüberträufeln, Petersilie darüberstreuen.'],
 'Die Sauce dickt nach. Einfach mit etwas Wasser wieder cremig rühren.')
r('zucchini-pfanne','Mediterrane Zucchini-Tomaten-Pfanne mit Oliven, Kapern und Hirse','Zucchini-Pfanne','Pfanne','main',20,'pfanne',
 'Schmeckt nach Urlaub an der Ligurischen Küste. Oliven und Kapern bringen Würze, die Hirse macht satt.',
 [('Zucchini',200,'in Halbmonden'),('Kirschtomaten',150,'halbiert'),('Rote Zwiebel',40,'in Streifen'),('Knoblauch',3,''),('Olivenöl',8,''),('Grüne Oliven',15,'halbiert'),('Kapern',5,'1 TL'),('Basilikum',3,''),('Hirse (gegart)',120,'ca. 40 g roh')],
 ['Hirse garen oder vom Vortag nehmen.','Zucchini in heißem Öl scharf anbraten, bis sie Farbe nehmen.','Zwiebel und Knoblauch 2 Minuten mitbraten, dann Tomaten, Oliven und Kapern zugeben.','4 Minuten schmoren, bis die Tomaten aufplatzen.','Hirse unterheben, mit Pfeffer, Oregano und Basilikum abschmecken.'],
 'Pfanne nicht überladen, sonst kochen die Zucchini statt zu bräunen.')
r('pilz-miso-bruehe','Pilz-Miso-Brühe mit Lauch, Kartoffel und Spinat','Pilz-Miso-Brühe','Suppe','main',25,'pilz',
 'Umami für den Abend. Miso und gebratene Pilze geben Tiefe wie eine lange gekochte Brühe.',
 [('Champignons',90,'in Scheiben'),('Lauch',60,'in Ringen'),('Karotten',40,'in Stiften'),('Kartoffeln',120,'klein gewürfelt'),('Olivenöl',5,''),('Gemüsebrühe',350,''),('Helle Misopaste',7,'gut 1 TL'),('Babyspinat',30,'')],
 ['Pilze im Öl bei hoher Hitze braun braten.','Lauch und Karotte 2 Minuten mitbraten.','Kartoffeln und Brühe zugeben, 12 Minuten köcheln.','Vom Herd nehmen, Miso in etwas Brühe glatt rühren und einrühren (nicht mehr kochen).','Spinat in die Schale geben und mit der heißen Suppe übergießen.'],
 'Miso ist salzig. Erst danach abschmecken, meist braucht es kein Salz mehr.')
r('gruenkohl-chips','Knusprige Grünkohl-Chips mit geräuchertem Paprika','Grünkohl-Chips','Snack','snack',20,'chips',
 'Der Snack fürs Knabberbedürfnis. Frisch aus dem Ofen und richtig knusprig.',
 [('Grünkohl',60,'ohne Strunk, gezupft'),('Olivenöl',5,'1 TL'),('Paprikapulver, geräuchert',1,'½ TL')],
 ['Ofen auf 140 °C Umluft vorheizen.','Grünkohl waschen und sehr gut trocken schleudern.','Mit Öl, Paprika und Salz einmassieren und mit Abstand auf ein Blech legen.','15 bis 20 Minuten backen, bis die Blätter knistern. Nach 10 Minuten wenden.'],
 'Luftdicht verpackt bleiben die Chips 2 Tage knusprig.')
r('rote-bete-carpaccio','Rote-Bete-Carpaccio mit Walnüssen, Rucola und Zitronen-Hirse','Rote-Bete-Carpaccio','Salat','main',15,'rotebete',
 'Das Finale für Tag 5. Sieht aus wie im Restaurant und steht in einer Viertelstunde auf dem Tisch.',
 [('Rote Bete (vorgegart)',150,'hauchdünn gehobelt'),('Rucola',30,''),('Walnusskerne',8,'grob gehackt'),('Olivenöl',5,''),('Zitronensaft',10,''),('Hirse (gegart)',80,'')],
 ['Rote Bete hauchdünn hobeln und auf einem Teller auslegen.','Öl, Zitronensaft, Salz und Pfeffer verrühren.','Hirse mit der Hälfte des Dressings mischen und in die Mitte setzen.','Rucola daraufgeben, Walnüsse kurz rösten und darüberstreuen.','Restliches Dressing über die Bete träufeln.'],
 'Einweghandschuhe tragen, Rote Bete färbt stark.')
r('nussmix','Nussmix aus Walnüssen und Mandeln','Nussmix','Snack','snack',2,'nuesse',
 'Das Frühstück der Fastentage: eine kleine Handvoll gute Fette, dazu ein großer Becher Kräutertee.',
 [('Walnusskerne',10,''),('Mandeln',10,'')],['Nüsse abwiegen und in kleine Dosen füllen, am besten gleich für alle fünf Tage.','Langsam essen und dazu einen großen Becher Kräutertee trinken.'],
 'Kurz in der Pfanne geröstet schmecken die Nüsse intensiver.')
r('oliven','Würzige Oliven mit Zitronenabrieb','Oliven','Snack','snack',2,'oliven',
 'Salzig, fettreich und sättigend. Genau der richtige Snack für den Nachmittag.',
 [('Grüne Oliven',30,'ca. 8 Stück')],['Oliven abtropfen lassen.','Mit etwas Zitronenabrieb, Chiliflocken und Thymian mischen.'],'Wer Hunger hat, isst die Oliven langsam und trinkt ein Glas Wasser dazu.')
r('beilagensalat','Beilagensalat mit Gurke und Zitronen-Öl-Dressing','Beilagensalat','Salat','side',5,'salat',
 'Frisch, knackig und in fünf Minuten fertig.',
 [('Blattsalat',80,''),('Gurke',80,'in Scheiben'),('Olivenöl',8,''),('Zitronensaft',10,'')],['Salat waschen und trocken schleudern.','Gurke in Scheiben schneiden.','Öl, Zitronensaft, Salz und Pfeffer verrühren und unterheben.'],'Frische Kräuter wie Dill oder Schnittlauch machen ihn besonders.')
# 25 neue Rezeptideen
r('fenchel-orangen-suppe','Fenchel-Orangen-Suppe mit Safran','Fenchelsuppe','Suppe','main',30,'suppe-hell',
 'Fein, leicht süßlich und mit einem Hauch Safran. Ein Gericht wie im Süden Italiens.',
 [('Fenchel',250,'in Streifen, Grün aufheben'),('Zwiebeln',30,''),('Kartoffeln',70,'gewürfelt'),('Olivenöl',9,''),('Gemüsebrühe',300,''),('Orange',50,'Filets und Saft')],
 ['Zwiebel und Fenchel im Öl 5 Minuten dünsten.','Kartoffel, Brühe und eine Prise Safran zugeben, 18 Minuten köcheln.','Orangensaft zugeben und fein pürieren.','Mit Orangenfilets und Fenchelgrün servieren.'],'Statt Safran passt auch eine Prise Kurkuma.')
r('gazpacho','Tomaten-Paprika-Gazpacho mit Gurke','Gazpacho','Suppe','main',15,'gazpacho',
 'Kalte Suppe für warme Tage. Kein Herd, nur ein Mixer.',
 [('Tomaten',250,'reif'),('Rote Paprika',100,''),('Gurke',100,''),('Rote Zwiebel',20,''),('Knoblauch',2,''),('Olivenöl',12,''),('Apfelessig',10,''),('Kartoffeln',60,'gekocht, für die Bindung')],
 ['Gemüse grob schneiden.','Alles mit Öl, Essig, Salz und 100 ml kaltem Wasser fein pürieren.','Mindestens 1 Stunde kalt stellen.','Mit Gurkenwürfeln und einem Tropfen Öl servieren.'],'Je reifer die Tomaten, desto besser die Suppe.')
r('thai-curry-bruehe','Thai-Curry-Brühe mit Pak Choi und Kokos','Thai-Curry-Brühe','Suppe','main',25,'curry',
 'Aromatisch, wärmend und leicht scharf. Mit Limette und Koriander ein kleiner Urlaub.',
 [('Pak Choi',150,'geviertelt'),('Champignons',80,'in Scheiben'),('Süßkartoffel',100,'klein gewürfelt'),('Kokosmilch (vollfett)',40,''),('Rote Currypaste',10,'1 TL'),('Gemüsebrühe',350,''),('Limettensaft',10,''),('Ingwer',5,'')],
 ['Currypaste und Ingwer in einem Topf kurz anrösten.','Brühe, Kokosmilch und Süßkartoffel zugeben, 10 Minuten köcheln.','Pilze und Pak Choi zugeben, 4 Minuten garen.','Mit Limettensaft und Koriander abschmecken.'],'Currypaste ohne Fischsauce kaufen, dann bleibt das Gericht pflanzlich.')
r('brokkoli-lauch-suppe','Brokkoli-Lauch-Cremesuppe mit Mandelsplittern','Brokkolisuppe','Suppe','main',25,'suppe-gruen',
 'Grün, cremig und ohne Sahne. Die gerösteten Mandeln geben Biss.',
 [('Brokkoli',200,'in Röschen'),('Lauch',80,'in Ringen'),('Kartoffeln',80,'gewürfelt'),('Olivenöl',8,''),('Gemüsebrühe',350,''),('Mandeln',8,'gehobelt')],
 ['Lauch im Öl 3 Minuten dünsten.','Kartoffel und Brühe zugeben, 10 Minuten köcheln.','Brokkoli zugeben, 6 Minuten garen und fein pürieren.','Mit Muskat, Salz und Pfeffer abschmecken, Mandeln rösten und darüberstreuen.'],'Ein paar Brokkoliröschen vor dem Pürieren herausnehmen und als Einlage verwenden.')
r('zucchini-nudeln-pesto','Zucchini-Nudeln mit Walnuss-Basilikum-Pesto','Zucchini-Nudeln','Pfanne','main',15,'zoodles',
 'Pasta-Gefühl ohne Pasta. Das Pesto ist in drei Minuten gemixt.',
 [('Zucchini',300,'spiralisiert'),('Kirschtomaten',100,'halbiert'),('Basilikum',15,''),('Walnusskerne',12,''),('Olivenöl',8,''),('Zitronensaft',10,''),('Knoblauch',2,''),('Kartoffeln',80,'gekocht, gewürfelt')],
 ['Basilikum, Walnüsse, Öl, Zitronensaft, Knoblauch und Salz zu Pesto mixen.','Zucchini-Nudeln 1 Minute in einer heißen Pfanne schwenken.','Pesto, Tomaten und Kartoffelwürfel unterheben.','Sofort servieren.'],'Zucchini-Nudeln nicht salzen, bevor sie in die Pfanne kommen, sonst ziehen sie Wasser.')
r('rotkohl-apfel-salat','Rotkohl-Apfel-Salat mit gerösteten Sonnenblumenkernen','Rotkohlsalat','Salat','main',15,'salat-bunt',
 'Knackig, süß-sauer und voller Farbe. Wird mit jeder Stunde im Kühlschrank besser.',
 [('Rotkohl',200,'fein gehobelt'),('Apfel',60,'in Stiften'),('Sonnenblumenkerne',10,''),('Olivenöl',8,''),('Apfelessig',15,''),('Kartoffeln',80,'gekocht, lauwarm')],
 ['Rotkohl mit Salz kräftig durchkneten, bis er weich wird.','Essig, Öl und Pfeffer zugeben, Apfel unterheben.','Sonnenblumenkerne ohne Fett rösten.','Mit lauwarmen Kartoffelwürfeln anrichten und mit Kernen bestreuen.'],'Am Vorabend zubereitet schmeckt der Salat noch runder.')
r('ofen-tomaten-kraeuterkruste','Ofen-Tomaten mit Leinsamen-Kräuterkruste und Hirse','Ofen-Tomaten','Ofengericht','main',30,'ofengemuese',
 'Saftige Tomaten unter einer knusprigen Kruste. Schmeckt nach Sommer, auch im Winter.',
 [('Tomaten',300,'halbiert'),('Leinsamen',8,'geschrotet'),('Petersilie',10,''),('Knoblauch',3,''),('Olivenöl',8,''),('Hirse (gegart)',80,'ca. 25 g roh')],
 ['Ofen auf 200 °C vorheizen.','Leinsamen, Petersilie, Knoblauch, Öl und Salz mischen.','Tomaten mit der Schnittfläche nach oben in eine Form setzen und die Kruste daraufgeben.','20 Minuten backen und mit Hirse servieren.'],'Ein paar Thymianzweige in der Form geben zusätzliches Aroma.')
r('leinsamen-cracker','Leinsamen-Kräuter-Cracker','Leinsamen-Cracker','Snack','snack',60,'cracker',
 'Knuspriger Ersatz für Brot. Einmal backen, für die ganze Woche.',
 [('Leinsamen',15,'ganz'),('Sonnenblumenkerne',5,''),('Rote Paprika',30,'fein gewürfelt, als Beilage')],
 ['Für 5 Portionen 75 g Leinsamen und 25 g Sonnenblumenkerne mit 120 ml Wasser, Salz und Kräutern 20 Minuten quellen lassen.','Dünn auf Backpapier streichen und bei 150 °C 45 Minuten backen.','Abkühlen lassen und in Stücke brechen.','Pro Portion mit Paprikastreifen servieren.'],'Die Masse so dünn wie möglich streichen, dann werden die Cracker richtig knusprig.')
r('tapenade-gemuesesticks','Oliven-Tapenade mit Gemüsesticks','Tapenade','Snack','snack',10,'gemuesesticks',
 'Würziger Dip, knackiges Gemüse. Perfekt für den Nachmittag.',
 [('Grüne Oliven',25,'entsteint'),('Kapern',3,''),('Olivenöl',3,''),('Karotten',60,'in Sticks'),('Gurke',60,'in Sticks'),('Rote Paprika',50,'in Streifen')],
 ['Oliven, Kapern, Öl, etwas Zitronenabrieb und Pfeffer grob pürieren.','Gemüse in Sticks schneiden.','Zusammen servieren.'],'Die Tapenade hält im Glas 4 Tage im Kühlschrank.')
r('ofen-kichererbsen','Gewürzte Ofen-Kichererbsen','Ofen-Kichererbsen','Snack','snack',30,'kichererbsen',
 'Knusprig wie Chips, aber aus Hülsenfrüchten. Kleine Portion, großer Genuss.',
 [('Kichererbsen (gegart)',40,'gut abgetrocknet'),('Olivenöl',3,''),('Paprikapulver, geräuchert',1,'')],
 ['Ofen auf 200 °C vorheizen.','Kichererbsen trocken tupfen und mit Öl, Paprika und Salz mischen.','25 Minuten rösten, zwischendurch schütteln.'],'Kichererbsen vor dem Rösten gut trocknen, sonst werden sie nicht knusprig.')
r('avocado-gurken-kaltschale','Avocado-Gurken-Kaltschale mit Dill','Avocado-Kaltschale','Suppe','main',10,'kaltschale',
 'Cremig, frisch und blitzschnell. Ideal für Tag 1, wenn es etwas mehr sein darf.',
 [('Avocado',80,'½ Frucht'),('Gurke',250,''),('Zitronensaft',15,''),('Dill',5,''),('Olivenöl',5,''),('Knoblauch',1,'')],
 ['Alles mit 100 ml kaltem Wasser und Salz fein pürieren.','Abschmecken und 30 Minuten kalt stellen.','Mit Gurkenwürfeln und Dill servieren.'],'Ein Eiswürfel im Mixer macht die Suppe sofort kalt.')
r('hummus-bowl','Hummus-Bowl mit Ofengemüse und Rucola','Hummus-Bowl','Bowl','main',30,'bowl',
 'Für Tag 1: eine richtige Mahlzeit mit cremigem Hummus und geröstetem Gemüse.',
 [('Kichererbsen (gegart)',60,'für den Hummus'),('Tahin',10,''),('Zitronensaft',15,''),('Zucchini',120,'in Stücken'),('Rote Paprika',120,'in Stücken'),('Rote Zwiebel',40,'in Spalten'),('Olivenöl',10,''),('Rucola',20,'')],
 ['Gemüse mit Öl und Salz bei 220 °C 20 Minuten rösten.','Kichererbsen mit Tahin, Zitronensaft, Salz und 2 EL Wasser cremig pürieren.','Hummus in eine Schale streichen, Ofengemüse und Rucola daraufgeben.'],'Etwas Kreuzkümmel im Hummus macht ihn orientalischer.')
r('gemuese-lasagne','Gemüse-Lasagne ohne Nudeln mit Cashew-Creme','Gemüse-Lasagne','Ofengericht','main',50,'lasagne',
 'Schichten aus Zucchini, Tomate und Pilzen mit einer cremigen Cashew-Decke. Wohlfühlessen für Tag 1.',
 [('Zucchini',250,'in Längsscheiben'),('Tomaten, passiert',200,''),('Champignons',80,'gehackt'),('Zwiebeln',40,''),('Olivenöl',8,''),('Cashewkerne',20,'eingeweicht'),('Zitronensaft',5,'')],
 ['Zwiebel und Pilze im Öl braten, Tomaten zugeben und 10 Minuten zu einer Sauce köcheln.','Cashews mit Zitronensaft, Salz und 60 ml Wasser cremig mixen.','Zucchini und Sauce abwechselnd in eine kleine Form schichten, mit Cashew-Creme abschließen.','Bei 190 °C 30 Minuten backen.'],'Zucchinischeiben vorher salzen und abtupfen, dann wird die Lasagne nicht wässrig.')
r('ofen-ratatouille','Ratatouille aus dem Ofen','Ratatouille','Ofengericht','main',45,'ratatouille',
 'Der Klassiker aus der Provence, langsam geschmort. Duftet nach Kräutern und Sommer.',
 [('Aubergine',150,'gewürfelt'),('Zucchini',120,'gewürfelt'),('Rote Paprika',100,'gewürfelt'),('Tomaten',150,'gewürfelt'),('Zwiebeln',40,''),('Knoblauch',3,''),('Olivenöl',10,''),('Kartoffeln',80,'gewürfelt')],
 ['Ofen auf 200 °C vorheizen.','Alles mit Öl, Kräutern der Provence und Salz mischen.','In einer Form 35 Minuten schmoren, einmal umrühren.'],'Am nächsten Tag aufgewärmt schmeckt Ratatouille noch besser.')
r('spinat-dal','Spinat-Kokos-Dal mit Tomaten','Spinat-Dal','Pfanne','main',25,'dal',
 'Ein kleines, würziges Dal. Linsen in kleiner Menge, damit das Eiweiß im Rahmen bleibt.',
 [('Rote Linsen (gegart)',50,'ca. 20 g roh'),('Babyspinat',100,''),('Kokosmilch (vollfett)',30,''),('Tomaten',100,'gewürfelt'),('Zwiebeln',40,''),('Ingwer',5,''),('Olivenöl',5,''),('Süßkartoffel',80,'klein gewürfelt')],
 ['Zwiebel und Ingwer im Öl anschwitzen, Currypulver und Kreuzkümmel kurz mitrösten.','Süßkartoffel, Tomaten und 150 ml Wasser zugeben, 10 Minuten köcheln.','Linsen und Kokosmilch zugeben, 5 Minuten weiterkochen.','Spinat unterheben, bis er zusammenfällt.'],'Mit Limettensaft und Koriander abschmecken.')
r('blumenkohl-reis-bowl','Kurkuma-Blumenkohl-Reis mit Cashews','Blumenkohl-Reis','Pfanne','main',20,'blumenkohlreis',
 'Goldgelb, würzig und leicht. Der Blumenkohl übernimmt die Rolle von Reis.',
 [('Blumenkohl',250,'fein gerieben'),('Karotten',60,'gerieben'),('Zwiebeln',30,''),('Olivenöl',8,''),('Cashewkerne',8,'grob gehackt'),('Petersilie',5,''),('Kartoffeln',80,'gekocht, gewürfelt')],
 ['Zwiebel im Öl anschwitzen, 1 TL Kurkuma kurz mitrösten.','Blumenkohl, Karotte und Kartoffel zugeben und 6 Minuten unter Rühren braten.','Mit Salz, Pfeffer und Zitrone abschmecken.','Mit gerösteten Cashews und Petersilie servieren.'],'Blumenkohl in der Küchenmaschine reiben spart viel Zeit.')
r('gefuellte-paprika','Gefüllte Paprika mit Kräuter-Hirse','Gefüllte Paprika','Ofengericht','main',40,'paprika',
 'Bunte Paprika, gefüllt mit Hirse, Tomate und Kräutern. Sieht toll aus und macht satt.',
 [('Rote Paprika',200,'1 große Schote, halbiert'),('Hirse (gegart)',100,''),('Tomaten',100,'gewürfelt'),('Zwiebeln',30,''),('Olivenöl',8,''),('Petersilie',10,'')],
 ['Ofen auf 200 °C vorheizen.','Zwiebel im Öl anschwitzen, Tomaten, Hirse und Petersilie unterheben und würzen.','Paprikahälften füllen und in eine Form setzen.','25 Minuten backen.'],'Ein Schuss Gemüsebrühe in der Form verhindert, dass die Paprika anbrennt.')
r('suesskartoffel-avocado-dip','Süßkartoffel-Spalten mit Avocado-Limetten-Dip','Süßkartoffel-Spalten','Ofengericht','main',35,'suesskartoffel',
 'Außen knusprig, innen weich, dazu ein cremiger Dip. Fingerfood für Fastentage.',
 [('Süßkartoffel',150,'in Spalten'),('Olivenöl',6,''),('Avocado',50,''),('Limettensaft',10,''),('Paprikapulver, geräuchert',1,''),('Blattsalat',50,'')],
 ['Ofen auf 220 °C vorheizen.','Süßkartoffel mit Öl, Paprika und Salz mischen, 25 Minuten rösten.','Avocado mit Limette und Salz zerdrücken.','Mit Salat und Dip servieren.'],'Spalten mit Abstand legen, dann werden sie knuspriger.')
r('gurkensalat-sesam','Asiatischer Gurkensalat mit Sesam','Gurkensalat','Salat','snack',10,'gurke',
 'Knackig, erfrischend, leicht scharf. Passt als Snack oder zu jeder Suppe.',
 [('Gurke',250,'gestückelt'),('Sesam',5,'geröstet'),('Sesamöl',4,''),('Apfelessig',10,'oder Reisessig'),('Knoblauch',1,'')],
 ['Gurke mit dem Messerrücken anschlagen und in Stücke brechen.','Mit Salz 10 Minuten ziehen lassen, Wasser abgießen.','Mit Essig, Sesamöl, Knoblauch und Chili mischen.','Mit Sesam bestreuen.'],'Ein paar Chiliflocken machen den Salat richtig spannend.')
r('erbsen-minz-suppe','Erbsen-Minz-Suppe','Erbsensuppe','Suppe','main',20,'suppe-gruen2',
 'Leuchtend grün und frisch. Die Minze macht den Unterschied.',
 [('Erbsen (TK)',120,''),('Zwiebeln',40,''),('Kartoffeln',60,'gewürfelt'),('Gemüsebrühe',300,''),('Olivenöl',8,''),('Minze',5,'')],
 ['Zwiebel im Öl anschwitzen, Kartoffel und Brühe zugeben, 10 Minuten köcheln.','Erbsen zugeben, 4 Minuten garen.','Mit Minze fein pürieren und abschmecken.'],'Nicht zu lange kochen, damit die Farbe leuchtend bleibt.')
r('karotten-ingwer-suppe','Karotten-Ingwer-Suppe mit Kokos','Karottensuppe','Suppe','main',25,'karottensuppe',
 'Süß, scharf und cremig. Eine Suppe, die durch den Winter trägt.',
 [('Karotten',200,'in Scheiben'),('Ingwer',8,''),('Zwiebeln',40,''),('Kokosmilch (vollfett)',40,''),('Gemüsebrühe',300,''),('Olivenöl',3,'')],
 ['Zwiebel und Ingwer im Öl anschwitzen.','Karotten und Brühe zugeben, 18 Minuten weich kochen.','Kokosmilch zugeben und fein pürieren.','Mit Salz, Pfeffer und Limette abschmecken.'],'Mit einem Klecks Kokosmilch und Chiliöl servieren.')
r('champignon-pfanne-cashew','Champignon-Pfanne mit Cashew-Rahm und Kartoffeln','Champignon-Pfanne','Pfanne','main',25,'pilzpfanne',
 'Rahmig wie bei Oma, nur ohne Sahne. Die Cashews machen die Sauce cremig.',
 [('Champignons',200,'in Scheiben'),('Kartoffeln',150,'gekocht, in Scheiben'),('Cashewkerne',12,'eingeweicht'),('Zwiebeln',40,''),('Olivenöl',6,''),('Petersilie',5,'')],
 ['Cashews mit 80 ml Wasser und Salz cremig mixen.','Pilze in heißem Öl braun braten, Zwiebel zugeben.','Kartoffeln zugeben und kurz mitbraten.','Cashew-Rahm angießen, 2 Minuten köcheln, mit Petersilie servieren.'],'Pilze erst salzen, wenn sie gebräunt sind.')
r('rote-bete-suppe','Rote-Bete-Suppe mit Meerrettich und Walnüssen','Rote-Bete-Suppe','Suppe','main',25,'rote-bete-suppe',
 'Tiefrot, erdig und mit einem frischen Kick vom Meerrettich.',
 [('Rote Bete (vorgegart)',180,'gewürfelt'),('Kartoffeln',80,''),('Zwiebeln',40,''),('Olivenöl',6,''),('Gemüsebrühe',300,''),('Meerrettich',5,'frisch gerieben'),('Walnusskerne',5,'')],
 ['Zwiebel im Öl anschwitzen, Kartoffel und Brühe zugeben, 12 Minuten köcheln.','Rote Bete zugeben und fein pürieren.','Mit Meerrettich, Salz und einem Spritzer Zitrone abschmecken.','Mit gehackten Walnüssen servieren.'],'Ein paar Dillspitzen passen wunderbar dazu.')
r('aubergine-salsa','Gegrillte Aubergine mit Tomaten-Kräuter-Salsa','Aubergine mit Salsa','Pfanne','main',25,'aubergine',
 'Rauchige Auberginenscheiben, darauf eine frische Salsa. Mediterran und leicht.',
 [('Aubergine',250,'in Scheiben'),('Olivenöl',10,''),('Tomaten',120,'fein gewürfelt'),('Rote Zwiebel',20,'fein gewürfelt'),('Petersilie',10,''),('Zitronensaft',10,''),('Kartoffeln',80,'gekocht')],
 ['Auberginenscheiben dünn mit Öl bestreichen und in einer Grillpfanne von beiden Seiten 4 Minuten braten.','Tomaten, Zwiebel, Petersilie, Zitronensaft und Salz mischen.','Salsa auf die Aubergine geben und mit Kartoffeln servieren.'],'Aubergine nicht ertränken: wenig Öl mit dem Pinsel reicht.')
r('feldsalat-ofenkuerbis','Feldsalat mit Ofen-Kürbis und Kürbiskernen','Kürbis-Feldsalat','Salat','main',30,'kuerbissalat',
 'Herbst auf dem Teller: süßer Ofenkürbis, nussiger Feldsalat, ein Hauch Balsamico.',
 [('Hokkaido-Kürbis',175,'in Spalten'),('Karotten',60,'in Stiften'),('Feldsalat',50,''),('Kürbiskerne',8,''),('Olivenöl',8,''),('Balsamico',10,''),('Rote Zwiebel',20,'in Ringen')],
 ['Kürbis und Karotten mit der Hälfte des Öls und Salz bei 210 °C 25 Minuten rösten.','Restliches Öl mit Balsamico und Pfeffer verrühren.','Feldsalat mit Dressing mischen, Kürbis, Karotten und Zwiebel daraufgeben.','Kürbiskerne rösten und darüberstreuen.'],'Der Kürbis kann lauwarm oder kalt auf den Salat.')
r('pak-choi-sesam','Gebratener Pak Choi mit Ingwer und Sesam','Pak Choi','Pfanne','main',15,'pakchoi',
 'In zehn Minuten fertig, knackig und voller Aroma.',
 [('Pak Choi',250,'halbiert'),('Ingwer',5,''),('Knoblauch',2,''),('Sesamöl',6,''),('Sesam',5,''),('Süßkartoffel',120,'gedämpft'),('Limettensaft',10,'')],
 ['Süßkartoffel in Würfeln 12 Minuten dämpfen.','Pak Choi mit der Schnittfläche nach unten im Sesamöl 3 Minuten braten.','Ingwer und Knoblauch zugeben, mit 2 EL Wasser ablöschen und 2 Minuten dünsten.','Mit Limette, Sesam und Süßkartoffel servieren.'],'Statt Salz einen Spritzer Sojasauce, aber sparsam.')
r('pilz-lauch-kartoffel-suppe','Kartoffel-Lauch-Suppe mit gebratenen Pilzen','Kartoffel-Lauch-Suppe','Suppe','main',30,'suppe-hell2',
 'Hausmannskost in leicht: cremig gemixt, obendrauf knusprige Pilze.',
 [('Kartoffeln',150,'gewürfelt'),('Lauch',120,'in Ringen'),('Gemüsebrühe',350,''),('Olivenöl',8,''),('Champignons',60,'in Scheiben'),('Petersilie',5,'')],
 ['Lauch in der Hälfte des Öls dünsten, Kartoffel und Brühe zugeben, 15 Minuten köcheln.','Fein pürieren und mit Muskat abschmecken.','Pilze im restlichen Öl knusprig braten.','Suppe mit Pilzen und Petersilie servieren.'],'Ein paar Lauchringe für die Garnitur aufheben.')
# Zweite Welle (04.11.2026): 16 Rezepte für Lücken bei Saison, Küchen und kalten Gerichten, dazu 4 Frühstücke.
N.update({'Spargel':(28.0,2.0,0.2,5.4,3.8),'Bärlauch':(26.0,1.9,0.2,5.1,2.9),'Kohlrabi':(28.0,1.9,0.2,5.4,3.7),'Radieschen':(18.0,1.1,0.1,3.8,2.1),
 'Schnittlauch':(29.0,2.6,0.7,4.1,1.5),'Kresse':(31.0,4.2,0.7,3.8,0.2),'Wirsing':(37.0,2.8,0.3,6.9,3.5),'Rosenkohl':(40.0,4.5,0.3,6.7,1.6),
 'Pastinaken':(59.0,2.7,0.4,11.8,3.1),'Granatapfel':(79.0,0.7,0.6,18.3,16.1),'Tomatenmark':(81.0,3.4,0.2,17.9,12.9),'Kreuzkümmel':(375,17.8,22.3,44.2,2.3),
 'Chili':(40.0,1.9,0.4,7.7,6.2),'Weinessig':(25.0,0,0,0,0),'Koriander':(23,2.1,0.5,3.7,0.9),'Tomaten (Dose)':(24.0,1.2,0.3,4.2,3.2),
 'Zimt':(247,4.0,1.2,80.6,2.2),'Kurkuma':(312,9.7,3.3,67.1,3.2),'Oregano (getrocknet)':(265,9.0,4.3,68.9,4.1),'Frühlingszwiebeln':(27.0,1.9,0.2,5.6,2.8),
 'Vollkornreis (gegart)':(128.0,3.0,0.9,27.7,0.3),'Senf':(111.0,5.5,7.0,7.4,2.8),'Mandelmus':(559.0,25.3,46.6,14.8,4.4),'Kokosraspeln':(676.0,7.4,65.2,22.6,7.1),
 'Apfelmus ungesüßt':(63.0,0.4,0.3,15.2,11.1),'Chiasamen':(479.0,22.1,32.8,43.9,0.5),'Mandeldrink ungesüßt':(24.0,0.9,2.2,0.3,0.2),'Heidelbeeren':(61.0,0.5,0.6,14.6,9.7)})
r('mandel-kokos-riegel','Mandel-Kokos-Riegel mit Leinsamen und Zimt','Mandel-Riegel','Snack','snack',15,'riegel',
 'Dein eigener Fastenriegel: nussig, leicht nach Zimt und ganz ohne Zucker. Einmal machen, fünf Tage genießen.',
 [('Mandelmus',10,'1 gehäufter TL'),('Mandeln',8,'grob gehackt'),('Kokosraspeln',6,''),('Leinsamen',5,'geschrotet'),('Apfelmus ungesüßt',10,'1 EL'),('Zimt',0.5,'1 Prise')],
 ['Alle Zutaten für fünf Riegel abwiegen (also jede Menge mal fünf) und in einer Schüssel gut verkneten.','Die Masse in eine mit Backpapier ausgelegte kleine Form drücken, etwa 1 cm hoch.','Mindestens 2 Stunden kalt stellen, dann in fünf gleich große Riegel schneiden.','Einzeln in Papier wickeln und im Kühlschrank lagern.'],
 'Mandeln vorher 5 Minuten ohne Fett rösten. Das macht den Riegel deutlich aromatischer.')
r('spargel-baerlauch-kartoffeln','Grüner Spargel mit Bärlauch-Kartoffeln und Zitrone','Spargel mit Bärlauch','Pfanne','main',25,'spargel',
 'Der Frühling auf einem Teller: knackiger grüner Spargel, dazu Kartoffeln in leuchtend grünem Bärlauchöl.',
 [('Spargel',250,'grün, unteres Drittel geschält'),('Kartoffeln',150,'klein, mit Schale'),('Bärlauch',15,'fein gehackt'),('Olivenöl',12,'aufgeteilt'),('Zitronensaft',5,'')],
 ['Kartoffeln in Salzwasser 15 bis 18 Minuten garen, abgießen und halbieren.','Bärlauch mit 8 g Öl und einer Prise Salz fein pürieren.','Spargel in einer Pfanne im restlichen Öl 5 bis 6 Minuten braten, bis er Farbe hat und noch Biss.','Kartoffeln mit dem Bärlauchöl mischen.','Spargel mit Zitronensaft beträufeln, salzen, pfeffern und mit den Kartoffeln anrichten.'],
 'Außerhalb der Bärlauchsaison nimmst Du Basilikum und eine halbe Knoblauchzehe.')
r('kohlrabi-carpaccio','Kohlrabi-Radieschen-Carpaccio mit Kräuteröl und lauwarmen Kartoffeln','Kohlrabi-Carpaccio','Salat','main',20,'kohlrabi',
 'Hauchdünn, knackig und frisch. Das Kräuteröl und ein paar Walnüsse machen daraus ein richtiges Essen.',
 [('Kohlrabi',150,'hauchdünn gehobelt'),('Radieschen',60,'in Scheiben'),('Kartoffeln',100,'gekocht, lauwarm'),('Olivenöl',10,''),('Zitronensaft',10,''),('Schnittlauch',5,'fein geschnitten'),('Kresse',5,''),('Walnusskerne',5,'gehackt')],
 ['Kartoffeln garen und lauwarm in Scheiben schneiden.','Kohlrabi und Radieschen hauchdünn hobeln und fächerartig auf einen Teller legen.','Öl, Zitronensaft, Schnittlauch, Salz und Pfeffer verrühren.','Kartoffeln dazulegen, alles mit dem Kräuteröl beträufeln.','Mit Kresse und gerösteten Walnüssen bestreuen.'],
 'Den Kohlrabi 10 Minuten vorher salzen. Er wird dann zart, bleibt aber knackig.')
r('baerlauch-kartoffel-suppe','Bärlauch-Kartoffel-Suppe mit Kokos','Bärlauchsuppe','Suppe','main',25,'baerlauchsuppe',
 'Samtig, knallgrün und mit dem typischen Knoblaucharoma. Die Frühlingssuppe schlechthin.',
 [('Kartoffeln',150,'gewürfelt'),('Zwiebeln',40,''),('Bärlauch',30,'grob gehackt'),('Gemüsebrühe',350,''),('Olivenöl',8,''),('Kokosmilch (vollfett)',30,'')],
 ['Zwiebel im Öl glasig dünsten.','Kartoffeln und Brühe zugeben, 15 Minuten weich kochen.','Kokosmilch und Bärlauch zugeben und sofort fein pürieren.','Mit Salz, Pfeffer und Muskat abschmecken.'],
 'Bärlauch erst ganz zum Schluss zugeben. Kocht er mit, wird die Suppe grau und bitter.')
r('wirsing-eintopf','Wirsing-Kartoffel-Eintopf mit Kümmel','Wirsing-Eintopf','Eintopf','main',35,'wirsing',
 'Deftig wie bei Oma, nur leichter. Kümmel und Majoran geben dem Eintopf seinen Charakter.',
 [('Wirsing',150,'in Streifen'),('Kartoffeln',130,'gewürfelt'),('Karotten',40,'in Scheiben'),('Zwiebeln',30,''),('Olivenöl',12,''),('Gemüsebrühe',350,'')],
 ['Zwiebel im Öl andünsten, ½ TL Kümmel kurz mitrösten.','Kartoffeln, Karotten und Brühe zugeben, 10 Minuten köcheln.','Wirsing zugeben und weitere 10 Minuten garen.','Mit Majoran, Salz und Pfeffer abschmecken.'],
 'Am nächsten Tag schmeckt der Eintopf noch besser. Gleich doppelt kochen.')
r('ofen-rosenkohl','Ofen-Rosenkohl mit Süßkartoffel, Walnüssen und Balsamico','Ofen-Rosenkohl','Ofengericht','main',35,'rosenkohl',
 'Wer Rosenkohl nicht mag, hat ihn noch nicht aus dem Ofen gegessen. Karamellisiert, nussig, leicht süßsauer.',
 [('Rosenkohl',180,'halbiert'),('Süßkartoffel',100,'gewürfelt'),('Rote Zwiebel',20,'in Spalten'),('Olivenöl',10,''),('Walnusskerne',6,''),('Balsamico',8,'')],
 ['Ofen auf 220 °C Umluft vorheizen.','Rosenkohl, Süßkartoffel und Zwiebel mit Öl und Salz mischen, Rosenkohl mit der Schnittfläche nach unten aufs Blech legen.','25 Minuten rösten, bis die Schnittflächen dunkelbraun sind.','Walnüsse die letzten 4 Minuten mitrösten.','Mit Balsamico beträufeln und pfeffern.'],
 'Die Schnittfläche nach unten ist der ganze Trick. Nur so wird der Rosenkohl süß statt bitter.')
r('pastinaken-suppe','Pastinaken-Suppe mit gerösteten Walnüssen','Pastinakensuppe','Suppe','main',30,'pastinakensuppe',
 'Cremig, leicht süßlich und nussig. Ein Wintergemüse, das viel zu selten auf den Tisch kommt.',
 [('Pastinaken',150,'gewürfelt'),('Kartoffeln',60,'gewürfelt'),('Zwiebeln',30,''),('Olivenöl',8,''),('Gemüsebrühe',300,''),('Walnusskerne',6,'grob gehackt')],
 ['Zwiebel im Öl glasig dünsten.','Pastinaken und Kartoffeln kurz mitbraten, Brühe angießen.','20 Minuten köcheln und fein pürieren.','Mit Muskat, Salz und einem Spritzer Zitrone abschmecken.','Walnüsse ohne Fett rösten und darüberstreuen.'],
 'Eine Prise Currypulver passt hervorragend zur Süße der Pastinake.')
r('baba-ganoush-teller','Baba Ganoush mit Ofenkartoffeln, Gurke und Granatapfel','Baba Ganoush','Kalte Küche','main',45,'baba-ganoush',
 'Rauchige Auberginencreme mit Tahin, wie im Libanon. Mit Kartoffelspalten und Gurke zum Dippen.',
 [('Aubergine',250,'ganz'),('Tahin',10,'2 TL'),('Olivenöl',8,''),('Zitronensaft',10,''),('Knoblauch',2,''),('Kartoffeln',80,'in Spalten'),('Gurke',60,'in Sticks'),('Petersilie',5,''),('Granatapfel',10,'Kerne')],
 ['Ofen auf 230 °C vorheizen. Aubergine mehrmals einstechen und 35 Minuten rösten, bis sie zusammenfällt.','Kartoffelspalten mit der Hälfte des Öls und Salz für die letzten 25 Minuten aufs Blech geben.','Auberginenfleisch auskratzen, mit Tahin, Zitronensaft, Knoblauch und Salz zerdrücken.','Creme anrichten, restliches Öl, Petersilie und Granatapfelkerne darauf.','Mit Kartoffeln und Gurke servieren.'],
 'Für echtes Raucharoma die Aubergine direkt über der Gasflamme schwärzen.')
r('muhammara-gemuesesticks','Muhammara (Paprika-Walnuss-Dip) mit Gurke und Fenchel','Muhammara','Snack','snack',15,'muhammara',
 'Der syrische Lieblingsdip: süß, rauchig, leicht scharf. Macht aus Gemüsesticks einen Snack, auf den Du Dich freust.',
 [('Rote Paprika',80,'geröstet, gehäutet'),('Walnusskerne',10,'geröstet'),('Olivenöl',4,''),('Zitronensaft',3,''),('Tomatenmark',3,''),('Kreuzkümmel',0.5,''),('Gurke',80,'in Sticks'),('Fenchel',60,'in Streifen')],
 ['Paprika im Ofen bei 230 °C 20 Minuten rösten, bis die Haut schwarz wird, kurz abdecken und häuten.','Mit Walnüssen, Öl, Zitronensaft, Tomatenmark, Kreuzkümmel, Chiliflocken und Salz grob pürieren.','Mit Gurke und Fenchel servieren.'],
 'Paprika aus dem Glas geht auch. Gut abtropfen lassen, sonst wird der Dip wässrig.')
r('harissa-ofenkarotten','Harissa-Ofenkarotten mit Blumenkohl und Tahin-Zitrone','Harissa-Karotten','Ofengericht','main',35,'harissa-karotten',
 'Feurig, süß und cremig zugleich. Die schnelle Harissa aus Tomatenmark und Gewürzen machst Du selbst.',
 [('Karotten',120,'längs halbiert'),('Blumenkohl',150,'in Röschen'),('Olivenöl',10,''),('Tomatenmark',5,''),('Chili',2,'fein gehackt'),('Kreuzkümmel',1,'½ TL'),('Paprikapulver, geräuchert',1,''),('Knoblauch',2,''),('Tahin',8,''),('Zitronensaft',10,''),('Petersilie',5,'')],
 ['Ofen auf 220 °C vorheizen.','Öl, Tomatenmark, Chili, Kreuzkümmel, Paprika, Knoblauch und Salz zur Harissa verrühren.','Karotten und Blumenkohl darin wenden und 25 Minuten rösten.','Tahin mit Zitronensaft und 2 EL Wasser glatt rühren.','Gemüse anrichten, Tahinsauce darüber, mit Petersilie bestreuen.'],
 'Wer es milder mag, lässt die frische Chili weg. Das Raucharoma bleibt.')
r('escalivada','Escalivada: katalanisches Ofengemüse mit Knoblauchöl','Escalivada','Ofengericht','main',50,'escalivada',
 'Paprika, Aubergine und Zwiebel, im Ganzen geröstet und in Streifen gezupft. Simpel, rauchig und wunderbar ölig.',
 [('Rote Paprika',100,'ganz'),('Aubergine',200,'ganz'),('Rote Zwiebel',40,'halbiert'),('Olivenöl',12,''),('Knoblauch',2,'fein gehackt'),('Weinessig',5,'am besten Sherryessig'),('Petersilie',5,''),('Kartoffeln',100,'gekocht')],
 ['Ofen auf 220 °C vorheizen. Gemüse im Ganzen mit wenig Öl einreiben und 40 Minuten rösten, einmal wenden.','Kurz abdecken und abkühlen lassen, dann Paprika und Aubergine häuten.','Alles in lange Streifen zupfen und auf einer Platte auslegen.','Restliches Öl mit Knoblauch, Essig und Salz verrühren und darübergeben.','Mit Petersilie bestreuen und lauwarm mit den Kartoffeln servieren.'],
 'Escalivada schmeckt lauwarm am besten und hält sich 3 Tage im Kühlschrank.')
r('pkhali','Pkhali: georgische Spinat-Walnuss-Bällchen mit Granatapfel','Pkhali','Kalte Küche','main',30,'pkhali',
 'Kaum bekannt und sofort ein Lieblingsgericht: Spinat mit Walnüssen, Koriander und Essig, gekrönt mit Granatapfel.',
 [('Babyspinat',120,''),('Walnusskerne',15,''),('Zwiebeln',20,'sehr fein gehackt'),('Knoblauch',2,''),('Koriander',5,''),('Weinessig',5,''),('Olivenöl',5,''),('Granatapfel',15,'Kerne'),('Kartoffeln',100,'gekocht'),('Gurke',80,'in Scheiben')],
 ['Spinat in kochendem Wasser 1 Minute blanchieren, kalt abschrecken und sehr gut ausdrücken.','Walnüsse, Knoblauch, Koriander und eine Prise Salz fein mahlen.','Spinat fein hacken und mit Nusspaste, Zwiebel, Essig und Öl verkneten.','Zu kleinen Bällchen formen und in jedes eine Mulde drücken.','Mit Granatapfelkernen füllen und mit Kartoffeln und Gurke servieren.'],
 'Eine Prise Bockshornklee und Koriandersamen machen das Aroma echt georgisch.')
r('gemuese-tajine','Marokkanische Gemüse-Tajine mit Zimt, Oliven und Zitrone','Gemüse-Tajine','Eintopf','main',40,'tajine',
 'Warm, duftend und ein bisschen exotisch. Zimt, Kreuzkümmel und Oliven machen das Gemüse zum Festessen.',
 [('Karotten',50,'in Stücken'),('Süßkartoffel',60,'gewürfelt'),('Blumenkohl',80,'in Röschen'),('Zucchini',100,'in Stücken'),('Zwiebeln',30,''),('Tomaten (Dose)',80,''),('Grüne Oliven',20,''),('Olivenöl',8,''),('Zitronensaft',5,''),('Zimt',0.5,''),('Kreuzkümmel',1,''),('Kurkuma',0.5,''),('Ingwer',3,''),('Koriander',5,'')],
 ['Zwiebel im Öl andünsten, Gewürze und Ingwer 1 Minute mitrösten.','Karotten, Süßkartoffel und Blumenkohl zugeben, Tomaten und 100 ml Wasser angießen.','Zugedeckt 15 Minuten schmoren.','Zucchini und Oliven zugeben, weitere 10 Minuten garen.','Mit Zitronensaft und Salz abschmecken, mit Koriander bestreuen.'],
 'Ein Stück eingelegte Salzzitrone statt Zitronensaft macht die Tajine authentisch.')
r('briam','Briam: griechisches Ofengemüse mit Oregano','Briam','Ofengericht','main',60,'briam',
 'Kartoffeln, Zucchini und Tomaten, langsam im Olivenöl geschmort. Schmeckt nach Sommer auf Kreta.',
 [('Zucchini',150,'in Scheiben'),('Kartoffeln',130,'in dünnen Scheiben'),('Rote Paprika',40,'in Streifen'),('Tomaten',100,'gewürfelt'),('Rote Zwiebel',30,'in Ringen'),('Olivenöl',14,''),('Knoblauch',3,''),('Oregano (getrocknet)',0.5,''),('Petersilie',5,'')],
 ['Ofen auf 190 °C vorheizen.','Gemüse mit Öl, Knoblauch, Oregano, Salz und Pfeffer mischen und in eine Auflaufform geben.','50 ml Wasser angießen, mit Folie abdecken und 30 Minuten garen.','Folie abnehmen und weitere 25 Minuten rösten, bis die Ränder braun sind.','Mit Petersilie bestreuen.'],
 'Briam schmeckt lauwarm am besten. Gut zum Vorkochen.')
r('miso-aubergine','Ofen-Aubergine mit Miso-Glasur, Sesam und Vollkornreis','Miso-Aubergine','Ofengericht','main',35,'miso-aubergine',
 'Butterweiche Aubergine mit salzig-würziger Misoglasur. Ein japanischer Klassiker, ganz ohne Zucker.',
 [('Aubergine',250,'längs halbiert'),('Helle Misopaste',10,'2 TL'),('Sesamöl',8,''),('Ingwer',3,'gerieben'),('Limettensaft',5,''),('Sesam',4,''),('Frühlingszwiebeln',15,'in Ringen'),('Vollkornreis (gegart)',70,'ca. 25 g roh')],
 ['Ofen auf 210 °C vorheizen. Schnittflächen rautenförmig einschneiden und mit der Hälfte des Öls bestreichen.','Mit der Schnittfläche nach unten 20 Minuten backen.','Miso mit restlichem Öl, Ingwer, Limettensaft und 1 TL Wasser verrühren.','Auberginen umdrehen, mit der Glasur bestreichen und 8 Minuten weiterbacken.','Mit Sesam und Frühlingszwiebeln bestreuen und mit Reis servieren.'],
 'Die letzten 2 Minuten unter den Grill, dann karamellisiert die Glasur.')
r('mediterraner-kartoffelsalat','Mediterraner Kartoffelsalat mit Oliven, Kapern und Rucola','Kartoffelsalat','Kalte Küche','main',30,'kartoffelsalat',
 'Ohne Mayo, dafür mit Oliven, Kapern und einem Senf-Vinaigrette. Perfekt zum Mitnehmen ins Büro.',
 [('Kartoffeln',200,'festkochend'),('Grüne Oliven',20,'halbiert'),('Kapern',5,''),('Kirschtomaten',80,'halbiert'),('Rote Zwiebel',20,'fein gewürfelt'),('Rucola',20,''),('Olivenöl',10,''),('Weinessig',10,''),('Senf',3,'½ TL'),('Petersilie',5,'')],
 ['Kartoffeln in der Schale 20 Minuten garen, pellen und in Scheiben schneiden.','Essig, Senf, Öl, Salz und Pfeffer verrühren und noch warm über die Kartoffeln geben.','15 Minuten ziehen lassen.','Oliven, Kapern, Tomaten, Zwiebel und Petersilie unterheben.','Kurz vor dem Essen den Rucola unterheben.'],
 'Die Kartoffeln nehmen das Dressing nur warm richtig auf.')
# Frühstück (Planer-Schalter „Mit Frühstück“)
r('hirse-porridge','Hirse-Kokos-Porridge mit Zimtapfel und Walnüssen','Hirse-Porridge','Frühstück','breakfast',15,'porridge',
 'Warm, cremig und nach Zimt duftend. Ein Frühstück, das sich gar nicht nach Fasten anfühlt.',
 [('Hirse (gegart)',70,'ca. 25 g roh, am Vorabend gekocht'),('Kokosmilch (vollfett)',25,''),('Apfel',40,'gewürfelt'),('Walnusskerne',5,'gehackt'),('Zimt',0.5,'1 Prise')],
 ['Hirse mit Kokosmilch und 50 ml Wasser 3 Minuten cremig erwärmen.','Apfel mit Zimt und 1 EL Wasser 2 Minuten in einer kleinen Pfanne dünsten.','Porridge in eine Schale geben, Zimtapfel und Walnüsse darauf.'],
 'Hirse gleich für drei Tage kochen. Sie hält sich im Kühlschrank problemlos.')
r('chia-kokos-pudding','Chia-Kokos-Pudding mit Heidelbeeren','Chia-Pudding','Frühstück','breakfast',5,'chiapudding',
 'Am Abend in zwei Minuten angerührt, am Morgen fertig. Cremig, frisch und sättigend.',
 [('Chiasamen',10,'1 EL'),('Kokosmilch (vollfett)',40,''),('Mandeldrink ungesüßt',60,''),('Heidelbeeren',40,'')],
 ['Chiasamen mit Kokosmilch und Mandeldrink verrühren.','Nach 5 Minuten noch einmal umrühren, damit nichts verklumpt.','Abgedeckt über Nacht in den Kühlschrank stellen.','Morgens mit Heidelbeeren servieren.'],
 'Eine Prise Vanille oder abgeriebene Zitronenschale macht den Pudding noch runder.')
r('suesskartoffel-toast','Süßkartoffel-Toast mit Avocado, Tomate und Kresse','Süßkartoffel-Toast','Frühstück','breakfast',15,'suesskartoffel-toast',
 'Brot ist in diesen Tagen tabu, Toast trotzdem nicht: Süßkartoffelscheiben aus dem Toaster.',
 [('Süßkartoffel',80,'in 7 mm dicken Scheiben'),('Avocado',60,''),('Kirschtomaten',40,'geviertelt'),('Olivenöl',4,''),('Kürbiskerne',4,'geröstet'),('Kresse',3,'')],
 ['Süßkartoffelscheiben zwei- bis dreimal auf höchster Stufe toasten, bis sie weich sind. Alternativ 15 Minuten bei 210 °C im Ofen.','Avocado mit Salz, Pfeffer und einem Spritzer Zitrone zerdrücken.','Scheiben mit Avocado bestreichen, Tomaten darauflegen.','Mit Öl beträufeln, mit Kürbiskernen und Kresse bestreuen.'],
 'Die Scheiben am Vorabend im Ofen garen, dann morgens nur kurz in den Toaster.')
r('zucchini-roesti','Zucchini-Kartoffel-Rösti mit Kräuter-Avocado','Zucchini-Rösti','Frühstück','breakfast',25,'roesti',
 'Herzhaft, knusprig und ohne Ei. Für alle, die morgens lieber etwas Deftiges mögen.',
 [('Zucchini',100,'grob geraspelt'),('Kartoffeln',80,'roh, grob geraspelt'),('Leinsamen',3,'geschrotet'),('Olivenöl',8,''),('Avocado',25,''),('Schnittlauch',5,''),('Zitronensaft',3,'')],
 ['Zucchini salzen, 10 Minuten ziehen lassen und kräftig ausdrücken.','Mit Kartoffeln, Leinsamen, Salz und Pfeffer mischen.','Im heißen Öl zu drei flachen Rösti formen und je Seite 4 Minuten goldbraun braten.','Avocado mit Zitronensaft, Schnittlauch und Salz zerdrücken und dazu servieren.'],
 'Die Zucchini wirklich gut ausdrücken. Sonst werden die Rösti nicht knusprig.')
# Saison nach deutschem Freilandkalender der Hauptzutaten. Fehlt ein Eintrag, gilt das Rezept als ganzjährig.
F_,S_,H_,W_='Frühling','Sommer','Herbst','Winter'
SEASON={
 'kuerbissuppe':[H_,W_],'ofen-blumenkohl':[S_,H_],'zucchini-pfanne':[S_],'gruenkohl-chips':[H_,W_],'rote-bete-carpaccio':[H_,W_],
 'fenchel-orangen-suppe':[W_],'gazpacho':[S_],'brokkoli-lauch-suppe':[S_,H_],'zucchini-nudeln-pesto':[S_],'rotkohl-apfel-salat':[H_,W_],
 'ofen-tomaten-kraeuterkruste':[S_],'avocado-gurken-kaltschale':[S_],'hummus-bowl':[S_],'gemuese-lasagne':[S_,H_],'ofen-ratatouille':[S_],
 'blumenkohl-reis-bowl':[S_,H_],'gefuellte-paprika':[S_],'gurkensalat-sesam':[S_],'erbsen-minz-suppe':[F_,S_],'karotten-ingwer-suppe':[H_,W_],
 'rote-bete-suppe':[H_,W_],'aubergine-salsa':[S_],'feldsalat-ofenkuerbis':[H_,W_],'pilz-lauch-kartoffel-suppe':[H_,W_],
 'spargel-baerlauch-kartoffeln':[F_],'kohlrabi-carpaccio':[F_,S_],'baerlauch-kartoffel-suppe':[F_],'wirsing-eintopf':[H_,W_],
 'ofen-rosenkohl':[H_,W_],'pastinaken-suppe':[H_,W_],'baba-ganoush-teller':[S_],'muhammara-gemuesesticks':[S_,H_],'escalivada':[S_],
 'pkhali':[F_,H_],'gemuese-tajine':[H_,W_],'briam':[S_],'miso-aubergine':[S_,H_],'zucchini-roesti':[S_],
}
assert not set(SEASON)-{x['slug'] for x in R}, set(SEASON)-{x['slug'] for x in R}
for x in R: x['season']=SEASON.get(x['slug'],[])
