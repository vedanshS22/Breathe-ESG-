```

```

```
# Backend Architecture Specification
## Breathe ESG — Ingestion, Workflow & Operational Service Design

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- backend system architecture
- service-layer organization
- ingestion orchestration
- operational workflow execution
- persistence boundaries
- transactional behavior
- backend runtime philosophy

The backend is:
# the operational core of the entire platform.

The frontend is primarily:
- visibility
- interaction
- workflow rendering

The backend owns:
- ingestion
- normalization
- validation
- persistence
- approvals
- auditability
- operational state transitions

This document explains how those workflows are structured internally.

---

# 2. Backend Philosophy

The backend should behave like:
# operational enterprise infrastructure.

NOT:
- tutorial CRUD code
- controller-heavy frameworks
- business logic inside views
- abstraction-heavy architecture experiments

The backend intentionally prioritizes:
- deterministic workflows
- explicit orchestration
- operational clarity
- transactional consistency
- maintainability

over:
- clever abstractions
- excessive indirection
- microservice theatrics
- premature scalability

The strongest backend is:
# the easiest backend to reason about operationally.

---

# 3. Architectural Style

The backend uses:
# modular monolith architecture.

This is an intentional decision.

The platform intentionally avoids:
- microservices
- event-driven orchestration
- distributed queues
- Kafka
- service meshes

Reason:
the assignment scope does not justify distributed operational complexity.

The platform primarily requires:
- transactional consistency
- centralized normalization
- predictable workflows
- simpler debugging

A modular monolith provides all of these effectively.

---

# 4. High-Level Backend Topology

```text id="a1back"
HTTP Request
    ↓
APIView
    ↓
Service Layer
    ↓
Validation Layer
    ↓
Persistence Layer
    ↓
PostgreSQL
```

This separation is intentional.

Each layer owns distinct responsibilities.

---

# 5. Repository Structure

Expected structure:

```

```

```
backend/
    emissions/
    services/
    validators/
    api/
    uploads/
```

This structure intentionally isolates:

-   
persistence  

-   
workflows  

-   
validation  

-   
transport  

-   
ingestion  


---

# 6. Folder Responsibilities

---

# emissions/

Owns:

-   
models  

-   
serializers  

-   
persistence contracts  

-   
relational entities  


Examples:

```

```

```
models.py
serializers.py
```

This layer should NOT contain:

-   
normalization logic  

-   
parsing workflows  

-   
orchestration logic  


The emissions layer represents:

# database structure only.

---

# services/

Owns:

-   
ingestion orchestration  

-   
parsing  

-   
normalization  

-   
workflow execution  

-   
operational business logic  


Examples:

```

```

```
upload_service.py
sap_normalizer.py
utility_parser.py
review_service.py
```

This is:

# the operational brain of the platform.

---

# validators/

Owns:

-   
suspicious detection  

-   
anomaly rules  

-   
operational validation workflows  


Examples:

```

```

```
quantity_validator.py
travel_validator.py
```

Validation remains isolated because:

-   
normalization transforms  

-   
validation evaluates  


These are fundamentally different concerns.

---

# api/

Owns:

-   
API views  

-   
request validation  

-   
response formatting  

-   
endpoint coordination  


Views should remain:

# extremely thin.

---

# uploads/

Owns:

-   
upload persistence  

-   
file handling  

-   
storage coordination  


The uploaded source artifact is part of:

# the audit trail.

---

# 7. Request Lifecycle

The backend request lifecycle intentionally remains explicit.

Example upload flow:

```

```

```
HTTP Upload Request
    ↓
APIView Receives Request
    ↓
UploadService Executes
    ↓
RawUpload Persisted
    ↓
Parser Extracts Rows
    ↓
Normalizer Transforms Rows
    ↓
Validators Execute
    ↓
EmissionRecords Persist
    ↓
Response Returned
```

Every stage has:

-   
explicit ownership  

-   
explicit failure semantics  

-   
explicit operational responsibility  


---

# 8. Service Layer Philosophy

The service layer is:

# the most important architectural layer.

All operational workflows belong here.

Examples:

-   
ingestion orchestration  

-   
normalization execution  

-   
review workflows  

-   
approval logic  

-   
audit generation  


---

# Correct Flow

```

```

```
class UploadService:

    def process_upload(self):
        ...
```

---

# Forbidden Flow

```

```

```
class UploadView(APIView):

    def post(self):
        # parsing
        # normalization
        # validation
        # persistence
```

Views must never own operational workflows.

---

# 9. Upload Orchestration Architecture

The upload workflow is the ingestion boundary.

The upload pipeline should behave:

```

```

```
Receive File
    ↓
Persist Raw Upload
    ↓
Parse Operational Rows
    ↓
Normalize Records
    ↓
Validate Records
    ↓
Persist Final Records
```

This sequence must remain:

# deterministic.

---

# Why This Matters

A common architectural mistake:

-   
normalize before persistence  

-   
transform transiently  

-   
lose raw source traceability  


This platform intentionally preserves:

# raw source fidelity first.

---

# 10. Parsing Architecture

Parsing answers:

```

```

```
“What structurally exists in the source artifact?”
```

The parser owns:

-   
CSV parsing  

-   
encoding handling  

-   
row extraction  

-   
delimiter handling  


The parser does NOT own:

-   
emissions logic  

-   
scope assignment  

-   
suspicious detection  


---

# Expected Parser Structure

```

```

```
services/
    parsers/
        sap_parser.py
        utility_parser.py
        travel_parser.py
```

Parsers remain:

# source-isolated.

---

# 11. Normalization Architecture

Normalization answers:

```

