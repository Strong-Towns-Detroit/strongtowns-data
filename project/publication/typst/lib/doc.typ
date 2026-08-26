// doc.typ — the document chassis: metadata, title page, document control,
// revision history, running head/foot, and the `formal-doc` wrapper.

#import "theme.typ": *
#import "status.typ": *
#import "tables.typ": kv-table, approval-table
#import "sources.typ": as-of

// The metadata contract. Every formal document supplies this dictionary;
// anything omitted falls back to a value that reads as missing, never as OK.
#let default-artifact = (
  artifact-id:            "",
  title:                  "[UNTITLED DOCUMENT]",
  subtitle:               "",
  issue-id:               "",
  revision:               "",
  status:                 "review-required",
  issue-purpose:          "",
  parcel-ids:             (),
  owner-role:             "",
  required-reviewer-role: "",
  source-draft:           "",
  source-draft-sha256:    "",
  source-as-of:           "",
  confidentiality:        "internal",
  issued-at:              none,
  // Contract-side attribution: who prepared this and for whom.
  prepared-by:            "",
  prepared-for:           "",
)

// Typst parses `(..a, ..b)` as an ARRAY literal; `+` is the dictionary merge
// operator, with the right-hand side winning on conflicting keys.
#let merge-artifact(a) = default-artifact + a

// Renders an empty value as a visible gap rather than blank space.
#let _f(v) = if v == none or v == "" or v == () {
  text(fill: rgb("#a33"), style: "italic", "— not supplied —")
} else if type(v) == array {
  v.join(", ")
} else {
  v
}

#let _mono(v) = if v == none or v == "" {
  text(fill: rgb("#a33"), style: "italic", "— not supplied —")
} else {
  text(font: fonts.mono, size: 7pt, v)
}

#let confidentiality-label(c) = upper(str(c)).replace("-", " ")

// ------------------------------------------------------------ document control

#let doc-control(a) = {
  let a = merge-artifact(a)
  block(
    width: 100%,
    stroke: 0.6pt + rule-col,
    radius: 3pt,
    inset: 0pt,
    {
      block(width: 100%, inset: (x: 8pt, y: 5pt), fill: accent,
        text(font: fonts.sans, size: sizes.micro, weight: 700, fill: white,
             tracking: 0.8pt, "DOCUMENT CONTROL"))
      block(inset: 8pt, grid(
        columns: (1fr, 1fr),
        column-gutter: 14pt,
        kv-table(
          ("Artifact ID",      _f(a.artifact-id)),
          ("Issue ID",         _f(a.issue-id)),
          ("Revision",         _f(a.revision)),
          ("Status",           status-chip(a.status)),
          ("Issue purpose",    _f(a.issue-purpose)),
          ("Issued at",        if a.issued-at == none { text(fill: ink-soft, "not issued") } else { a.issued-at }),
        ),
        kv-table(
          ("Owner role",       _f(a.owner-role)),
          ("Required reviewer", _f(a.required-reviewer-role)),
          ("Parcel IDs",       if a.parcel-ids == () { text(fill: ink-soft, "not parcel-specific") } else { a.parcel-ids.join(", ") }),
          ("Confidentiality",  confidentiality-label(a.confidentiality)),
          ("Source as-of",     _f(a.source-as-of)),
          ("Prepared by",      _f(a.prepared-by)),
        ),
      ))
      // Provenance chain back to the Markdown draft, if one exists.
      if a.source-draft != "" {
        block(width: 100%, inset: (x: 8pt, y: 6pt), fill: rgb("#f7f9fa"),
          stroke: (top: 0.4pt + rule-col), {
            text(font: fonts.sans, size: sizes.micro, weight: 600, fill: ink-soft,
                 tracking: 0.4pt, "SOURCE DRAFT")
            linebreak()
            _mono(a.source-draft)
            linebreak()
            _mono("sha256:" + a.source-draft-sha256)
          })
      }
    },
  )
}

// ------------------------------------------------------------ revision history
// rows: ((issue-id, revision, date, purpose, prepared-by, approved-by), ...)
#let revision-history(..rows) = table(
  columns: (auto, auto, auto, 1.4fr, 1fr, 1fr),
  inset: (x: 6pt, y: 5pt),
  stroke: (x, y) => (top: if y == 0 { none } else { 0.4pt + rule-col }, rest: none),
  fill: (x, y) => if y == 0 { accent } else if calc.odd(y) { rgb("#f7f9fa") } else { white },
  table.header(
    ..("Issue", "Rev", "Date", "Purpose of issue", "Prepared by", "Approved by")
      .map(h => text(font: fonts.sans, size: 6.5pt, weight: 700, fill: white,
                     tracking: 0.5pt, upper(h)))
  ),
  ..rows.pos().map(r => (
    text(font: fonts.mono, size: sizes.micro, r.at(0)),
    text(font: fonts.mono, size: sizes.micro, r.at(1)),
    text(font: fonts.mono, size: sizes.micro, r.at(2)),
    text(size: sizes.micro, r.at(3)),
    text(size: sizes.micro, r.at(4)),
    text(size: sizes.micro, r.at(5)),
  )).flatten(),
)

