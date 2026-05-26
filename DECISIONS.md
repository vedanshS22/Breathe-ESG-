# DECISIONS.md

## 1. SAP Ingestion Mechanism

I chose SAP material-document style flat-file CSV uploads, not live OData/BAPI integration.

Why:

- The assignment is a four-day prototype.
- Enterprise SAP access requires credentials, network allowlists, and tenant-specific customization.
- A flat-file export is realistic for analyst onboarding and can still represent SAP messiness: plant codes, material document references, quantity/unit fields, German headers, and hostile date formats.

Subset handled:

- fuel/procurement rows with plant, posting date, material document, fuel type, quantity, and unit.

Ignored:

- live SAP authentication
- plant lookup master data
- movement-type-specific semantics
- purchase order joins

Question for PM:

- Which SAP object is the client actually giving us: material documents, purchase orders, goods movements, or a custom ABAP report?

## 2. Utility Ingestion Mechanism

I chose utility portal CSV exports rather than PDF bill extraction.

Why:

- CSV is more realistic for a prototype ingestion pipeline than OCR/PDF parsing.
- Utility usage exports commonly include meter identifiers, usage units, and billing/interval periods.
- Billing periods do not always match calendar months, so the model uses `start_date` and `end_date`.

Subset handled:

- electricity consumption by meter and billing period.

Ignored:

- PDF bill OCR
- tariff cost calculation
- interval-load profiles
- demand charges
- taxes and riders

Question for PM:

- Are analysts uploading monthly billing summaries or interval Green Button-style exports?

## 3. Corporate Travel Ingestion Mechanism

I chose CSV/JSON export upload from a travel or expense platform.

Why:

- Concur/Navan-style integrations are usually credentialed enterprise integrations.
- CSV export lets the prototype demonstrate the hard part: category mapping and missing distance handling.
- Flights, hotels, and ground transport normalize differently, so one source still creates multiple operational categories.

Subset handled:

- flights, hotels, and ground transport.
- flights can estimate distance for a small known airport-pair table when distance is absent.

Ignored:

- full itinerary APIs
- cabin class
- radiative forcing or emission-factor selection
- employee identity workflows

Question for PM:

- Should the platform normalize travel activity only, or calculate emissions using cabin class, fare class, and country-specific factors?

## 4. Authentication

I did not build authentication or RBAC.

Why:

- The assignment grading emphasizes data model, source realism, decisions, and analyst workflow.
- Adding auth would consume time without improving the ingestion architecture.

Future:

- Add user accounts and tenant-scoped permissions before real deployment.

## 5. Suspicious Records

I treat suspicious records as ingestible review events, not hard failures.

Why:

- Real operational ESG data is noisy.
- Analysts need visibility into anomalies.
- Rejecting whole files because one row is bad destroys ingestion continuity.

Hard failures are reserved for unsupported source types, empty files, unsupported file extensions, and structurally ambiguous files such as duplicate headers.

## 6. Deployment

The repo includes a Render blueprint for the Django API. The React app can be deployed separately as a static site with `VITE_API_BASE_URL` pointed at the deployed backend.

Question for PM:

- Is a single deployed backend plus static frontend acceptable, or should the prototype be deployed as one combined service?

