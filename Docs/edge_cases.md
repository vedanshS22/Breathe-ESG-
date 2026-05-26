```

```

```
# Edge Cases & Failure Semantics
## Breathe ESG — Operational Failure Handling Specification

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- anticipated operational edge cases
- ingestion failure scenarios
- normalization inconsistencies
- transactional risks
- analyst workflow conflicts
- deployment failure modes
- expected system behavior under abnormal conditions

This is NOT merely a debugging checklist.

This document defines:
# operational failure semantics.

The purpose is to ensure the platform behaves:
- predictably
- safely
- traceably
- consistently

under non-ideal operational conditions.

Enterprise operational data is inherently messy.

The system must therefore assume:
- malformed inputs
- inconsistent exports
- operational anomalies
- partial corruption
- invalid business data
- human mistakes

from the beginning.

---

# 2. Failure Handling Philosophy

The platform intentionally prioritizes:
# ingestion continuity over aggressive rejection.

This is a very important architectural decision.

The system should prefer:
```text id="e1edge"
ingest
    ↓
flag
    ↓
review
```

rather than:

```

```

```
reject entire uploads aggressively.
```

Reason:  
  
real enterprise operational systems contain noisy data constantly.

Destroying ingestion continuity because a few rows are malformed is operationally unrealistic.

The platform should therefore:

-   
preserve source data  

-   
isolate failures  

-   
surface anomalies  

-   
escalate suspicious records to analysts  


instead of silently discarding operational information.

---

# 3. Ingestion Layer Edge Cases

The ingestion boundary is the first operational trust boundary in the platform.

The ingestion layer must assume uploaded artifacts may be:

-   
invalid  

-   
incomplete  

-   
corrupted  

-   
incorrectly formatted  

-   
operationally inconsistent  


---

# 3.1 Unsupported File Types

## Scenario

User uploads:

```

```

```
PDF
XLSX
DOCX
```

instead of supported formats.

---

# Risk

The parser pipeline expects structured ingestion formats.

Unexpected formats can:

-   
break parsing assumptions  

-   
generate inconsistent workflows  

-   
produce ambiguous failures  


---

# Expected Behavior

The system should:

-   
reject unsupported formats early  

-   
preserve error traceability  

-   
avoid partial ingestion attempts  


---

# Expected Response

```

```

```
{
  "error": "Unsupported file type"
}
```

---

# Architectural Rule

Validation should occur:

# before persistence orchestration begins.

---

# 3.2 Empty File Uploads

## Scenario

User uploads:

```

```

```
0-byte CSV
```

or structurally empty file.

---

# Risk

The ingestion pipeline may:

-   
parse successfully  

-   
produce zero operational rows  

-   
create misleading ingestion state  


---

# Expected Behavior

The platform should:

-   
reject structurally empty uploads  

-   
preserve upload failure visibility  

-   
avoid creating meaningless ingestion records  


---

# Expected Operational Result

```

```

```
Upload rejected with deterministic error state
```

---

# 3.3 Corrupted Upload Streams

## Scenario

Upload interrupted during transfer.

---

# Risk

Partial uploads may:

-   
create invalid files  

-   
break parser assumptions  

-   
corrupt ingestion lifecycle  


---

# Expected Behavior

The platform should:

-   
abort upload safely  

-   
avoid partial persistence  

-   
preserve transactional integrity  


No partial RawUpload records should remain.

---

# 3.4 Oversized Uploads

## Scenario

Large operational exports exceed memory thresholds.

---

# Risk

Potential:

-   
memory exhaustion  

-   
parser crashes  

-   
degraded platform performance  


---

# Expected Behavior

The MVP should:

-   
reject uploads above configured threshold  

-   
fail gracefully  

-   
preserve platform stability  


Future scalability:

-   
chunked ingestion  

-   
streaming uploads  


but intentionally excluded from MVP scope.

---

# 3.5 Duplicate Uploads

## Scenario

Same operational export uploaded multiple times.

---

# Risk

Potential:

-   
duplicated operational records  

-   
inflated emissions activity  

-   
analyst confusion  


---

# Expected Behavior

The platform should:

-   
allow deterministic duplicate handling  

-   
optionally flag duplicate uploads  

-   
preserve ingestion traceability  


The system should never silently deduplicate operational data automatically.

Reason:  
  
duplicate uploads may sometimes be operationally intentional.

---

# 4. Parsing Layer Edge Cases

The parsing layer must assume:

# upstream operational exports are structurally unreliable.

---

# 4.1 Inconsistent Delimiters

## Scenario

SAP export uses:

```