// ----------------------------------------------------------------- title page

#let artifact-title-page(a, doc-class: "") = {
  let a = merge-artifact(a)
  page(header: none, footer: none, numbering: none, {
    // Masthead
    grid(
      columns: (1fr, auto),
      align: (left + top, right + top),
      {
        if brand.logo != none { brand.logo; v(6pt) }
        text(font: fonts.sans, size: sizes.h2, weight: 700, tracking: 0.5pt, brand.org-name)
        linebreak()
        text(font: fonts.sans, size: sizes.micro, fill: ink-soft, tracking: 0.6pt,
             upper(brand.org-unit))
      },
      {
        if doc-class != "" {
          text(font: fonts.sans, size: sizes.micro, weight: 600, fill: ink-soft,
               tracking: 1.2pt, upper(doc-class))
          linebreak()
        }
        text(font: fonts.mono, size: sizes.micro, fill: ink-soft, a.artifact-id)
      },
    )
    v(4pt)
    line(length: 100%, stroke: 1.2pt + accent)

    v(1fr)

    // Title block
    text(font: fonts.sans, size: sizes.title, weight: 700, hyphenate: false, a.title)
    if a.subtitle != "" {
      v(6pt)
      text(font: fonts.sans, size: sizes.h2, weight: 400, fill: ink-soft, a.subtitle)
    }
    if a.parcel-ids != () {
      v(8pt)
      text(font: fonts.mono, size: sizes.small, fill: ink-soft,
           "Parcels: " + a.parcel-ids.join(", "))
    }

    v(16pt)
    status-banner(a.status)

    v(1fr)

    doc-control(a)

    v(10pt)
    text(font: fonts.sans, size: sizes.micro, fill: ink-soft,
         confidentiality-label(a.confidentiality) + " — " + brand.org-name
         + if a.prepared-for != "" { " — prepared for " + a.prepared-for } else { "" })
  })
}

// ------------------------------------------------------------------- chassis

#let formal-doc(
  artifact: (:),
  geom: geometry.standard,
  doc-class: "",
  cover: true,
  toc: false,
  toc-depth: 2,
  numbered-headings: true,
  // Correspondence renders its own letterhead first; the status/currency
  // preamble must not float above it.
  preamble: true,
  body,
) = {
  let a = merge-artifact(artifact)
  let st = status-of(a.status)

  set document(title: a.title, author: if a.prepared-by != "" { a.prepared-by } else { brand.org-name })

  set page(
    ..geom,
    background: status-watermark(a.status),
    header: {
      set text(font: fonts.sans, size: sizes.micro, fill: ink-soft)
      grid(
        columns: (1fr, auto),
        align: (left + bottom, right + bottom),
        {
          if a.artifact-id != "" {
            text(font: fonts.mono, weight: 600, a.artifact-id)
            [ #h(4pt) · #h(4pt) ]
          }
          a.title
        },
        status-chip(a.status, size: 6pt),
      )
      v(2pt)
      line(length: 100%, stroke: 0.5pt + rule-col)
    },
    footer: {
      line(length: 100%, stroke: 0.5pt + rule-col)
      v(2pt)
      set text(font: fonts.sans, size: sizes.micro, fill: ink-soft)
      grid(
        columns: (1fr, auto, 1fr),
        align: (left, center, right),
        confidentiality-label(a.confidentiality),
        context {
          let cur = counter(page).get().first()
          let tot = counter(page).final().first()
          [Page #cur of #tot]
        },
        {
          if a.issue-id != "" { a.issue-id }
          if a.revision != "" { [ rev #a.revision] }
        },
      )
    },
  )

  set text(font: fonts.serif, size: sizes.body, fill: ink, lang: "en", region: "us")
  set par(justify: true, leading: 0.65em, spacing: 0.9em)
  set heading(numbering: if numbered-headings { "1.1" } else { none })
  set table(fill: none)

  show heading.where(level: 1): it => block(width: 100%, above: 20pt, below: 10pt, {
    line(length: 100%, stroke: 0.8pt + accent)
    v(5pt)
    text(font: fonts.sans, size: sizes.h1, weight: 700, it)
  })
  show heading.where(level: 2): it => block(above: 15pt, below: 7pt,
    text(font: fonts.sans, size: sizes.h2, weight: 700, it))
  show heading.where(level: 3): it => block(above: 11pt, below: 5pt,
    text(font: fonts.sans, size: sizes.h3, weight: 600, fill: ink-soft, it))
  show link: it => text(fill: accent, it)
  show raw: set text(font: fonts.mono, size: sizes.small)

  if cover {
    artifact-title-page(a, doc-class: doc-class)
    counter(page).update(1)
  }

  // Restate status at the head of the body. A reader who opens to page 1
  // without the cover still learns the document is not approved.
  if preamble {
    if not st.final {
      status-banner(a.status)
      v(10pt)
    }
    if a.source-as-of != "" {
      as-of(a.source-as-of)
      v(10pt)
    }
  }

  if toc {
    show outline.entry.where(level: 1): it => text(weight: 700, it)
    outline(title: "Contents", depth: toc-depth, indent: 1em)
    v(10pt)
  }

  body
}
