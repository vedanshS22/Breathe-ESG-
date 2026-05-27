# TRADEOFFS.md

## 1. No Live Enterprise Integrations

I did not build live SAP, utility, Concur, or Navan connectors.

Why:

- They require tenant credentials, OAuth scopes, network allowlists, sandbox access, and customer-specific setup.
- The assignment evaluates ingestion architecture and judgment more than connector plumbing.
- Parser/normalizer boundaries make live connectors addable later.

## 2. No CO2e Calculation Engine

I did not calculate final emissions totals.

Why:

- The hard part here is source normalization, provenance, categorization, and review.
- Emission factors vary by geography, period, method, and category.
- Factor versioning should be added after activity records are trustworthy.

## 3. No PDF/OCR Utility Bill Extraction

I did not parse PDF bills.

Why:

- PDF layouts vary heavily across utilities.
- OCR confidence and table extraction would dominate the prototype risk.
- Utility portal CSV is a cleaner first ingestion surface.

Later work:

- PDF template classification
- extraction coordinates
- manual confidence review
- reconciliation against meter/account IDs
