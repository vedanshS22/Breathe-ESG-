# TRADEOFFS.md

## 1. No PDF Utility Bill Extraction

I did not build PDF parsing or OCR for utility bills.

Why:

- PDF bills vary wildly by utility.
- OCR would become the riskiest part of the prototype.
- The assignment is about judgment, and utility portal CSV/Green Button-like exports are a cleaner way to demonstrate ingestion, billing periods, units, and suspicious usage.

What would be needed later:

- PDF template classification
- table extraction
- manual review of extraction confidence
- source file page/coordinate traceability

## 2. No Live SAP, Concur, or Navan API Connections

I did not build live enterprise API pulls.

Why:

- Real integrations require credentials, scopes, tenant setup, and legal/customer access.
- A prototype should prove the internal pipeline before external integration work.
- The parser/normalizer boundaries are source-isolated, so API pulls can be added later without rewriting downstream review workflows.

What would be needed later:

- credential storage
- scheduled pulls
- retry and rate-limit handling
- source sync state
- idempotency keys

## 3. No Carbon Emissions Calculation Engine

I did not calculate CO2e totals.

Why:

- The assignment explicitly says the hard part is not computing carbon.
- Activity normalization, auditability, and analyst signoff need to be trustworthy before emissions factors are applied.
- Emission factors vary by geography, fuel type, year, electricity grid region, travel mode, cabin class, and methodology.

What would be needed later:

- factor datasets
- versioned factor selection
- calculation provenance
- recalculation workflows when factors change

