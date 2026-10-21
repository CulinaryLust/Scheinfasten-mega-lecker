import json, os
exec(open('recipes_src.py').read())
def nut(rc,m=1):
    s=[0]*5
    for i in rc['ingredients']:
        v=N[i['name']]
        for k in range(5): s[k]+=v[k]*i['amount']/100*m
    return s
by={x['slug']:x for x in R}
if __name__=='__main__':
    for x in R:
        s=nut(x); k=s[0]
        print(f"{x['slug']:28s} {x['slot']:5s} {k:5.0f} P{s[1]*4/k*100:3.0f} F{s[2]*9/k*100:3.0f} C{s[3]*4/k*100:3.0f} Z{s[4]:4.0f}")
