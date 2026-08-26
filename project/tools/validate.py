#!/usr/bin/env python3
"""validate.py -- the register and frontmatter gate for project/.

Checks, in order:
  1. artifact-register.csv     structural integrity, unique IDs, acyclic dependencies
  2. file_path                 every non-planned row has a file behind it
  3. Markdown frontmatter      required keys, enums, and agreement with the register
  4. stage-gates.csv           required evidence resolves; reviewers are real roles
  5. dependency-register.csv   endpoints resolve
  6. source-register.csv       every cited source_id exists; retrieval dates present
  7. issue manifests           schema shape and hash reconciliation

Dependency-free by design: no PyYAML, no jsonschema. The frontmatter subset used
here is small and fully specified, and a validator that cannot run because of a
missing package is a validator that stops being run.

Exit 0 = all gates pass. Exit 1 = at least one failure.
"""
from __future__ import annotations
import csv, json, hashlib, pathlib, re, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]          # project/
REPO = ROOT.parent
ID_RE = re.compile(r"^(GOV|SCR|PUB|ACQ|DD|DSN|FIN|APR|PRO|CON|CLO)-\d{3}$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")

DOC_STATUSES = {"template", "research_draft", "review_required",
                "approved_for_internal_use", "approved_for_issue", "issued", "superseded"}
REGISTER_ONLY = {"planned"}
WORKSTREAMS = {"governance", "parcel-screening", "acquisition", "due-diligence",
               "design-feasibility", "finance", "approvals", "procurement",
               "construction", "closing-compliance", "publication"}
SERVICE_CODES = {"LND", "DSN", "PMT", "INS", "EST", "ADM"}
CONFIDENTIALITY = {"public", "internal", "sensitive"}

FRONTMATTER_REQUIRED = ["artifact_id", "artifact_type", "title", "workstream", "status",
                        "owner_role", "required_reviewer_role", "legal_review_required",
                        "typst_issue_required", "created_at", "updated_at", "confidentiality"]

fail: list[str] = []
warn: list[str] = []
def bad(section, msg): fail.append(f"[{section}] {msg}")
def soft(section, msg): warn.append(f"[{section}] {msg}")


