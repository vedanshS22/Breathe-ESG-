```

```

```
# Problem Statement
## Breathe ESG — Enterprise ESG Ingestion & Analyst Review Platform

Author: Vedansh Shrivastava

---

# Overview

This project is a prototype ESG operational data platform designed to ingest, normalize, validate, and review enterprise emissions-related activity data from heterogeneous operational systems.

The core problem being solved is not emissions calculation itself.

The core problem is:
# operational data fragmentation.

Large enterprises store emissions-relevant activity data across multiple disconnected systems:
- ERP systems such as SAP
- utility billing exports
- travel management platforms
- manually maintained spreadsheets
- operational vendor reports

These systems were never designed to work together.

Each system:
- uses different schemas
- expresses units differently
- formats dates inconsistently
- contains incomplete or noisy data
- exposes operational information in incompatible structures

As a result, ESG reporting teams face a major operational challenge before they can even begin emissions accounting.

The real-world workflow is typically:
1. collect operational data manually
2. clean and normalize the data
3. identify suspicious records
4. verify source traceability
5. review and approve records internally
6. prepare evidence for auditors

This project focuses on building the operational infrastructure for that workflow.

---

# Business Problem

Enterprise sustainability teams need a reliable way to consolidate operational activity data into a unified reviewable system.

Without normalization and operational review infrastructure:
- analysts cannot trust source data
- auditors cannot trace transformations
- reporting becomes inconsistent
- operational errors propagate silently
- ESG calculations become unreliable

The platform therefore acts as:
- an ingestion pipeline
- a normalization engine
- an operational review system
- an audit-support platform

rather than a simple CRUD application.

---

# Core Product Goal

The primary objective of the system is to transform heterogeneous operational inputs into a standardized, reviewable emissions dataset.

The platform must:
1. ingest operational source data
2. preserve source fidelity
3. normalize records into a canonical schema
4. identify suspicious operational records
5. support analyst review workflows
6. preserve audit traceability

The system intentionally prioritizes:
- operational correctness
- traceability
- explainability
- auditability
- workflow clarity

over:
- feature quantity
- infrastructure scale
- advanced UI complexity

---

# Primary Use Case

An enterprise customer uploads operational activity data from multiple systems.

Examples:
- SAP fuel procurement exports
- electricity consumption exports
- corporate travel activity

The platform:
1. parses uploaded files
2. transforms heterogeneous rows into a common schema
3. validates suspicious records
4. surfaces records for analyst review
5. locks approved records for audit integrity

This creates a traceable operational pipeline from raw source data to approved emissions activity.

---

# Why This Problem Exists

Enterprise systems evolved independently.

An ERP system, utility billing system, and travel platform do not share:
- naming conventions
- schemas
- units
- operational assumptions

Example:

SAP may express fuel consumption as:

```text
Qty = 5000
UOM = L
```

A utility export may express electricity usage as:

```

```

```
kWh = 1200
```

A travel platform may express transportation activity as:

```

```

```
from_airport = DEL
to_airport = LHR
```

These records cannot be analyzed consistently without transformation.

Normalization therefore becomes the central architectural concern.

---

# System Responsibilities

The platform is responsible for:

-   
accepting heterogeneous operational uploads  

-   
preserving raw source artifacts  

-   
parsing structured operational rows  

-   
mapping source-specific structures into a canonical model  

-   
assigning emissions scopes  

-   
validating suspicious operational anomalies  

-   
enabling analyst workflows  

-   
maintaining audit history  


The platform is NOT responsible for:

-   
advanced carbon calculation engines  

-   
lifecycle analysis  

-   
procurement optimization  

-   
climate forecasting  

-   
realtime ERP synchronization  

-   
OCR document extraction  

-   
enterprise-scale workflow orchestration  


These are intentionally excluded from the prototype scope.

---

# Intended Users

The primary users are:

-   
ESG analysts  

-   
sustainability operations teams  

-   
internal reviewers  

-   
audit-support teams  


The platform is optimized for operational review workflows rather than end-user consumer interactions.

The UI should therefore behave like:

```

