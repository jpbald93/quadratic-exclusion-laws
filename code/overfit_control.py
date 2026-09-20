"""CONTROL: does conditioning on a RANDOM partition with the same number of
cells also destroy the correlation? If yes, the 96% reduction is an artifact
of slicing thin, not evidence about p-1 structure."""
from sympy import primerange, factorint, n_order
import math, random, hashlib
from collections import defaultdict
LIM=3_000_000
BASES=[2,3,5,6,7,10,11,13,15,17,21,29]
SMALLSET=[3,5,7,11,13]
random.seed(7)
glob=defaultdict(lambda:[[0,0],[0,0]])
sig_c=defaultdict(lambda: defaultdict(lambda:[[0,0],[0,0]]))
rnd_c=defaultdict(lambda: defaultdict(lambda:[[0,0],[0,0]]))
for p in primerange(5,LIM):
    f=factorint(p-1); fac=list(f)
    v2=min(f.get(2,0),4)
    mask=0
    for k,q in enumerate(SMALLSET):
        if q in f: mask|=1<<k
    nlarge=min(sum(1 for q in fac if q!=2 and q not in SMALLSET),3)
    sig=(v2*32+mask)*4+nlarge
    rsig=random.randrange(640)          # same cell count, no information
    art={a:(math.gcd(a,p)==1 and n_order(a,p)==p-1) for a in BASES}
    for i,a in enumerate(BASES):
        for b in BASES[i+1:]:
            glob[(a,b)][art[a]][art[b]]+=1
            sig_c[(a,b)][sig][art[a]][art[b]]+=1
            rnd_c[(a,b)][rsig][art[a]][art[b]]+=1
def phi(m):
    n00,n01=m[0];n10,n11=m[1];n=n00+n01+n10+n11
    r0,r1,c0,c1=n00+n01,n10+n11,n00+n10,n01+n11
    if min(r0,r1,c0,c1)==0 or n==0: return None,0
    return (n11*n00-n10*n01)/math.sqrt(r0*r1*c0*c1),n
def pooled(cells,minn=200):
    num=den=0
    for k,mm in cells.items():
        r,n=phi(mm)
        if r is not None and n>=minn: num+=r*n;den+=n
    return num/den if den else None
g=[];s=[];r=[]
for k in glob:
    a,_=phi(glob[k]); g.append(a)
    s.append(pooled(sig_c[k])); r.append(pooled(rnd_c[k]))
mg=sum(g)/len(g); ms=sum(s)/len(s); mr=sum(r)/len(r)
print(f"primes<{LIM:,}  pairs={len(g)}")
print(f"  unconditional          phi = {mg:.5f}")
print(f"  | real signature (640) phi = {ms:.5f}   ({100*(1-abs(ms)/abs(mg)):.1f}% removed)")
print(f"  | RANDOM 640 cells     phi = {mr:.5f}   ({100*(1-abs(mr)/abs(mg)):.1f}% removed)  <- control")
