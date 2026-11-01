# Erzeugt die Datendateien der Webseite aus recipes_src.py
import json, os
from plan_check import *
PLAN={
1:[('Morgens','nussmix',1.5,'fixed'),('Mittags','minestrone',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1.5,'fixed'),('Abends','kuerbissuppe',1,'main'),('Abends','beilagensalat',1,'fixed')],
2:[('Morgens','nussmix',0.5,'fixed'),('Mittags','gefuellte-paprika',1,'main'),('Nachmittags','ofen-kichererbsen',1,'snack'),('Abends','kuerbissuppe',1,'main')],
3:[('Morgens','nussmix',0.5,'fixed'),('Mittags','hummus-bowl',1,'main'),('Nachmittags','oliven',1,'fixed'),('Abends','pilz-lauch-kartoffel-suppe',1,'main')],
4:[('Morgens','nussmix',0.5,'fixed'),('Mittags','rotkohl-apfel-salat',1,'main'),('Nachmittags','oliven',1,'fixed'),('Abends','zucchini-pfanne',1,'main')],
5:[('Morgens','nussmix',0.5,'fixed'),('Mittags','ofen-tomaten-kraeuterkruste',1,'main'),('Nachmittags','gurkensalat-sesam',1,'snack'),('Abends','rote-bete-carpaccio',1,'main')],
}
for d,it in PLAN.items():
    s,p,o=ok(d,it); assert o,(d,s,p); print('Tag',d,round(s[0]),[round(x) for x in p])
out='../src/data'; os.makedirs(out,exist_ok=True)
json.dump({k:list(v) for k,v in N.items()},open(f'{out}/nutrients.json','w'),ensure_ascii=False,indent=1)
json.dump(R,open(f'{out}/recipes.json','w'),ensure_ascii=False,indent=1)
json.dump({'reference':{'day1':{'kcal':1090,'protein':10,'fat':56,'carbs':34},'day2to5':{'kcal':725,'protein':9,'fat':44,'carbs':47},
  'source':'Wei M et al. Sci Transl Med 2017;9(377):eaai8700','tolerance':{'kcalPercent':5,'macroPoints':5}},
  'days':{str(d):[{'meal':m,'recipe':k,'portion':x,'type':t} for m,k,x,t in it] for d,it in PLAN.items()}},
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
for x in FS.F:
    label, glight, gcap = FS.GROUPS[x['group']]
    light = x['light'] or glight
    alts = x['alts'] or (FS.ALTS.get(x['group'], []) if light != 'g' else [])
    bad = [a for a in alts if a not in names]
    assert not bad, (x['name'], bad)
    if x['bls']:
        v = bt[x['name']]; src = {'db': 'BLS', 'code': x['bls'], 'name': bls[x['bls']]['name']}
    else:
        v = tuple(N[x['name']]) + (None,); src = {'db': 'USDA', 'code': None, 'name': None}
    foods.append({'name': x['name'], 'group': x['group'], 'groupLabel': label, 'light': light,
                  'cap': gcap if x['cap'] is None else x['cap'], 'syn': x['syn'], 'alts': alts,
                  'why': x['why'] or FS.WHY.get(x['group']) or (FS.WHY['y'] if light == 'y' else ''),
                  'piece': list(x['piece']) if x['piece'] else None, 'n': list(v), 'src': src})
json.dump(foods, open(f'{out}/foods.json', 'w'), ensure_ascii=False, indent=1)
print(len(foods), 'Lebensmittel exportiert,', sum(f['src']['db'] == 'BLS' for f in foods), 'aus dem BLS')
