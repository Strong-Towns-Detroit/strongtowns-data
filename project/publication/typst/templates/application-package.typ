// application-package.typ — application / proposal package for submission to an
// external authority. The submission-control block is deliberately at the front:
// a package that cannot state its deadline and recipient is not ready to send.

#import "../lib/lib.typ": *

#let application-package(
  artifact: (:),
  submitted-to: "[RECEIVING AUTHORITY]",
  program: "[PROGRAM / PATHWAY]",
  submission-method: "[PORTAL / EMAIL / IN PERSON]",
  submission-deadline: "[DEADLINE]",
  applicant: "[APPLICANT LEGAL NAME]",
  applicant-entity-type: "[ENTITY TYPE]",
  contact: "[CONTACT NAME, EMAIL, PHONE]",
  attachments: (),
  toc: true,
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: "Application package",
                        cover: true, toc: toc)

  heading(level: 1, numbering: none)[Submission control]
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    kv-table(
      ("Submitted to", submitted-to),
      ("Program / pathway", program),
      ("Method", submission-method),
      ("Deadline", submission-deadline),
    ),
    kv-table(
      ("Applicant", applicant),
      ("Entity type", applicant-entity-type),
      ("Contact", contact),
    ),
  )
  v(10pt)

  warning(title: "Before submitting")[
    Confirm the receiving authority's current form versions, fee amounts, and submission
    method against the source register. Requirements published on an authority's website
    change without notice; a package assembled against a stale requirement will be rejected.
  ]
  v(10pt)

  body

  if attachments != () {
    pagebreak()
    show: appendix
    heading(level: 1)[Attachment index]
    attachment-index(..attachments)
  }
}
