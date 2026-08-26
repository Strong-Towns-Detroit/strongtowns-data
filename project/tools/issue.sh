#!/usr/bin/env bash
# issue.sh — produce a formally issued PDF and its manifest.
#
#   ./issue.sh <artifact-id> <issue-id> <revision> <source.typ> "<purpose>" <approver-role> [source.md]
#
# This mechanises the RECORDING half of the issue gate (GOV-002 §5): hashes,
# compiler version, compile command, producer commit. It does NOT and cannot
# decide that the document is correct. A human must still open the PDF and read
# it -- Typst renders a missing value or an overflowing table without complaint.
set -euo pipefail

[[ $# -ge 6 ]] || { sed -n '3,5p' "$0" >&2; exit 2; }
AID="$1"; ISS="$2"; REV="$3"; SRC="$4"; PURPOSE="$5"; APPROVER="$6"; MD="${7:-}"

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

command -v typst >/dev/null || { echo "BLOCKED: typst not installed; cannot issue." >&2; exit 3; }
[[ -f "$SRC" ]] || { echo "error: no such Typst source: $SRC" >&2; exit 2; }

# An issue records the commit that produced it. That is meaningless if the tree
# has uncommitted changes.
if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree is dirty. Commit before issuing -- the manifest" >&2
  echo "       records producer_git_commit, which must reproduce this PDF." >&2
  exit 1
fi

OUTDIR="project/publication/issued/$AID/$ISS"
PDF="$OUTDIR/$AID-$ISS-$REV.pdf"
MAN="$OUTDIR/manifest.json"
[[ -e "$PDF" ]] && { echo "error: $PDF exists. Issues are never regenerated in place." >&2; exit 1; }
mkdir -p "$OUTDIR"

CMD="typst compile $SRC $PDF --root $ROOT"
echo "compiling: $CMD"
LOG=$($CMD 2>&1) || { echo "$LOG" >&2; exit 1; }
[[ -z "$LOG" ]] || { echo "error: compiled with warnings; refusing to issue." >&2
                     echo "$LOG" >&2; rm -f "$PDF"; exit 1; }

sha() { shasum -a 256 "$1" | awk '{print $1}'; }
python3 - "$AID" "$ISS" "$REV" "$SRC" "$(sha "$SRC")" "$PURPOSE" "$APPROVER" \
           "$MD" "$PDF" "$(sha "$PDF")" "$(typst --version | awk '{print $2}')" \
           "$(git rev-parse --short HEAD)" "$CMD" "$MAN" <<'PY'
import json, sys, datetime, hashlib, os
(aid, iss, rev, src, srcsha, purpose, approver, md, pdf, pdfsha,
 tv, commit, cmd, man) = sys.argv[1:15]
m = {
  "artifact_id": aid, "issue_id": iss, "revision": rev, "issue_purpose": purpose,
  "typst_source": src, "typst_source_sha256": srcsha,
  "source_markdown": md or None,
  "source_markdown_sha256": (hashlib.sha256(open(md,'rb').read()).hexdigest()
                             if md and os.path.exists(md) else None),
  "supporting_data": [],
  "typst_version": tv, "compile_command": cmd, "producer_git_commit": commit,
  "issued_at": datetime.date.today().isoformat(),
  "approver_role": approver, "approver_name": None,
  "visual_inspection_by": None,
  "pdf_path": pdf, "pdf_sha256": pdfsha,
  "supersedes_issue_id": None, "confidentiality": "internal",
}
json.dump(m, open(man, "w"), indent=2)
open(man, "a").write("\n")
PY

echo "issued: $PDF"
echo "manifest: $MAN"
cat <<'EOT'

NOT YET COMPLETE. Before this counts as issued:
  - open the PDF and read it end to end;
  - set visual_inspection_by in the manifest;
  - list supporting_data with hashes for any data the document cites;
  - set supersedes_issue_id and mark the prior issue superseded, if applicable;
  - set status: issued and latest_issue_id in the Markdown draft's frontmatter;
  - confirm the required review is recorded in GOV-015;
  - run: python3 project/tools/validate.py
EOT
