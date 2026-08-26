#!/usr/bin/env bash
# compile-check.sh — the publication compile gate.
#
# Compiles the library self-test and every template example into
# project/publication/build/ (disposable output). Any warning or error is a
# gate failure: warnings here are almost always missing fonts or unresolved
# imports, both of which change how an issued PDF looks.
#
# This does NOT issue anything. Compilation is not approval.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TYPST_DIR="$ROOT/project/publication/typst"
BUILD_DIR="$ROOT/project/publication/build"

command -v typst >/dev/null 2>&1 || {
  echo "BLOCKED: typst not installed. Sources are generated but unverified."
  echo "         Install: brew install typst"
  exit 3
}

mkdir -p "$BUILD_DIR"
echo "typst $(typst --version | awk '{print $2}')  root=$ROOT"
echo

pass=0; fail=0
while IFS= read -r src; do
  rel="${src#"$TYPST_DIR"/}"
  out="$BUILD_DIR/$(basename "${rel%.typ}").pdf"
  log=$(typst compile "$src" "$out" --root "$ROOT" 2>&1)
  if [[ -n "$log" ]]; then
    printf 'FAIL  %s\n' "$rel"
    printf '%s\n' "$log" | sed 's/^/      /'
    fail=$((fail + 1))
  else
    printf 'ok    %-42s -> build/%s\n' "$rel" "$(basename "$out")"
    pass=$((pass + 1))
  fi
done < <(find "$TYPST_DIR" -name '*.typ' \
           -not -path '*/lib/*' -not -path '*/templates/*' | sort)

echo
echo "compiled: $pass   failed: $fail"
[[ $fail -eq 0 ]] || exit 1