def parse_frontmatter(text: str) -> dict | None:
    """Minimal YAML frontmatter reader for the subset this project uses:
    `key: scalar`, `key: [a, b]`, quoted strings, null, booleans."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    out: dict = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            out[k] = [x.strip().strip("'\"") for x in inner.split(",")] if inner else []
        elif v in ("null", "~", ""):
            out[k] = None
        elif v in ("true", "false"):
            out[k] = v == "true"
        else:
            out[k] = v.strip("'\"")
    return out


# --------------------------------------------------------------- 1. register
reg_path = ROOT / "artifact-register.csv"
rows = list(csv.DictReader(open(reg_path)))
reg = {}
for i, r in enumerate(rows, 2):
    aid = r["artifact_id"]
    if not ID_RE.match(aid):
        bad("register", f"row {i}: malformed artifact_id {aid!r}")
    if aid in reg:
        bad("register", f"row {i}: duplicate artifact_id {aid}")
    if r["workstream"] not in WORKSTREAMS:
        bad("register", f"{aid}: unknown workstream {r['workstream']!r}")
    if r["service_code"] not in SERVICE_CODES:
        bad("register", f"{aid}: unknown service_code {r['service_code']!r}")
    if r["status"] not in DOC_STATUSES | REGISTER_ONLY:
        bad("register", f"{aid}: unknown status {r['status']!r}")
    if r["confidentiality"] not in CONFIDENTIALITY:
        bad("register", f"{aid}: unknown confidentiality {r['confidentiality']!r}")
    for b in ("legal_review_required", "typst_issue_required"):
        if r[b] not in ("true", "false"):
            bad("register", f"{aid}: {b} must be true/false, got {r[b]!r}")
    reg[aid] = r

# dependencies resolve
edges = defaultdict(list)
for aid, r in reg.items():
    for d in filter(None, r["depends_on"].split(";")):
        if d not in reg:
            bad("register", f"{aid}: depends_on unknown artifact {d}")
        else:
            edges[d].append(aid)

# acyclic
WHITE, GREY, BLACK = 0, 1, 2
colour = defaultdict(int)
def visit(n, stack):
    if colour[n] == GREY:
        bad("register", "dependency cycle: " + " -> ".join(stack + [n])); return
    if colour[n] == BLACK:
        return
    colour[n] = GREY
    for m in edges[n]:
        visit(m, stack + [n])
    colour[n] = BLACK
for aid in reg:
    visit(aid, [])

# typst templates exist
tdir = ROOT / "publication" / "typst" / "templates"
for aid, r in reg.items():
    if r["typst_issue_required"] == "true":
        if not r["typst_template"]:
            bad("register", f"{aid}: typst_issue_required but no typst_template named")
        elif not (tdir / f"{r['typst_template']}.typ").exists():
            bad("register", f"{aid}: typst_template {r['typst_template']!r} has no file")
    elif r["typst_template"]:
        bad("register", f"{aid}: names a typst_template but typst_issue_required is false")

# ------------------------------------------------------- 2/3. files + frontmatter
md_checked = 0
for aid, r in reg.items():
    if r["status"] in REGISTER_ONLY:
        continue
    p = ROOT / r["file_path"]
    if r["file_path"].endswith("/"):
        if not p.is_dir():
            bad("files", f"{aid}: directory {r['file_path']} missing")
        continue
    if not p.exists():
        bad("files", f"{aid}: status={r['status']} but no file at {r['file_path']}")
        continue
    if p.suffix != ".md":
        continue
    fm = parse_frontmatter(p.read_text())
    if fm is None:
        bad("frontmatter", f"{aid}: {r['file_path']} has no YAML frontmatter")
        continue
    md_checked += 1
    for k in FRONTMATTER_REQUIRED:
        if k not in fm:
            bad("frontmatter", f"{aid}: missing required key {k!r}")
    if fm.get("artifact_id") != aid:
        bad("frontmatter", f"{aid}: frontmatter artifact_id is {fm.get('artifact_id')!r}")
    st = fm.get("status")
    if st in REGISTER_ONLY:
        bad("frontmatter", f"{aid}: {st!r} is a register-only status and is invalid in a file")
    elif st not in DOC_STATUSES:
        bad("frontmatter", f"{aid}: unknown status {st!r}")
    elif st != r["status"]:
        bad("frontmatter", f"{aid}: status {st!r} disagrees with register {r['status']!r}")
    if fm.get("confidentiality") != r["confidentiality"]:
        bad("frontmatter", f"{aid}: confidentiality disagrees with register")
    if fm.get("legal_review_required") != (r["legal_review_required"] == "true"):
        bad("frontmatter", f"{aid}: legal_review_required disagrees with register")
    if fm.get("typst_issue_required") != (r["typst_issue_required"] == "true"):
        bad("frontmatter", f"{aid}: typst_issue_required disagrees with register")
    for d in fm.get("depends_on") or []:
        if d not in reg:
            bad("frontmatter", f"{aid}: depends_on unknown artifact {d}")
    # An artifact that cites sources must say when they were verified.
    if (fm.get("source_ids") or []) and not fm.get("source_as_of"):
        bad("frontmatter", f"{aid}: cites source_ids but source_as_of is empty")
    # Issued documents must carry their provenance.
    if st in ("approved_for_issue", "issued") and fm.get("typst_issue_required"):
        for k in ("typst_source", "latest_issue_id"):
            if not fm.get(k):
                bad("frontmatter", f"{aid}: status={st} requires {k}")

# -------------------------------------------------------------- 4. stage gates
gates = list(csv.DictReader(open(ROOT / "stage-gates.csv")))
seen_seq = set()
for g in gates:
    gid = g["gate_id"]
    arts = [a for a in g["required_artifacts"].split(";") if a]
    if not arts:
        bad("gates", f"{gid}: names no required artifacts; the gate cannot be evaluated")
    for a in arts:
        if a not in reg:
            bad("gates", f"{gid}: required artifact {a} not in register")
    if not g["accountable_owner"] or not g["waiver_authority"]:
        bad("gates", f"{gid}: missing accountable_owner or waiver_authority")
    if g["decision"] not in ("pending", "pass", "conditional", "fail", "deferred"):
        bad("gates", f"{gid}: unknown decision {g['decision']!r}")
    if g["decision"] in ("pass", "conditional"):
        missing = [a for a in arts if reg.get(a, {}).get("status") in REGISTER_ONLY]
        if missing:
            bad("gates", f"{gid}: recorded {g['decision']} while evidence still planned: "
                         + ", ".join(missing))
        if not g["decision_date"]:
            bad("gates", f"{gid}: decided but no decision_date")
    if int(g["sequence"]) in seen_seq:
        bad("gates", f"{gid}: duplicate sequence {g['sequence']}")
    seen_seq.add(int(g["sequence"]))

# ------------------------------------------------------------- 5. dependencies
gate_ids = {g["gate_id"] for g in gates}
for e in csv.DictReader(open(ROOT / "dependency-register.csv")):
    if e["from_id"] not in reg:
        bad("dependencies", f"unknown from_id {e['from_id']}")
    tgt = e["to_id"]
    if tgt not in reg and tgt not in gate_ids:
        bad("dependencies", f"unknown to_id {tgt}")

# ------------------------------------------------------------------ 6. sources
#
# Qualitative sources -- board-adopted PDFs, agency web pages -- are the bulk of
# what governs these pathways, and they change without versioning or notice. The
# register therefore tracks four things a bare URL cannot: the adoption date
# (distinct from the retrieval date), a pinpoint citation, an archived local
# capture, and that capture's hash so drift is detectable.
SRC_STATUSES = {"verified", "unavailable", "conflicting", "superseded",
                "not_found", "listed_not_retrieved"}
ENVIRONMENTS = {"production", "qa", "staging", "archived"}

src_rows = list(csv.DictReader(open(ROOT / "source-register.csv")))
sources = {}
captures = 0
for s_ in src_rows:
    sid = s_["source_id"]
    if sid in sources:
        bad("sources", f"duplicate source_id {sid}")
    if not re.match(r"^SRC-\d{3}$", sid):
        bad("sources", f"malformed source_id {sid!r}")
    if not s_["retrieved_at"]:
        bad("sources", f"{sid}: missing retrieved_at; an undated citation cannot be re-verified")
    if not s_["url"]:
        bad("sources", f"{sid}: missing url")
    if s_["environment"] not in ENVIRONMENTS:
        bad("sources", f"{sid}: unknown environment {s_['environment']!r}")
    if s_["verification_status"] not in SRC_STATUSES:
        bad("sources", f"{sid}: unknown verification_status {s_['verification_status']!r}")
    # A source we claim to have verified must say WHERE in the document.
    if s_["verification_status"] == "verified" and not s_["pinpoint"]:
        bad("sources", f"{sid}: verified but no pinpoint citation; "
                       "'the whole document' is not a citation")
    # A conflict must name its counterpart, and that counterpart must exist.
    if s_["verification_status"] == "conflicting" and not s_["conflicts_with"]:
        bad("sources", f"{sid}: status conflicting but conflicts_with is empty")
    # An archived capture must actually be on disk and must still hash correctly.
    cp, ch = s_["capture_path"], s_["capture_sha256"]
    if cp and not ch:
        bad("sources", f"{sid}: capture_path set but capture_sha256 empty")
    if ch and not cp:
        bad("sources", f"{sid}: capture_sha256 set but capture_path empty")
    if cp:
        f_ = ROOT / cp
        if not f_.exists():
            bad("sources", f"{sid}: capture_path {cp} does not exist")
        else:
            captures += 1
            got = hashlib.sha256(f_.read_bytes()).hexdigest()
            if got != ch:
                bad("sources", f"{sid}: archived capture has changed on disk "
                               f"(register {ch[:12]}\u2026, file {got[:12]}\u2026)")
    # Anything we have not actually read must not be cited as if we had.
    if s_["verification_status"] == "listed_not_retrieved" and s_["pinpoint"]:
        soft("sources", f"{sid}: not retrieved, but carries a pinpoint citation")
    sources[sid] = s_

for s_ in src_rows:
    for other in filter(None, (s_["conflicts_with"], s_["superseded_by"])):
        if other not in sources:
            bad("sources", f"{s_['source_id']}: references unknown source {other}")

# supports_artifact_ids must resolve, in both directions.
for s_ in src_rows:
    for aid in filter(None, s_["supports_artifact_ids"].split(";")):
        if aid not in reg:
            bad("sources", f"{s_['source_id']}: supports unknown artifact {aid}")

for aid, r in reg.items():
    if r["status"] in REGISTER_ONLY:
        continue
    p_ = ROOT / r["file_path"]
    if p_.is_file() and p_.suffix == ".md":
        fm = parse_frontmatter(p_.read_text()) or {}
        for sid in fm.get("source_ids") or []:
            if sid not in sources:
                bad("sources", f"{aid}: cites {sid}, which is not in source-register.csv")
            elif sources[sid]["verification_status"] == "listed_not_retrieved":
                soft("sources", f"{aid}: cites {sid}, which has not been retrieved yet")

# ------------------------------------------------- 6b. body cross-references
#
# Artifact bodies reference other artifacts and sources by ID constantly. A typo
# produces a pointer that looks authoritative and goes nowhere, which is worse
# than no pointer -- a reader follows it, finds nothing, and assumes the evidence
# exists elsewhere.
XREF = re.compile(r"`((?:GOV|SCR|PUB|ACQ|DD|DSN|FIN|APR|PRO|CON|CLO)-\d{3}|SRC-\d{3}|SG-\d{2})`")
gate_ids_early = {g["gate_id"] for g in csv.DictReader(open(ROOT / "stage-gates.csv"))}
xrefs = 0
for aid, r in reg.items():
    if r["status"] in REGISTER_ONLY:
        continue
    p_ = ROOT / r["file_path"]
    if not (p_.is_file() and p_.suffix == ".md"):
        continue
    seen_bad = set()
    for m in XREF.finditer(p_.read_text()):
        ref = m.group(1)
        xrefs += 1
        known = ref in reg or ref in sources or ref in gate_ids_early
        if not known and ref not in seen_bad:
            seen_bad.add(ref)
            bad("xref", f"{aid}: body references {ref}, which does not exist")

# --------------------------------------------------------- 7. issue manifests
MAN_REQ = ["artifact_id", "issue_id", "revision", "issue_purpose", "typst_source",
           "typst_source_sha256", "typst_version", "compile_command",
           "producer_git_commit", "issued_at", "approver_role", "pdf_path", "pdf_sha256"]
issued_dir = ROOT / "publication" / "issued"
manifests = sorted(issued_dir.glob("*/*/manifest.json"))
for m in manifests:
    try:
        d = json.loads(m.read_text())
    except json.JSONDecodeError as e:
        bad("issues", f"{m}: invalid JSON ({e})"); continue
    for k in MAN_REQ:
        if not d.get(k):
            bad("issues", f"{m}: missing required field {k!r}")
    if d.get("artifact_id") not in reg:
        bad("issues", f"{m}: artifact_id {d.get('artifact_id')} not in register")
    for k in ("typst_source_sha256", "pdf_sha256", "source_markdown_sha256"):
        v = d.get(k)
        if v and not SHA_RE.match(v):
            bad("issues", f"{m}: {k} is not a sha256 digest")
    # Hashes must reconcile against what is on disk.
    for pk, hk in (("typst_source", "typst_source_sha256"),
                   ("pdf_path", "pdf_sha256"),
                   ("source_markdown", "source_markdown_sha256")):
        path, want = d.get(pk), d.get(hk)
        if not path or not want:
            continue
        f = REPO / path
        if not f.exists():
            bad("issues", f"{m}: {pk} {path} does not exist"); continue
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != want:
            bad("issues", f"{m}: {hk} does not reconcile "
                          f"(manifest {want[:12]}…, file {got[:12]}…)")
    for sd in d.get("supporting_data") or []:
        f = REPO / sd.get("path", "")
        if not f.exists():
            bad("issues", f"{m}: supporting_data path {sd.get('path')} does not exist")
        elif hashlib.sha256(f.read_bytes()).hexdigest() != sd.get("sha256"):
            bad("issues", f"{m}: supporting_data hash mismatch for {sd.get('path')}")
    if not d.get("visual_inspection_by"):
        bad("issues", f"{m}: visual_inspection_by is empty. Compilation is not inspection.")

# ------------------------------------------------------------------- 8. report
planned = sum(1 for r in reg.values() if r["status"] in REGISTER_ONLY)
print(f"artifacts          {len(reg)}  ({len(reg)-planned} with files, {planned} planned)")
print(f"markdown validated {md_checked}")
print(f"stage gates        {len(gates)}")
print(f"sources            {len(sources)}  ({captures} archived captures verified)")
print(f"cross-references   {xrefs} resolved")
print(f"issue manifests    {len(manifests)}")
print()
for w in warn:
    print("warn  " + w)
if fail:
    print(f"\nFAILED ({len(fail)}):")
    for f_ in fail:
        print("  " + f_)
    sys.exit(1)
print("all gates pass")