```

```
;
```

instead of:

```

```

```
,
```

---

# Risk

Parser misreads entire operational structure.

---

# Expected Behavior

The parser should:

-   
detect delimiters automatically  
  
OR  

-   
fail with deterministic parser error  


The parser should never silently misinterpret structure.

---

# 4.2 Invalid Encodings

## Scenario

Operational export encoded using:

```

```

```
latin1
cp1252
```

instead of UTF-8.

---

# Risk

Character corruption.

Examples:

-   
localized fuel names  

-   
analyst comments  

-   
vendor names  


---

# Expected Behavior

The parser should:

-   
attempt encoding fallback  

-   
preserve parsing traceability  

-   
surface deterministic failures  


---

# 4.3 Missing Required Columns

## Scenario

Expected:

```

```

```
Qty
```

Actual:

```

```

```
missing
```

---

# Risk

Normalization pipeline cannot infer operational meaning reliably.

---

# Expected Behavior

The platform should:

-   
isolate parsing failure  

-   
surface missing-column diagnostics  

-   
preserve upload traceability  


---

# 4.4 Duplicate Headers

## Scenario

CSV contains:

```

```

```
Qty,Qty,UOM
```

---

# Risk

Ambiguous operational mapping.

---

# Expected Behavior

The parser should:

-   
normalize safely  
  
OR  

-   
reject deterministically  


Silent ambiguity is forbidden.

---

# 4.5 Partial Row Corruption

## Scenario

Rows 1-100 valid.

Row 101 malformed.

Rows 102+ valid.

---

# Risk

Entire ingestion aborted unnecessarily.

---

# Expected Behavior

The parser should:

-   
isolate malformed rows  

-   
continue parsing remaining rows  

-   
preserve operational continuity  


---

# 5. Normalization Layer Edge Cases

The normalization layer assumes:

# upstream operational semantics are inconsistent.

---

# 5.1 Mixed Unit Representations

## Scenario

Same operational meaning expressed as:

```

```

```
L
ltr
Liters
litre
```

---

# Risk

Fragmented analytics and inconsistent reporting.

---

# Expected Behavior

All units normalize into:

```

```

```
liters
```

through centralized mapping.

---

# 5.2 Unknown Operational Categories

## Scenario

Unexpected value:

```

```

```
BioFuel-X
```

---

# Risk

Normalization mapping incomplete.

---

# Expected Behavior

The platform should:

-   
preserve original value  

-   
apply fallback category  

-   
surface analyst visibility  


The system should never silently discard unknown operational values.

---

# 5.3 Invalid Dates

## Scenario

```

```

```
32/13/2026
```

---

# Risk

Impossible operational chronology.

---

# Expected Behavior

The record should:

-   
remain traceable  

-   
become suspicious  

-   
surface to analysts  


---

# 5.4 Missing Quantity

## Scenario

```

```

```
{
  "Qty": null
}
```

---

# Risk

Operational activity incomplete.

---

# Expected Behavior

The system should:

-   
partially normalize  

-   
flag suspicious  

-   
preserve source payload  


NOT:

```

```

```
abort ingestion entirely.
```

---

# 5.5 Unknown Scope Classification

## Scenario

Normalization cannot confidently infer:

```

```

```
Scope 1 / 2 / 3
```

---

# Risk

Incorrect emissions classification.

---

# Expected Behavior

The system should:

-   
fallback safely  

-   
preserve analyst visibility  

-   
avoid silent assumptions  


---

# 6. Validation Layer Edge Cases

Validation exists because:

# enterprise operational data contains anomalies constantly.

---

# 6.1 Negative Quantities

## Scenario

```

```

```
-5000 kWh
```

---

# Risk

Impossible operational activity.

---

# Expected Behavior

Flag suspicious immediately.

---

# 6.2 Extremely High Usage

## Scenario

```

```

```
999999999 kWh
```

---

# Risk

Potential:

-   
unit mismatch  

-   
operational corruption  

-   
parser issue  


---

# Expected Behavior

The record should:

-   
remain ingestible  

-   
become suspicious  

-   
require analyst review  


---

# 6.3 Invalid Airport Codes

## Scenario

```

