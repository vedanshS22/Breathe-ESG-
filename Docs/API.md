```

```

```
# API Design Specification
## Breathe ESG — REST API Architecture & Contracts

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- REST API philosophy
- endpoint contracts
- request/response structure
- API ownership boundaries
- workflow semantics
- transport-layer behavior
- operational API guarantees

The API layer exists to expose:
# operational workflows.

The APIs represent:
- ingestion workflows
- normalization visibility
- analyst review workflows
- operational querying
- audit traceability

The API layer intentionally avoids:
- transport-layer business logic
- hidden orchestration
- direct database manipulation inside views
- frontend-owned workflows

The API boundary exists between:
```text id="a1api2"
Operational UI
```

and:

```

```

```
Backend Workflow Services
```

---

# 2. API Philosophy

The API architecture intentionally prioritizes:

-   
explicitness  

-   
deterministic behavior  

-   
operational clarity  

-   
predictable state transitions  

-   
resource-oriented workflows  


The API should never feel:

-   
magical  

-   
implicit  

-   
overloaded  

-   
unpredictable  


Every endpoint should make it obvious:

-   
what operation occurred  

-   
what state changed  

-   
what workflow executed  


The API layer behaves like:

# operational transport infrastructure.

---

# 3. REST Philosophy

The platform uses:

# REST APIs.

Reason:  
  
the workflows are:

-   
operationally predictable  

-   
resource-oriented  

-   
CRUD-adjacent  


The platform does not require:

-   
GraphQL orchestration  

-   
realtime subscriptions  

-   
complex client-driven querying  


REST provides:

-   
operational simplicity  

-   
easier debugging  

-   
explicit workflows  

-   
lower implementation overhead  


---

# 4. API Layer Responsibilities

The API layer owns:

-   
HTTP request handling  

-   
request validation  

-   
response formatting  

-   
endpoint routing  


The API layer does NOT own:

-   
normalization logic  

-   
parsing workflows  

-   
suspicious detection  

-   
ingestion orchestration  


Those belong inside:

# services/.

---

# Correct Architectural Flow

```

```

```
HTTP Request
    ↓
APIView
    ↓
Service Layer
    ↓
Persistence Layer
```

---

# Forbidden Flow

```

```

```
APIView
    ↓
Normalization Logic
    ↓
Database Writes
```

Views must remain:

# thin coordinators only.

---

# 5. API Versioning Philosophy

The MVP intentionally avoids:

```

```

```
/v1/
/v2/
```

because:

-   
API surface area remains small  

-   
prototype complexity should stay low  


Future extensibility may support:

```

```

```
/api/v1/
```

but versioning is intentionally deferred.

---

# 6. Authentication & Authorization

The MVP intentionally excludes:

-   
authentication  

-   
RBAC  

-   
SSO  

-   
JWT workflows  

-   
permissions architecture  


Reason:  
  
the assignment evaluates:

-   
ingestion architecture  

-   
normalization workflows  

-   
operational system design  


NOT:

-   
enterprise identity systems  


The APIs therefore assume:

# trusted internal prototype environment.

Authentication architecture may be added later without affecting:

-   
ingestion workflows  

-   
normalization architecture  

-   
persistence structure  


---

# 7. API Response Philosophy

Responses should remain:

-   
explicit  

-   
operationally meaningful  

-   
deterministic  

-   
structured consistently  


The API should never:

-   
hide failures  

-   
swallow errors  

-   
expose ambiguous responses  


---

# Success Response Example

```

```

```
{
  "success": true,
  "data": {}
}
```

---

# Failure Response Example

```

```

```
{
  "success": false,
  "error": "Unsupported file type"
}
```

---

# Validation Failure Example

```

```

```
{
  "success": false,
  "validation_errors": {
    "source_type": "Required field"
  }
}
```

---

# 8. Upload APIs

# Purpose

Expose ingestion boundary workflows.

Uploads represent:

# operational source artifacts.

The uploaded source file itself is part of the audit trail.

---

# Endpoint

```

```

```
POST /api/uploads/
```

---

# Responsibilities

This endpoint owns:

-   
upload acceptance  

-   
source association  

-   
raw upload persistence  

-   
ingestion initiation  


This endpoint does NOT own:

-   
normalization  

-   
suspicious detection  

-   
analyst review  


---

# Example Request

```

```

```
POST /api/uploads/
Content-Type: multipart/form-data
```

---

# Example Payload

```

```

```
{
  "company_id": 1,
  "source_type": "sap",
  "file": "<csv>"
}
```

---

# Example Response

```

```

```
{
  "success": true,
  "upload_id": 15,
  "status": "uploaded"
}
```

---

# Expected Backend Flow

```

```

```
Receive Upload
    ↓
Persist RawUpload
    ↓
Trigger Parsing Workflow
    ↓
Return Upload Metadata
```

---

# Failure Cases

Examples:

-   
unsupported file type  

-   
empty upload  

-   
corrupted upload stream  

-   
oversized upload  


Failures should remain:

# deterministic and traceable.

---

# 9. Record Query APIs

# Purpose

Expose normalized operational records.

---

# Endpoint

```

```

```
GET /api/records/
```

---

# Responsibilities

This endpoint owns:

-   
operational querying  

-   
filtering  

-   
pagination  

-   
analyst visibility  


---

# Example Query Parameters

```

```

```
GET /api/records/?scope=Scope%201&status=pending
```

---

# Example Response

```

```

```
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "scope": "Scope 1",
      "category": "Fuel",
      "quantity": 5000
    }
  ]
}
```

---

# API Rules

The API exposes:

# normalized operational truth only.

The API should never expose:

-   
parser internals  

-   
source-native ingestion structures  

-   
normalization implementation details  


---

# 10. Suspicious Record APIs

# Purpose

Expose operational anomalies to analysts.

---

# Endpoint

```

