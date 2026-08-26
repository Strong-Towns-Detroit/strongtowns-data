// appendix.typ — appendices, attachment indexes, and binder dividers.

#import "theme.typ": sizes, fonts, ink-soft, rule-col, accent, tone-of, geometry

// Switch heading numbering to A / A.1 and restart.
//
// This MUST be applied as a show rule -- `#show: appendix` -- not called as
// `#appendix-start()`. A `set` rule inside a function body applies only to that
// body, so a plain call would restart the counter without ever changing the
// numbering scheme, silently leaving appendices numbered as body sections.
#let appendix(body) = {
  counter(heading).update(0)
  set heading(numbering: "A.1")
  body
}

// rows: ((tab, title, description, pages, source), ...)
#let attachment-index(..rows) = table(
  columns: (auto, 1.3fr, 1.6fr, auto, 1fr),
  inset: (x: 6pt, y: 5pt),
  stroke: (x, y) => (top: if y == 0 { none } else { 0.4pt + rule-col }, rest: none),
  fill: (x, y) => if y == 0 { accent } else if calc.odd(y) { rgb("#f7f9fa") } else { white },
  table.header(
    ..("Tab", "Attachment", "Description", "Pages", "Source / custodian")
      .map(h => text(font: fonts.sans, size: 6.5pt, weight: 700, fill: white,
                     tracking: 0.5pt, upper(h)))
  ),
  ..rows.pos().map(r => (
    text(font: fonts.mono, size: sizes.micro, weight: 700, r.at(0)),
    text(size: sizes.small, r.at(1)),
    text(size: sizes.micro, r.at(2)),
    text(font: fonts.mono, size: sizes.micro, r.at(3)),
    text(size: sizes.micro, fill: ink-soft, r.at(4)),
  )).flatten(),
)

// Full-page tab divider for a physical or PDF binder.
#let binder-divider(tab: "A", title: "[SECTION TITLE]", contents: ()) = page(
  header: none, footer: none, numbering: none,
  {
    v(1fr)
    align(center, {
      text(font: fonts.sans, size: 90pt, weight: 800, fill: accent.transparentize(20%), tab)
      v(6pt)
      text(font: fonts.sans, size: 18pt, weight: 600, tracking: 1pt, upper(title))
    })
    v(20pt)
    if contents.len() > 0 {
      align(center, block(width: 62%, align(left, {
        line(length: 100%, stroke: 0.5pt + rule-col)
        v(6pt)
        for c in contents {
          text(size: sizes.small, [• #c])
          linebreak()
        }
      })))
    }
    v(1fr)
  },
)
