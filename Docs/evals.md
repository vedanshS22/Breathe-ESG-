```

```

```
# Evaluation & Verification Specification
## Breathe ESG — System Validation Strategy

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- system verification strategy
- phase-by-phase validation rules
- operational correctness criteria
- ingestion validation standards
- normalization accuracy expectations
- workflow verification behavior
- acceptance testing philosophy

The purpose of evaluation is NOT:
# “does the app run?”

The purpose is:
# “does the platform behave operationally correctly under realistic conditions?”

The evaluation strategy intentionally focuses on:
- deterministic behavior
- operational consistency
- auditability
- traceability
- ingestion reliability
- normalization correctness
- workflow integrity

The system should be considered successful only if:
- operational flows remain coherent
- failure semantics remain predictable
- data lifecycle remains traceable
- analysts can trust the platform operationally

---

# 2. Evaluation Philosophy

The platform should be evaluated the same way enterprise operational systems are evaluated.

Meaning:
- not only happy paths
- not only UI visibility
- not only CRUD correctness

The evaluation strategy must verify:
- ingestion resilience
- transformation consistency
- failure isolation
- transaction safety
- operational recoverability
- audit integrity

The evaluation philosophy intentionally prioritizes:
# operational trustworthiness.

---

# 3. Evaluation Scope

The following layers must be verified independently:

```text id="a1eval"
Ingestion Layer
    ↓
Parsing Layer
    ↓
Normalization Layer
    ↓
Validation Layer
    ↓
Persistence Layer
    ↓
Review Workflow Layer
    ↓
Audit Layer
    ↓
Locking Layer
    ↓
Deployment Layer
```

Each layer has:

-   
independent success criteria  

-   
independent failure semantics  

-   
independent operational guarantees  


No phase should depend entirely on downstream UI testing.

---

# 4. General Testing Philosophy

The platform should validate:

-   
happy path behavior  

-   
malformed input behavior  

-   
transaction rollback behavior  

-   
suspicious detection behavior  

-   
operational recovery behavior  


The system should never:

-   
fail silently  

-   
partially mutate critical records  

-   
lose source traceability  

-   
hide ingestion failures  


The testing strategy intentionally assumes:

# real enterprise data is messy.

---

# 5. Phase 1 Evaluation — Ingestion Boundary

# Objective

Verify the platform can safely receive and preserve operational source artifacts.

At this phase, the system should prove:

-   
upload reliability  

-   
source traceability  

-   
deterministic upload handling  


before transformation logic exists.

---

# Success Criteria

The ingestion layer is considered operationally correct when:

-   
uploads persist successfully  

-   
upload metadata remains queryable  

-   
unsupported files fail deterministically  

-   
corrupted uploads do not partially persist  

-   
upload traceability exists  


---

# Evaluation Cases

---

## Case 1 — Valid SAP CSV Upload

### Input

```

```

```
sap_fuel_export.csv
```

### Expected Result

-   
upload stored successfully  

-   
RawUpload record created  

-   
upload timestamp preserved  

-   
company association stored  


---

## Case 2 — Unsupported File Type

### Input

```

```

```
utility_bill.pdf
```

### Expected Result

-   
upload rejected  

-   
HTTP 400 returned  

-   
no RawUpload persisted  


---

## Case 3 — Empty CSV

### Input

```

```

```
0-byte CSV
```

### Expected Result

-   
ingestion rejected  

-   
deterministic error response returned  

-   
failure logged  


---

## Case 4 — Corrupted Upload Stream

### Scenario

Interrupted upload request.

### Expected Result

-   
no partial persistence  

-   
upload aborted safely  


---

# Operational Guarantees Verified

This phase verifies:

-   
ingestion durability  

-   
upload traceability  

-   
upload isolation  

-   
deterministic upload failures  


---

# 6. Phase 2 Evaluation — Parsing Layer

# Objective

Verify uploaded artifacts convert into structured row-level objects safely.

---

# Success Criteria

The parsing layer is operationally correct when:

-   
rows parse reliably  

-   
malformed rows isolate safely  

-   
encoding variability is tolerated  

-   
parser failures remain traceable  


---

# Evaluation Cases

---

## Case 1 — Valid CSV Parsing

### Input

```

```

```
Fuel_Type,Qty,UOM
Diesel,5000,L
```

### Expected Result

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

---

## Case 2 — Semicolon Delimiters

### Input

```

```

```
Fuel_Type;Qty;UOM
```

### Expected Result

-   
delimiter detected correctly  
  
OR  

-   
deterministic parser failure  


---

## Case 3 — Invalid Encoding

### Input

```

