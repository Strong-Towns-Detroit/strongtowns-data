// memo.typ — formal memorandum.
//
//   #import "../templates/memo.typ": memo
//   #show: memo.with(artifact: (...), to: ("Fletcher Liverance, CEO",), from: "...", re: "...")

#import "../lib/lib.typ": *

#let memo(
  artifact: (:),
  to: (),
  from: "",
  cc: (),
  date: "",
  re: "",
  body,
) = {
  let a = merge-artifact(artifact)
  show: formal-doc.with(artifact: artifact, doc-class: "Memorandum", cover: false)

  // Masthead
  grid(columns: (1fr, auto), align: (left + top, right + top),
    {
      text(font: fonts.sans, size: sizes.h2, weight: 700, tracking: 0.4pt, brand.org-name)
      linebreak()
      text(font: fonts.sans, size: 15pt, weight: 300, tracking: 3pt, fill: ink-soft, "MEMORANDUM")
    },
    text(font: fonts.mono, size: sizes.micro, fill: ink-soft, a.artifact-id),
  )
  v(4pt)
  line(length: 100%, stroke: 1.2pt + accent)
  v(8pt)

  kv-table(
    ("To",   if to == () { "[RECIPIENT]" } else { to.join("; ") }),
    ("From", if from == "" { "[AUTHOR]" } else { from }),
    ..if cc != () { (("cc", cc.join("; ")),) } else { () },
    ("Date", if date == "" { "[DATE]" } else { date }),
    ("Re",   if re == "" { a.title } else { re }),
  )
  v(10pt)
  body

  v(18pt)
  line(length: 40%, stroke: 0.5pt + rule-col)
  v(4pt)
  text(size: sizes.micro, fill: ink-soft,
    [This memorandum records analysis and recommendation. Decisions on acquisition, design,
     and submission rest with #if a.prepared-for != "" { a.prepared-for } else { "the Company" }.])
}
