# The General Exclusion Law for Consecutive Artin Primes

Status: proof drafted 2026-08-16; classification verified computationally for all
bases a = 2..30 (exact agreement, `verify_classification.py`), and the
nonemptiness criterion verified for a = 2..79 (`check_criterion.py`).

---

## Setup and notation

Let `a >= 2` be an integer that is not a perfect square. For a prime `p` with
`p | a` excluded, say `p` is *Artin base a* if `a` is a primitive root mod `p`.

Let `d = sqf(a)` be the squarefree part of `a`, and let

    D = d          if d = 1 (mod 4)
    D = 4d         otherwise

be the discriminant of `K = Q(sqrt(a)) = Q(sqrt(d))`. Write `f = |D|` for the
conductor. Let `chi_a = (d | .)` be the associated quadratic character; by
quadratic reciprocity `chi_a` is a character mod `f`, i.e.

    chi_a(p) depends only on p mod f.                                  (1)

**Basic obstruction (classical).** If `a` is a primitive root mod `p` then `a`
is a non-residue mod `p`, so

    p Artin base a   ==>   chi_a(p) = -1.                              (2)

(For `p > 2`: a square cannot generate the cyclic group of even order `p-1`.)

---

## Definition (flip / preserve / mixed shift)

For an even `g`, and for the set `R_f` of residues `r mod f` that are coprime to
`f` and actually attained by primes, say `g` is:

- a **flip shift** if `chi_a(r + g) = -chi_a(r)` for all `r in R_f`;
- a **preserve shift** if `chi_a(r + g) = +chi_a(r)` for all `r in R_f`;
- **mixed** otherwise.

## Theorem 1 (General exclusion law)

If `g` is a flip shift for base `a`, then **no** pair of primes `(p, q)` with
`q = p + g'` for any `g' = g (mod f)` can both be Artin base `a`.

*Proof.* By (1) and the flip property, `chi_a(q) = -chi_a(p)`. Hence at least one
of `chi_a(p), chi_a(q)` equals `+1`, and by (2) that prime is not Artin. ∎

This is unconditional and elementary. The base-10 case (`d = 10`, `f = 40`, flip
shift `g = 20`) is the theorem of the first paper; it is one instance.

---

## Theorem 2 (Classification of flip shifts)

Factor `D` into **prime discriminants**, `D = D_1 D_2 ... D_k`, where each `D_i`
is one of: `-4`; `8` or `-8`; `q*` for an odd prime `q | d`, with
`q* = q` if `q = 1 (mod 4)` and `q* = -q` if `q = 3 (mod 4)`.
This factorization is unique, and correspondingly

    chi_a = chi_{D_1} * ... * chi_{D_k},      chi_{D_i} of conductor |D_i|.

Each component's behaviour under `r -> r + g` is determined by `g` alone:

| component `D_i` | conductor | flip iff | preserve iff | else |
|---|---|---|---|---|
| `-4` | 4 | `g = 2 (mod 4)` | `g = 0 (mod 4)` | — |
| `8` or `-8` | 8 | `g = 4 (mod 8)` | `g = 0 (mod 8)` | mixed (`g = 2,6 mod 8`) |
| `-3` | 3 | `g != 0 (mod 3)` | `g = 0 (mod 3)` | — |
| `q*`, `q >= 5` | `q` | never | `g = 0 (mod q)` | mixed |

Then `g` is a flip shift for `a` **iff** no component is mixed at `g` and an
**odd** number of components flip at `g`; and a preserve shift iff no component
is mixed and an even number flip.

*Proof sketch of the component table.*
- `chi_{-4}(r) = (-1)^((r-1)/2)` depends on `r mod 4`; adding `g = 2 (mod 4)`
  toggles `r mod 4` between `1` and `3`, flipping the sign; `g = 0 (mod 4)` fixes it.
- `chi_8(r) = +1` iff `r = ±1 (mod 8)`. The classes `{1,7}` and `{3,5}` are
  interchanged by `r -> r + 4`, so `g = 4 (mod 8)` flips; `g = 0` preserves.
  For `g = 2 (mod 8)`: `1 -> 3` (flip) but `3 -> 5` (preserve), hence mixed.
  Same for `chi_{-8}`, whose value set is `{1,3}` — again swapped by `+4`.
- `chi_{-3}(r) = +1` iff `r = 1 (mod 3)`. Since `r` is coprime to 3, `r` ranges
  over `{1,2}`, and `chi_{-3}` is *injective* on that set. Adding `g != 0 (mod 3)`
  necessarily moves `1 <-> 2`, so it flips; `g = 0 (mod 3)` fixes.
  (This is why base 3 has *three* flip shifts: the mod-3 component flips for
  two-thirds of shifts.)