```

```
latin1 encoded SAP export
```

### Expected Result

-   
fallback parsing strategy  

-   
operational traceability preserved  


---

## Case 4 — Partially Corrupted Rows

### Scenario

Row 50 malformed.

Rows 1-49 valid.

Rows 51-100 valid.

### Expected Result

-   
malformed row isolated  

-   
remaining rows parse successfully  


---

# Operational Guarantees Verified

This phase verifies:

-   
parsing resilience  

-   
row extraction correctness  

-   
malformed row isolation  

-   
encoding tolerance  


---

# 7. Phase 3 Evaluation — Normalization Layer

# Objective

Verify heterogeneous operational structures normalize into canonical records consistently.

---

# Success Criteria

Normalization is operationally correct when:

-   
all sources map into canonical schema  

-   
units normalize consistently  

-   
scope assignment remains deterministic  

-   
source fidelity remains preserved  


---

# Evaluation Cases

---

## Case 1 — SAP Fuel Normalization

### Input

```

```

```
{
  "Fuel_Type": "Diesel",
  "Qty": 5000,
  "UOM": "L"
}
```

### Expected Result

```

```

```
{
  "scope": "Scope 1",
  "category": "Fuel",
  "quantity": 5000,
  "normalized_unit": "liters"
}
```

---

## Case 2 — Utility Scope Classification

### Input

```

```

```
{
  "kWh": 1200
}
```

### Expected Result

```

```

```
Scope 2
```

---

## Case 3 — Unknown Fuel Type

### Input

```

```

```
BioFuel-X
```

### Expected Result

-   
fallback category assigned  

-   
source payload preserved  

-   
analyst visibility retained  


---

## Case 4 — Invalid Date

### Input

```

```

```
32/13/2026
```

### Expected Result

-   
suspicious flag generated  

-   
normalization continuity preserved  


---

# Operational Guarantees Verified

This phase verifies:

-   
canonical transformation consistency  

-   
source-isolated normalization  

-   
unit normalization correctness  

-   
source fidelity preservation  


---

# 8. Phase 4 Evaluation — Persistence Layer

# Objective

Verify normalized operational records persist safely and transactionally.

---

# Success Criteria

Persistence is operationally correct when:

-   
normalized records persist consistently  

-   
raw payloads remain preserved  

-   
failed transactions rollback safely  

-   
database state remains coherent  


---

# Evaluation Cases

---

## Case 1 — Successful Record Persistence

### Expected Result

-   
EmissionRecord created  

-   
raw_data preserved  

-   
relational integrity maintained  


---

## Case 2 — Transaction Failure

### Scenario

Database failure during row 98 insertion.

### Expected Result

-   
entire transaction rollback  

-   
no partial persistence  


---

## Case 3 — Invalid JSON Serialization

### Scenario

Non-serializable payload detected.

### Expected Result

-   
deterministic persistence failure  

-   
ingestion traceability preserved  


---

## Case 4 — Duplicate Upload

### Scenario

Same source file uploaded twice.

### Expected Result

-   
deterministic duplicate handling  

-   
operational visibility preserved  


---

# Operational Guarantees Verified

This phase verifies:

-   
transactional integrity  

-   
rollback safety  

-   
persistence consistency  

-   
source traceability preservation  


---

# 9. Phase 5 Evaluation — Validation Engine

# Objective

Verify suspicious operational anomalies are surfaced correctly.

---

# Success Criteria

Validation is operationally correct when:

-   
suspicious records are identifiable  

-   
anomaly rules execute deterministically  

-   
ingestion continuity remains stable  


---

# Evaluation Cases

---

## Case 1 — Negative Quantity

### Input

```

```

```
-5000 kWh
```

### Expected Result

-   
record flagged suspicious  

-   
analyst visibility preserved  


---

## Case 2 — Extremely High Usage

### Input

```

```

```
999999999 kWh
```

### Expected Result

-   
anomaly warning generated  

-   
record remains ingestible  


---

## Case 3 — Missing Unit

### Input

```

```

```
{
  "quantity": 5000,
  "unit": null
}
```

### Expected Result

-   
suspicious flag generated  


---

## Case 4 — Invalid Airport Code

### Input

```

