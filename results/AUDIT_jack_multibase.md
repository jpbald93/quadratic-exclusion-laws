# jack audit: `multibase_delta.c` at 10⁹ — 2026-09-11

## Verdict: PASS — output byte-identical to the shipped `multibase_1e9.json`

This is the 11-base census the entire 20-page manuscript rests on, and it had
never been independently recomputed. The referee named reproducibility as the
item blocking a minor-revision recommendation.

## Method

Source fetched **from the public repository**, not from this workspace — so
this tests the reproduction route a referee would actually take:

```
git clone --depth 1 https://github.com/jpbald93/consecutive-artin.git
# HEAD: 5ccd9b2
multibase/code/multibase_delta.c   sha256 103db30b432ed9936a38cae1270bbf968d9c3c01d29e6e02e8ca682d127d66c7
```

That hash matches the local `code/multibase_delta.c` exactly, so the public
artifact and the working copy are the same program.

Compiled `gcc -O3 -march=native` on jack (AMD Ryzen AI MAX+ 395, 32 cores,
gcc 15.2.0) — a different compiler and architecture from the original run —
and executed at limit 10⁹.

## Result

```
jack     md5 54e1339ddbe6c23bbb7c7e1abdf06c55   mb_jack.json
shipped  md5 54e1339ddbe6c23bbb7c7e1abdf06c55   results/multibase_1e9.json
```

**Byte-identical.** Reported `primes=50,847,532`, `pairs=50,847,531`,
matching the shipped file.

Since every contingency table in the manuscript — Table 2 (verification),
Table 5 (δ by base), the conductor correlations, the exclusion-class
incidence totals — is derived from this single JSON, reproducing it bit-for-bit
independently re-establishes the empirical basis of the whole paper.

Note this is stronger than re-running `regenerate_all.py`, which recomputes
*claims from the JSON*. This recomputes *the JSON from the primes*, so the two
checks together now cover the full chain:

```
primes --[multibase_delta.c]--> multibase_1e9.json --[regenerate_all.py]--> manuscript claims
   ^ verified here (byte-identical)        ^ verified by artifact_gate.sh (PASS)
```

## Provenance

- jack: AMD Ryzen AI MAX+ 395, 32 cores, Ubuntu, gcc 15.2.0
- `/tmp/p23_audit/mb_jack.json`
- Run concurrently with the two Paper 3 audits; ~2.5 minutes wall-clock.

Deterministic integer tallies: a correct re-run is byte-identical, and
anything else would have been a finding rather than rounding.
