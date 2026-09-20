#!/bin/bash
# artifact_gate.sh — the gate that WOULD have caught findings F2 and F3.
#
# Lesson learned the hard way: across three audit rounds every check was run
# against the PDF TEXT, and none against the delivered CODE. The result was a
# figure script that crashed with KeyError on the public repository, and four
# "verification" scripts that scanned the wrong gap-class domain. Both had been
# broken for rounds; text screening cannot see either.
#
# Rule: a claim in the Data Availability section is a claim like any other and
# must be executed, not merely read.
#
# Run from this directory:  ./artifact_gate.sh
# Exits non-zero on any failure.

set -u
cd "$(dirname "$0")" || exit 1
fail=0
note() { printf '  [%s] %s\n' "$1" "$2"; }

echo "artifact_gate.sh — executing every delivered artifact"
echo "======================================================"

# 1. The single regeneration entry point must run and self-check.
echo
echo "1. code/regenerate_all.py"
if out=$(timeout 1800 python3 regenerate_all.py 2>&1); then
  note ok "PASS ($(echo "$out" | grep -c '\[ok \]') checks)"
else
  note FAIL "regenerate_all.py exited non-zero"
  echo "$out" | tail -20
  fail=1
fi

# 2. The figure script must actually produce the figure.
echo
echo "2. paper/make_figs.py"
if out=$(cd ../paper && timeout 600 python3 make_figs.py 2>&1); then
  note ok "$out"
  [ -f ../paper/fig_delta_conductor.pdf ] || { note FAIL "no PDF produced"; fail=1; }
else
  note FAIL "make_figs.py crashed"
  echo "$out" | tail -12
  fail=1
fi

# 3. Every .py must either execute-parse or be marked SUPERSEDED.
echo
echo "3. all delivered Python scripts"
for f in *.py; do
  if grep -q SUPERSEDED "$f"; then
    note ok "$f (marked historical)"
  elif python3 -c "import ast;ast.parse(open('$f').read())" 2>/dev/null; then
    note ok "$f (parses)"
  else
    note FAIL "$f does not parse and is not marked superseded"; fail=1
  fi
done

# 4. The manuscript must build clean.
echo
echo "4. LaTeX build"
if (cd ../paper && for i in 1 2 3; do
      pdflatex -interaction=nonstopmode multibase_exclusion.tex >/dev/null 2>&1
    done); then
  log=../paper/multibase_exclusion.log
  bad=$(grep -cE '^(Overfull|Underfull)' "$log" 2>/dev/null | head -1 | tr -dc '0-9'); bad=${bad:-0}
  und=$(grep -ci undefined "$log" 2>/dev/null | head -1 | tr -dc '0-9'); und=${und:-0}
  pp=$(pdfinfo ../paper/multibase_exclusion.pdf 2>/dev/null | awk '/Pages/{print $2}')
  note "$([ "$bad" -eq 0 ] && [ "$und" -eq 0 ] && echo ok || echo FAIL)" \
       "$pp pp, $bad bad boxes, $und undefined refs"
  { [ "$bad" -eq 0 ] && [ "$und" -eq 0 ]; } || fail=1
else
  note FAIL "pdflatex failed"; fail=1
fi

# 5. The Lean gate, if a build tree is reachable.
echo
echo "5. Lean development"
# NEVER run `lake build` inside the shipped source-only copy: with no .lake it
# rebuilds Mathlib from scratch, which needs ~8 GB and once filled this disk.
# Verify the sources are byte-identical to the upstream tree that passed instead.
UP=${ARTIN_LEAN_DIR:-$HOME/Projects/artin-lean/artin}
LEANDIR=""
for cand in ../lean ../../lean; do
  if [ -x "$cand/gate.sh" ]; then LEANDIR="$cand"; break; fi
done
if [ -z "$LEANDIR" ]; then
  note skip "no lean/gate.sh at ../lean or ../../lean (layout differs)"
