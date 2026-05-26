```

```

```
# Normalization Architecture Specification
## Breathe ESG — Canonical Transformation Pipeline

Author: Vedansh Shrivastava

---

# 1. Purpose of the Normalization Layer

Normalization is the conceptual core of the entire platform.

The system is fundamentally solving:
# heterogeneous operational data transformation.

Enterprise ESG systems receive operational activity data from multiple disconnected upstream systems:
- ERP platforms
- utility portals
- travel management tools
- spreadsheets
- vendor exports

Each source expresses operational activity differently.

Examples:
- inconsistent field names
- inconsistent units
- inconsistent date formats
- inconsistent category definitions
- incomplete operational metadata

Without normalization:
- records cannot be queried consistently
- analytics become fragmented
- validations become unreliable
- approvals lose meaning
- auditability breaks

The normalization layer therefore exists to transform operational chaos into:
# one canonical internal emissions model.

---

# 2. Core Architectural Philosophy

The normalization system is intentionally designed around the following principle:

```text id="9cc2sq"
Upstream systems are not trusted to provide consistent operational structure.
```

The platform assumes:

-   
inconsistent schemas  

-   
malformed fields  

-   
legacy formatting  

-   
operational noise  

-   
evolving upstream exports  


The normalization layer therefore acts as:

-   
a translation boundary  

-   
a canonicalization engine  

-   
a schema stabilization layer  


between:

```

```

```
untrusted operational sources
```

and:

```

```

```
trusted internal operational records
```

---

# 3. Why Normalization Exists

Consider the following examples.

---

# SAP Export

```

```

```
{
  "Fuel_Type": "Diesel",
  "Qty": 5000,
  "UOM": "L"
}
```

---

# Utility Export

```

```

```
{
  "Meter_ID": "MTR001",
  "kWh": 1200
}
```

---

# Travel Export

```

```

```
{
  "from_airport": "DEL",
  "to_airport": "LHR"
}
```

These structures are operationally incompatible.

The normalization layer transforms all of them into:

# one canonical operational schema.

Example:

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
unified querying  

-   
analyst review  

-   
suspicious detection  

-   
reporting  

-   
audit workflows  


---

# 4. Normalization Pipeline Lifecycle

The normalization layer exists inside the ingestion lifecycle.

The full operational lifecycle is:

```

```

```
Receive Source File
    ↓
Persist Raw Upload
    ↓
Parse Source Rows
    ↓
Normalize Rows
    ↓
Validate Records
    ↓
Persist Emission Records
    ↓
Analyst Review
```

Normalization should never occur before:

```

```

```
raw source preservation.
```

This is a system invariant.

---

# 5. Source-Specific Normalization Strategy

The platform intentionally isolates normalization logic by source type.

Reason:

-   
upstream systems evolve independently  

-   
schemas differ fundamentally  

-   
operational assumptions vary  

-   
validation logic differs  


The architecture intentionally avoids:

```

```

```
one giant universal normalizer.
```

Instead, normalization is segmented into dedicated services.

---

# Expected Structure

```

```

```
services/
    sap_normalizer.py
    utility_normalizer.py
    travel_normalizer.py
```

Each normalizer owns:

-   
source-specific mappings  

-   
source-specific cleaning rules  

-   
source-specific assumptions  

-   
category classification  

-   
unit standardization  


---

# 6. Canonical Emission Record Contract

Regardless of upstream source, every normalized record must conform to a stable operational contract.

The canonical normalized structure is:

```

```

```
{
  "scope": "",
  "category": "",
  "quantity": "",
  "normalized_unit": "",
  "start_date": "",
  "end_date": "",
  "source_type": "",
  "raw_data": {}
}
```

This schema becomes:

# the operational source of truth.

All downstream workflows depend on this contract remaining stable.

---

# 7. Raw Data Preservation

The normalization layer must never destroy source fidelity.

Every normalized record must retain:

-   
original source payload  

-   
source metadata  

-   
upload traceability  


Example:

---

# Original SAP Row

```

```

```
{
  "Plant": "PLT01",
  "Fuel_Type": "Diesel",
  "Qty": 5000,
  "UOM": "L"
}
```

---

# Normalized Record

```

```

```
{
  "scope": "Scope 1",
  "category": "Fuel",
  "quantity": 5000,
  "normalized_unit": "liters",
  "raw_data": {
    "Plant": "PLT01",
    "Fuel_Type": "Diesel",
    "Qty": 5000,
    "UOM": "L"
  }
}
```

The raw payload remains part of the operational record.

This is critical for:

-   
audit verification  

-   
debugging  

-   
transformation reproducibility  

-   
analyst trust  


---

# 8. Scope Classification Rules

The normalization layer owns:

# emissions scope assignment.

Upstream systems are not trusted to provide consistent scope classifications.

---

# Scope Mapping Strategy

---

## Scope 1

Represents:

-   
direct emissions  

-   
fuel combustion  

-   
operational fuel usage  


Examples:

-   
diesel  

-   
natural gas  

-   
generators  


---

## Scope 2

Represents:

-   
purchased electricity  


Examples:

-   
utility consumption  

-   
facility electricity  


---

## Scope 3

Represents:

-   
indirect operational emissions  


Examples:

-   
flights  

-   
hotels  

-   
procurement  

-   
logistics  


---

# Example Mapping

```

```

```
if source_type == "utility":
    scope = "Scope 2"

elif source_type == "travel":
    scope = "Scope 3"

elif source_type == "sap":
    scope = "Scope 1"
```

The normalization layer owns this classification logic centrally.

---

# 9. Category Classification Rules

Categories provide operational specificity within scopes.

Examples:

```

