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
