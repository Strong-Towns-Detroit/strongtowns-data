// stage-gate-package.typ — the evidence package supporting a go/no-go decision
// at a defined stage gate.

#import "../lib/lib.typ": *

#let gate-decisions = (
  "pass":        (label: "PASS", tone: "ok"),
  "conditional": (label: "CONDITIONAL PASS — WAIVER RECORDED", tone: "warn"),
  "fail":        (label: "FAIL", tone: "stop"),
  "deferred":    (label: "DEFERRED — NOT DECIDED", tone: "neutral"),
  "pending":     (label: "PENDING DECISION", tone: "stop"),
)

#let gate-decision-chip(d) = {
  let k = lower(str(d)).replace("_", "-")
  let s = if k in gate-decisions { gate-decisions.at(k) } else {
    (label: "UNRECOGNISED (" + upper(str(d)) + ")", tone: "stop")
  }
  let t = tone-of(s.tone)
  box(inset: (x: 6pt, y: 3pt), radius: 2pt, fill: t.bg, stroke: 0.6pt + t.bd,
      text(font: fonts.sans, size: sizes.small, weight: 700, fill: t.fg,
           tracking: 0.5pt, s.label))
}

#let stage-gate-package(
  artifact: (:),
  gate-id: "[GATE ID]",
  gate-name: "[GATE NAME]",
  accountable-owner: "[OWNER ROLE]",
  reviewers: (),
  waiver-authority: "[WAIVER AUTHORITY]",
  decision: "pending",
  decision-date: "",
  required-artifacts: (),
  blockers: (),
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: "Stage-gate package",
                        cover: true, toc: false)

  heading(level: 1)[Gate identification]
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    kv-table(
      ("Gate", gate-id + " — " + gate-name),
      ("Accountable owner", accountable-owner),
      ("Reviewers", if reviewers == () { "[REVIEWERS]" } else { reviewers.join("; ") }),
    ),
    kv-table(
      ("Waiver authority", waiver-authority),
      ("Decision", gate-decision-chip(decision)),
      ("Decision date", if decision-date == "" { "—" } else { decision-date }),
    ),
  )
  v(10pt)

  heading(level: 1)[Required evidence]
  text(size: sizes.small)[
    The gate cannot pass while any row below is absent, silently unknown, missing a required
    professional review, or citing a requirement without source support.
  ]
  v(6pt)
  if required-artifacts == () {
    unresolved(topic: "Required evidence not enumerated")[
      This package lists no required artifacts. A gate with no stated evidence requirement
      cannot be evaluated and must not be recorded as passed.
    ]
  } else {
    checklist(..required-artifacts)
  }
  v(10pt)

  heading(level: 1)[Open blockers]
  if blockers == () {
    note[No blockers recorded. Confirm this is a finding, not an omission.]
  } else {
    risk-table(..blockers)
  }
  v(10pt)

  body

  pagebreak()
  heading(level: 1)[Gate decision and signature]
  block(width: 100%, inset: 10pt, stroke: 0.6pt + rule-col, radius: 3pt, {
    text(font: fonts.sans, size: sizes.small, weight: 600, "Decision recorded: ")
    gate-decision-chip(decision)
    v(8pt)
    text(size: sizes.micro, fill: ink-soft)[
      A conditional pass requires the waiver authority named above to sign, and the waived
      condition to be carried forward to the next gate as an open item.
    ]
  })
  v(10pt)
  approval-table(
    ("Preparer", "", "Evidence assembled and verified complete", "", ""),
    ("Reviewer", "", "Technical adequacy of evidence", "", ""),
    ("Decision authority", "", "Gate decision on behalf of Company", "", ""),
  )
}