```

```
“What does the operational data mean?”
```

Normalization owns:

-   
canonical mapping  

-   
scope classification  

-   
category mapping  

-   
unit standardization  

-   
date normalization  


---

# Expected Structure

```

```

```
services/
    normalizers/
        sap_normalizer.py
        utility_normalizer.py
        travel_normalizer.py
```

---

# Why Source Isolation Exists

SAP logic should never affect:

-   
travel normalization  

-   
utility normalization  


Source isolation improves:

-   
maintainability  

-   
extensibility  

-   
debugging clarity  


---

# 12. Validation Architecture

Validation exists because:

# enterprise operational data is noisy.

Validation owns:

-   
suspicious detection  

-   
anomaly rules  

-   
operational warnings  


Examples:

-   
negative quantity  

-   
abnormal spikes  

-   
invalid dates  

-   
invalid airport codes  


---

# Validation Philosophy

Validation should:

```

```

```
flag records
```

NOT:

```

```

```
destroy ingestion continuity aggressively.
```

---

# 13. Persistence Architecture

Persistence owns:

-   
transactional writes  

-   
relational consistency  

-   
operational durability  


The database is:

# the operational source of truth.

---

# Required Pattern

```

```

```
with transaction.atomic():
```

All ingestion workflows must remain:

# transaction-safe.

---

# Why Transactionality Matters

Partial ingestion states create:

-   
operational distrust  

-   
audit inconsistency  

-   
workflow corruption  


The platform intentionally prioritizes:

# atomic operational consistency.

---

# 14. Audit Architecture

Auditability is a first-class concern.

Every material workflow mutation must generate:

-   
timestamp  

-   
previous value  

-   
new value  

-   
operational action  


Audit logs represent:

# historical operational truth.

NOT:

# current operational state.

---

# 15. Approval Workflow Architecture

The approval workflow exists because:

# ESG systems are human-reviewed systems.

The platform intentionally assumes:

-   
analysts verify records  

-   
suspicious data requires investigation  

-   
approvals require operational review  


---

# Approval Flow

```

```

```
Pending
    ↓
Approved
    ↓
Locked
```

Approved records become:

# immutable.

---

# Why Locking Exists

Approved records should never mutate silently.

Immutability preserves:

-   
audit integrity  

-   
analyst accountability  

-   
reporting trust  


---

# 16. API View Philosophy

APIView responsibilities:

-   
request validation  

-   
service coordination  

-   
response formatting  


APIViews should never:

-   
normalize records  

-   
orchestrate workflows  

-   
manipulate transactions directly  


---

# Correct Example

```

```

```
class UploadView(APIView):

    def post(self, request):

        service = UploadService()

        result = service.process(request)

        return Response(result)
```

---

# 17. Error Handling Philosophy

Backend failures should remain:

-   
explicit  

-   
traceable  

-   
operationally meaningful  


The backend should never:

-   
swallow exceptions silently  

-   
partially mutate workflows  

-   
hide ingestion failures  


---

# Forbidden Pattern

```

```

```
except:
    pass
```

Forbidden.

---

# Correct Pattern

```

```

```
except Exception as e:
    logger.exception(e)
    raise ValidationError(...)
```

---

# 18. Logging Strategy

The backend should log:

-   
upload lifecycle  

-   
parsing failures  

-   
normalization failures  

-   
suspicious counts  

-   
approval events  

-   
rollback events  


Logs should optimize:

# operational debugging visibility.

---

# 19. Runtime Philosophy

The backend intentionally remains:

# synchronous.

The MVP avoids:

-   
Celery  

-   
Redis queues  

-   
distributed workers  

-   
async orchestration  


Reason:  
  
the ingestion scale does not justify operational complexity.

Synchronous workflows provide:

-   
simpler debugging  

-   
deterministic execution  

-   
lower infrastructure overhead  


---

# 20. Backend Edge Cases

---

# Partial Transaction Failure

Expected Behavior:  
  
rollback entire ingestion transaction.

---

# Invalid Source Data

Expected Behavior:  
  
flag suspicious without corrupting workflow.

---

# Duplicate Uploads

Expected Behavior:  
  
deterministic duplicate handling.

---

# Invalid Normalization Mapping

Expected Behavior:  
  
fallback category + analyst visibility.

---

# Database Failure

Expected Behavior:  
  
transaction rollback + explicit failure.

---

# 21. Backend Performance Philosophy

The backend optimizes for:

-   
operational correctness  

-   
deterministic behavior  

-   
maintainability  


NOT:

-   
hyperscale ingestion  

-   
realtime streaming  

-   
distributed concurrency  


Premature optimization intentionally avoided.

---

# 22. Backend Invariants

The following guarantees must never be violated.

---

# Invariant 1

```

```

```
Raw source data must remain preserved before transformation.
```

---

# Invariant 2

```

```

```
Business workflows remain service-owned.
```

---

# Invariant 3

```

```

```
Approved records must remain immutable.
```

---

# Invariant 4

```

```

```
Validation failures must never silently mutate source values.
```

---

# Invariant 5

```

```

```
Audit history must remain append-only.
```

---

# Invariant 6

```

```

```
All ingestion persistence must remain transactional.
```

---

# 23. Final Backend Philosophy

This backend should ultimately feel like:

-   
operational enterprise infrastructure  

-   
ingestion-focused workflow architecture  

-   
audit-sensitive systems engineering  

-   
deterministic operational software  


The backend intentionally prioritizes:

-   
operational clarity  

-   
deterministic workflows  

-   
transactional consistency  

-   
explainability  

-   
maintainability  


over:

-   
infrastructure theatrics  

-   
abstraction-heavy architecture  

-   
premature scalability  

-   
distributed complexity  


The strongest backend is not the backend with the most infrastructure.

It is the backend whose operational behavior remains easiest to reason about