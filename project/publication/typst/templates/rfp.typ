// rfp.typ — request for proposal (architect, consultant, builder, trade).

#import "../lib/lib.typ": *

#let rfp(
  artifact: (:),
  solicitation-no: "[RFP NUMBER]",
  issued-date: "[ISSUE DATE]",
  questions-due: "[QUESTIONS DUE]",
  proposals-due: "[PROPOSALS DUE]",
  contact: "[SINGLE POINT OF CONTACT]",
  submission-method: "[SUBMISSION METHOD]",
  scope-summary: none,
  evaluation: (),
  toc: true,
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: "Request for proposal",
                        cover: true, toc: toc)

  heading(level: 1, numbering: none)[Solicitation control]
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    kv-table(
      ("Solicitation no.", solicitation-no),
      ("Issued", issued-date),
      ("Questions due", questions-due),
    ),
    kv-table(
      ("Proposals due", proposals-due),
      ("Submit via", submission-method),
      ("Sole point of contact", contact),
    ),
  )
  v(8pt)
  note(title: "Contact restriction")[
    All questions must go to the single point of contact named above. Contact with any other
    project participant regarding this solicitation may disqualify a proposer.
  ]
  v(10pt)

  if scope-summary != none {
    heading(level: 1)[Scope summary]
    scope-summary
  }

  body

  if evaluation != () {
    heading(level: 1)[Evaluation criteria]
    text(size: sizes.small)[
      Proposals are evaluated on the criteria and weights below. Weights are disclosed so
      proposers can allocate effort; they are not a scoring formula the Company is bound to.
    ]
    v(6pt)
    base-table(
      columns: (auto, 1fr, auto),
      align: (left, left, right),
      table.header(
        ..("ID", "Criterion", "Weight").map(h =>
          text(font: fonts.sans, size: sizes.micro, weight: 700, fill: white,
               tracking: 0.5pt, upper(h)))
      ),
      ..evaluation.map(r => (
        text(font: fonts.mono, size: sizes.micro, r.at(0)),
        text(size: sizes.small, r.at(1)),
        text(font: fonts.mono, size: sizes.small, r.at(2)),
      )).flatten(),
    )
  }
}
