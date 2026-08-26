#import "../templates/form-checklist.typ": form-checklist
#import "../lib/lib.typ": *
#show: form-checklist.with(
  artifact: (
    artifact-id: "DD-002",
    title: "Integrated Parcel Diligence Checklist",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "michigan_licensed_attorney",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  form-no: "F-DD-002",
  parcel: "[PARCEL ID]",
  instructions: [Complete one per candidate parcel. Attach evidence for every verified row.],
)
= Title and encumbrances
#checklist(
  ("T-01", "Title commitment ordered", "not-found", "—", ""),
  ("T-02", "Exception documents obtained", "blocked", "—", "Awaiting commitment"),
)
= Zoning and dimensional
#checklist(("Z-01", "Zoning district confirmed in writing", "not-found", "—", ""))
