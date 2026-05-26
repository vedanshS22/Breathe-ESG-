```

```

```
# Data Model Specification
## Breathe ESG — Canonical Data Architecture

Author: Vedansh Shrivastava

---

# 1. Purpose of the Data Model

The data model exists to support a very specific operational problem:
# transforming heterogeneous enterprise operational data into a normalized, reviewable, and auditable emissions dataset.

The architecture is intentionally designed around:
- source traceability
- canonical normalization
- analyst workflows
- audit integrity
- operational lifecycle management

The database is not simply storing uploaded rows.

It is modeling:
- ingestion lifecycle
- transformation lifecycle
- review lifecycle
- audit lifecycle

The schema therefore separates:
1. source artifacts
2. normalized operational records
3. historical mutations

These concerns must remain isolated.

---

# 2. Architectural Modeling Philosophy

The platform uses a relational schema because the operational workload is:
- transactional
- audit-sensitive
- relationship-heavy
- analyst-query-driven

The system requires:
- strong consistency
- transactional guarantees
- historical traceability
- relational filtering
- canonical querying

PostgreSQL is intentionally selected because it supports:
- relational integrity
- JSON payload storage
- transactional safety
- operational querying

The data model intentionally avoids:
- document-first storage
- schema-less operational records
- deeply nested persistence structures

because normalized emissions workflows are inherently relational.

---

# 3. Core Architectural Principle

The most important modeling principle in the system is:

```text id="6cg9ut"
Raw operational source data must remain preserved independently from normalized operational records.
```

This separation exists because:

-   
upstream schemas change frequently  

-   
normalization rules evolve  

-   
analysts require source verification  

-   
auditors require transformation traceability  


The system therefore stores:

-   
raw source files  

-   
raw row payloads  

-   
normalized operational records  


simultaneously.

---

# 4. Entity Relationship Overview

```

```

```
Company
   │
   ├── DataSource
   │        │
   │        └── RawUpload
   │
   └── EmissionRecord
              │
              └── AuditLog
```

This structure intentionally separates:

-   
source ingestion  

-   
operational normalization  

-   
historical mutation tracking  


Each entity has a distinct ownership responsibility.

---

# 5. Company Entity

## Purpose

Represents the tenant organization whose operational data is being processed.

The platform is designed as:

# multi-tenant architecture.

Even though authentication and tenant isolation may remain lightweight in the prototype, the schema must still support future tenant separation cleanly.

Every operational record in the system ultimately belongs to a company.

---

# Responsibilities

The Company entity owns:

-   
uploaded source artifacts  

-   
normalized records  

-   
analyst workflows  

-   
audit history  


No operational record should exist outside a company boundary.

---

# Example

```

```

```
class Company(models.Model):

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
```

---

# Why This Entity Exists

Without company ownership:

-   
tenant isolation becomes impossible  

-   
audit boundaries become unclear  

-   
future scalability becomes painful  


The entity exists even in MVP form because:

# tenant ownership is a system-level concern.

---

# 6. DataSource Entity

## Purpose

Represents the operational origin of uploaded data.

Examples:

-   
SAP  

-   
Utility Portal  

-   
Travel Platform  


The system intentionally models sources explicitly because:

-   
normalization logic is source-dependent  

-   
operational trust varies by source  

-   
ingestion behavior differs by source type  


---

# Responsibilities

The DataSource entity owns:

-   
source classification  

-   
ingestion metadata  

-   
source-specific operational context  


---

# Example

```