```

```
XXXINVALID
```

### Expected Result

-   
suspicious travel record  

-   
source payload preserved  


---

# Operational Guarantees Verified

This phase verifies:

-   
anomaly detection consistency  

-   
suspicious escalation workflows  

-   
ingestion continuity preservation  


---

# 10. Phase 6 Evaluation — Analyst Review APIs

# Objective

Verify operational review workflows behave consistently.

---

# Success Criteria

Review APIs are operationally correct when:

-   
analysts can review records  

-   
approvals work correctly  

-   
rejections work correctly  

-   
invalid state transitions fail safely  


---

# Evaluation Cases

---

## Case 1 — Approve Record

### Expected Result

-   
status changes to approved  

-   
audit event generated  


---

## Case 2 — Reject Record

### Expected Result

-   
status changes to rejected  


---

## Case 3 — Approve Locked Record

### Expected Result

-   
mutation rejected deterministically  


---

## Case 4 — Invalid Record ID

### Expected Result

-   
HTTP 404 returned  


---

# Operational Guarantees Verified

This phase verifies:

-   
review workflow consistency  

-   
operational state transitions  

-   
analyst action traceability  


---

# 11. Phase 7 Evaluation — Frontend Operational UI

# Objective

Verify analyst workflows remain operationally usable through the frontend.

---

# Success Criteria

Frontend is operationally correct when:

-   
uploads work end-to-end  

-   
review queues render correctly  

-   
suspicious indicators remain visible  

-   
analyst actions execute successfully  


---

# Evaluation Cases

---

## Case 1 — Upload Through UI

### Expected Result

-   
upload succeeds  

-   
records appear in review queue  


---

## Case 2 — Approve Through UI

### Expected Result

-   
UI state updates correctly  

-   
backend reflects approval  


---

## Case 3 — Network Failure

### Expected Result

-   
graceful error state  

-   
no UI crash  


---

## Case 4 — Empty Queue

### Expected Result

-   
operational empty-state rendering  


---

# Operational Guarantees Verified

This phase verifies:

-   
frontend-backend integration  

-   
operational usability  

-   
UI workflow continuity  


---

# 12. Phase 8 Evaluation — Audit Logging

# Objective

Verify historical operational mutations remain traceable.

---

# Success Criteria

Audit logging is operationally correct when:

-   
every material mutation creates audit history  

-   
old/new values remain preserved  

-   
actor attribution exists  


---

# Evaluation Cases

---

## Case 1 — Approval Audit Event

### Expected Result

-   
audit entry created  

-   
actor stored  

-   
timestamp stored  


---

## Case 2 — Edit Audit Event

### Expected Result

-   
old_value preserved  

-   
new_value preserved  


---

## Case 3 — Missing Actor Identity

### Expected Result

-   
mutation rejected  


---

## Case 4 — Audit Write Failure

### Expected Result

-   
mutation rollback executed  


---

# Operational Guarantees Verified

This phase verifies:

-   
auditability integrity  

-   
mutation traceability  

-   
historical reproducibility  


---

# 13. Phase 9 Evaluation — Record Locking

# Objective

Verify approved records become immutable.

---

# Success Criteria

The locking layer is operationally correct when:

-   
approved records reject future mutations  

-   
operational immutability remains enforceable  


---

# Evaluation Cases

---

## Case 1 — Edit Approved Record

### Expected Result

-   
modification rejected  


---

## Case 2 — Delete Approved Record

### Expected Result

-   
deletion blocked  


---

## Case 3 — Concurrent Mutation Attempt

### Expected Result

-   
latest-state validation enforced  


---

# Operational Guarantees Verified

This phase verifies:

-   
audit integrity preservation  

-   
post-approval immutability  


---

# 14. Phase 10 Evaluation — Deployment & Production Hardening

# Objective

Verify the system behaves reliably in production environments.

---

# Success Criteria

Deployment is operationally correct when:

-   
uploads work externally  

-   
APIs remain reachable  

-   
DB connectivity remains stable  

-   
environment configuration behaves correctly  


---

# Evaluation Cases

---

## Case 1 — Production Upload

### Expected Result

-   
upload succeeds externally  


---

## Case 2 — Missing Environment Variables

### Expected Result

-   
fail-fast startup behavior  


---

## Case 3 — Broken Upload Storage

### Expected Result

-   
deterministic startup failure  


---

## Case 4 — Production CORS

### Expected Result

-   
frontend-backend communication succeeds  


---

# Operational Guarantees Verified

This phase verifies:

-   
infrastructure correctness  

-   
production reliability  

-   
deployment traceability  


---

# 15. Final Evaluation Philosophy

This platform should be evaluated as:

-   
operational enterprise software  

-   
ingestion infrastructure  

-   
normalization architecture  

-   
analyst workflow tooling  

-   
audit-sensitive systems engineering  


The evaluation strategy intentionally prioritizes:

-   
deterministic behavior  

-   
operational trust  

-   
traceability  

-   
workflow consistency  

-   
failure predictability  


over:

-   
UI appearance  

-   
superficial functionality  

-   
happy-path-only behavior  


The strongest operational platform is not the platform that only works under perfect conditions.

It is the platform that behaves predictably when enterprise operational chaos inevitably appears.