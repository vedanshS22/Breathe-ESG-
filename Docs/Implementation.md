```

```

```
# Implementation Plan
## Breathe ESG — Incremental System Execution Strategy

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines the implementation sequencing strategy for the ESG ingestion and analyst review platform.

The purpose of the implementation plan is not task tracking.

Its purpose is to:
- establish execution order
- stabilize architecture incrementally
- isolate operational failures
- reduce rework
- validate assumptions phase-by-phase
- define deterministic success criteria
- define operational edge-case handling

The system should not be implemented feature-by-feature randomly.

The platform should be developed:
# pipeline-first.

Meaning:
- ingestion reliability first
- normalization consistency second
- persistence correctness third
- operational workflows fourth
- auditability last

because every downstream workflow depends entirely on upstream operational correctness.

---

# 2. System Execution Philosophy

The implementation order mirrors the lifecycle of operational data inside the platform.

The operational lifecycle is:

```text id="x1pln0"
Source Upload
    ↓
Raw File Preservation
    ↓
Row Parsing
    ↓
Normalization
    ↓
Validation
    ↓
Persistence
    ↓
Analyst Review
    ↓
Audit Logging
    ↓
Record Locking
```

The implementation sequence intentionally follows this same order.

This prevents:

-   
unstable APIs  

-   
frontend rework  

-   
inconsistent schemas  

-   
duplicated transformation logic  

-   
operational coupling  


Every phase must become operationally stable before the next phase begins.

---

# 3. Full Execution Roadmap

```

```

```
Phase 1  → Ingestion Boundary
Phase 2  → Parsing Layer
Phase 3  → Normalization Engine
Phase 4  → Persistence Layer
Phase 5  → Validation Engine
Phase 6  → Analyst Review APIs
Phase 7  → Frontend Operational UI
Phase 8  → Audit Logging
Phase 9  → Record Locking
Phase 10 → Deployment & Production Hardening
Phase 11 → Documentation Finalization
```

This order should not be changed.

---

# 4. Phase 1 — Ingestion Boundary

# Objective

Establish the system’s ability to safely receive and preserve operational source artifacts.

At this phase the platform is NOT yet concerned with:

-   
normalization  

-   
validation  

-   
analytics  

-   
dashboards  

-   
emissions logic  


The only responsibility is:

# safely accepting operational uploads.

---

# Why This Phase Exists

The uploaded source file itself is part of the audit trail.

The system must prove:

-   
uploaded artifacts are durable  

-   
uploads are traceable  

-   
ingestion failures are isolated  

-   
source preservation is guaranteed  


before any transformation begins.

Without reliable ingestion:

-   
auditability breaks  

-   
debugging becomes impossible  

-   
transformations become unreliable  


---

# Responsibilities

The ingestion layer owns:

-   
upload acceptance  

-   
file persistence  

-   
upload metadata  

-   
source-type identification  

-   
company ownership association  


The ingestion layer does NOT own:

-   
normalization  

-   
parsing semantics  

-   
suspicious detection  


---

# Expected API

```

```

```
POST /api/upload/
```

---

# Expected Internal Flow

```

```

```
Receive Upload
    ↓
Validate File Type
    ↓
Persist RawUpload
    ↓
Store Upload Metadata
    ↓
Return Upload Reference
```

---

# Expected Models

```

```

```
RawUpload
Company
DataSource
```

---

# Success Criteria

The phase is complete when:

-   
uploads persist reliably  

-   
files remain retrievable  

-   
source metadata is queryable  

-   
ingestion errors fail deterministically  

-   
upload lifecycle is traceable  


---

# Edge Cases

---

## Unsupported File Type

Example:

```

```

```
sample.pdf
```

Expected Behavior:  
  
Reject upload gracefully with validation error.

---

## Empty File Upload

Example:

```

```

```
0-byte CSV
```

Expected Behavior:  
  
Reject upload and preserve failure reason.

---

## Missing Source Type

Example:

```

