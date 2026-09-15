# BZA intake dates

The first recorded hearing is not the application filing date.

A BZA docket export can provide application, hearing, and disposition dates.
Request the case number, address, parcel, filing date, BSEED referral date,
completeness date, hearings, postponements, and final disposition. Keep these
dates separate when calculating how long a case took.

Accela's `openedDate` is a possible intake date. Confirm that the permit record
matches the BZA case before using it. A matching address alone is insufficient;
one property can have several unrelated permits.

The [intake lookup](bza-maintenance.md#add-project-types-and-intake-candidates)
produces `intake_date_candidates.csv`. Review the address, case number, record
type, and supporting evidence, including rows labeled `strong_candidate`.
Set `ACCELA_APP_ID` or `ACCELA_ACCESS_TOKEN` before running the lookup.