```

```
GET /api/records/suspicious/
```

---

# Responsibilities

This endpoint owns:

-   
suspicious visibility  

-   
anomaly review workflows  

-   
operational escalation visibility  


---

# Example Response

```

```

```
{
  "results": [
    {
      "id": 44,
      "is_suspicious": true,
      "reason": "Negative quantity"
    }
  ]
}
```

---

# Why Separate Endpoint Exists

Operational ESG workflows frequently prioritize:

# suspicious-first review queues.

This improves:

-   
analyst efficiency  

-   
anomaly visibility  

-   
operational review speed  


---

# 11. Approval APIs

# Purpose

Expose analyst workflow state transitions.

---

# Endpoint

```

```

```
POST /api/records/{id}/approve/
```

---

# Responsibilities

This endpoint owns:

-   
approval workflow execution  

-   
operational state transition  

-   
record locking  

-   
audit event triggering  


---

# Expected Backend Flow

```

```

```
Receive Approval Request
    ↓
Validate Current State
    ↓
Update Status
    ↓
Lock Record
    ↓
Generate Audit Event
```

---

# Example Response

```

```

```
{
  "success": true,
  "status": "approved"
}
```

---

# Failure Cases

Examples:

-   
invalid record id  

-   
already approved  

-   
locked record  

-   
invalid state transition  


Failures must remain:

# deterministic.

---

# 12. Rejection APIs

# Endpoint

```

```

```
POST /api/records/{id}/reject/
```

---

# Responsibilities

This endpoint owns:

-   
rejection state transitions  

-   
analyst workflow mutation  

-   
audit generation  


---

# Example Response

```

```

```
{
  "success": true,
  "status": "rejected"
}
```

---

# 13. Audit APIs

# Purpose

Expose operational mutation history.

---

# Endpoint

```

```

```
GET /api/audit-logs/
```

---

# Responsibilities

Audit endpoints own:

-   
mutation visibility  

-   
historical traceability  

-   
operational reconstruction  


Audit logs represent:

# historical operational truth.

---

# Example Response

```

```

```
{
  "results": [
    {
      "action": "approved",
      "timestamp": "2026-05-26T10:00:00Z"
    }
  ]
}
```

---

# 14. Pagination Strategy

List endpoints should support:

-   
pagination  

-   
deterministic ordering  

-   
operational filtering  


---

# Example Parameters

```

```

```
?page=1&page_size=20
```

---

# Why Pagination Exists

Operational datasets may grow large.

Pagination improves:

-   
frontend performance  

-   
operational usability  

-   
API stability  


---

# 15. Filtering Strategy

Record APIs should support:

-   
scope filtering  

-   
status filtering  

-   
suspicious filtering  

-   
source filtering  


---

# Example

```

```

```
GET /api/records/?source_type=sap&status=pending
```

---

# Why Filtering Matters

Analysts work:

-   
queue-first  

-   
workflow-first  

-   
anomaly-first  


Filtering improves:

# operational review efficiency.

---

# 16. Error Handling Philosophy

APIs must fail:

-   
explicitly  

-   
predictably  

-   
traceably  


The API layer should never:

-   
swallow exceptions silently  

-   
expose stack traces  

-   
return ambiguous failures  


---

# Bad Response Example

```

```

```
{
  "error": "Something failed"
}
```

Forbidden.

---

# Correct Response Example

```

```

```
{
  "success": false,
  "error": "Invalid airport code"
}
```

---

# 17. HTTP Status Code Conventions

---

# 200 OK

Successful retrieval.

---

# 201 Created

Successful creation.

Examples:

-   
upload success  

-   
operational creation  


---

# 400 Bad Request

Client validation failure.

Examples:

-   
invalid file type  

-   
malformed request  


---

# 404 Not Found

Resource missing.

---

# 409 Conflict

Invalid workflow transition.

Examples:

-   
approving locked record  


---

# 500 Internal Server Error

Unexpected operational failure.

Should remain:

-   
internally logged  

-   
minimally exposed externally  


---

# 18. Transactional API Guarantees

All workflow mutations must remain:

# transaction-safe.

Examples:

-   
approvals  

-   
rejections  

-   
audit writes  


Required pattern:

```

```

```
transaction.atomic()
```

The API should never partially mutate operational workflows.

---

# 19. API Logging Strategy

Important API events should log:

-   
upload started  

-   
upload completed  

-   
normalization failed  

-   
suspicious record detected  

-   
approval executed  

-   
rollback triggered  


The logging strategy should optimize:

# operational debugging visibility.

---

# 20. API Invariants

The following guarantees must never be violated.

---

# Invariant 1

```

```

```
Views must remain thin coordinators.
```

---

# Invariant 2

```

```

```
Business workflows must remain service-owned.
```

---

# Invariant 3

```

```

```
Operational state transitions must remain explicit.
```

---

# Invariant 4

```

```

```
Approved records must remain immutable.
```

---

# Invariant 5

```

```

```
Audit history must remain reproducible.
```

---

# Invariant 6

```

```

```
APIs must fail deterministically.
```

---

# 21. Final API Philosophy

This API architecture should ultimately feel like:

-   
operational enterprise infrastructure  

-   
deterministic workflow transport  

-   
ingestion-focused backend systems  

-   
audit-sensitive operational tooling  


The API layer intentionally prioritizes:

-   
explicit behavior  

-   
predictable workflows  

-   
operational clarity  

-   
deterministic failures  

-   
maintainable contracts  


over:

-   
transport abstraction complexity  

-   
hidden orchestration  

-   
RPC-style endpoint chaos  

-   
premature API sophistication  


The strongest API architecture is not the API with the most endpoints.

It is the API whose operational behavior remains easiest to reason about.