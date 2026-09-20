# Quadratic exclusion laws for consecutive Artin primes in arbitrary bases

Reproduction package for the paper of the same name.

Call an odd prime $p$ **Artin base $a$** if $a$ is a primitive root modulo $p$.
Being Artin base $a$ forces the quadratic character value $\chi_a(p) = -1$, and
$\chi_a$ has conductor $f$, so this necessary condition depends only on
$p \bmod f$. The paper determines, for **every** non-square base $a$, the exact
set of gap classes on which that quadratic obstruction forbids two primes from
both being Artin base $a$.

Two mechanisms produce such **exclusion classes**:

- **Reversal** — $\chi_a(q) = -\chi_a(p)$ for all admissible $p,\ q = p+g$, so
  one of the pair is a quadratic residue base $a$. These classes are
  classified completely, via the factorisation of the discriminant of
  $\mathbb{Q}(\sqrt{a})$ into prime discriminants.
- **Inadmissibility** — operates when no reversing class exists. Its analysis
  rests on the counting identity $4N_{--}(g) = T(g) - A(g) - B(g) + S(g)$,
  proved for every modulus, prime or composite.

The resulting **complete dichotomy**: base $a$ admits a quadratic exclusion
class if and only if $d$ is even, $d \equiv 3 \pmod 4$, $3 \mid d$, or $d = 5$
(where $d$ is the squarefree part of $a$).

An important caveat the paper makes throughout: the quadratic obstruction is
**necessary but not sufficient** for Artin status. An exclusion class is a
proof of impossibility; the *absence* of one is not a proof of possibility.

## Layout

```
paper/     manuscript (LaTeX source + PDF) and the figure
code/      the multi-base census program and the verification scripts
results/   contingency tables, summaries, logs, audit records
lean/      Lean 4 development with its axiom-dependency gate
```

## Reproducing every claim

One entry point regenerates every headline claim from the primary contingency
data and **exits non-zero on any mismatch**:

```bash
python3 code/regenerate_all.py
```

It checks the dichotomy over all 72 non-square bases $a \le 80$, the
exhaustion proposition, the 14,803-case identity check, the prime-conductor
evaluation in both cases, the twin-prime counts, and the correlations, scaled
products and incidence totals of the verification and correlation sections.
Expected final line:

```
PASS — every checked manuscript claim reproduced.
```

## Regenerating the census from scratch

`regenerate_all.py` recomputes the claims *from* the contingency data. To
rebuild that data from the primes themselves:

```bash
gcc -O3 -march=native -o multibase_delta code/multibase_delta.c -lm
./multibase_delta 1000000000 > results/multibase_1e9.json
```

Modular exponentiation is done in 128-bit arithmetic, and the factorisation of
$p-1$ is shared across all eleven bases, which is what makes the run cheap.
The program writes no intermediate table: it accumulates the $2\times2$
contingency counts directly, globally and per gap $g \le 300$.

This census has been independently recomputed on separate hardware and agrees
byte-for-byte; see `results/AUDIT_jack_multibase.md`. That closes the chain
`primes → multibase_delta.c → JSON → regenerate_all.py → claims`, which
`regenerate_all.py` alone does not (it trusts the JSON).

## Lean 4 development

```bash
cd lean
lake exe cache get    # mathlib binary cache — do this FIRST
./gate.sh             # => PASS (14 theorems, standard axioms only)
```

Fetch the cache before building. Without it `lake` compiles Mathlib from
source, which costs hours and tens of gigabytes.

The Lean development plays a specific and slightly unusual role here: it was
used to **refute two claims of an earlier version of this paper**, and then to
prove the corrected replacement.

| file | contents |
|---|---|
| `Artin/Paper2.lean` | machine-checked refutation of the superseded gap-2 twin-prime claim (5 and 7 are twin primes and 3 is a primitive root of **both**), and of the superseded counting formula |
| `Artin/Paper2Rebuild.lean` | the corrected counting identity |

`gate.sh` requires three things: no `sorry`, `admit`, `axiom` or
`native_decide` in the sources; a successful build **by exit status**, not by
matching a success string; and every audited declaration depending only on
Lean's three standard axioms — `propext`, `Classical.choice`, `Quot.sound`.
The expected number of `#print axioms` reports is pinned, so deleting an audit
line fails the gate instead of passing vacuously.

## A note on the superseded scripts

Earlier versions of this work implemented a reversal-only classification, and
the scripts for it scanned only even least residues — which misses the
odd-residue classes of odd conductors. Those scripts are **not** included in
this repository. They are retained as historical artifacts in the author's
combined repository, marked as superseded. The reproduction route here is
`regenerate_all.py` and nothing else.

## Licence

The manuscript, figures and prose are under **CC BY 4.0**
(`LICENSE-CC-BY-4.0.txt`). The code and Lean development are under the **MIT
Licence** (`LICENSE`).

## Status

Preprint; not peer reviewed, not yet submitted to a journal.