```

```
class DataSource(models.Model):

    SOURCE_TYPES = [
        ("sap", "SAP"),
        ("utility", "Utility"),
        ("travel", "Travel"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    source_type = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
```

---

# Why Separate DataSource Exists

A common mistake is embedding source_type directly everywhere.

This becomes operationally messy over time.

Separating source ownership enables:

-   
ingestion metrics  

-   
source-specific monitoring  

-   
future integration expansion  

-   
operational visibility  


It also creates a stable boundary for normalization orchestration.

---

# 7. RawUpload Entity

## Purpose

Represents the uploaded source artifact itself.

This entity is one of the most important entities in the system.

The uploaded file is part of the audit trail.

The platform should never:

-   
parse transiently  

-   
normalize without preservation  

-   
discard source artifacts  


because ESG workflows require traceability.

---

# Responsibilities

RawUpload owns:

-   
uploaded file reference  

-   
upload timestamp  

-   
ingestion metadata  

-   
source traceability  


---

# Example

```

```

```
class RawUpload(models.Model):

    source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to="uploads/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
```

---

# Why RawUpload Exists Separately

A raw uploaded file represents:

# source-of-truth operational evidence.

This is fundamentally different from:

# normalized operational records.

Keeping them separate enables:

-   
reprocessing  

-   
debugging  

-   
audit reproduction  

-   
normalization evolution  


without destroying original source fidelity.

---

# 8. EmissionRecord Entity

## Purpose

Represents the canonical normalized operational emissions record.

This entity is the operational heart of the platform.

Everything upstream eventually transforms into:

# EmissionRecord.

This entity intentionally represents:

-   
standardized activity  

-   
analyst-reviewable operational records  

-   
queryable normalized emissions activity  


regardless of source origin.

---

# Core Modeling Philosophy

All heterogeneous source data must eventually normalize into:

# one canonical schema.

This is the core architectural idea behind the entire system.

Example:

SAP may provide:

```

```

```
Qty
```

Utility may provide:

```

```

```
kWh
```

Travel may provide:

```

```

```
distance
```

Internally all become:

```

```

```
quantity
```

inside EmissionRecord.

---

# Example

```

```

```
class EmissionRecord(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    source_type = models.CharField(max_length=50)

    scope = models.CharField(max_length=20)

    category = models.CharField(max_length=100)

    quantity = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    raw_data = models.JSONField()

    is_suspicious = models.BooleanField(
        default=False
    )

    suspicious_reason = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    locked = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
```

---

# Why raw_data Exists

This field preserves:

# row-level source fidelity.

Example:

```

```

```
{
  "Fuel_Type": "Diesel",
  "Qty": 5000,
  "UOM": "L"
}
```

must remain accessible even after normalization becomes:

```

```

```
{
  "scope": "Scope 1",
  "category": "Fuel",
  "quantity": 5000,
  "unit": "liters"
}
```

Without raw payload preservation:

-   
auditability breaks  

-   
debugging becomes unreliable  

-   
transformations become unverifiable  


---

# Why status Exists

The platform models:

# operational review lifecycle.

Records are not instantly trusted.

They move through states:

```

```

```
pending
    ↓
approved / rejected
```

This mirrors real ESG operational review processes.

---

# Why locked Exists

Approved records must become immutable.

This is critical for:

-   
audit trust  

-   
analyst accountability  

-   
reporting integrity  


Once approved:

```

```

```
locked = true
```

Future mutation attempts should fail.

---

# Why is_suspicious Exists

Enterprise operational data is messy.

The platform assumes:

-   
anomalies  

-   
malformed records  

-   
operational inconsistencies  


Suspicious records should remain operationally visible rather than silently discarded.

This supports:

-   
human review  

-   
operational transparency  

-   
anomaly escalation  


---

# 9. AuditLog Entity

## Purpose

Tracks immutable historical changes to operational records.

This entity represents:

# historical state transitions.

NOT current operational state.

---

# Example

```

```

```
class AuditLog(models.Model):

    record = models.ForeignKey(
        EmissionRecord,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=100)

    old_value = models.JSONField(
        null=True,
        blank=True
    )

    new_value = models.JSONField(
        null=True,
        blank=True
    )

    changed_by = models.CharField(max_length=255)

    timestamp = models.DateTimeField(
        auto_now_add=True
    )
```

---

# Why Separate AuditLog Exists

A major architectural mistake is mixing:

-   
current operational state  
  
with:  

-   
historical mutation history  


These are fundamentally different concerns.

EmissionRecord represents:

```

```

```
current operational truth
```

AuditLog represents:

```

```

```
historical operational mutation history
```

Separating them preserves:

-   
clean operational queries  

-   
immutable audit history  

-   
traceable analyst actions  


---

# 10. Lifecycle of a Record

A normalized operational record moves through the following lifecycle:

```

```

```
Raw Upload
    ↓
Parsed Row
    ↓
Normalized EmissionRecord
    ↓
Validation
    ↓
Suspicious Flagging
    ↓
Analyst Review
    ↓
Approved / Rejected
    ↓
Locked for Audit
```

The schema is intentionally designed around this lifecycle.

---

# 11. Modeling Invariants

The following rules must never be violated.

---

# Invariant 1

```

```

```
Raw source payloads must remain preserved.
```

---

# Invariant 2

```

```

```
Normalized records must remain traceable to source artifacts.
```

---

# Invariant 3

```

```

```
Approved records must become immutable.
```

---

# Invariant 4

```

```

```
Audit history must remain append-only.
```

---

# Invariant 5

```

```

```
Validation failures must never silently mutate source values.
```

---

# 12. Transaction Philosophy

All ingestion persistence should occur inside transactional boundaries.

Reason:

-   
partial imports create operational inconsistency  

-   
failed transformations can corrupt audit trust  

-   
ingestion pipelines fail frequently in real systems  


The platform should fail atomically wherever possible.

---

# 13. Why JSONField Is Used

The platform intentionally uses:

```

```

```
JSONField
```

for:

-   
raw source preservation  

-   
transformation traceability  

-   
flexible upstream schema support  


This is not schema laziness.

It is an intentional design choice because upstream operational systems evolve independently.

The normalized schema remains relational.

The raw source payload remains semi-structured.

This hybrid approach is operationally realistic.

---

# 14. Final Data Modeling Philosophy

The data model should ultimately be understood as:

-   
an operational ingestion schema  

-   
a normalization persistence layer  

-   
an analyst workflow state model  

-   
an auditability architecture  


The schema intentionally prioritizes:

-   
lifecycle clarity  

-   
traceability  

-   
operational correctness  

-   
explainability  

-   
audit integrity  


over:

-   
abstraction-heavy modeling  

-   
premature optimization  

-   
excessive schema fragmentation  


The strongest possible model is not the most complex schema.

It is the most operationally coherent schema.

```

```

```

```

