// status.typ — the artifact status vocabulary and its visual treatment.
//
// The status set is closed. An unrecognised status renders as a loud failure
// rather than falling back to something benign: in this system an unknown
// condition must never read as clear.

#import "theme.typ": tones, tone-of, sizes, fonts

// Markdown frontmatter uses snake_case; Typst metadata uses kebab-case.
// Accept either spelling and canonicalise to kebab-case.
#let canon(s) = lower(str(s)).replace("_", "-")

#let status-table = (
  "template": (
    label: "TEMPLATE — NOT A RECORD",
    tone: "neutral", final: false, issued: false, watermark: "TEMPLATE",
    note: "Reusable blank. Fill a copy; never complete the template in place.",
  ),
  "research-draft": (
    label: "RESEARCH DRAFT",
    tone: "warn", final: false, issued: false, watermark: "DRAFT",
    note: "Content is being gathered. Claims may be uncited or unverified. Not for external use.",
  ),
  "review-required": (
    label: "REVIEW REQUIRED",
    tone: "stop", final: false, issued: false, watermark: "REVIEW REQUIRED",
    note: "Complete but unreviewed. Required reviewer has not signed off. Not for external use or reliance.",
  ),
  "approved-for-internal-use": (
    label: "APPROVED — INTERNAL USE ONLY",
    tone: "info", final: false, issued: false, watermark: "INTERNAL USE ONLY",
    note: "Approved for internal decision-making. Not cleared for distribution outside the project team.",
  ),
  "approved-for-issue": (
    label: "APPROVED FOR ISSUE",
    tone: "ok", final: true, issued: false, watermark: none,
    note: "",
  ),
  "issued": (
    label: "ISSUED",
    tone: "ok", final: true, issued: true, watermark: none,
    note: "",
  ),
  "superseded": (
    label: "SUPERSEDED",
    tone: "stop", final: false, issued: false, watermark: "SUPERSEDED",
    note: "A later issue replaces this document. Do not rely on it.",
  ),
)

#let status-of(s) = {
  let k = canon(s)
  if k in status-table {
    status-table.at(k)
  } else {
    (
      label: "UNRECOGNISED STATUS (" + upper(str(s)) + ")",
      tone: "stop", final: false, issued: false, watermark: "UNVALIDATED",
      note: "This document declares a status outside the controlled vocabulary. "
          + "Treat it as unapproved until corrected.",
    )
  }
}

#let status-is-final(s) = status-of(s).final
#let status-is-issued(s) = status-of(s).issued

// Small inline chip, for headers and register tables.
#let status-chip(s, size: sizes.micro) = {
  let st = status-of(s)
  let t = tone-of(st.tone)
  box(
    inset: (x: 5pt, y: 2.5pt),
    radius: 2pt,
    fill: t.bg,
    stroke: 0.5pt + t.bd,
    text(font: fonts.sans, size: size, weight: 600, fill: t.fg, tracking: 0.4pt, st.label),
  )
}

// Full-width banner. Rendered on the title page and again at the top of the
// body whenever the document is not approved or issued.
#let status-banner(s) = {
  let st = status-of(s)
  let t = tone-of(st.tone)
  block(
    width: 100%,
    inset: (x: 10pt, y: 8pt),
    radius: 3pt,
    fill: t.bg,
    stroke: (left: 3pt + t.fg, rest: 0.5pt + t.bd),
    {
      text(font: fonts.sans, size: sizes.small, weight: 700, fill: t.fg, tracking: 0.6pt, st.label)
      if st.note != "" {
        linebreak()
        v(1pt)
        text(font: fonts.sans, size: sizes.micro, fill: t.fg, st.note)
      }
    },
  )
}

// Diagonal page watermark for any non-final status.
#let status-watermark(s) = {
  let st = status-of(s)
  if st.watermark == none { return none }
  let t = tone-of(st.tone)
  place(
    center + horizon,
    rotate(-30deg, text(
      font: fonts.sans,
      size: 58pt,
      weight: 800,
      tracking: 3pt,
      fill: t.fg.transparentize(88%),
      st.watermark,
    )),
  )
}
