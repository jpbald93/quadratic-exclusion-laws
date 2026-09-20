#!/bin/bash
# Rebuild the Paper 2 submission set from the CURRENT paper/multibase_exclusion.tex.
# Produces, in submission/:
#   multibase_exclusion_manuscript.pdf   named manuscript
#   multibase_exclusion_anonymous.pdf    anonymized (author/thanks/ORCID/email stripped, metadata cleared)
#   multibase_exclusion_source.zip       flat named LaTeX source + figure
#   multibase_exclusion_reproduction.zip portable package (excludes archives + correspondence)
# Usage:  bash code/build_submission.sh
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
SUB="$ROOT/submission"
TEX="$ROOT/paper/multibase_exclusion.tex"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== named manuscript"
cd "$ROOT/paper"
for i in 1 2 3; do pdflatex -interaction=nonstopmode multibase_exclusion.tex >/dev/null 2>&1; done
BOX=$(grep -cE '^(Overfull|Underfull)' multibase_exclusion.log || true)
UND=$(grep -ciE 'undefined|multiply.defined' multibase_exclusion.log || true)
PAGES=$(pdfinfo multibase_exclusion.pdf | awk '/^Pages/{print $2}')
echo "   pages=$PAGES badboxes=$BOX undefined=$UND"
[ "$BOX" = "0" ] || { echo "FAIL: overfull/underfull boxes"; exit 1; }
[ "$UND" = "0" ] || { echo "FAIL: undefined references"; exit 1; }
cp multibase_exclusion.pdf "$SUB/multibase_exclusion_manuscript.pdf"

echo "== anonymous manuscript"
cp "$TEX" "$WORK/anon.tex"
cp "$ROOT/paper/fig_delta_conductor.pdf" "$WORK/"
python3 - "$WORK/anon.tex" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p).read()
s = s.replace(r'\author{Josh Bald}', r'\author{}')
# drop the corresponding-author \thanks{...} block (balanced braces)
i = s.find(r'\thanks{')
if i != -1:
    j = i + len(r'\thanks{'); d = 1
    while d and j < len(s):
        if s[j] == '{': d += 1
        elif s[j] == '}': d -= 1
        j += 1
    s = s[:i] + s[j:]
# strip identifying strings anywhere else (e.g. acknowledgements, data availability)
s = s.replace('Josh Bald', 'the author')
# anonymise the self-citation: the bibliography prints "J.~Bald" and the
# discussion refers to the companion paper as the author's earlier work.
s = s.replace('J.~Bald,', '[Author],')
s = s.replace(r'the author in earlier\nwork~\cite{BaldConsecutive}',
              r'the present author in earlier work~\cite{BaldConsecutive}')
s = s.replace('jpbald93@gmail.com', 'email withheld for review')
s = s.replace('0009-0002-1317-6489', 'ORCID withheld for review')
s = re.sub(r'https?://github\.com/jpbald93/[^\s}{,)]*', 'repository URL withheld for review', s)
s = s.replace('jpbald93', 'withheld')
# suppress PDF metadata that hyperref would otherwise populate
s = s.replace(r'\begin{document}',
              '\\hypersetup{pdfauthor={},pdftitle={},pdfsubject={},pdfkeywords={},pdfcreator={}}\n\\begin{document}', 1)
open(p, 'w').write(s)
PY
cd "$WORK"
for i in 1 2 3; do pdflatex -interaction=nonstopmode anon.tex >/dev/null 2>&1; done
APAGES=$(pdfinfo anon.pdf | awk '/^Pages/{print $2}')
[ "$APAGES" = "$PAGES" ] || { echo "FAIL: anon page count $APAGES != $PAGES"; exit 1; }
# hard screen: no identifying string may survive in the extracted text or metadata
pdftotext -layout anon.pdf anon.txt
if grep -qiE 'josh|bald|jpbald93|0009-0002-1317-6489|github\.com/jpbald93' anon.txt; then
  echo "FAIL: identifying text in anonymous PDF"; grep -niE 'josh|bald|jpbald93' anon.txt | head; exit 1
fi
pdfinfo anon.pdf > anon_meta.txt
if grep -iE '^(Author|Title|Subject|Keywords)' anon_meta.txt | grep -qiE 'josh|bald|primitive|artin'; then
  echo "FAIL: identifying metadata in anonymous PDF"; exit 1
fi
cp anon.pdf "$SUB/multibase_exclusion_anonymous.pdf"
cp anon_meta.txt "$ROOT/results/anonymous_pdf_metadata.txt"
echo "   pages=$APAGES, no identifying text or metadata"

echo "== named source zip"
rm -f "$SUB/multibase_exclusion_source.zip"
cd "$ROOT/paper"
zip -q -X "$SUB/multibase_exclusion_source.zip" multibase_exclusion.tex fig_delta_conductor.pdf

echo "== reproduction zip"
REPRO="$WORK/repro"
mkdir -p "$REPRO"/{code,paper,results,submission,lean/Artin}
cp "$ROOT"/code/*.py "$ROOT"/code/*.c "$ROOT"/code/*.sh "$REPRO/code/"
cp "$ROOT"/paper/multibase_exclusion.{tex,pdf} "$ROOT"/paper/fig_delta_conductor.{pdf,png} "$ROOT"/paper/make_figs.py "$REPRO/paper/"
cp "$ROOT"/results/* "$REPRO/results/" 2>/dev/null || true
cp "$SUB/multibase_exclusion_anonymous.pdf" "$SUB/multibase_exclusion_source.zip" "$SUB/SUBMISSION_CHECKLIST.md" "$REPRO/submission/"
cp "$ROOT"/lean/Artin/*.lean "$REPRO/lean/Artin/"
cp "$ROOT"/lean/{Artin.lean,gate.sh,BUILD.md,README_LEAN.md,lakefile.toml,lean-toolchain,lake-manifest.json} "$REPRO/lean/"
cp "$ROOT"/{README.md,LICENSE,START_HERE.md,FINAL_STATUS.md,CHANGELOG.md} "$REPRO/" 2>/dev/null || true
# NOTE: archives/ and the private endorsement draft are deliberately excluded.
cd "$REPRO"
find . -type f ! -name MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
rm -f "$SUB/multibase_exclusion_reproduction.zip"
zip -qr -X "$SUB/multibase_exclusion_reproduction.zip" .
if unzip -l "$SUB/multibase_exclusion_reproduction.zip" | grep -qiE 'endorsement|archive/'; then
  echo "FAIL: reproduction zip contains excluded material"; exit 1
fi

echo "== done"
cd "$SUB" && ls -la *.pdf *.zip
