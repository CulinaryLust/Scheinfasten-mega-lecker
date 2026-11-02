from plan_check import *
import itertools, sys
DAY=int(sys.argv[1]) if len(sys.argv)>1 else 2
mains=[x['slug'] for x in R if x['slot']=='main']
snacks=[[],[('Nachmittags','oliven',1,'fixed')],[('Nachmittags','gruenkohl-chips',1,'snack')],[('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1,'fixed')],[('Nachmittags','tapenade-gemuesesticks',1,'snack')],[('Nachmittags','gurkensalat-sesam',1,'snack')],[('Nachmittags','ofen-kichererbsen',1,'snack')]]
res=[]
for a,b in itertools.permutations(mains,2):
  for sn in snacks:
    it=[('Morgens','nussmix',0.5,'fixed'),('Mittags',a,1,'main')]+sn+[('Abends',b,1,'main')]
    s,p,o=ok(DAY,it)
    if o:
      err=abs(s[0]-725)/725*100+sum(abs(x-y) for x,y in zip(p,(9,44,47)))
      res.append((round(err,1),a,b,[x[1] for x in sn],round(s[0]),[round(x) for x in p],round(s[4],1)))
res.sort()
print(len(res))
for r in res[:40]: print(r)
