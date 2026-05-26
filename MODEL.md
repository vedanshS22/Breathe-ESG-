# MODEL.md

## Data Model Rationale

The model is organized around the lifecycle of operational ESG data:

```text
Company -> DataSource -> RawUpload -> EmissionRecord -> AuditLog
                         |
                         -> IngestionIssue
```

The central rule is that raw operational evidence must remain separate from normalized review records. Uploads are source-of-truth artifacts; emission records are the canonical analyst-facing representation.

## Entities

### Company

Represents the tenant boundary. Every source, upload, record, issue, and audit event is reachable through a company. Even though authentication is intentionally light in this prototype, the schema keeps multi-tenancy explicit so the app does not have to be redesigned later.

### DataSource

Represents a source type for a company: `sap`, `utility`, or `travel`.

This is separated from `EmissionRecord.source_type` so the app can later attach source-specific configuration, credentials, lookup tables, or operational health metadata without changing every record.

### RawUpload

Stores the uploaded artifact and ingestion metadata:

- original filename
- file size
- content type
- upload timestamp
- ingestion status
- row counts
- success/failure counts

The uploaded file is preserved before parsing or normalization. This supports audit traceability, reprocessing, and debugging.

### EmissionRecord

The canonical normalized record. All sources normalize into the same operational contract:

- `scope`
- `category`
- `quantity`
- `normalized_unit`
- `start_date`
- `end_date`
- `source_type`
- `raw_data`
- `metadata`
- `is_suspicious`
- `suspicious_reason`
- `status`
- `locked`

`raw_data` preserves the row-level source payload. `metadata` carries source-specific details such as SAP plant code, utility meter ID, travel airport pair, and normalization warnings.

Records include direct links to `Company`, `DataSource`, and `RawUpload`. This makes every normalized row traceable back to the source artifact that produced it.

### IngestionIssue

Captures row-level failures or whole-file parsing problems. Analysts need to see what failed, not only what normalized successfully.

Fields include:

- upload reference
- stage: parsing, normalization, validation, persistence
- row number
- message
- raw row payload

### AuditLog

Append-only mutation history for analyst actions. Approval and rejection write old/new values, actor, action, and timestamp.

Approved records become `locked = true`. Locking is enforced in the review service so approved rows cannot be rejected or mutated through workflow endpoints.

## Scope Categorization

Scope is assigned during normalization, not trusted from upstream systems:

- SAP fuel/procurement flat file -> Scope 1
- Utility electricity portal export -> Scope 2
- Corporate travel export -> Scope 3

This keeps scope classification deterministic and backend-owned.

## Unit Normalization

Common units are normalized centrally:

- `L`, `ltr`, `litre`, `liters` -> `liters`
- `kWh`, `kilowatt hour` -> `kwh`
- `km`, `kilometers` -> `km`
- `night`, `nights` -> `nights`

Unknown units are not discarded. They are preserved and flagged suspicious for analyst review.

## Audit Trail

Auditability exists at three levels:

1. Raw file preservation through `RawUpload`
2. Row-level fidelity through `EmissionRecord.raw_data`
3. Workflow mutation history through `AuditLog`

This is deliberately heavier than a simple CRUD schema because ESG reporting needs evidence and reproducibility, not just current values.

