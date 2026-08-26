// theme.typ — page geometry, typography, and branding placeholders.
//
// Branding is intentionally neutral. Replace the `brand` values (and set `logo`
// to an `image(...)`) when visual identity is decided. Nothing else in the
// library hardcodes a colour or a name.

#let brand = (
  org-name:   "[ORGANIZATION NAME]",
  org-unit:   "[PROGRAM / DIVISION]",
  address:    "[STREET ADDRESS, CITY, STATE ZIP]",
  contact:    "[CONTACT NAME, EMAIL, PHONE]",
  logo:       none,          // e.g. image("../assets/logo.svg", width: 34mm)
  logo-width: 34mm,
)

// Only families verified present on the build machine are listed. Typst emits a
// warning for every unknown family in a fallback list, which would drown the
// real diagnostics in the compile gate. To adopt a licensed brand face later,
// install it and prepend it here.
#let fonts = (
  serif: ("Libertinus Serif", "New Computer Modern"),
  sans:  ("Helvetica Neue", "Helvetica", "Arial"),
  mono:  ("Menlo", "DejaVu Sans Mono", "Courier New"),
)

#let sizes = (
  title:  22pt,
  h1:     14pt,
  h2:     11.5pt,
  h3:     10.5pt,
  body:   10.5pt,
  small:  9pt,
  micro:  7.5pt,
)

// Semantic tone ramp. `fg` = text/rule, `bg` = fill, `bd` = border.
#let tones = (
  neutral: (fg: rgb("#3f4854"), bg: rgb("#f2f4f6"), bd: rgb("#c5ced8")),
  info:    (fg: rgb("#14324f"), bg: rgb("#e8eef5"), bd: rgb("#9db4c9")),
  ok:      (fg: rgb("#1d5638"), bg: rgb("#e9f2ed"), bd: rgb("#9cc0ac")),
  warn:    (fg: rgb("#7d4b00"), bg: rgb("#fcf3e2"), bd: rgb("#d9b784")),
  stop:    (fg: rgb("#8a1f1f"), bg: rgb("#fbecec"), bd: rgb("#d9a5a5")),
)

#let tone-of(name) = if name in tones { tones.at(name) } else { tones.neutral }

#let accent    = tones.info.fg
#let rule-col  = rgb("#c5ced8")
#let ink       = rgb("#15181c")
#let ink-soft  = rgb("#5c6672")

// Page geometry presets.
#let geometry = (
  // Standard issued document.
  standard: (paper: "us-letter", margin: (top: 2.9cm, bottom: 2.4cm, left: 2.2cm, right: 2.2cm)),
  // Three-hole punched binder stock: extra gutter on the bind edge.
  binder:   (paper: "us-letter", margin: (top: 2.9cm, bottom: 2.4cm, left: 3.4cm, right: 1.8cm)),
  // Correspondence.
  letter:   (paper: "us-letter", margin: (top: 3.4cm, bottom: 2.6cm, left: 2.5cm, right: 2.5cm)),
  // Wide tabular schedules.
  wide:     (paper: "us-letter", flipped: true, margin: (top: 2.2cm, bottom: 2.0cm, left: 1.8cm, right: 1.8cm)),
)
