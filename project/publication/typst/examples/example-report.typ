#import "../templates/report.typ": report
#import "../lib/lib.typ": *
#show: report.with(
  artifact: (
    artifact-id: "DD-027",
    title: "Red-Flag Memorandum — [ADDRESS]",
    issue-id: "ISS-000", revision: "A", status: "template",
    issue-purpose: "Template compile check",
    owner-role: "contractor_program_manager",
    required-reviewer-role: "michigan_licensed_attorney",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  summary: [[Two or three sentences a decision-maker can act on.]],
  distribution: ("Fletcher Liverance, CEO", "[COUNSEL]"),
)
= Findings
#risk-table(("RSK-000", "[RISK]", "[L]", "[I]", "[OWNER]", "[RESPONSE]"))
= Conditions examined
#checklist(("DD-00", "[CONDITION]", "not-found", "[EVIDENCE]", "[NOTE]"))
= Sources
#source-table(("SRC-000", "[TITLE]", "[AUTHORITY]", "[URL]", "[DATE]", "[REQUIREMENT]"))
