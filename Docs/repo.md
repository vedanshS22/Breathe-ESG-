```

```

```
# Repository Structure Specification
## Breathe ESG — Project Organization & Codebase Layout

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- repository organization
- folder ownership
- module boundaries
- architectural layering
- code placement rules
- dependency direction
- structural conventions

The purpose of repository structure is NOT:
# “keeping files organized aesthetically.”

The purpose is:
# enforcing architectural discipline through physical structure.

A well-structured repository:
- prevents workflow leakage
- reduces accidental coupling
- improves maintainability
- improves onboarding
- improves AI-assisted code generation
- improves debugging clarity

The repository structure should make it obvious:
- where logic belongs
- where logic does NOT belong
- which layer owns which responsibility

The repository itself becomes:
# architectural enforcement.

---

# 2. Repository Philosophy

The repository should feel like:
# operational enterprise software.

NOT:
- tutorial projects
- feature-dump codebases
- framework-generated chaos
- abstraction-heavy experiments

The structure intentionally prioritizes:
- explicit boundaries
- operational clarity
- service ownership
- deterministic layering

over:
- deep nesting
- generic utility dumping
- excessive abstraction

---

# 3. High-Level Repository Layout

```text id="a1repo"
breathe-esg/
│
├── backend/
│
├── frontend/
│
├── docs/
│
├── sample_data/
│
├── scripts/
│
├── .env.example
│
├── docker-compose.yml
│
├── README.md
│
└── requirements.txt
```

This layout intentionally separates:

-   
operational backend logic  

-   
frontend rendering  

-   
architectural documentation  

-   
development tooling  

-   
infrastructure configuration  


---

# 4. Root-Level Responsibilities

---

# backend/

Owns:

-   
ingestion workflows  

-   
normalization logic  

-   
persistence  

-   
APIs  

-   
auditability  

-   
operational orchestration  


This is:

# the operational core of the platform.

---

# frontend/

Owns:

-   
analyst UI  

-   
operational dashboards  

-   
upload workflows  

-   
review queues  


This is:

# the operational interaction layer.

---

# docs/

Owns:

-   
architecture specifications  

-   
implementation plans  

-   
normalization contracts  

-   
operational decisions  


This directory represents:

# the architectural source of truth.

---

# sample_data/

Owns:

-   
example ingestion files  

-   
test CSVs  

-   
normalization fixtures  


Examples:

```

```

```
sap_sample.csv
utility_sample.csv
travel_sample.csv
```

These files support:

-   
local testing  

-   
parser validation  

-   
demo workflows  


---

# scripts/

Owns:

-   
setup automation  

-   
migration helpers  

-   
operational tooling  


Examples:

```

```

```
seed_data.py
reset_db.py
```

This directory intentionally excludes:

-   
business logic  

-   
workflow orchestration  


---

# 5. Backend Structure

Expected backend structure:

```

```

```
backend/
│
├── emissions/
├── services/
├── validators/
├── api/
├── uploads/
├── config/
├── manage.py
└── requirements.txt
```

Each folder owns:

# a distinct architectural responsibility.

---

# 6. emissions/ Structure

# Purpose

Owns:

-   
database models  

-   
serializers  

-   
persistence contracts  

-   
relational entities  


Expected structure:

```

```

```
emissions/
│
├── models.py
├── serializers.py
├── migrations/
└── admin.py
```

---

# Responsibilities

The emissions layer owns:

-   
persistence schema  

-   
relational integrity  

-   
ORM definitions  


The emissions layer must NOT own:

-   
normalization  

-   
parsing  

-   
workflow orchestration  

-   
suspicious detection  


This separation is critical.

---

# Why This Matters

Persistence structure and operational workflows are:

# different architectural concerns.

Mixing them creates:

-   
fat models  

-   
hidden workflows  

-   
difficult debugging  

-   
operational ambiguity  


---

# 7. services/ Structure

# Purpose

Owns:

-   
ingestion workflows  

-   
parsing  

-   
normalization  

-   
approvals  

-   
orchestration  


This is:

# the operational brain of the platform.

---

# Expected Structure

```

```

```
services/
│
├── ingestion/
│   ├── upload_service.py
│   └── ingestion_service.py
│
├── parsers/
│   ├── sap_parser.py
│   ├── utility_parser.py
│   └── travel_parser.py
│
├── normalizers/
│   ├── sap_normalizer.py
│   ├── utility_normalizer.py
│   └── travel_normalizer.py
│
├── review/
│   ├── approval_service.py
│   └── rejection_service.py
│
└── audit/
    └── audit_service.py
```

---

# Why Services Are Segmented

The platform intentionally separates:

-   
parsing  

-   
normalization  

-   
review workflows  

-   
audit workflows  


because they evolve independently.

This improves:

-   
maintainability  

-   
extensibility  

-   
debugging clarity  


---

# 8. validators/ Structure

# Purpose

Owns:

-   
suspicious detection  

-   
anomaly evaluation  

-   
operational validation rules  


Expected structure:

```

```

```
validators/
│
├── quantity_validator.py
├── utility_validator.py
├── travel_validator.py
└── validation_engine.py
```

---

# Why Validation Is Separate

Validation answers:

```

```

```
“Does this data look operationally suspicious?”
```

Normalization answers:

```

```

```
“What does this operational data mean?”
```

These concerns must remain isolated.

---

# 9. api/ Structure

# Purpose

Owns:

-   
transport layer  

-   
API views  

-   
routing  

-   
request validation  

-   
response formatting  


Expected structure:

```

