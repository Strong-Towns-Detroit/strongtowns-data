// letter.typ — correspondence. No cover page; letterhead only.

#import "../lib/lib.typ": *

#let letter(
  artifact: (:),
  date: "[DATE]",
  recipient: (),
  salutation: "Dear [NAME]:",
  closing: "Sincerely,",
  signer: "[NAME]",
  signer-title: "[TITLE]",
  enclosures: (),
  body,
) = {
  let a = merge-artifact(artifact)
  show: formal-doc.with(artifact: artifact, doc-class: "Letter",
                        geom: geometry.letter, cover: false, numbered-headings: false,
                        preamble: false)

  // Letterhead
  if brand.logo != none { brand.logo; v(4pt) }
  text(font: fonts.sans, size: sizes.h2, weight: 700, tracking: 0.4pt, brand.org-name)
  linebreak()
  text(font: fonts.sans, size: sizes.micro, fill: ink-soft, brand.address)
  v(3pt)
  line(length: 100%, stroke: 1pt + accent)
  v(16pt)

  // Status warning belongs below the letterhead, not above it -- but it must
  // still appear before the reader reaches the substance of the letter.
  if not status-is-final(a.status) {
    status-banner(a.status)
    v(14pt)
  }

  text(date)
  v(12pt)
  for l in recipient { l; linebreak() }
  v(12pt)
  salutation
  v(8pt)

  body

  v(16pt)
  closing
  v(30pt)
  line(length: 60mm, stroke: 0.5pt + ink)
  v(2pt)
  text(size: sizes.small, weight: 600, signer)
  linebreak()
  text(size: sizes.small, fill: ink-soft, signer-title)

  if enclosures != () {
    v(12pt)
    text(size: sizes.small, weight: 600, "Enclosures:")
    linebreak()
    for e in enclosures { text(size: sizes.small, [• #e]); linebreak() }
  }
}
