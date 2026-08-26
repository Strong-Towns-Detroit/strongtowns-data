// report.typ — issued project report (diligence findings, progress, red-flag).

#import "../lib/lib.typ": *

#let report(
  artifact: (:),
  toc: true,
  summary: none,
  distribution: (),
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: "Report", cover: true, toc: toc)

  if summary != none {
    heading(level: 1, numbering: none)[Executive summary]
    block(width: 100%, inset: (x: 10pt, y: 8pt), fill: tone-of("info").bg,
          stroke: (left: 3pt + tone-of("info").fg, rest: 0.5pt + tone-of("info").bd),
          summary)
    v(10pt)
  }

  if distribution != () {
    heading(level: 1, numbering: none)[Distribution]
    for d in distribution [ • #d \ ]
    v(10pt)
  }

  body
}