elif [ -d "$UP/.lake" ]; then
  same=1
  for f in Artin.lean gate.sh lakefile.toml lean-toolchain Artin/Exclusion.lean \
           Artin/Bridge.lean Artin/Check.lean Artin/Paper2.lean \
           Artin/Paper2Rebuild.lean Artin/TripleExclusion.lean; do
    if [ -f "$LEANDIR/$f" ] && [ -f "$UP/$f" ]; then
      a=$(sha256sum "$LEANDIR/$f" | cut -d" " -f1)
      b=$(sha256sum "$UP/$f"     | cut -d" " -f1)
      [ "$a" = "$b" ] || { note FAIL "lean/$f differs from upstream"; same=0; fail=1; }
    else
      note FAIL "lean/$f missing"; same=0; fail=1
    fi
  done
  [ "$same" -eq 1 ] && note ok "10 Lean sources byte-identical to the upstream tree"
  out=$(cd "$UP" && timeout 1800 ./gate.sh 2>&1)
  note "$(echo "$out" | grep -q PASS && echo ok || echo FAIL)" "upstream gate: $out"
  echo "$out" | grep -q PASS || fail=1
else
  note skip "no upstream Lean build tree; set ARTIN_LEAN_DIR to verify (see lean/BUILD.md)"
fi

# 6. No stale duplicate manuscripts, and no retracted claim in a live doc.
#    Added after a verification pass found an 18-page duplicate of the paper at
#    the top of multibase/ (never updated by three fix rounds, still carrying
#    retracted claims) and a README describing the superseded classification.
#    The gate above could not see either: it only runs code.
echo
echo "6. stale-artifact sweep"
pdfs=$(find .. -name 'multibase_exclusion.pdf' -not -path '*/archive/*' | wc -l | tr -dc '0-9')
if [ "${pdfs:-0}" -gt 1 ]; then
  note FAIL "$pdfs copies of multibase_exclusion.pdf outside archive/ (expect 1)"
  find .. -name 'multibase_exclusion.pdf' -not -path '*/archive/*' | sed 's|^|        |'
  fail=1
else
  note ok "single manuscript copy outside archive/"
fi
# Retracted strings that must never appear in a LIVE doc. Audit reports and
# changelogs legitimately quote them, so those paths are excluded.
bad_live=0
for pat in '63,105,745' 'know of no base' 'two central theorems' 'not in Mathlib'; do
  hits=$(grep -rl --include='*.md' -- "$pat" .. 2>/dev/null \
         | grep -v -e '/reaudit/' -e '/rebuild/' -e '/archive/' || true)
  if [ -n "$hits" ]; then
    note FAIL "retracted claim '$pat' in live doc: $(echo "$hits" | tr '\n' ' ')"
    bad_live=1; fail=1
  fi
done
[ "$bad_live" -eq 0 ] && note ok "no retracted claims in live docs"
# The Lean theorem count quoted in docs must match what the gate reports.
if [ -d "${ARTIN_LEAN_DIR:-$HOME/Projects/artin-lean/artin}/.lake" ]; then
  n=$(cd "${ARTIN_LEAN_DIR:-$HOME/Projects/artin-lean/artin}" && ./gate.sh 2>&1 \
      | grep -o '[0-9]\+ theorems' | grep -o '[0-9]\+')
  wrong=$(grep -rl 'theorems, standard axioms' .. --include=*.md 2>/dev/null \
          | xargs grep -l 'PASS (' 2>/dev/null \
          | xargs grep -L "$n theorems" 2>/dev/null | grep -v -e '/reaudit/' -e '/archive/' || true)
  if [ -n "$wrong" ]; then
    note FAIL "docs quote a theorem count != $n: $(echo "$wrong" | tr '\n' ' ')"; fail=1
  else
    note ok "quoted Lean theorem count matches gate ($n)"
  fi
fi

echo
echo "======================================================"
if [ "$fail" -eq 0 ]; then
  echo "ARTIFACT GATE: PASS"
else
  echo "ARTIFACT GATE: FAIL"
fi
exit "$fail"