- For odd `q >= 5`: the residues coprime to `q` split into `(q-1)/2` residues with
  `chi = +1` and `(q-1)/2` with `chi = -1`, and both classes have size `>= 2`.
  A translation `r -> r + g` with `g != 0` is a fixed-point-free permutation of
  `Z/q`, and since it is not the identity it cannot map the QR set onto itself or
  onto its complement — the QR set is not a coset of any subgroup for `q >= 5`
  (equivalently: the QR indicator is not a translate of ±itself, since a
  translation-invariant-up-to-sign structure would force the Gauss sum modulus to
  degenerate). So the behaviour is class-dependent: mixed.
- Multiplicativity of `chi_a` gives the parity rule. ∎

**Computational status.** The predicted flip and preserve sets agree *exactly*
with brute force for every base `2 <= a <= 30` (all 25 non-square bases):
`CLASSIFICATION THEOREM: VERIFIED`.

---

## Corollary 3 (Which bases admit an exclusion law)

Base `a` (non-square, `d = sqf(a)`) admits at least one flip shift **iff**

    d is even,   or   d = 3 (mod 4),   or   3 | d.

Equivalently: iff the prime-discriminant factorization of `D` contains one of
`-4`, `±8`, `-3`.

*Proof.* By Theorem 2 a flip shift needs at least one flip-capable component,
and by the table the flip-capable components are exactly `-4`, `±8`, `-3`.
Conversely if such a component exists, choose `g` divisible by every other
component's conductor and lying in that component's flip class — possible by CRT
since the moduli are coprime. ∎

**Verified for `a = 2..79`: no mismatches.**

Consequence: **bases with `d = 1 (mod 4)`, `d` odd, `3 ∤ d` have NO exclusion
law at all.** Smallest cases `d = 5, 13, 17, 29, 37, 41, 53, 61` — matching the
scan, where bases 5, 13, 17, 20, 29 have empty flip sets.

---

## Corollary 4 — **REFUTED 2026-08-16. DO NOT PUT THIS IN THE PAPER.**

The prediction below (that |delta| should be ordered by excluded-gap density) was
tested at 3e6 and at 1e9 (50,847,531 consecutive pairs, 11 bases) and is FALSE.

Measured at 1e9:

| base | f | #flip | excl. weight | delta | z |
|---|---|---|---|---|---|
| 5 | 5 | 0 | 0.0000 | -0.066563 | -478.9 |
| 2 | 8 | 1 | 0.2636 | -0.050199 | -361.0 |
| 3 | 12 | 3 | 0.5312 | -0.046676 | -335.4 |
| 13 | 13 | 0 | 0.0000 | -0.042573 | -305.6 |
| 21 | 21 | 1 | 0.0530 | -0.038345 | -275.2 |
| 17 | 17 | 0 | 0.0000 | -0.033025 | -236.7 |
| 6 | 24 | 3 | 0.2442 | -0.025205 | -180.4 |
| 29 | 29 | 0 | 0.0000 | -0.022422 | -160.4 |
| 11 | 44 | 1 | 0.0353 | -0.018909 | -135.2 |
| 10 | 40 | 1 | 0.0436 | -0.014140 | -101.0 |
| 7 | 28 | 1 | 0.0702 | -0.013491 | -96.4 |

- Base 5 has NO exclusion law yet the LARGEST |delta|.
- Base 3 excludes 53% of gap classes by weight and ranks only 3rd.
- mean |delta| with a law = 0.0296 ; without = 0.0411 -> ratio **0.72x (backwards)**.
- `r(excluded_gap_weight, |delta|) = 0.2309` — weak, and confounded (small
  conductors happen to be the even/3-divisible ones).

**Why:** the exclusion law is an ABSOLUTE constraint on a SMALL SET of gap
classes. Those classes are a minority of all consecutive pairs, so they barely
shift the global statistic. The exclusion law is *locally deterministic but
globally negligible*.

## Corollary 4' (REPLACEMENT — the real cross-base law)

|delta(a)| is governed by the CONDUCTOR SIZE, not by exclusion density.
At 1e9, over 11 bases:

    r(log f, |delta|)      = -0.9574
    r(1/sqrt(f), |delta|)  = +0.9511
    r(1/f, |delta|)        = +0.9208
    r(excl_weight, |delta|)= +0.2309    (the refuted mechanism)

Mechanism: chi_a is determined mod f, so there are ~phi(f) admissible classes.
Smaller f => fewer classes => the Lemke Oliver--Soundararajan transition bias is
spread over fewer channels and concentrates into a larger per-base correlation.

