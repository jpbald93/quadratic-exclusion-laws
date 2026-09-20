#!/usr/bin/env python3
"""
regenerate_all.py — single documented entry point that regenerates every
headline claim of the paper from primary data, and FAILS LOUDLY on mismatch.

Run from this directory:

    python3 regenerate_all.py

It writes nothing outside `../results/regenerated/` and prints a PASS/FAIL
summary. Every number it checks is one that appears in the manuscript.

Supersedes, for the purposes of reproducing the FINAL manuscript:
  * scan_exclusion.py / verify_classification.py — these scan only
    `range(2, f+1, 2)`, i.e. even least residues, which MISSES odd-residue
    classes of odd conductors (e.g. 7 mod 21) and the class 0 mod 5. They are
    retained in the repository as historical artifacts of the superseded
    (reversal-only) classification and must NOT be used to verify the
    corrected class set.
  * analyze_delta.py — uses `flip_shifts` only, so it omits base-5
    inadmissibility classes entirely.

The correct class domain, per Definition 7 of the paper, is: every gap class
admitting an even representative — all g mod f when f is odd, the even g when
f is even.
"""
import json, math, os, sys
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(RES, "regenerated")

failures = []
notes = []


def check(label, got, want, tol=0.0):
    ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: got {got!r}, expected {want!r}")
    if not ok:
        failures.append(f"{label}: got {got!r}, expected {want!r}")
    return ok


# ---------------------------------------------------------------- arithmetic
def sqf(n):
    r, m = 1, n
    d = 2
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e % 2:
            r *= d
        d += 1
    if m > 1:
        r *= m
    return r


def disc(d):
    return d if d % 4 == 1 else 4 * d


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def kronecker(D, n):
    """Kronecker symbol (D|n) for fundamental discriminant D and n > 0."""
    if gcd(D, n) != 1:
        return 0
    res, m = 1, n
    while m % 2 == 0:
        if D % 2 == 0:
            return 0
        res *= 1 if D % 8 == 1 else -1
        m //= 2
    if m == 1:
        return res
    # Jacobi symbol (D|m) for odd m > 1
    a, b, t = D % m, m, 1
    while a:
        while a % 2 == 0:
            a //= 2
            if b % 8 in (3, 5):
                t = -t
        a, b = b, a
        if a % 4 == 3 and b % 4 == 3:
            t = -t
        a %= b
    return res * (t if b == 1 else 0)


def class_domain(f):
    """Gap classes admitting an even representative (Definition 7)."""
    return list(range(f)) if f % 2 else list(range(0, f, 2))


def exclusion_and_reversing(d):
    D, f = disc(d), abs(disc(d))
    units = [r for r in range(f) if gcd(r, f) == 1]
    rev, exc = [], []
    for g in class_domain(f):
        pairs = [r for r in units if gcd(r + g, f) == 1]
        if not pairs:
            continue
        if all(kronecker(D, (r + g) % f) == -kronecker(D, r) for r in pairs):
            rev.append(g)
        if not any(kronecker(D, r) == -1 and kronecker(D, (r + g) % f) == -1
                   for r in pairs):
            exc.append(g)
    return f, rev, exc


# ------------------------------------------------------- 1. the dichotomy
def check_dichotomy():
    print("\n1. Complete dichotomy (Corollary 20), all non-square 2 <= a <= 80")
    bases = [a for a in range(2, 81) if isqrt(a) ** 2 != a]
    check("non-square base count", len(bases), 72)
    mism = []
    for a in bases:
        d = sqf(a)
        f, rev, exc = exclusion_and_reversing(d)
        pred = (d % 2 == 0) or (d % 4 == 3) or (d % 3 == 0) or (d == 5)
        if bool(exc) != pred:
            mism.append(a)
    check("dichotomy mismatches", len(mism), 0)
    return bases


# ------------------------------------- 2. exhaustion (Proposition 21)
def check_exhaustion():
    print("\n2. Exhaustion: exclusion set == reversing set unless d = 5")
    extra = {}
    for a in range(2, 300):
        if isqrt(a) ** 2 == a:
            continue
        d = sqf(a)
        if d == 1:
            continue
        f, rev, exc = exclusion_and_reversing(d)
        diff = sorted(set(exc) - set(rev))
        if diff:
            extra.setdefault(d, diff)
    check("squarefree parts with extra classes", sorted(extra), [5])
    check("base-5 extra classes", extra.get(5), [2, 3])


# --------------------------------------- 3. the counting identity
def check_identity():
    print("\n3. Counting identity 4N = T - A - B + S (all shifts, unfiltered)")
    total, bad = 0, 0
    for a in range(2, 121):
        if isqrt(a) ** 2 == a:
            continue
        d = sqf(a)
        if d == 1:
            continue
        D, f = disc(d), abs(disc(d))
        for g in range(f):                       # NB: all shifts, not filtered
            U = [r for r in range(f)
                 if kronecker(D, r) and kronecker(D, (r + g) % f)]
            N = sum(1 for r in U
                    if kronecker(D, r) == -1 and kronecker(D, (r + g) % f) == -1)
            T = len(U)
            A = sum(kronecker(D, r) for r in U)
            B = sum(kronecker(D, (r + g) % f) for r in U)
            S = sum(kronecker(D, r) * kronecker(D, (r + g) % f) for r in U)
            total += 1
            if 4 * N != T - A - B + S:
                bad += 1
    check("(base, shift) cases", total, 14803)
    check("identity failures", bad, 0)


