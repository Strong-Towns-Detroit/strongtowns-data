#import "../templates/binder.typ": binder
#import "../lib/lib.typ": *
#show: binder.with(
  artifact: (
    artifact-id: "CLO-006",
    title: "Closing Binder — [ADDRESS]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "michigan_licensed_attorney",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  binder-type: "Closing",
  transaction: "[TRANSACTION]",
  custodian: "Krabby Company LLC",
  retention: "[RETENTION PERIOD]",
  tabs: (
    (tab: "A", title: "Conveyance documents", description: "Deed and transfer records",
     pages: "—", custodian: "[TITLE CO]", contents: ("Executed deed", "Recording receipt")),
    (tab: "B", title: "Title", description: "Commitment and final policy",
     pages: "—", custodian: "[TITLE CO]", contents: ("Final policy",)),
  ),
)
= Assembly notes
[How this binder was assembled and what remains outstanding.]
