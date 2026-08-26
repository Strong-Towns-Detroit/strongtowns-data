#import "../templates/letter.typ": letter
#import "../lib/lib.typ": *
#show: letter.with(
  artifact: (
    artifact-id: "APR-011",
    title: "Correspondence — [SUBJECT]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "company_decision_authority",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  date: "[DATE]",
  recipient: ("[NAME]", "[TITLE]", "[AGENCY]", "[ADDRESS]"),
  salutation: "Dear [NAME]:",
  signer: "[CONTRACTOR NAME]",
  signer-title: "Construction Program Manager",
  enclosures: ("[ENCLOSURE]",),
)
[Body of the letter.]