```

```
Scope 1 → Fuel
Scope 2 → Electricity
Scope 3 → Business Travel
```

Categories are intentionally normalized into stable operational terminology.

Upstream systems may contain:

-   
inconsistent labels  

-   
localized names  

-   
vendor-specific terminology  


Normalization must standardize these.

---

# 10. Unit Normalization

Unit normalization is one of the most operationally important transformation stages.

Enterprise operational systems frequently express identical activity in inconsistent units.

Examples:

```

```

```
L
ltr
Liters
litre
```

All should normalize into:

```

```

```
liters
```

---

# Central Unit Mapping

Normalization should use centralized mapping dictionaries.

Example:

```

```

```
UNIT_MAPPINGS = {
    "L": "liters",
    "ltr": "liters",
    "Liters": "liters"
}
```

This avoids:

-   
duplicated normalization logic  

-   
inconsistent transformations  

-   
operational ambiguity  


---

# 11. Date Normalization

Date inconsistency is expected across enterprise systems.

Examples:

```

```

```
01.05.2026
2026/05/01
May 1 2026
```

All dates should normalize into:

```

```

```
ISO-8601
```

Example:

```

```

```
2026-05-01
```

The normalization layer owns:

-   
parsing  

-   
conversion  

-   
fallback handling  


---

# 12. Missing Data Philosophy

The system assumes:

# upstream operational data is imperfect.

Normalization should therefore tolerate:

-   
missing fields  

-   
incomplete metadata  

-   
malformed rows  


where operationally possible.

The platform should prefer:

```

```

```
flagging suspicious records
```

rather than:

```

```

```
destroying ingestion continuity.
```

---

# Example

Missing quantity:

```

```

```
{
  "Qty": null
}
```

Expected behavior:

-   
normalize partially  

-   
flag suspicious  

-   
surface to analyst review  


NOT:

```

```

```
abort entire upload.
```

---

# 13. Unknown Value Handling

The normalization layer must gracefully handle unknown operational categories.

Example:

```

```

```
BioFuel-X
```

Unknown values should:

-   
remain preserved in raw_data  

-   
receive fallback normalized categories  

-   
become analyst-visible  


The platform should never silently discard unknown operational information.

---

# 14. Validation vs Normalization

A critical architectural distinction:

Normalization:

```

```

```
transforms operational structure
```

Validation:

```

```

```
evaluates operational correctness
```

These are different responsibilities.

Example:

---

# Normalization Responsibility

```

```

```
Convert:
"L" → "liters"
```

---

# Validation Responsibility

```

```

```
Detect:
quantity < 0
```

This separation must remain explicit in architecture.

---

# 15. Suspicious Record Philosophy

The platform intentionally treats suspicious records as:

# operational review events.

NOT:

# ingestion failures.

Reason:  
  
enterprise operational data is inherently noisy.

Rejecting entire uploads aggressively is operationally unrealistic.

The system should therefore:

-   
ingest  

-   
flag  

-   
escalate  


rather than:

-   
discard  

-   
fail silently  

-   
destroy imports  


---

# 16. Source-Specific Normalization Examples

---

# SAP Example

---

## Raw

```

```

```
{
  "Fuel_Type": "Diesel",
  "Qty": 5000,
  "UOM": "L"
}
```

---

## Normalized

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

# Utility Example

---

## Raw

```

```

```
{
  "kWh": 1200
}
```

---

## Normalized

```

```

```
{
  "scope": "Scope 2",
  "category": "Electricity",
  "quantity": 1200,
  "normalized_unit": "kwh"
}
```

---

# Travel Example

---

## Raw

```

```

```
{
  "from_airport": "DEL",
  "to_airport": "LHR"
}
```

---

## Normalized

```

```

```
{
  "scope": "Scope 3",
  "category": "Business Travel",
  "quantity": 6700,
  "normalized_unit": "km"
}
```

---

# 17. Transaction Philosophy

Normalization should execute inside transactional ingestion boundaries.

Reason:

-   
partial transformations create operational inconsistency  

-   
ingestion failures are common  

-   
analysts require trustworthy imports  


The system should prefer:

```

```

```
atomic operational consistency.
```

---

# 18. Performance Philosophy

The normalization pipeline is intentionally synchronous in MVP form.

Reason:

-   
assignment scale is limited  

-   
infrastructure simplicity matters  

-   
operational clarity is prioritized  


The architecture intentionally avoids:

-   
Celery  

-   
distributed queues  

-   
stream processors  


These may be future extensions but are not justified for the prototype scope.

---

# 19. Future Extensibility

The normalization architecture is intentionally designed to support:

-   
additional source systems  

-   
evolving mappings  

-   
new scopes/categories  

-   
enhanced validation rules  


without rewriting ingestion foundations.

New sources should integrate by:

1.   
adding a parser  

2.   
adding a source normalizer  

3.   
implementing canonical mapping  


without changing downstream workflows.

---

# 20. Normalization Invariants

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
All normalized records must conform to canonical schema.
```

---

# Invariant 3

```

```

```
Validation must never silently mutate source values.
```

---

# Invariant 4

```

```

```
Unknown operational values must remain traceable.
```

---

# Invariant 5

```

```

```
Normalization logic must remain source-isolated.
```

---

# 21. Final Normalization Philosophy

The normalization layer should ultimately be understood as:

-   
a canonical transformation boundary  

-   
an operational schema stabilization layer  

-   
an ingestion reliability mechanism  

-   
an auditability-preserving transformation engine  


The normalization system intentionally prioritizes:

-   
operational consistency  

-   
explainability  

-   
traceability  

-   
deterministic transformations  

-   
analyst visibility  


over:

-   
hidden automation  

-   
aggressive data rejection  

-   
abstraction-heavy pipelines  


The strongest normalization system is not the most complex pipeline.

It is the most operationally trustworthy pipeline.