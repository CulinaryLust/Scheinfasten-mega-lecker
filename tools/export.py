# Erzeugt die Datendateien der Webseite aus recipes_src.py
import json, os
from plan_check import *
PLAN={
1:[('Morgens','nussmix',1.5,'fixed'),('Mittags','ofen-blumenkohl',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1.5,'fixed'),('Abends','kuerbissuppe',1,'main'),('Abends','beilagensalat',1,'fixed')],
2:[('Morgens','nussmix',0.5,'fixed'),('Mittags','zucchini-pfanne',1,'main'),('Nachmittags','oliven',1.5,'fixed'),('Abends','aubergine-salsa',1,'main')],
3:[('Morgens','nussmix',0.5,'fixed'),('Mittags','rote-bete-carpaccio',1,'main'),('Nachmittags','oliven',1.5,'fixed'),('Abends','suesskartoffel-avocado-dip',1,'main')],
4:[('Morgens','nussmix',0.5,'fixed'),('Mittags','rotkohl-apfel-salat',1,'main'),('Nachmittags','oliven',1,'fixed'),('Abends','spinat-dal',1,'main')],
5:[('Morgens','nussmix',0.5,'fixed'),('Mittags','minestrone',1,'main'),('Nachmittags','oliven',1,'fixed'),('Abends','pak-choi-sesam',1,'main')],
}
for d,it in PLAN.items():
    s,p,o=ok(d,it); assert o,(d,[round(x) for x in s],[round(x,1) for x in p]); print('Tag',d,round(s[0]),[round(x) for x in p],'Zucker',round(s[4],1),'g')
# Variante „Mit Frühstück“ (Schalter im Planer): Frühstück statt Nussmix, Hauptgerichte auf 85 %.
# Tag 1 behält eine halbe Portion Nussmix, weil Longos 56 % Fett sonst nicht erreichbar sind.
BF={1:('chia-kokos-pudding',1.35),2:('zucchini-roesti',0.85),3:('hirse-porridge',0.7),4:('suesskartoffel-toast',0.7),5:('chia-kokos-pudding',0.7)}
PLAN_BF={}
for d,it in PLAN.items():
    b,bp=BF[d]
    PLAN_BF[d]=([('Morgens','nussmix',0.5,'fixed')] if d==1 else [])+[('Morgens',b,bp,'breakfast')]+[(m,k,round(p*0.85,2) if t=='main' else p,t) for m,k,p,t in it if k!='nussmix']
    s,p,o=ok(d,PLAN_BF[d]); assert o,('Frühstück',d,[round(x) for x in s],[round(x,1) for x in p]); print('Mit Frühstück Tag',d,round(s[0]),[round(x) for x in p],'Zucker',round(s[4],1),'g')
out='../src/data'; os.makedirs(out,exist_ok=True)
json.dump({k:list(v) for k,v in N.items()},open(f'{out}/nutrients.json','w'),ensure_ascii=False,indent=1)
json.dump(R,open(f'{out}/recipes.json','w'),ensure_ascii=False,indent=1)
json.dump({'reference':{'day1':{'kcal':1090,'protein':10,'fat':56,'carbs':34},'day2to5':{'kcal':725,'protein':9,'fat':44,'carbs':47},
  'source':'Brandhorst S et al. Cell Metab 2015;22(1):86-99 (Methoden, Human FMD)',
  'sourceNote':'Wei M et al. Sci Transl Med 2017 (Methoden) nennt für Tag 1 ca. 4.600 kJ (ca. 1.100 kcal) mit 11 % Eiweiß, 46 % Fett, 43 % Kohlenhydraten und für Tag 2 bis 5 ca. 3.000 kJ (ca. 717 kcal) mit denselben Anteilen 9/44/47 %.',
  'sugarMaxPercent':SUGAR_MAX_PCT,
  'tolerance':{'kcalPercent':5,'macroPoints':5,'proteinPoints':PROTEIN_TOL}},
  'days':{str(d):[{'meal':m,'recipe':k,'portion':x,'type':t} for m,k,x,t in it] for d,it in PLAN.items()},
  'breakfastDays':{str(d):[{'meal':m,'recipe':k,'portion':x,'type':t} for m,k,x,t in it] for d,it in PLAN_BF.items()}},
  open(f'{out}/plan.json','w'),ensure_ascii=False,indent=1)

# Lebensmitteldatenbank für den Rechner
import foods_src as FS
bls = json.load(open('bls_values.json'))
bt = FS.bls_table()
names = {x['name'] for x in FS.F}
assert len(names) == len(FS.F), 'Doppelter Name in foods_src.py'
missing = sorted({i['name'] for x in R for i in x['ingredients']} - names)
assert not missing, f'Zutaten ohne Eintrag in foods_src.py: {missing}'
foods = []
FS_KCAL = lambda n: next(f['n'][0] for f in foods if f['name'] == n)
for x in FS.F:
    label, glight, gcap = FS.GROUPS[x['group']]
    light = x['light'] or glight
    alts = x['alts'] or (FS.ALTS.get(x['group'], []) if light != 'g' else [])
    bad = [a for a in alts if a not in names]
    assert not bad, (x['name'], bad)
    if x['bls']:
        v = bt[x['name']]; src = {'db': 'BLS', 'code': x['bls'], 'name': bls[x['bls']]['name']}
    else:
        v = tuple(x['n'] or N[x['name']]) + (None,); src = {'db': 'USDA', 'code': None, 'name': None}
    cap, capWhy = FS.limit(gcap if x['cap'] is None else x['cap'], v)
    if x['name'] in FS.PUMPKIN and cap == FS.PUMPKIN_MAX: capWhy = 'kuerbis'
    foods.append({'name': x['name'], 'group': x['group'], 'groupLabel': label, 'light': light,
                  'cap': cap, 'capWhy': capWhy, 'syn': x['syn'], 'alts': alts,
                  'why': x['why'] or FS.WHY.get(x['group']) or (FS.WHY['y'] if light == 'y' else ''),
                  'piece': list(x['piece']) if x['piece'] else None, 'n': list(v), 'src': src})
# Jede Rezeptmenge (1 Portion) muss unter der Obergrenze des Rechners liegen, sonst widersprechen sich Rezept und Rechner.
CAP = {f['name']: f['cap'] for f in foods}
over = []
for x in R:
    tot = {}
    for i in x['ingredients']: tot[i['name']] = tot.get(i['name'], 0) + i['amount']
    over += [f"{x['slug']}: {n} {g} g > {CAP[n]} g" for n, g in tot.items() if CAP[n] and g > CAP[n] and FS_KCAL(n) > 5]
# Kürbis: auch die größte Portion (Faktor 1,15) bleibt unter dem Richtwert.
over += [f"{x['slug']}: Kürbis über {FS.PUMPKIN_MAX} g bei Faktor 1,15" for x in R if sum(i['amount'] for i in x['ingredients'] if i['name'] in FS.PUMPKIN) * 1.15 > FS.PUMPKIN_MAX + 2]
assert not over, 'Rezeptmengen über der Obergrenze:\n' + '\n'.join(over)
json.dump(foods, open(f'{out}/foods.json', 'w'), ensure_ascii=False, indent=1)
print(len(foods), 'Lebensmittel exportiert,', sum(f['src']['db'] == 'BLS' for f in foods), 'aus dem BLS')
