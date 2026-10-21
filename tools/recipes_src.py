# Quelle der Rezeptdaten. Erzeugt src/data/*.json. Nährwerte je 100 g:
# kcal, Eiweiß, Fett, Kohlenhydrate, davon Zucker (Richtwerte, an USDA FoodData Central angelehnt; vor Veröffentlichung mit BLS prüfen)
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
 [('Hokkaido-Kürbis',300,'mit Schale gewürfelt'),('Zwiebeln',40,''),('Ingwer',5,'frisch gerieben'),('Olivenöl',3,''),('Gemüsebrühe',250,''),('Kokosmilch (vollfett)',40,''),('Kürbiskerne',8,'1 EL')],
 ['Zwiebel im Öl 3 Minuten anschwitzen, Ingwer und Kürbis kurz mitrösten.','Brühe angießen und zugedeckt 15 Minuten weich kochen.','Kokosmilch einrühren (1 TL zum Garnieren zurückbehalten) und fein pürieren.','Kürbiskerne ohne Fett rösten, bis sie knacken.','Mit Salz, Pfeffer und Limette abschmecken und mit Kernen servieren.'],
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
 [('Rotkohl',200,'fein gehobelt'),('Apfel',60,'in Stiften'),('Sonnenblumenkerne',10,''),('Olivenöl',8,''),('Apfelessig',15,''),('Kartoffeln',100,'gekocht, lauwarm')],
 ['Rotkohl mit Salz kräftig durchkneten, bis er weich wird.','Essig, Öl und Pfeffer zugeben, Apfel unterheben.','Sonnenblumenkerne ohne Fett rösten.','Mit lauwarmen Kartoffelwürfeln anrichten und mit Kernen bestreuen.'],'Am Vorabend zubereitet schmeckt der Salat noch runder.')
r('ofen-tomaten-kraeuterkruste','Ofen-Tomaten mit Leinsamen-Kräuterkruste und Hirse','Ofen-Tomaten','Ofengericht','main',30,'ofengemuese',
 'Saftige Tomaten unter einer knusprigen Kruste. Schmeckt nach Sommer, auch im Winter.',
 [('Tomaten',300,'halbiert'),('Leinsamen',8,'geschrotet'),('Petersilie',10,''),('Knoblauch',3,''),('Olivenöl',8,''),('Hirse (gegart)',100,'')],
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
 [('Süßkartoffel',180,'in Spalten'),('Olivenöl',6,''),('Avocado',50,''),('Limettensaft',10,''),('Paprikapulver, geräuchert',1,''),('Blattsalat',50,'')],
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
 [('Karotten',250,'in Scheiben'),('Ingwer',8,''),('Zwiebeln',40,''),('Kokosmilch (vollfett)',40,''),('Gemüsebrühe',300,''),('Olivenöl',3,'')],
 ['Zwiebel und Ingwer im Öl anschwitzen.','Karotten und Brühe zugeben, 18 Minuten weich kochen.','Kokosmilch zugeben und fein pürieren.','Mit Salz, Pfeffer und Limette abschmecken.'],'Mit einem Klecks Kokosmilch und Chiliöl servieren.')
r('champignon-pfanne-cashew','Champignon-Pfanne mit Cashew-Rahm und Kartoffeln','Champignon-Pfanne','Pfanne','main',25,'pilzpfanne',
 'Rahmig wie bei Oma, nur ohne Sahne. Die Cashews machen die Sauce cremig.',
 [('Champignons',200,'in Scheiben'),('Kartoffeln',150,'gekocht, in Scheiben'),('Cashewkerne',12,'eingeweicht'),('Zwiebeln',40,''),('Olivenöl',6,''),('Petersilie',5,'')],
 ['Cashews mit 80 ml Wasser und Salz cremig mixen.','Pilze in heißem Öl braun braten, Zwiebel zugeben.','Kartoffeln zugeben und kurz mitbraten.','Cashew-Rahm angießen, 2 Minuten köcheln, mit Petersilie servieren.'],'Pilze erst salzen, wenn sie gebräunt sind.')
