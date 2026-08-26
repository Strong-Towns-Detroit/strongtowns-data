#import "../templates/rfp.typ": rfp
#import "../lib/lib.typ": *
#show: rfp.with(
  artifact: (
    artifact-id: "PRO-001",
    title: "Request for Proposal — [SERVICE]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "company_decision_authority",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  solicitation-no: "[RFP-000]",
  contact: "[CONTRACTOR NAME], Construction Program Manager",
  scope-summary: [[Scope summary.]],
  evaluation: (("E-01", "Relevant experience", "30%"), ("E-02", "Fee", "25%"),
               ("E-03", "Schedule", "25%"), ("E-04", "Capacity", "20%")),
)
= Instructions to proposers
[Format, page limits, submission mechanics.]
= Scope of services
[Detailed scope.]
= Required qualifications
#checklist(("Q-01", "[QUALIFICATION]", "not-found", "—", "Verify at evaluation"))