```

```
{
  "file": "sap.csv"
}
```

Expected Behavior:  
  
Return request validation error.

---

## Large File Upload

Problem:  
  
Potential memory exhaustion.

Expected Behavior:  
  
Gracefully reject above configured size threshold.

---

## Corrupted Upload

Problem:  
  
Incomplete upload stream.

Expected Behavior:  
  
Abort persistence safely without partial records.

---

# Test Cases

---

## Test Case 1 — Valid SAP Upload

Input:  
  
Valid CSV.

Expected Result:

-   
file stored  

-   
metadata persisted  

-   
upload id returned  


---

## Test Case 2 — Invalid Extension

Input:  
  
PDF upload.

Expected Result:

-   
HTTP 400  

-   
no file persistence  


---

## Test Case 3 — Empty File

Input:  
  
Blank CSV.

Expected Result:

-   
ingestion rejected  

-   
error logged  


---

## Test Case 4 — Missing Company

Input:  
  
Invalid company id.

Expected Result:

-   
request rejected  

-   
no upload persisted  


---

# 5. Phase 2 — Parsing Layer

# Objective

Convert uploaded source artifacts into structured row-level operational objects.

At this phase:

-   
uploads already exist safely  

-   
source artifacts already persist  


Now the platform establishes:

# structured operational extraction.

---

# Why This Phase Exists

Parsing answers:

```

```

```
“What structurally exists inside the source artifact?”
```

NOT:

```

```

```
“What does the data operationally mean?”
```

Parsing is intentionally separated from normalization.

This creates:

-   
cleaner architecture  

-   
isolated failures  

-   
predictable transformations  

-   
easier debugging  


---

# Responsibilities

The parsing layer owns:

-   
CSV parsing  

-   
JSON parsing  

-   
delimiter handling  

-   
encoding handling  

-   
row extraction  


It does NOT own:

-   
scope assignment  

-   
category classification  

-   
validation  

-   
operational interpretation  


---

# Expected Output

```

```

```
[
  {
    "Fuel_Type": "Diesel",
    "Qty": 5000,
    "UOM": "L"
  }
]
```

At this stage records remain:

# source-native structures.

---

# Success Criteria

The phase is complete when:

-   
source rows extract reliably  

-   
malformed rows remain isolated  

-   
encoding variability is tolerated  

-   
parsing failures remain traceable  


---

# Edge Cases

---

## Inconsistent Delimiters

Example:

```

```

```
semicolon-separated SAP exports
```

Expected Behavior:  
  
Delimiter detection fallback.

---

## Invalid Encoding

Example:

```

```

```
latin1 SAP export
```

Expected Behavior:  
  
Fallback encoding strategy.

---

## Missing Columns

Example:

```

```

```
missing Qty column
```

Expected Behavior:  
  
Parser warning + structured failure.

---

## Duplicate Headers

Example:

```

```

```
Qty,Qty,UOM
```

Expected Behavior:  
  
Header normalization or rejection.

---

## Partial Corruption

Problem:  
  
Some rows malformed.

Expected Behavior:  
  
Continue parsing remaining rows.

---

# Test Cases

---

## Test Case 1 — Valid CSV Parsing

Expected Result:  
  
Rows extracted successfully.

---

## Test Case 2 — Malformed Row

Expected Result:  
  
Malformed row isolated without parser crash.

---

## Test Case 3 — Alternate Encoding

Expected Result:  
  
Rows parse correctly using fallback encoding.

---

## Test Case 4 — Missing Required Columns

Expected Result:  
  
Structured parsing error returned.

---

# 6. Phase 3 — Normalization Engine

# Objective

Transform heterogeneous source-native rows into canonical operational records.

This phase is:

# the conceptual core of the platform.

---

# Why This Phase Exists

Enterprise operational systems are structurally inconsistent.

Without normalization:

-   
validation fragments  

-   
analytics break  

-   
review workflows become unreliable  

-   
reporting loses consistency  


Normalization creates:

# operational coherence.

---

# Responsibilities

The normalization layer owns:

-   
canonical mapping  

-   
unit normalization  

-   
scope assignment  

-   
category assignment  

-   
date normalization  

-   
source standardization  


---

# Expected Internal Contract

```

```

```
{
  "scope": "",
  "category": "",
  "quantity": "",
  "normalized_unit": "",
  "date": ""
}
```

All operational sources must normalize into this shape.

---

# Expected Architecture

```

```

```
services/
    sap_normalizer.py
    utility_normalizer.py
    travel_normalizer.py
```

Normalization must remain:

# source-isolated.

---

# Success Criteria

The phase is complete when:

-   
all sources normalize consistently  

-   
scope assignment works reliably  

-   
units standardize deterministically  

-   
raw source fidelity remains preserved  


---

# Edge Cases

---

## Mixed Units

Examples:

```

```

```
L
ltr
Liters
```

Expected Behavior:  
  
Normalize into:

```

```

```
liters
```

---

## Invalid Dates

Example:

```