Scaling check (`|delta| * f` and `|delta| * sqrt(f)` columns) shows neither pure
1/f nor 1/sqrt(f) is exact — `|delta|*f` drifts 0.33 -> 0.83, `|delta|*sqrt(f)`
drifts 0.15 -> 0.13 (flatter). So `1/sqrt(f)` is the better single-parameter fit
but the truth is presumably a sum over the phi(f) LOS channels rather than a
clean power of f. **State this as a measured empirical law with the caveat, not
as a conjectured exact power.** Deriving the constant from the LOS channel sum
is the natural theory follow-up.

---

## SUPERSEDED prediction (kept for the record only)

### Corollary 4 (Density of excluded gaps, and a quantitative prediction)

Let `F(a)` be the number of flip classes among the `f/2` even residue classes
mod `f`. The exclusion law removes a proportion `F(a) / (f/2)` of gap classes.
From the classification:

| base | `f` | flip shifts | excluded fraction of even gap classes |
|---|---|---|---|
| 3, 12, 27 | 12 | 4, 6, 8 | 3/6 = **50%** |
| 2, 8, 18 | 8 | 4 | 1/4 = 25% |
| 21 | 21 | 14 | 1/10 |
| 6, 24 | 24 | 8, 12, 16 | 3/12 = 25% |
| 7, 28 | 28 | 14 | 1/14 |
| 10 | 40 | 20 | 1/20 |
| 5, 13, 17, 29 | — | none | **0%** |

Weighting by the actual gap distribution (small gaps dominate), base 3 is by far
the most constrained. This yields a **falsifiable prediction**: the
consecutive-pair Artin anticorrelation `delta(a)` should satisfy

    |delta(3)| > |delta(2)| ~ |delta(6)| > |delta(7)| > |delta(10)| > ... > |delta(5)| ~ (residual only)

with bases `5, 13, 17, 29` showing only the weaker Lemke Oliver–Soundararajan
residue-channel effect and no exclusion contribution.

---

## Empirical confirmation of Theorem 1 (already run)

Consecutive prime pairs up to 3e6, gaps in predicted flip classes:

| base | `f` | flip shift(s) | pairs | doubly-Artin | control (preserve shift) |
|---|---|---|---|---|---|
| 2 | 8 | 4 | 57,786 | **0** | 9,698 / 35,704 |
| 3 | 12 | 4, 6, 8 | 117,005 | **0** | 9,735 / 34,297 |
| 6 | 24 | 8, 12, 16 | 51,643 | **0** | 2,709 / 9,179 |
| 7 | 28 | 14 | 13,492 | **0** | 1,072 / 4,163 |
| 10 | 40 | 20 | 7,222 | **0** | 401 / 1,512 |
| 11 | 44 | 22 | 6,361 | **0** | 193 / 708 |
| 21 | 21 | 14 | 11,829 | **0** | — |

~265,000 pairs, zero exceptions; controls ~27% doubly-Artin as expected.

---

## What still needs doing

1. **The `q >= 5` mixed argument — CLEAN PROOF FOUND (verified numerically).**
   Suppose `chi(r+g) = e*chi(r)` for a fixed `e = ±1` and all `r` coprime to `q`
   with `r+g` also coprime. Sum against `chi(r)`:

       S(g) := sum_{r mod q} chi(r) chi(r+g).

   Standard evaluation (substitute `r -> rt`, or note it is a Jacobi-type sum):
   **`S(g) = -1` for every `g != 0 (mod q)`** — confirmed numerically for
   `q = 3,5,7,11,13,17,19,23` (all values exactly `-1`).
   If the relation held with sign `e`, the sum would instead be
   `e * #{r : r, r+g both coprime to q} = e*(q-2)`.
   For `q >= 5`, `q - 2 >= 3 > 1`, so `|e(q-2)| != 1`: contradiction. Hence mixed. ∎

   **IMPORTANT subtlety (this is why `q = 3` is genuinely different, not an
   exception being swept under the rug):** for `q = 3` we get `q - 2 = 1`, so
   `e*(q-2) = ±1` and the argument gives *no* contradiction. Concretely: only
   ONE residue `r` survives the condition that `r` and `r+g` are both coprime to
   3, and a condition on a single residue is vacuously a "flip". So the `-3`
   component's flipping behaviour is not an accident of small numbers — it is
   exactly the boundary case where the Jacobi-sum obstruction degenerates. Say
   this explicitly in the paper; a referee will look for it.
2. Full `delta(a)` measurement to 1e9 per base to test Corollary 4's ordering.
3. Decide framing: "Exclusion laws for consecutive Artin primes in arbitrary
   bases" — theorem + classification + prediction + confirmation.

