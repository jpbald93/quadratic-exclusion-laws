#!/usr/bin/env python3
"""Empirically verify predicted exclusion laws for several bases up to 3e6."""
from sympy import primerange, n_order
from scan_exclusion import scan_base, conductor
import json

LIMIT = 3_000_000
BASES = [2, 3, 6, 7, 10, 11, 21]

primes = list(primerange(5, LIMIT))
print(f"primes loaded: {len(primes)}", flush=True)

# cache Artin status per base
results = {}
for a in BASES:
    info = scan_base(a)
    f = info["conductor"]
    flips = info["flip_shifts"]
    artin = {}
    def is_artin(p):
        if p in artin: return artin[p]
        v = (a % p != 0) and n_order(a, p) == p - 1
        artin[p] = v
        return v
    per_shift = {}
    for g0 in flips:
        n_pairs = both = 0
        for i in range(len(primes) - 1):
            p, q = primes[i], primes[i+1]
            if (q - p) % f != g0 % f:
                continue
            n_pairs += 1
            if is_artin(p) and is_artin(q):
                both += 1
        per_shift[g0] = {"pairs": n_pairs, "doubly_artin": both}
        print(f"base {a} (f={f}) shift {g0}: pairs={n_pairs} doubly_artin={both}", flush=True)
    # control: a preserve shift, expect NONZERO doubly-artin
    ctrl = {}
    for g0 in info["preserve_shifts"][:2]:
        n_pairs = both = 0
        for i in range(len(primes) - 1):
            p, q = primes[i], primes[i+1]
            if (q - p) % f != g0 % f:
                continue
            n_pairs += 1
            if is_artin(p) and is_artin(q):
                both += 1
        ctrl[g0] = {"pairs": n_pairs, "doubly_artin": both}
        print(f"  CONTROL base {a} shift {g0} (preserve): pairs={n_pairs} doubly_artin={both}", flush=True)
    results[a] = {"conductor": f, "flip": per_shift, "control": ctrl}

json.dump(results, open("verify_results.json","w"), indent=2)
print("done")
