# Paper 2 submission set — Quadratic exclusion laws for consecutive Artin primes in arbitrary bases

Built from the current `paper/multibase_exclusion.tex` by
`code/build_submission.sh`, which aborts if any gate below fails.

## Artifacts

| file | what it is |
|---|---|
| `multibase_exclusion_manuscript.pdf` | named manuscript, 22 pp |
| `multibase_exclusion_anonymous.pdf` | anonymised (author, email, ORCID, repo URL stripped; PDF metadata cleared) |
| `multibase_exclusion_source.zip` | flat named LaTeX source + figure, compiles standalone |
| `multibase_exclusion_reproduction.zip` | portable package: code, paper, results, Lean sources |

## Gates that passed at build time

- Manuscript build: **22 pp, 0 overfull/underfull boxes, 0 undefined references**.
- Anonymous PDF: **no identifying text**, and Author/Title/Subject/Keywords/Creator
  metadata fields empty.
- Source zip compiles standalone.
- Reproduction zip excludes archives and private correspondence.

## Independent verification behind this manuscript

Five independent audit rounds, each run on a different model from the one that
drafted the text; the fifth (2026-09-20, a different vendor) is at
`audit_2026-09-20/AUDIT_astra_noncomputational.md` and returned MAJOR REVISION.
It found the prior art above, and a false assertion inside the exhaustion
proposition: item (2) claimed the conductor-8 components are never free, while
the same proof's final paragraph used their freeness at g = 2, 6 (mod 8). The
final paragraph is correct and item (2) has been restated. Both were verified
independently before the fixes were applied, each gated on producing a located, quoted, scope-declared
report. Reports are in `reaudit/` (`REPORT_DATA.md`, `REPORT_MATH.md`,
`REPORT_CONFIRM.md`, `REPORT_REFEREE.md`). Roughly 40 corrections were applied;
`rebuild/REWRITE_DONE.md` records each one and why.

Reproduce every headline claim from the primary contingency data:

```bash
cd code && python3 regenerate_all.py     # exits non-zero on any mismatch
```

Execute every delivered artifact end to end:

```bash
cd code && ./artifact_gate.sh            # => ARTIFACT GATE: PASS
```

## Machine verification — exact scope

The Lean 4 development covers the **counting identity in full generality**, and
the **prime-conductor count for `d = 5` and `d = 13` only**. `gate.sh` reports
`PASS (34 theorems, standard axioms only)` and rejects `sorry` and
`native_decide`.

**Not** formalised: the general-`d` count, the composite dichotomy
(Corollary 20), the exhaustion proposition (Proposition 21), the reversing
classification, and everything empirical. Section 4 of the paper states this;
do not describe the paper as "verified by Lean" without this qualification.

## What is NOT claimed

- No journal acceptance, and no referee outside this audit chain has seen it.
- **No priority is claimed for the classification of forbidden gap classes.**
  Tinkova, Waxman and Zindulka, *Artin twin primes*, J. Number Theory 247
  (2023), 274-304, obtained the same conditions in the fixed-shift setting.
  Their Theorem 1.1 and this classification were checked to agree on all 72
  non-square bases a <= 80, the exceptional squarefree part d = 5 included.
  Section "Relation to Tinkova-Waxman-Zindulka" states the overlap and what
  this paper adds: the converse direction as a theorem rather than a
  conjecture, a derivation from one counting identity, coverage of perfect-power
  bases their hypothesis omits, Lean verification, and the consecutive-pair
  cross-base correlation.
- The classified obstruction is **quadratic**: an exclusion class proves
  impossibility; the absence of one proves nothing.
- The conductor/correlation association is a **descriptive comparison** among
  the quantities examined, over eleven bases at one bound. No mechanism is
  established and no exponent of `f` is identified.
- The `z` values are effect-to-scale ratios against a reference model known to
  be false here (overlapping pairs, deterministic census), not hypothesis tests.
- The 10^9 runtime is a reported observation, not a timed portable benchmark.

## Before submitting

1. **Venue.** INTEGERS is ineligible under its AI-content policy. Experimental
   Mathematics is the intended target; confirm its current AI-disclosure rules
   still permit the disclosure in Section 8 as written.
2. **Author decision required** on whether to submit at all — this set is built
   and gated, not sent.
3. `endorsement_email_pollack.md` in Paper 1's `submission/` is **not** to be
   sent as written; see `review_2026-09-10/REPORT_C.md` `## Publication strategy`.
4. Consider minting a Zenodo DOI for the Lean development and citing it in Data
   Availability (requires the author's login/ORCID).
