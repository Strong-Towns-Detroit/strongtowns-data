// binder.typ — closing or compliance binder. Wider bind-edge gutter, an index
// that drives the tabs, and a divider page per tab.

#import "../lib/lib.typ": *

#let binder(
  artifact: (:),
  binder-type: "[CLOSING / COMPLIANCE]",
  transaction: "[TRANSACTION OR OBLIGATION]",
  custodian: "[RECORD CUSTODIAN]",
  retention: "[RETENTION PERIOD]",
  tabs: (),
  body,
) = {
  show: formal-doc.with(artifact: artifact, doc-class: binder-type + " binder",
                        geom: geometry.binder, cover: true, toc: false)

  heading(level: 1)[Binder control]
  kv-table(
    ("Binder type", binder-type),
    ("Transaction / obligation", transaction),
    ("Record custodian", custodian),
    ("Retention period", retention),
  )
  v(10pt)

  note(title: "Completeness")[
    A binder is a record, not a summary. Every tab listed in the index must be present in the
    assembled PDF. A tab listed but not attached is a defect in the record, and is recorded
    here as #condition-chip("blocked") rather than omitted from the index.
  ]
  v(10pt)

  heading(level: 1)[Index of tabs]
  if tabs == () {
    unresolved(topic: "Empty binder index")[No tabs enumerated.]
  } else {
    attachment-index(..tabs.map(t => (t.tab, t.title, t.at("description", default: ""),
                                      t.at("pages", default: "—"),
                                      t.at("custodian", default: ""))))
  }

  body

  // One divider page per tab, in index order.
  for t in tabs {
    binder-divider(
      tab: t.tab,
      title: t.title,
      contents: t.at("contents", default: ()),
    )
  }
}