```

```
internal operational software
```

rather than:

```

```

```
consumer SaaS marketing UI
```

---

# Operational Workflow

The intended operational lifecycle is:

```

```

```
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
Suspicious Detection
    ↓
Analyst Review
    ↓
Approval / Rejection
    ↓
Audit Locking
```

Each stage has different responsibilities and failure semantics.

The architecture intentionally separates these concerns.

---

# Source Systems

The prototype supports three operational domains.

---

# 1. SAP Fuel & Procurement Data

Represents:

-   
fuel usage  

-   
operational procurement  

-   
plant-level operational activity  


Chosen format:

-   
CSV export  


The system assumes:

-   
inconsistent units  

-   
messy column naming  

-   
operational noise  

-   
legacy formatting behavior  


---

# 2. Utility Electricity Data

Represents:

-   
electricity consumption  

-   
billing periods  

-   
meter-based operational activity  


Chosen format:

-   
utility portal CSV export  


The system assumes:

-   
inconsistent billing cycles  

-   
varying units  

-   
operational gaps  


---

# 3. Corporate Travel Data

Represents:

-   
flights  

-   
hotels  

-   
transportation activity  


Chosen format:

-   
structured export/API-style JSON or CSV  


The system assumes:

-   
inconsistent airport casing  

-   
missing distances  

-   
category-specific operational logic  


---

# Canonical Internal Model

The platform transforms heterogeneous records into a unified operational schema.

Regardless of source type, records normalize into fields such as:

```

```

```
{
  "scope": "",
  "category": "",
  "quantity": "",
  "unit": "",
  "date": ""
}
```

This standardization enables:

-   
filtering  

-   
analytics  

-   
validation  

-   
operational review  

-   
audit traceability  


Without normalization, downstream workflows become fragmented and unreliable.

---

# Scope Classification

The platform supports:

-   
Scope 1  

-   
Scope 2  

-   
Scope 3  


classification.

Examples:

```

```

```
Fuel combustion
    → Scope 1

Purchased electricity
    → Scope 2

Business travel
    → Scope 3
```

Scope assignment is handled internally during normalization.

Upstream systems are not trusted to provide standardized scope metadata.

---

# Auditability Requirements

Auditability is a first-class system concern.

Every normalized record must retain:

-   
original source context  

-   
raw payload snapshot  

-   
upload metadata  

-   
analyst review history  


Approved records must become immutable.

This is critical because ESG reporting workflows are audit-sensitive.

The system must therefore preserve:

-   
traceability  

-   
reproducibility  

-   
historical accountability  


at every stage of the pipeline.

---

# Validation Philosophy

The platform assumes operational data is imperfect.

The system must tolerate:

-   
malformed rows  

-   
missing fields  

-   
inconsistent units  

-   
operational anomalies  


Validation should therefore:

-   
flag suspicious records  

-   
preserve ingestion continuity  

-   
surface anomalies to analysts  


rather than:

-   
reject entire uploads aggressively  


This mirrors real-world operational ESG workflows.

---

# Technical Philosophy

The system is intentionally designed as:

-   
a modular monolith  

-   
a lightweight ETL pipeline  

-   
an operational review system  

-   
an auditability-first architecture  


The platform intentionally avoids:

-   
distributed systems complexity  

-   
premature scalability optimization  

-   
unnecessary infrastructure abstraction  


The goal is:

# architectural clarity and operational realism.

---

# Success Criteria

The project is considered successful if:

1.   
Heterogeneous source files can be ingested reliably.  

2.   
Uploaded operational data can be normalized into a unified schema.  

3.   
Suspicious records are surfaced automatically.  

4.   
Analysts can review, approve, reject, and lock records.  

5.   
Every normalized record remains traceable back to its source artifact.  

6.   
The architecture remains internally coherent, explainable, and operationally realistic.  


---

# Final Product Identity

This platform should ultimately be understood as:

```

```

```
Enterprise ESG Ingestion Pipeline
+
Normalization Engine
+
Operational Analyst Workflow System
+
Auditability-First Review Platform
```

That identity should remain consistent throughout the entire implementation.