```

```
from_airport = XXXINVALID
```

---

# Risk

Travel normalization unreliable.

---

# Expected Behavior

Flag suspicious while preserving source payload.

---

# 6.4 Missing Units

## Scenario

```

```

```
quantity = 5000
unit = null
```

---

# Risk

Operational meaning ambiguous.

---

# Expected Behavior

Flag for analyst review.

---

# 7. Persistence Layer Edge Cases

Persistence failures are operationally dangerous because they can corrupt:

-   
auditability  

-   
analyst trust  

-   
ingestion consistency  


---

# 7.1 Partial Transaction Failures

## Scenario

Rows 1-100 inserted.

Row 101 fails.

---

# Risk

Partial ingestion corruption.

---

# Expected Behavior

Entire transaction rollback.

---

# Architectural Rule

All ingestion persistence must occur inside:

```

```

```
transaction.atomic()
```

---

# 7.2 JSON Serialization Failures

## Scenario

Invalid raw payload structure.

---

# Risk

Persistence interruption.

---

# Expected Behavior

Reject operational write deterministically.

---

# 7.3 Database Connectivity Loss

## Scenario

PostgreSQL connection interruption.

---

# Risk

Inconsistent operational state.

---

# Expected Behavior

Rollback safely and preserve ingestion failure traceability.

---

# 8. Analyst Workflow Edge Cases

The platform assumes:

# human operational workflows are imperfect.

---

# 8.1 Concurrent Approvals

## Scenario

Two analysts approve same record simultaneously.

---

# Risk

Race conditions.

---

# Expected Behavior

Latest-state validation before mutation.

---

# 8.2 Editing Locked Records

## Scenario

Analyst attempts modifying approved record.

---

# Risk

Audit integrity corruption.

---

# Expected Behavior

Reject modification deterministically.

---

# 8.3 Rejecting Already Approved Record

## Scenario

State-transition conflict.

---

# Expected Behavior

Reject invalid transition.

---

# 9. Audit Layer Edge Cases

Audit history is compliance-sensitive.

---

# 9.1 Missing Actor Identity

## Scenario

Mutation triggered without authenticated user.

---

# Risk

Non-attributable operational changes.

---

# Expected Behavior

Reject mutation.

---

# 9.2 Audit Write Failure

## Scenario

Operational mutation succeeds but audit insert fails.

---

# Risk

Invisible historical mutation.

---

# Expected Behavior

Rollback entire mutation transaction.

---

# 10. Deployment Edge Cases

Production introduces operational failures absent locally.

---

# 10.1 Missing Environment Variables

## Scenario

DATABASE_URL missing.

---

# Expected Behavior

Fail-fast startup behavior.

---

# 10.2 Broken Upload Storage Paths

## Scenario

Uploads directory inaccessible.

---

# Expected Behavior

Startup storage validation failure.

---

# 10.3 CORS Misconfiguration

## Scenario

Frontend blocked from backend APIs.

---

# Expected Behavior

Environment-specific CORS configuration.

---

# 10.4 Production Database Limits

## Scenario

Connection exhaustion.

---

# Expected Behavior

Graceful DB connection handling.

---

# 11. Failure Handling Invariants

The following rules must never be violated.

---

# Invariant 1

```

```

```
Raw source data must never be silently discarded.
```

---

# Invariant 2

```

```

```
Validation failures must not destroy ingestion continuity unnecessarily.
```

---

# Invariant 3

```

```

```
Partial transactional corruption must be prevented.
```

---

# Invariant 4

```

```

```
Suspicious operational records must remain analyst-visible.
```

---

# Invariant 5

```

```

```
Approved records must remain immutable.
```

---

# 12. Final Failure Philosophy

This platform should behave like:

# operational enterprise software under imperfect real-world conditions.

The system intentionally assumes:

-   
operational noise  

-   
malformed exports  

-   
inconsistent upstream systems  

-   
human mistakes  

-   
infrastructure failures  


The architecture therefore prioritizes:

-   
graceful degradation  

-   
deterministic failures  

-   
traceability  

-   
ingestion continuity  

-   
operational visibility  


over:

-   
aggressive rejection  

-   
silent failure  

-   
hidden mutation  

-   
brittle assumptions  


The strongest operational system is not the system that never encounters bad data.

It is the system that behaves predictably when bad data inevitably appears.