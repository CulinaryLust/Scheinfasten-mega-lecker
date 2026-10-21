from build_data import *
REF={1:(1090,10,56,34),2:(725,9,44,47)}
def day(items):
    s=[0]*5
    for _,k,m,_t in items:
        n=nut(by[k],m); s=[a+b for a,b in zip(s,n)]
    return s
def ok(d,items):
    s=day(items); r=REF[1 if d==1 else 2]; k=s[0]
    p=(s[1]*4/k*100,s[2]*9/k*100,s[3]*4/k*100)
    return s,p,abs(k-r[0])/r[0]<=.05 and all(abs(a-b)<=5 for a,b in zip(p,r[1:]))
PLAN={
1:[('Morgens','nussmix',1.5,'fixed'),('Mittags','minestrone',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1.5,'fixed'),('Abends','kuerbissuppe',1,'main'),('Abends','beilagensalat',1,'fixed')],
2:[('Morgens','nussmix',0.5,'fixed'),('Mittags','zucchini-pfanne',1,'main'),('Nachmittags','oliven',1,'fixed'),('Abends','kuerbissuppe',1,'main')],
3:[('Morgens','nussmix',0.5,'fixed'),('Mittags','ofen-ratatouille',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1,'fixed'),('Abends','karotten-ingwer-suppe',1,'main')],
4:[('Morgens','nussmix',0.5,'fixed'),('Mittags','ofen-blumenkohl',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Nachmittags','oliven',1,'fixed'),('Abends','pilz-miso-bruehe',1,'main')],
5:[('Morgens','nussmix',0.5,'fixed'),('Mittags','zucchini-nudeln-pesto',1,'main'),('Nachmittags','gruenkohl-chips',1,'snack'),('Abends','rote-bete-carpaccio',1,'main')],
}
if __name__=='__main__':
    for d,it in PLAN.items():
        s,p,o=ok(d,it); print(d,round(s[0]),[round(x) for x in p],o)
