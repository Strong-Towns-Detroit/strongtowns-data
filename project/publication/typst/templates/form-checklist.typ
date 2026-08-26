// form-checklist.typ — a fillable form or completion checklist.
//
// Every checklist row carries a condition state from the controlled vocabulary.
// There is no blank/neutral default: an unmarked row is an unknown, and this
// template renders unknowns as failures rather than as silence.

#import "../lib/lib.typ": *

#let form-checklist(
  artifact: (:),
  form-no: "[FORM NO.]",
  completed-by: "",
  completed-date: "",
  parcel: "",
  instructions: none,
  landscape: false,
  cover: false,
  body,
) = {
  let a = merge-artifact(artifact)
  show: formal-doc.with(
    artifact: artifact,
    doc-class: "Form / checklist",
    geom: if landscape { geometry.wide } else { geometry.standard },
    cover: cover,
  )

  if not cover {
    grid(columns: (1fr, auto), align: (left + top, right + top),
      {
        text(font: fonts.sans, size: sizes.h1, weight: 700, a.title)
        linebreak()
        text(font: fonts.sans, size: sizes.micro, fill: ink-soft, tracking: 0.6pt,
             upper(brand.org-name))
      },
      text(font: fonts.mono, size: sizes.micro, fill: ink-soft,
           a.artifact-id + " · " + form-no),
    )
    v(4pt)
    line(length: 100%, stroke: 1pt + accent)
    v(8pt)
  }

  kv-table(
    ("Parcel", if parcel == "" { "not parcel-specific" } else { parcel }),
    ("Completed by", if completed-by == "" { "________________________" } else { completed-by }),
    ("Date completed", if completed-date == "" { "________________" } else { completed-date }),
  )
  v(8pt)

  if instructions != none {
    note(title: "Instructions")[#instructions]
    v(8pt)
  }

  warning(title: "Unknowns are not clears")[
    A condition that has not been checked is recorded as #condition-chip("not-found") or
    #condition-chip("blocked") — never left blank and never marked
    #condition-chip("verified"). Blank rows block the stage gate this form feeds.
  ]
  v(10pt)

  body
}
