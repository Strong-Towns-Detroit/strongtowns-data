// tables.typ — checklists, condition states, risk, parcel, budget, approvals.

#import "theme.typ": tones, tone-of, sizes, fonts, rule-col, ink-soft, accent

#let _head(body) = text(font: fonts.sans, size: sizes.micro, weight: 700,
                        fill: white, tracking: 0.5pt, upper(body))

#let _hrow(..cells) = table.header(..cells.pos().map(c => _head(c)))

#let base-table(columns: auto, align: left, ..rows) = table(
  columns: columns,
  align: align,
  inset: (x: 6pt, y: 5pt),
  stroke: (x, y) => (
    top: if y == 0 { none } else { 0.4pt + rule-col },
    bottom: none, left: none, right: none,
  ),
  fill: (x, y) => if y == 0 { accent } else if calc.odd(y) { rgb("#f7f9fa") } else { white },
  ..rows,
)

// ---------------------------------------------------------------- conditions
//
// The controlled vocabulary for any verifiable condition. `not_found` is a
// deliberate amber, not a green: searching and finding nothing is a different
// epistemic state from confirming a negative.

#let condition-states = (
  "verified":                     (label: "VERIFIED",       tone: "ok"),
  "not-found":                    (label: "NOT FOUND",      tone: "warn"),
  "not-applicable":               (label: "N/A",            tone: "neutral"),
  "professional-review-required": (label: "PRO REVIEW REQ", tone: "warn"),
  "blocked":                      (label: "BLOCKED",        tone: "stop"),
)

#let condition-chip(state) = {
  let k = lower(str(state)).replace("_", "-")
  let s = if k in condition-states { condition-states.at(k) } else {
    (label: "UNKNOWN (" + upper(str(state)) + ")", tone: "stop")
  }
  let t = tone-of(s.tone)
  box(inset: (x: 4pt, y: 2pt), radius: 2pt, fill: t.bg, stroke: 0.5pt + t.bd,
      text(font: fonts.sans, size: 6.5pt, weight: 700, fill: t.fg, tracking: 0.3pt, s.label))
}

// items: ((id, requirement, state, evidence, note), ...)
#let checklist(..items) = base-table(
  columns: (auto, 1fr, auto, 0.9fr, 0.9fr),
  _hrow("ID", "Requirement", "State", "Evidence", "Note"),
  ..items.pos().map(r => (
    text(font: fonts.mono, size: sizes.micro, r.at(0)),
    text(size: sizes.small, r.at(1)),
    condition-chip(r.at(2)),
    text(size: sizes.micro, r.at(3)),
    text(size: sizes.micro, fill: ink-soft, r.at(4)),
  )).flatten(),
)

// ---------------------------------------------------------------------- risk
// rows: ((id, risk, likelihood, impact, owner, response), ...)
#let risk-table(..rows) = base-table(
  columns: (auto, 1.6fr, auto, auto, auto, 1.4fr),
  _hrow("ID", "Risk / issue", "Likelihood", "Impact", "Owner", "Response"),
  ..rows.pos().map(r => (
    text(font: fonts.mono, size: sizes.micro, r.at(0)),
    text(size: sizes.small, r.at(1)),
    text(size: sizes.micro, r.at(2)),
    text(size: sizes.micro, r.at(3)),
    text(size: sizes.micro, r.at(4)),
    text(size: sizes.micro, r.at(5)),
  )).flatten(),
)

// ------------------------------------------------------------------- parcels
// rows: ((parcel-id, address, area, zoning, frontage, status), ...)
#let parcel-schedule(..rows) = base-table(
  columns: (auto, 1.4fr, auto, auto, auto, auto),
  _hrow("Parcel ID", "Address / description", "Area", "Zoning", "Frontage", "Status"),
  ..rows.pos().map(r => (
    text(font: fonts.mono, size: sizes.micro, r.at(0)),
    text(size: sizes.small, r.at(1)),
    text(size: sizes.micro, r.at(2)),
    text(size: sizes.micro, r.at(3)),
    text(size: sizes.micro, r.at(4)),
    text(size: sizes.micro, r.at(5)),
  )).flatten(),
)

// -------------------------------------------------------------------- budget
//
// `basis` is mandatory and is the point of the table: it forces every line to
// declare whether the number is a quote, an estimate, or a placeholder.
// rows: ((code, item, amount, basis, confidence), ...)
#let budget-table(currency: "$", total-label: "Total", ..rows) = {
  let rs = rows.pos()
  base-table(
    columns: (auto, 1fr, auto, auto, auto),
    align: (left, left, right, left, left),
    _hrow("Code", "Line item", "Amount", "Basis", "Confidence"),
    ..rs.map(r => (
      text(font: fonts.mono, size: sizes.micro, r.at(0)),
      text(size: sizes.small, r.at(1)),
      text(font: fonts.mono, size: sizes.small, currency + r.at(2)),
      text(size: sizes.micro, r.at(3)),
      text(size: sizes.micro, r.at(4)),
    )).flatten(),
  )
}

// ----------------------------------------------------------------- approvals
// rows: ((role, name, scope, signature, date), ...)
#let approval-table(..rows) = table(
  columns: (auto, 1fr, 1.2fr, 1.4fr, auto),
  inset: (x: 6pt, y: 9pt),
  stroke: 0.4pt + rule-col,
  // Header labels are white; without this the row renders invisible.
  fill: (x, y) => if y == 0 { accent } else { white },
  table.header(
    _head("Role"), _head("Name"), _head("Scope of approval"),
    _head("Signature"), _head("Date"),
  ),
  ..rows.pos().map(r => (
    text(size: sizes.small, weight: 600, r.at(0)),
    text(size: sizes.small, r.at(1)),
    text(size: sizes.micro, r.at(2)),
    text(size: sizes.small, fill: ink-soft, r.at(3)),
    text(size: sizes.small, fill: ink-soft, r.at(4)),
  )).flatten(),
)

// Simple label/value block used by document-control sections.
#let kv-table(..pairs) = table(
  columns: (auto, 1fr),
  inset: (x: 6pt, y: 4pt),
  stroke: (x, y) => (top: if y == 0 { none } else { 0.4pt + rule-col }, rest: none),
  ..pairs.pos().map(p => (
    text(font: fonts.sans, size: sizes.micro, weight: 600, fill: ink-soft,
         tracking: 0.3pt, upper(p.at(0))),
    text(size: sizes.small, p.at(1)),
  )).flatten(),
)