```

```
32/13/2026
```

Expected Behavior:  
  
Flag suspicious.

---

## Unknown Fuel Types

Example:

```

```

```
BioFuel-X
```

Expected Behavior:  
  
Fallback category assignment.

---

## Missing Quantity

Example:

```

```

```
Qty = null
```

Expected Behavior:  
  
Partial normalization + suspicious flag.

---

## Unexpected Column Names

Example:

```

```

```
Kraftstoff
```

Expected Behavior:  
  
Source-specific mapping fallback.

---

# Test Cases

---

## Test Case 1 — SAP Unit Normalization

Input:

```

```

```
L
```

Expected Result:

```

```

```
liters
```

---

## Test Case 2 — Travel Scope Assignment

Expected Result:

```

```

```
Scope 3
```

---

## Test Case 3 — Invalid Date

Expected Result:  
  
Suspicious flag generated.

---

## Test Case 4 — Unknown Unit

Expected Result:  
  
Normalization fallback + analyst visibility.

---

# 7. Phase 4 — Persistence Layer

# Objective

Persist normalized operational records into PostgreSQL.

At this phase:

-   
uploads work  

-   
parsing works  

-   
normalization works  


Now records become:

# durable operational entities.

---

# Why This Phase Exists

Operational ESG systems require:

-   
durable records  

-   
transactional guarantees  

-   
relational querying  

-   
audit traceability  


The persistence layer establishes:

# operational source of truth.

---

# Responsibilities

The persistence layer owns:

-   
database writes  

-   
transactional safety  

-   
relational integrity  

-   
raw payload preservation  


---

# Architectural Constraint

All persistence must occur inside:

```

```

```
transaction.atomic()
```

Reason:

-   
partial imports destroy operational trust  

-   
ingestion failures are common  

-   
audit consistency matters  


---

# Success Criteria

The phase is complete when:

-   
normalized records persist safely  

-   
transaction rollbacks work correctly  

-   
raw payloads remain preserved  

-   
ingestion consistency remains stable  


---

# Edge Cases

---

## Partial Transaction Failure

Problem:  
  
Row 98 fails during insert.

Expected Behavior:  
  
Rollback safely.

---

## Invalid JSON Serialization

Problem:  
  
Non-serializable raw payload.

Expected Behavior:  
  
Structured ingestion failure.

---

## Duplicate Uploads

Problem:  
  
Same file uploaded twice.

Expected Behavior:  
  
Allow or flag duplicate deterministically.

---

# Test Cases

---

## Test Case 1 — Valid Persistence

Expected Result:  
  
Records stored successfully.

---

## Test Case 2 — DB Failure

Expected Result:  
  
Transaction rollback.

---

## Test Case 3 — Invalid Raw Payload

Expected Result:  
  
Serialization failure handled gracefully.

---

# 8. Phase 5 — Validation Engine

# Objective

Detect suspicious operational anomalies.

The platform assumes:

# enterprise operational data is noisy.

Validation exists to surface anomalies without destroying ingestion continuity.

---

# Responsibilities

The validation layer owns:

-   
suspicious detection  

-   
anomaly rules  

-   
operational warnings  


Validation does NOT own:

-   
parsing  

-   
normalization  

-   
persistence  


---

# Example Validation Rules

Examples:

-   
negative quantity  

-   
impossible dates  

-   
abnormal electricity spikes  

-   
invalid airport codes  

-   
missing units  


---

# Success Criteria

The phase is complete when:

-   
suspicious records become identifiable  

-   
anomalies remain analyst-visible  

-   
ingestion continuity remains stable  


---

# Edge Cases

---

## Extremely High Usage

Problem:  
  
Potential unit mismatch.

Expected Behavior:  
  
Suspicious flag.

---

## Negative Consumption

Problem:  
  
Impossible operational behavior.

Expected Behavior:  
  
Flag for review.

---

## Missing Units

Expected Behavior:  
  
Analyst-visible warning.

---

## Invalid Airport Codes

Expected Behavior:  
  
Travel validation warning.

---

# Test Cases

---

## Test Case 1 — Negative Quantity

Expected Result:  
  
Record flagged suspicious.

---

## Test Case 2 — Huge Electricity Usage

Expected Result:  
  
Suspicious anomaly warning.

---

## Test Case 3 — Missing Unit

Expected Result:  
  
Validation warning generated.

---

# 9. Phase 6 — Analyst Review APIs

# Objective

Expose operational review workflows.

At this stage the system becomes:

# analyst-operable.

---

# Responsibilities

The review layer owns:

-   
pending queues  

-   
suspicious queues  

-   
approvals  

-   
rejections  


---

# Expected APIs

```