# ------------------------------- 4. prime-conductor count (Theorem 18)
def check_prime_count():
    print("\n4. Prime-conductor count, both cases")
    bad = 0
    for d in (5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97):
        for g in range(d):
            N = sum(1 for r in range(d)
                    if legendre(r, d) == -1 and legendre(r + g, d) == -1)
            want = (d - 1) // 2 if g % d == 0 else (d - 3 + 2 * legendre(g, d)) // 4
            if N != want:
                bad += 1
    check("prime-count failures", bad, 0)
    check("N(0) for d=13", sum(1 for r in range(13) if legendre(r, 13) == -1), 6)


# --------------------------- 5. twin primes and base 5 (Section 8)
def check_twins():
    print("\n5. Twin-prime claim for base 5")
    LIM = 400000
    sieve = bytearray([1]) * LIM
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(LIM) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    primes = [i for i in range(LIM) if sieve[i]]
    pset = set(primes)

    def factor(n):
        fs, m, dd = set(), n, 2
        while dd * dd <= m:
            while m % dd == 0:
                fs.add(dd)
                m //= dd
            dd += 1
        if m > 1:
            fs.add(m)
        return fs

    def is_artin(a, p):
        if p <= 2 or a % p == 0:
            return False
        return all(pow(a, (p - 1) // l, p) != 1 for l in factor(p - 1))

    twins = [(p, p + 2) for p in primes if p > 2 and (p + 2) in pset]
    b5 = sum(1 for p, q in twins if is_artin(5, p) and is_artin(5, q))
    b3 = sum(1 for p, q in twins if is_artin(3, p) and is_artin(3, q))
    check("twin pairs below 400000", len(twins), 3804)
    check("twins with 5 primitive root of both", b5, 0)
    check("twins with 3 primitive root of both", b3, 953)


# --------------------- 6. empirical statistics from the primary matrices
def pear(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def check_statistics():
    print("\n6. Empirical statistics from primary contingency matrices")
    raw = json.load(open(os.path.join(RES, "multibase_1e9.json")))
    check("total consecutive pairs", raw["n_pairs"], 50847531)

    def delta_of(m):
        n00, n01 = m[0]
        n10, n11 = m[1]
        return n11 / (n10 + n11) - n01 / (n00 + n01)

    order = [5, 2, 3, 13, 21, 17, 6, 29, 11, 10, 7]
    conds = {2: 8, 3: 12, 5: 5, 6: 24, 7: 28, 10: 40, 11: 44,
             13: 13, 17: 17, 21: 21, 29: 29}
    ad, lf, ws = [], [], []
    for a in order:
        e = raw["bases"][str(a)]
        dl = delta_of(e["joint"])
        d = sqf(a)
        f, rev, exc = exclusion_and_reversing(d)
        tot = raw["n_pairs"]
        wsum = sum(sum(m[0]) + sum(m[1])
                   for g, m in e["gap"].items() if int(g) % f in exc)
        ad.append(abs(dl))
        lf.append(math.log(conds[a]))
        ws.append(wsum / tot)
    check("r(log f, |delta|)", round(pear(lf, ad), 3), -0.957, 0.001)
    r_w, r_lf, r_wlf = pear(ws, ad), pear(lf, ad), pear(ws, lf)
    check("r(w, |delta|)", round(r_w, 3), 0.646, 0.002)
    partial = (r_w - r_lf * r_wlf) / math.sqrt((1 - r_lf ** 2) * (1 - r_wlf ** 2))
    check("partial r(w,|delta| | log f)", round(partial, 3), 0.136, 0.002)
    prods = sorted(a * math.sqrt(math.exp(l)) for a, l in zip(ad, lf))
    check("min |delta| sqrt(f)", round(prods[0], 4), 0.0714, 0.0001)
    check("max |delta| sqrt(f)", round(prods[-1], 4), 0.1757, 0.0001)

    # incidence total and the zero doubly-Artin count
    inc, both = 0, 0
    for a in (2, 3, 5, 6, 7, 10, 11, 21):
        e = raw["bases"][str(a)]
        d = sqf(a)
        f, rev, exc = exclusion_and_reversing(d)
        for g, m in e["gap"].items():
            if int(g) % f in exc:
                inc += sum(m[0]) + sum(m[1])
                both += m[1][1]
    check("exclusion base-pair incidences", inc, 84981870)
    check("doubly-Artin pairs in exclusion classes", both, 0)

    # outside-exclusion sign reversal: all eight positive
    pos = 0
    for a in (2, 3, 5, 6, 7, 10, 11, 21):
        e = raw["bases"][str(a)]
        d = sqf(a)
        f, rev, exc = exclusion_and_reversing(d)
        tot = [[0, 0], [0, 0]]
        for g, m in e["gap"].items():
            if int(g) % f not in exc:
                for i in (0, 1):
                    for j in (0, 1):
                        tot[i][j] += m[i][j]
        if delta_of(tot) > 0:
            pos += 1
    check("exclusion bases with positive outside delta", pos, 8)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("regenerate_all.py — reproducing every headline claim")
    print("=" * 62)
    check_dichotomy()
    check_exhaustion()
    check_identity()
    check_prime_count()
    check_twins()
    check_statistics()
    print("\n" + "=" * 62)
    if failures:
        print(f"FAIL — {len(failures)} mismatch(es):")
        for f_ in failures:
            print("   -", f_)
        sys.exit(1)
    print("PASS — every checked manuscript claim reproduced.")
    with open(os.path.join(OUT, "regeneration_log.txt"), "w") as fh:
        fh.write("PASS\n")


if __name__ == "__main__":
    main()
