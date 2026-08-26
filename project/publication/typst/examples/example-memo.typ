#import "../templates/memo.typ": memo
#import "../lib/lib.typ": *
#show: memo.with(
  artifact: (
    artifact-id: "ACQ-016",
    title: "Acquisition Recommendation — [ADDRESS]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "company_decision_authority",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  to: ("Fletcher Liverance, CEO — Krabby Company LLC",),
  from: "[CONTRACTOR NAME], Construction Program Manager",
  date: "[DATE]",
  re: "Recommendation on candidate parcel [PARCEL ID]",
)
= Recommendation
[One sentence. Acquire / do not acquire / acquire subject to conditions.]
= Basis
[Buildable envelope, total project cost, estimated finished value, diligence status.]
#assumption(id: "ASM-000", owner: "contractor_program_manager", test: "[TEST]")[[ASSUMPTION]]
= Conditions
#checklist(("C-01", "[CONDITION]", "blocked", "—", "[NOTE]"))
