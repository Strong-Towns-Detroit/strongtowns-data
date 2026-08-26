#import "../templates/professional-handoff.typ": professional-handoff
#import "../lib/lib.typ": *
#show: professional-handoff.with(
  artifact: (
    artifact-id: "ACQ-020",
    title: "Counsel Instruction — [MATTER]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "michigan_licensed_attorney",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  discipline: "Michigan-licensed attorney",
  professional: "[FIRM, ATTORNEY, P-NUMBER]",
  engaged-by: "Krabby Company LLC",
  matter: "[MATTER]",
  response-requested-by: "[DATE]",
  questions: ([[First question presented.]], [[Second question presented.]]),
  materials: (("A", "[MATERIAL]", "[DESCRIPTION]", "—", "[CUSTODIAN]"),),
  assumptions: (assumption(id: "ASM-000", owner: "contractor_program_manager",
                           test: "[TEST]")[[ASSUMPTION]],),
)
= Background
[Facts.]
