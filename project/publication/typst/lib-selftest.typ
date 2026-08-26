// lib-selftest.typ — exercises every component in lib/. Not a project record.
// Compile as the library's regression check:
//   typst compile lib-selftest.typ ../build/lib-selftest.pdf --root ../../..

#import "lib/lib.typ": *

#show: formal-doc.with(
  doc-class: "Library self-test",
  artifact: (
    artifact-id: "PUB-000",
    title: "Publication Library Self-Test",
    subtitle: "Renders every shared component for visual inspection",
    issue-id: "ISS-000",
    revision: "A",
    status: "review-required",
    issue-purpose: "Verify the component library compiles and renders correctly",
    parcel-ids: ("00000000-1", "00000000-2"),
    owner-role: "contractor_program_manager",
    required-reviewer-role: "none_self_test",
    source-draft: "project/publication/typst/lib-selftest.typ",
    source-draft-sha256: "0000000000000000000000000000000000000000000000000000000000000000",
    source-as-of: "2026-08-26",
    confidentiality: "internal",
    prepared-by: "[CONTRACTOR NAME]",
    prepared-for: "Krabby Company LLC",
  ),
  toc: true,
)

= Callouts

#note[Ordinary explanatory aside.]
#info(title: "For information")[Context a reader may want but need not act on.]
#warning[Something that can go wrong if ignored.]
#review-required(reviewer: "Michigan-licensed attorney")[
  Conveyance language has not been reviewed by counsel.
]
#professional-review(discipline: "Licensed surveyor")[
  Boundary and encroachment conclusions require a sealed survey.
]
#assumption(id: "ASM-001", owner: "contractor_program_manager",
            test: "Confirm with BSEED plan review intake")[
  Plan review turnaround is assumed at 15 business days.
]
#unresolved(topic: "Fee schedule currency",
            sought: "Municipal fee schedule page; permit portal")[
  The current fee schedule could not be located at a stable URL.
]

= Status vocabulary

#grid(columns: (1fr, 1fr), row-gutter: 6pt, column-gutter: 8pt,
  ..("template", "research_draft", "review_required", "approved_for_internal_use",
     "approved_for_issue", "issued", "superseded", "not_a_real_status")
    .map(s => status-chip(s)))

= Condition states

#grid(columns: (1fr, 1fr, 1fr), row-gutter: 6pt, column-gutter: 6pt,
  ..("verified", "not_found", "not_applicable", "professional_review_required",
     "blocked", "who_knows").map(s => condition-chip(s)))

= Structured checklist

#checklist(
  ("DD-04.01", "Title commitment received and reviewed", "verified",
   "TC-2026-0114.pdf", ""),
  ("DD-04.02", "Recorded easements identified", "not_found",
   "Register of Deeds search", "Absence not confirmed"),
  ("DD-04.03", "Boundary survey obtained", "professional_review_required",
   "—", "Surveyor not yet engaged"),
  ("DD-04.04", "Wetland determination", "not_applicable",
   "NWI screen", "Outside mapped wetland"),
  ("DD-04.05", "Water/sewer tap availability", "blocked",
   "DWSD inquiry #4471", "Awaiting utility response"),
)

= Risk register

#risk-table(
  ("RSK-001", "Unrecorded utility easement crosses buildable envelope",
   "Medium", "High", "contractor_program_manager", "Order ALTA survey before offer"),
  ("RSK-002", "Permit fee schedule changes before submission",
   "Low", "Low", "contractor_program_manager", "Re-verify at submission"),
)

= Parcel schedule

#parcel-schedule(
  ("21001234.", "1234 Example St", "4,356 sf", "R1", "33 ft", "Under diligence"),
  ("21001235.", "1236 Example St", "4,356 sf", "R1", "33 ft", "Assemblage candidate"),
)

= Budget with basis

#budget-table(
  ("EST", "Site work and grading", "18,400", "Contractor estimate", "Low"),
  ("EST", "Foundation", "31,250", "Subcontractor quote", "High"),
  ("EST", "Permit and municipal fees", "4,900", "Published fee schedule", "Medium"),
  ("EST", "Design contingency", "12,000", "Placeholder", "None"),
)

= Sources

Requirements cited in this document derive from #src("SRC-001") and #src("SRC-002").

#source-table(
  ("SRC-001", "[Document title]", "[Publishing authority]",
   "https://example.gov/path", "2026-08-26", "Application completeness"),
  ("SRC-002", "[Document title]", "[Publishing authority]",
   "https://example.gov/other", "2026-08-26", "Fee calculation"),
)

= Approvals

#approval-table(
  ("Preparer", "[NAME]", "Content accuracy and source currency", "", ""),
  ("Reviewer", "[NAME]", "Michigan-licensed attorney — conveyance terms", "", ""),
  ("Approver", "Fletcher Liverance", "Authorises issue on behalf of Company", "", ""),
)

= Revision history

#revision-history(
  ("ISS-000", "A", "2026-08-26", "Initial self-test", "[PREPARER]", "—"),
)

#show: appendix

= Attachment index

#attachment-index(
  ("A", "Title commitment", "Commitment for title insurance", "12", "[Title company]"),
  ("B", "Survey", "Boundary and topographic survey", "2", "[Surveyor]"),
)

#binder-divider(tab: "C", title: "Permits and approvals",
  contents: ("Building permit application", "Plan review correspondence", "Issued permits"))

= After the divider

Content continues normally after a binder divider.