---

# PAPER #3: Cross-base (same-prime) Artin correlation — RESULTS 2026-08-17

Question: is `p Artin base a` correlated with `p Artin base b` for the SAME p?
Never measured before. Run at 1e9: 50,847,532 primes, 12 bases, 66 pairs.

## Headline: it's a near-complete NULL, explained by p-1 structure

    mean phi  unconditional                      = 0.03521   (all 66 pairs +, |z| up to 476)
    mean phi  | omega(p-1)                       = 0.01581   (55.1% removed)
    mean phi  | fine signature                   = 0.00186   (94.7% removed)

Fine signature = ( min(v2(p-1),4), bitmask of which of {3,5,7,11,13} divide p-1,
min(#prime factors > 13, 3) ) — 640 cells, 500 populated. This is exactly the
data the Kummer/Artin conditions see for small bases.

omega only removed ~55% because it is a CRUDE PROXY: it counts how many primes
divide p-1, but Artin status depends on WHICH ones.

## OVERFITTING CONTROL (this is what makes it publishable)

Conditioning on a RANDOM 640-cell partition with zero information:

    | real signature (640)  phi = 0.00124   (96.4% removed)
    | RANDOM 640 cells      phi = 0.03483   ( 0.0% removed)

Random slicing removes NOTHING. The reduction is real signal, not thin cells.

## ENTANGLEMENT REFUTED (my 2nd wrong mechanism guess this project)

I predicted pairs with chi_a*chi_b = chi_c would correlate MORE. They correlate LESS:

    in a triple      n=15  phi=0.03144  |om=0.01312  |sig=0.00487
    not in a triple  n=51  phi=0.03631  |om=0.01660  |sig=0.00097

## THE REAL RESIDUAL STRUCTURE: shared prime factors of sqf(a), sqf(b)

Not entanglement — the residual is driven by whether sqf(a) and sqf(b) SHARE a
prime factor. Sorted residuals for the 13 sharing pairs:

    2,10  gcd=2  phi|sig= -0.03426  z= -211.5
    5,15  gcd=5  phi|sig= -0.02550  z= -157.5
    6,10  gcd=2  phi|sig= -0.01437  z=  -86.3
    5,10  gcd=5  phi|sig= -0.01249  z=  -77.1
    7,21  gcd=7  phi|sig= -0.00597  z=  -39.8
   10,15  gcd=5  phi|sig= -0.00494  z=  -32.4
    ...
     2,6  gcd=2  phi|sig= +0.15977  z= +900.6   <-- HUGE OUTLIER, see below
    mean(sharing)  = 0.00521  (n=13)
    mean(coprime)  = 0.00103  (n=53)   <- essentially zero, 49 of 53 tiny

So: coprime pairs are genuinely INDEPENDENT after conditioning (mean 0.001).
Pairs sharing a prime factor retain real dependence, mostly NEGATIVE, up to
|z| = 211. The sign varies with which prime is shared and how (2,10 vs 2,6).

**The 2 vs 6 outlier (phi|sig = +0.16, z=901)** needs explaining before this is
publishable. Note 6 = 2*3, so sqf(2)=2 and sqf(6)=6 share the factor 2, and
Q(sqrt2) subset Q(sqrt2,sqrt6) which also contains Q(sqrt3). Suspect: when
a = 2 and b = 6 = 2*3, Artin base 6 nearly implies conditions on base 2 via the
shared quadratic subfield, i.e. genuine Kummer-degree collapse over the
compositum. INVESTIGATE: compute [Q(zeta_l, a^{1/l}, b^{1/l}) : Q] degrees.

## Assessment

Publishable as a null-result-with-mechanism + the shared-factor residual law.
WEAKER than paper #2 (which has a theorem). Target: Integers, or an
experimental note — NOT Experimental Mathematics.
Lead with the DECOMPOSITION + CONTROL, not with "all 66 pairs correlate"
(that headline is a confounder and a referee will say so).

**Open items for #3:**
1. Explain the (2,6) outlier via Kummer degrees over the compositum. This is
   the one piece of real theory the paper needs.
2. Check whether the negative residuals scale with the shared prime (2 vs 5 vs 7).
3. Cherubini--Perucca / Jarviniemi--Perucca--Sgobba entanglement results become
   CENTRAL here (they were tangential in paper #1) — read before writing.

**Files:** crossbase.c, crossbase_om.c, crossbase_fine.c (+ binaries),
analyze_crossbase.py, analyze_om.py, analyze_fine.py, overfit_control.py,
cond_test.py, crossbase_fine_1e9.json, crossbase_om_1e9.json.
