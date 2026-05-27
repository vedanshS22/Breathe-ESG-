# DECISIONS.md

## Ambiguity: What Counts As SAP Data?

I chose SAP material-document style flat files instead of live SAP APIs.

Why:

- Enterprise SAP access is tenant-specific and credentialed.
- A flat-file export is common during onboarding and implementation.
- It still exposes real SAP messiness: plant codes, posting dates, material document IDs, localized headers, quantities, and units.

Why German SAP fields:

- Many SAP operational exports use localized/custom ABAP report labels.
- German field names like `Werk`, `Buchungsdatum`, `Kraftstoff`, `Menge`, and `Einheit` demonstrate that the parser cannot assume polished English SaaS headers.

Handled subset:

- plant
- posting date
- material document
- fuel type
- quantity
- unit

Ignored:

- movement type semantics
- material master lookup
- PO joins
- live OData/BAPI auth

PM question:

- Which actual SAP object will customers provide: material documents, purchase orders, goods movement reports, or a custom export?

## Ambiguity: Utility Bills Or Utility Usage?

I chose utility portal CSV exports rather than PDF bill extraction.

Why:

- CSV demonstrates ingestion, validation, meter identity, billing periods, and kWh normalization without turning the prototype into OCR.
- Real utility portals often let business customers export usage tables.

Handled subset:

- meter/account
- billing start/end
- kWh usage
- tariff/rate label

Ignored:

- PDF/OCR
- demand charges
- taxes
- interval-load data
- Green Button XML parser

PM question:

- Are we ingesting monthly billing summaries, interval usage exports, or final invoices?

## Ambiguity: Travel Source Shape

I chose a corporate travel/expense platform export.

Why:

- Concur/Navan-style APIs are enterprise credentialed.
- CSV/JSON export is realistic for a prototype and still tests category mapping.
- Flights, hotels, and ground travel require different normalization.

Why airport-code travel model:

- Travel exports often contain origin/destination airport codes even when distance is missing.
- Airport pairs are enough to demonstrate Scope 3 inference and distance fallback.

Handled subset:

- flight distance or airport pair
- hotel nights
- ground/rail/taxi distance
- trip IDs and dates

Ignored:

- cabin class
- layovers
- radiative forcing
- employee identity
- emission-factor calculation

PM question:

- Should this normalize activity only, or calculate CO2e using cabin class, route, country, and factor year?

## Ambiguity: Dropdown Or Auto Categorization?

I kept both:

- Manual mode: analyst selects SAP, Utility, or Travel from the dropdown.
- Auto AI mode: backend inspects headers/file format and infers source type plus Scope 1/2/3 path.

Why:

- Analysts need control when source files are known.
- Auto mode helps when files arrive from mixed operational teams.
- The decision is stored in metadata so auditors can see whether categorization was manual or inferred.

## Ambiguity: What Is Suspicious?

Suspicious rows are ingested, not rejected.

Why:

- ESG data is messy.
- Analysts need evidence and review queues.
- One bad row should not block a full upload.

Hard failures are reserved for empty files, unsupported file types, missing required structural columns, and impossible parsing.
