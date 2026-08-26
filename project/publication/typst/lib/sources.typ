// sources.typ — citation discipline.
//
// A claim about a current external requirement is only usable here if it
// carries an authority, a URL, and a retrieval date. Requirements change; a
// citation without a retrieval date is not a citation, it is a memory.

#import "theme.typ": sizes, fonts, ink-soft, rule-col, accent, tone-of

// Inline cross-reference to a row in the source table. Rendered as a bracketed
// token rather than a superscript: these IDs are looked up, not skimmed past,
// and a 6pt superscript is illegible at print size.
#let src(id) = box(
  inset: (x: 2.5pt, y: 1pt),
  outset: (y: 1pt),
  radius: 1.5pt,
  fill: tone-of("info").bg,
  text(font: fonts.mono, size: 7pt, fill: tone-of("info").fg, id),
)

// rows: ((id, title, authority, url, retrieved, supports), ...)
#let source-table(..rows) = table(
  columns: (auto, 1.4fr, 1.1fr, 1.5fr, auto, 1.3fr),
  inset: (x: 5pt, y: 5pt),
  stroke: (x, y) => (top: if y == 0 { none } else { 0.4pt + rule-col }, rest: none),
  fill: (x, y) => if y == 0 { accent } else if calc.odd(y) { rgb("#f7f9fa") } else { white },
  table.header(
    ..("ID", "Document title", "Publishing authority", "URL", "Retrieved", "Requirement supported")
      .map(h => text(font: fonts.sans, size: 6.5pt, weight: 700, fill: white,
                     tracking: 0.5pt, hyphenate: false, upper(h)))
  ),
  ..rows.pos().map(r => (
    text(font: fonts.mono, size: 6.5pt, r.at(0)),
    text(size: sizes.micro, r.at(1)),
    text(size: sizes.micro, r.at(2)),
    text(font: fonts.mono, size: 6pt, fill: ink-soft, r.at(3)),
    text(font: fonts.mono, size: 6.5pt, r.at(4)),
    text(size: sizes.micro, r.at(5)),
  )).flatten(),
)

// Freshness stamp. Every researched document states the date its external
// claims were last checked, separately from when the file was edited.
#let as-of(date, scope: "external requirements") = block(
  width: 100%,
  inset: (x: 8pt, y: 5pt),
  radius: 2pt,
  fill: tone-of("info").bg,
  stroke: 0.4pt + tone-of("info").bd,
  text(font: fonts.sans, size: sizes.micro, fill: tone-of("info").fg,
       [Currency of #scope verified as of *#date*. Re-verify before relying on this document.]),
)