```

```
api/
│
├── views/
│   ├── upload_views.py
│   ├── record_views.py
│   └── audit_views.py
│
├── urls.py
└── responses.py
```

---

# Important Rule

Views should remain:

# extremely thin.

Views should NOT contain:

-   
normalization  

-   
parsing  

-   
ingestion orchestration  

-   
business workflows  


Views coordinate workflows only.

---

# 10. uploads/ Structure

# Purpose

Owns:

-   
upload persistence  

-   
source file handling  

-   
storage coordination  


Expected structure:

```

```

```
uploads/
│
├── storage.py
├── upload_handlers.py
└── file_utils.py
```

---

# Why uploads/ Exists Separately

Uploaded source artifacts are:

# audit-sensitive operational assets.

Separating upload infrastructure improves:

-   
traceability  

-   
storage clarity  

-   
ingestion separation  


---

# 11. config/ Structure

# Purpose

Owns:

-   
Django settings  

-   
environment configuration  

-   
runtime initialization  


Expected structure:

```

```

```
config/
│
├── settings.py
├── urls.py
├── wsgi.py
└── asgi.py
```

---

# Why Config Remains Isolated

Runtime configuration and operational workflows are different concerns.

Keeping config isolated improves:

-   
deployment clarity  

-   
environment management  

-   
runtime predictability  


---

# 12. Frontend Structure

Expected frontend structure:

```

```

```
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── layouts/
│   ├── types/
│   └── App.jsx
│
├── public/
├── package.json
└── vite.config.js
```

---

# 13. Frontend Folder Responsibilities

---

# components/

Owns:

-   
reusable UI primitives  

-   
tables  

-   
badges  

-   
upload widgets  


Examples:

```

```

```
UploadDropzone.jsx
RecordTable.jsx
SuspiciousBadge.jsx
```

---

# pages/

Owns:

-   
route-level operational screens  


Examples:

```

```

```
DashboardPage.jsx
ReviewQueuePage.jsx
UploadPage.jsx
```

---

# services/

Owns:

-   
API communication  

-   
HTTP requests  

-   
backend integration  


Examples:

```

```

```
recordService.js
uploadService.js
```

---

# hooks/

Owns:

-   
reusable operational hooks  

-   
React Query wrappers  


Examples:

```

```

```
useRecords.js
useUploads.js
```

---

# layouts/

Owns:

-   
sidebar layouts  

-   
navigation shells  

-   
operational structure  


---

# types/

Owns:

-   
shared frontend contracts  

-   
reusable interfaces  


---

# 14. Documentation Structure

Expected docs structure:

```

```

```
docs/
│
├── architecture.md
├── implementationPlan.md
├── normalization.md
├── dataModel.md
├── conventions.md
├── edgecases.md
├── decisions.md
├── deployment.md
├── apiDesign.md
└── frontendArchitecture.md
```

This directory represents:

# the architectural source of truth.

---

# 15. Sample Data Philosophy

The repository should include:

-   
representative ingestion files  

-   
realistic operational exports  

-   
normalization examples  


Reason:  
  
the ingestion pipeline should remain:

# demonstrable and testable.

---

# Example Sample Files

```

```

```
sap_fuel_export.csv
utility_consumption.csv
travel_activity.csv
```

---

# 16. Naming Conventions

The repository naming strategy intentionally prioritizes:

-   
explicitness  

-   
operational clarity  

-   
readability  


Avoid:

-   
ambiguous abbreviations  

-   
generic names  

-   
framework-style magic naming  


---

# Good Examples

```

```

```
sap_normalizer.py
approval_service.py
travel_validator.py
```

---

# Bad Examples

```

```

```
utils.py
helpers.py
common.py
manager.py
```

These become:

# architectural dumping grounds.

---

# 17. Dependency Direction Rules

Dependencies should flow:

```

```

```
API Layer
    ↓
Service Layer
    ↓
Persistence Layer
```

NOT:

```

```

```
Persistence Layer
    ↓
Business Workflows
```

Models should never orchestrate operational workflows.

---

# 18. Forbidden Structural Patterns

The following repository patterns are intentionally forbidden.

---

# Giant Utility Folders

Examples:

```

```

```
utils/
helpers/
common/
```

Reason:  
  
they accumulate unrelated logic and destroy boundaries.

---

# Fat Views

Views should never own:

-   
parsing  

-   
normalization  

-   
orchestration  


---

# Hidden Workflow Layers

Operational workflows should remain:

# explicit and traceable.

---

# Cross-Layer Mutation

Frontend should never bypass APIs.

Validators should not orchestrate persistence.

Models should not own workflows.

---

# 19. Repository Invariants

The following guarantees must never be violated.

---

# Invariant 1

```

```

```
Business workflows remain service-owned.
```

---

# Invariant 2

```

```

```
Views remain thin coordinators.
```

---

# Invariant 3

```

```

```
Normalization remains source-isolated.
```

---

# Invariant 4

```

```

```
Validation remains operationally isolated from transformation.
```

---

# Invariant 5

```

```

```
Raw source artifacts remain audit-traceable.
```

---

# Invariant 6

```

```

```
Repository structure reflects architectural ownership clearly.
```

---

# 20. Final Repository Philosophy

This repository should ultimately feel like:

-   
operational enterprise software  

-   
ingestion-focused infrastructure  

-   
workflow-oriented systems engineering  

-   
audit-sensitive operational tooling  


The repository intentionally prioritizes:

-   
explicit boundaries  

-   
operational clarity  

-   
maintainability  

-   
deterministic structure  

-   
architectural discipline  


over:

-   
deep abstraction  

-   
framework cleverness  

-   
generic utility sprawl  

-   
premature complexity  


The strongest repository structure is not the most complicated structure.

It is the structure that makes architectural ownership easiest to understand.