```

```
GET /api/records/pending/
GET /api/records/suspicious/
POST /api/records/{id}/approve/
POST /api/records/{id}/reject/
```

---

# Success Criteria

The phase is complete when:

-   
analysts can review records  

-   
suspicious rows are visible  

-   
approval state transitions work correctly  


---

# Edge Cases

---

## Approving Locked Record

Expected Behavior:  
  
Reject mutation.

---

## Concurrent Analyst Actions

Expected Behavior:  
  
Latest-state validation.

---

## Missing Record ID

Expected Behavior:  
  
404 response.

---

# Test Cases

---

## Test Case 1 — Approve Record

Expected Result:  
  
Status changes to approved.

---

## Test Case 2 — Reject Record

Expected Result:  
  
Status changes to rejected.

---

## Test Case 3 — Invalid Record

Expected Result:  
  
404 returned.

---

# 10. Phase 7 — Frontend Operational UI

# Objective

Expose operational workflows to analysts through a usable interface.

---

# Responsibilities

Frontend owns:

-   
upload flow  

-   
review queue  

-   
suspicious indicators  

-   
approval actions  


---

# Success Criteria

The phase is complete when:

-   
uploads work end-to-end  

-   
analysts can review records  

-   
operational workflows remain usable  


---

# Edge Cases

---

## Empty Review Queue

Expected Behavior:  
  
Graceful empty state.

---

## Network Failure

Expected Behavior:  
  
Retry/error handling.

---

## Slow API Response

Expected Behavior:  
  
Loading indicators.

---

# Test Cases

---

## Test Case 1 — Upload CSV

Expected Result:  
  
Records appear in review queue.

---

## Test Case 2 — Approve Via UI

Expected Result:  
  
Status updates correctly.

---

# 11. Phase 8 — Audit Logging

# Objective

Track immutable operational history.

---

# Responsibilities

Audit logging owns:

-   
mutation history  

-   
analyst accountability  

-   
historical reconstruction  


---

# Success Criteria

The phase is complete when:

-   
all material mutations generate logs  

-   
audit history becomes queryable  


---

# Edge Cases

---

## Missing User Identity

Expected Behavior:  
  
Reject mutation.

---

## Audit Write Failure

Expected Behavior:  
  
Rollback operational change.

---

# Test Cases

---

## Test Case 1 — Approval Audit Log

Expected Result:  
  
Audit entry created.

---

## Test Case 2 — Edit Audit Log

Expected Result:  
  
Old/new values preserved.

---

# 12. Phase 9 — Record Locking

# Objective

Prevent post-approval mutation.

---

# Success Criteria

The phase is complete when:

-   
approved records become immutable  

-   
edit attempts fail deterministically  


---

# Edge Cases

---

## Edit Locked Record

Expected Behavior:  
  
Mutation blocked.

---

## Delete Locked Record

Expected Behavior:  
  
Operation rejected.

---

# Test Cases

---

## Test Case 1 — Modify Approved Record

Expected Result:  
  
Validation error returned.

---

# 13. Phase 10 — Deployment & Production Hardening

# Objective

Deploy stable production-accessible system.

---

# Success Criteria

The phase is complete when:

-   
uploads work in production  

-   
APIs function externally  

-   
DB connectivity remains stable  


---

# Edge Cases

---

## Missing Environment Variables

Expected Behavior:  
  
Fail-fast startup validation.

---

## Broken Upload Paths

Expected Behavior:  
  
Startup storage verification.

---

## CORS Errors

Expected Behavior:  
  
Resolved through environment config.

---

# Test Cases

---

## Test Case 1 — Production Upload

Expected Result:  
  
Upload works externally.

---

## Test Case 2 — API Connectivity

Expected Result:  
  
Frontend/backend communicate successfully.

---

# 14. Final Implementation Philosophy

The platform should ultimately be implemented as:

-   
a stable ingestion pipeline  

-   
a deterministic normalization engine  

-   
an operational analyst review system  

-   
an auditability-first architecture  


The implementation intentionally prioritizes:

-   
operational correctness  

-   
deterministic behavior  

-   
architectural clarity  

-   
traceability  

-   
explainability  


over:

-   
unnecessary abstraction  

-   
infrastructure complexity  

-   
premature scaling  

-   
feature quantity  


The strongest implementation is not the most complex system.

It is the most operationally coherent system.

