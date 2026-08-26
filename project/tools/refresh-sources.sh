#!/usr/bin/env bash
# refresh-sources.sh -- drift detection for qualitative sources.
#
# Re-downloads every source that has an archived capture and compares the hash
# against source-register.csv. A changed hash means the agency republished the
# document: the requirement may have changed, and every artifact citing it is
# now suspect.
#
# This does NOT update the register. It tells you what to go re-read.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
changed=0; checked=0; unreachable=0

python3 - "$ROOT" <<'PY' | while IFS=$'\t' read -r sid url cap want; do
import csv, sys
for r in csv.DictReader(open(sys.argv[1] + "/source-register.csv")):
    if r["capture_path"] and r["capture_sha256"]:
        print("\t".join([r["source_id"], r["url"], r["capture_path"], r["capture_sha256"]]))
PY
  checked=$((checked+1))
  out="$TMP/$sid"
  if ! curl -fsSL --max-time 60 -o "$out" "$url"; then
    printf 'UNREACHABLE  %s  %s\n' "$sid" "$url"; unreachable=$((unreachable+1)); continue
  fi
  got=$(shasum -a 256 "$out" | awk '{print $1}')
  if [[ "$got" == "$want" ]]; then
    printf 'unchanged    %s\n' "$sid"
  else
    printf 'CHANGED      %s\n  registered %s\n  live       %s\n  re-read: %s\n' \
      "$sid" "$want" "$got" "$url"
    changed=$((changed+1))
  fi
done

cat <<'EOT'

A CHANGED hash is not a failure -- it is a signal. Re-read the document, update
the pinpoint citations and retrieved_at, re-archive the capture, and re-check
every artifact listed in that row's supports_artifact_ids.
EOT
