#import "../templates/stage-gate-package.typ": stage-gate-package
#import "../lib/lib.typ": *
#show: stage-gate-package.with(
  artifact: (
    artifact-id: "GOV-004",
    title: "Stage Gate 4 — Due Diligence Accepted",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "company_decision_authority",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  gate-id: "SG-04",
  gate-name: "Due diligence accepted",
  accountable-owner: "contractor_program_manager",
  reviewers: ("michigan_licensed_attorney", "company_decision_authority"),
  waiver-authority: "company_decision_authority",
  decision: "pending",
  required-artifacts: (
    ("DD-001", "Due-diligence plan and deadline calculator", "not-found", "—", ""),
    ("DD-027", "Red-flag memorandum", "blocked", "—", "Not yet drafted"),
  ),
  blockers: (("BLK-01", "[BLOCKER]", "[L]", "[I]", "[OWNER]", "[RESPONSE]"),),
)
= Notes
[Gate-specific commentary.]
