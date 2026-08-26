// callouts.typ — warnings, review gates, assumptions, and notes.

#import "theme.typ": tones, tone-of, sizes, fonts

#let callout(tone: "info", title: none, icon: none, body) = block(
  width: 100%,
  breakable: true,
  inset: (x: 10pt, y: 8pt),
  radius: 3pt,
  fill: tone-of(tone).bg,
  stroke: (left: 3pt + tone-of(tone).fg, rest: 0.5pt + tone-of(tone).bd),
  {
    if title != none {
      text(font: fonts.sans, size: sizes.small, weight: 700, fill: tone-of(tone).fg,
           tracking: 0.4pt, upper(title))
      v(3pt, weak: true)
    }
    set text(size: sizes.small)
    body
  },
)

#let note(title: "Note", body) = callout(tone: "neutral", title: title, body)
#let info(title: "For information", body) = callout(tone: "info", title: title, body)
#let warning(title: "Warning", body) = callout(tone: "warn", title: title, body)

// Hard gate: this document may not advance until the named reviewer signs off.
#let review-required(reviewer: "[REVIEWER ROLE]", body) = callout(
  tone: "stop",
  title: "Review required — " + reviewer,
  body,
)

// Licensed-professional boundary. Used wherever the project must stop
// producing its own conclusion and retain someone.
#let professional-review(discipline: "[DISCIPLINE]", body) = callout(
  tone: "stop",
  title: "Licensed professional required — " + discipline,
  body,
)

// A stated assumption. Every assumption carries an owner and a test that
// would confirm or refute it.
#let assumption(id: "", owner: "[ROLE]", test: "", body) = callout(
  tone: "warn",
  title: if id != "" { "Assumption " + id } else { "Assumption" },
  {
    body
    v(4pt, weak: true)
    set text(size: sizes.micro, fill: tone-of("warn").fg)
    [*Owner:* #owner]
    if test != "" { linebreak(); [*Resolved by:* #test] }
  },
)

// A requirement we went looking for and could not establish. Explicitly NOT
// the same as "no such requirement exists".
#let unresolved(topic: "[TOPIC]", sought: "", body) = callout(
  tone: "stop",
  title: "Unresolved — " + topic,
  {
    body
    if sought != "" {
      v(4pt, weak: true)
      set text(size: sizes.micro, fill: tone-of("stop").fg)
      [*Sources checked:* #sought]
    }
  },
)
