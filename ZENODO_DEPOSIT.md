# Zenodo deposit — Paper 2

Paste-ready. Files to upload are listed at the bottom.

**Deposit Paper 1 first.** This paper cites it as `BaldConsecutive` with a bare
GitHub URL; once Paper 1 has a DOI, replace that URL and rebuild before
depositing this one.

---

## Resource type

**Publication → Preprint**

## Title

```
Quadratic exclusion laws for consecutive Artin primes in arbitrary bases
```

## Authors

```
Bald, Josh
ORCID: 0009-0002-1317-6489
```

No affiliation — leave blank rather than inventing one.

## Description

Paste the manuscript abstract. Two things are worth adding after it, because a
reader cannot see either from the abstract alone and both are to your credit:

> The classification of forbidden gap classes given here was obtained
> independently, but is not new: Tinková, Waxman and Zindulka (*Artin twin
> primes*, J. Number Theory 247 (2023), 274–304) reached the same conditions
> in the fixed-shift setting. The two were checked to agree on all 72
> non-square bases a ≤ 80. What this paper adds is the converse direction as a
> theorem rather than a conjecture, a derivation from a single counting
> identity valid for every modulus, coverage of the perfect-power bases their
> hypothesis omits, machine verification in Lean 4, and a cross-base
> measurement of the consecutive-pair Artin correlation.
>
> The census has been independently recomputed on separate hardware and agrees
> byte-for-byte. A single entry point, `code/regenerate_all.py`, reproduces
> every headline claim and exits non-zero on any mismatch.

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)**

Manuscript CC BY 4.0; code and Lean stay MIT. Both files are in the package
and `LICENSE-CC-BY-4.0.txt` states the split. Do not select MIT as the record
licence — it is a software licence and the wrong instrument for a paper.

## Keywords

```
Artin's conjecture
primitive roots
consecutive primes
quadratic characters
prime discriminants
exclusion laws
Kronecker symbol
Lemke Oliver–Soundararajan bias
experimental number theory
Lean 4
formal verification
```

## Related identifiers

- `https://github.com/jpbald93/quadratic-exclusion-laws` — **is supplemented by**
- Paper 1's DOI once minted — **is continued by** (or **cites**)
- Leave the arXiv field empty until a posting exists.

## Subjects

Mathematics → Number Theory. MSC 2020: Primary 11A07; Secondary 11N05, 11N13,
11Y16, 11Y60.

## Version / date

`v1.0`, today's date. Do not backdate.

---

## Files to upload

| file | what it is |
|---|---|
| `submission/multibase_exclusion_manuscript.pdf` | the paper, 23 pp, named |
| `submission/multibase_exclusion_source.zip` | LaTeX source + figure |
| `submission/multibase_exclusion_reproduction.zip` | code, results, Lean |
| `LICENSE-CC-BY-4.0.txt` | licence split |

### Do NOT upload

- `submission/multibase_exclusion_anonymous.pdf` — blinded copy is for journal
  peer review; a Zenodo deposit is attributed.
- `backups/`, `archive/`, `rebuild/` — working material and superseded drafts.
- `audit_2026-09-20/` and `reaudit/` — optional. Honest and reflect well, but
  they are internal review correspondence; include only if you want the review
  history public.

Verified: neither zip contains private correspondence.

---

## State at time of writing

- 23 pp, 0 overfull/underfull boxes, 0 undefined references
- `MANIFEST.sha256` 58/58 verify
- `code/artifact_gate.sh` → **ARTIFACT GATE: PASS**
- `code/regenerate_all.py` → **PASS (20 checks)**
- Lean `gate.sh` → **PASS (34 theorems, standard axioms only)**
- anonymous PDF → 0 identifying strings
- every bibliography entry cited; no orphans