r('rote-bete-suppe','Rote-Bete-Suppe mit Meerrettich und Walnüssen','Rote-Bete-Suppe','Suppe','main',25,'rote-bete-suppe',
 'Tiefrot, erdig und mit einem frischen Kick vom Meerrettich.',
 [('Rote Bete (vorgegart)',200,'gewürfelt'),('Kartoffeln',80,''),('Zwiebeln',40,''),('Olivenöl',6,''),('Gemüsebrühe',300,''),('Meerrettich',5,'frisch gerieben'),('Walnusskerne',5,'')],
 ['Zwiebel im Öl anschwitzen, Kartoffel und Brühe zugeben, 12 Minuten köcheln.','Rote Bete zugeben und fein pürieren.','Mit Meerrettich, Salz und einem Spritzer Zitrone abschmecken.','Mit gehackten Walnüssen servieren.'],'Ein paar Dillspitzen passen wunderbar dazu.')
r('aubergine-salsa','Gegrillte Aubergine mit Tomaten-Kräuter-Salsa','Aubergine mit Salsa','Pfanne','main',25,'aubergine',
 'Rauchige Auberginenscheiben, darauf eine frische Salsa. Mediterran und leicht.',
 [('Aubergine',250,'in Scheiben'),('Olivenöl',10,''),('Tomaten',120,'fein gewürfelt'),('Rote Zwiebel',20,'fein gewürfelt'),('Petersilie',10,''),('Zitronensaft',10,''),('Kartoffeln',80,'gekocht')],
 ['Auberginenscheiben dünn mit Öl bestreichen und in einer Grillpfanne von beiden Seiten 4 Minuten braten.','Tomaten, Zwiebel, Petersilie, Zitronensaft und Salz mischen.','Salsa auf die Aubergine geben und mit Kartoffeln servieren.'],'Aubergine nicht ertränken: wenig Öl mit dem Pinsel reicht.')
r('feldsalat-ofenkuerbis','Feldsalat mit Ofen-Kürbis und Kürbiskernen','Kürbis-Feldsalat','Salat','main',30,'kuerbissalat',
 'Herbst auf dem Teller: süßer Ofenkürbis, nussiger Feldsalat, ein Hauch Balsamico.',
 [('Hokkaido-Kürbis',250,'in Spalten'),('Feldsalat',50,''),('Kürbiskerne',8,''),('Olivenöl',8,''),('Balsamico',10,''),('Rote Zwiebel',20,'in Ringen')],
 ['Kürbis mit der Hälfte des Öls und Salz bei 210 °C 25 Minuten rösten.','Restliches Öl mit Balsamico und Pfeffer verrühren.','Feldsalat mit Dressing mischen, Kürbis und Zwiebel daraufgeben.','Kürbiskerne rösten und darüberstreuen.'],'Der Kürbis kann lauwarm oder kalt auf den Salat.')
r('pak-choi-sesam','Gebratener Pak Choi mit Ingwer und Sesam','Pak Choi','Pfanne','main',15,'pakchoi',
 'In zehn Minuten fertig, knackig und voller Aroma.',
 [('Pak Choi',250,'halbiert'),('Ingwer',5,''),('Knoblauch',2,''),('Sesamöl',6,''),('Sesam',5,''),('Süßkartoffel',120,'gedämpft'),('Limettensaft',10,'')],
 ['Süßkartoffel in Würfeln 12 Minuten dämpfen.','Pak Choi mit der Schnittfläche nach unten im Sesamöl 3 Minuten braten.','Ingwer und Knoblauch zugeben, mit 2 EL Wasser ablöschen und 2 Minuten dünsten.','Mit Limette, Sesam und Süßkartoffel servieren.'],'Statt Salz einen Spritzer Sojasauce, aber sparsam.')
r('pilz-lauch-kartoffel-suppe','Kartoffel-Lauch-Suppe mit gebratenen Pilzen','Kartoffel-Lauch-Suppe','Suppe','main',30,'suppe-hell2',
 'Hausmannskost in leicht: cremig gemixt, obendrauf knusprige Pilze.',
 [('Kartoffeln',150,'gewürfelt'),('Lauch',120,'in Ringen'),('Gemüsebrühe',350,''),('Olivenöl',8,''),('Champignons',60,'in Scheiben'),('Petersilie',5,'')],
 ['Lauch in der Hälfte des Öls dünsten, Kartoffel und Brühe zugeben, 15 Minuten köcheln.','Fein pürieren und mit Muskat abschmecken.','Pilze im restlichen Öl knusprig braten.','Suppe mit Pilzen und Petersilie servieren.'],'Ein paar Lauchringe für die Garnitur aufheben.')
