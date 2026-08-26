#import "../templates/application-package.typ": application-package
#import "../lib/lib.typ": *
#show: application-package.with(
  artifact: (
    artifact-id: "ACQ-011",
    title: "Development Proposal — [PARCEL]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "michigan_licensed_attorney",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  submitted-to: "[RECEIVING AUTHORITY]",
  program: "[PATHWAY]",
  applicant: "Krabby Company LLC",
  applicant-entity-type: "Michigan limited liability company",
  attachments: (("A", "[ATTACHMENT]", "[DESCRIPTION]", "—", "[CUSTODIAN]"),),
)
= Proposed use
[Narrative.]
= Development schedule
#checklist(("M-01", "[MILESTONE]", "not-found", "—", "[NOTE]"))
= Completeness
#checklist(("AP-01", "[REQUIRED ITEM]", "blocked", "—", "Requirement not yet verified"))
