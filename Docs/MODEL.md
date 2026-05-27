# MODEL.md

## Model Shape

The product is multi-tenant from the first table:

```text
Company -> DataSource -> RawUpload -> EmissionRecord -> AuditLog
                         |
                         -> IngestionIssue
```

This is visible in the UI as `Company -> Upload -> Records`, and in the database through direct or reachable foreign keys. Every normalized row has a `company`, `source`, and `raw_upload`.

## Why These Entities

### Company

Company is the tenant boundary. Uploads, sources, records, issues, and audit logs must be explainable per customer. Authentication is light in this prototype, but the data model prevents cross-company mixing later.

### DataSource

DataSource represents one source type for one company: `sap`, `utility`, or `travel`. This leaves room for per-company credentials, mappings, parser settings, and sync health without rewriting records.

### RawUpload

RawUpload is the source-of-truth artifact. It stores file, original filename, size, content type, status, row counts, and timestamps. The normalized records are derived from this artifact, not a replacement for it.

### EmissionRecord

EmissionRecord is the canonical review row. It stores:

- tenant: `company`
- provenance: `source`, `raw_upload`, `source_row_number`, `source_reference`
- Scope 1/2/3 categorization: `scope`
- activity category: `category`
- normalized quantity and unit
- date range
- original row in `raw_data`
- source-specific and AI categorization notes in `metadata`
- review state: `status`, `locked`, approval/rejection timestamps

### IngestionIssue

IngestionIssue records parse, normalization, validation, and persistence failures without discarding the whole upload. Real ESG source data is noisy, so partial ingestion is intentional.

### AuditLog

AuditLog stores analyst actions. Approval locks the record, and rejection is blocked after lock. This creates a clear source-of-truth chain from raw file to review decision.

## Scope Categorization

The backend assigns scope:

- SAP fuel/procurement -> Scope 1
- Utility electricity -> Scope 2
- Corporate travel -> Scope 3

Manual mode uses the selected source dropdown. Auto AI mode infers source type from headers/file structure and stores the classifier decision in `metadata.categorization`.

## Unit Normalization

Common units are normalized centrally:

- `L`, `ltr`, `litre` -> `liters`
- `kWh`, `kilowatt hour` -> `kwh`
- `km`, `kilometers` -> `km`
- `mile`, `miles` -> `miles`
- `night`, `nights` -> `nights`

Unknown units are preserved and flagged suspicious rather than silently dropped.

## Separate Source Logic

Each source has isolated parser and normalizer files:

```text
services/parsers/sap_parser.py
services/parsers/utility_parser.py
services/parsers/travel_parser.py

services/normalizers/sap_normalizer.py
services/normalizers/utility_normalizer.py
services/normalizers/travel_normalizer.py
```

Validation is source-specific through `validators/registry.py`, `sap_validator.py`, `utility_validator.py`, and `travel_validator.py`, plus shared quantity validation.
