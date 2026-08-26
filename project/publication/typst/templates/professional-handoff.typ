// professional-handoff.typ — instruction package to counsel or another licensed
// professional.
//
// The purpose of this document class is to ask a question, not to answer it.
// It states what we know, what we assume, and precisely what we need decided --
// and it says on its face that nothing in it is professional advice.

#import "../lib/lib.typ": *

#let professional-handoff(
  artifact: (:),
  discipline: "[DISCIPLINE]",
  professional: "[FIRM / PROFESSIONAL, LICENCE NO.]",
  engaged-by: "[ENGAGING PARTY]",
  matter: "[MATTER DESCRIPTION]",
  response-requested-by: "[DATE]",
  questions: (),
  materials: (),
  assumptions: (),
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: "Professional handoff",
                        cover: true, toc: false)

  professional-review(discipline: discipline)[
    This package is prepared by a construction program manager, not by a licensed
    #lower(discipline). It contains no legal, engineering, surveying, tax, lending, or
    architectural advice and must not be relied on as such. Its only purpose is to present
    facts, assumptions, and questions so that #professional can advise.
  ]
  v(10pt)

  heading(level: 1)[Engagement]
  kv-table(
    ("Discipline", discipline),
    ("Professional", professional),
    ("Engaged by", engaged-by),
    ("Matter", matter),
    ("Response requested by", response-requested-by),
  )
  v(10pt)

  heading(level: 1)[Questions presented]
  if questions == () {
    unresolved(topic: "No questions stated")[
      A handoff with no explicit question cannot be answered and should not be sent.
    ]
  } else {
    for (i, q) in questions.enumerate() {
      block(width: 100%, inset: (x: 10pt, y: 7pt), below: 6pt,
            fill: tone-of("info").bg, stroke: (left: 3pt + tone-of("info").fg),
        {
          text(font: fonts.sans, size: sizes.micro, weight: 700,
               fill: tone-of("info").fg, "Q" + str(i + 1))
          linebreak()
          q
        })
    }
  }
  v(10pt)

  heading(level: 1)[Assumptions on which the questions rest]
  if assumptions == () {
    note[No assumptions declared. Confirm none are hiding.]
  } else {
    for a in assumptions { a }
  }
  v(10pt)

  heading(level: 1)[Materials provided]
  if materials != () { attachment-index(..materials) } else {
    note[No materials attached.]
  }
  v(10pt)

  body
}
