# Does conditioning on the STRUCTURE of p-1 kill the cross-base correlation?
# Artin base a requires a to avoid being an l-th power residue for each l | p-1.
# If p-1 = 2q (q prime), the conditions are few -> MANY bases Artin at once.
# That shared dependence on omega(p-1) is the natural common cause.
from sympy import primerange, factorint, n_order
import math
LIM=2_000_000
BASES=[2,3,5,6,7,10,11,13]
from collections import defaultdict
cells=defaultdict(lambda: defaultdict(lambda:[[0,0],[0,0]]))
glob=defaultdict(lambda:[[0,0],[0,0]])
for p in primerange(5,LIM):
    f=factorint(p-1); om=len(f)
    art={a:(a%p!=0 and math.gcd(a,p)==1 and n_order(a,p)==p-1) for a in BASES}
    for i,a in enumerate(BASES):
        for b in BASES[i+1:]:
            glob[(a,b)][art[a]][art[b]]+=1
            cells[(a,b)][om][art[a]][art[b]]+=1
def phi(m):
    n00,n01=m[0];n10,n11=m[1];n=n00+n01+n10+n11
    r0,r1,c0,c1=n00+n01,n10+n11,n00+n10,n01+n11
    if min(r0,r1,c0,c1)==0 or n==0: return None,0
    return (n11*n00-n10*n01)/math.sqrt(r0*r1*c0*c1), n
gs=[];rs=[]
for k,m in glob.items():
    g,_=phi(m); gs.append(g)
    num=den=0
    for om,mm in cells[k].items():
        r,n=phi(mm)
        if r is not None: num+=r*n; den+=n
    if den: rs.append(num/den)
print(f'primes < {LIM:,}, {len(gs)} base pairs')
print(f'mean phi, unconditional            = {sum(gs)/len(gs):.5f}')
print(f'mean phi, conditioned on omega(p-1)= {sum(rs)/len(rs):.5f}')
print(f'reduction = {100*(1-abs(sum(rs)/len(rs))/abs(sum(gs)/len(gs))):.1f}%')
