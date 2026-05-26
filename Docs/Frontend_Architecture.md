```

```

```
# Frontend Architecture Specification
## Breathe ESG — Operational UI & Frontend System Design

Author: Vedansh Shrivastava

---

# 1. Purpose of This Document

This document defines:
- frontend architecture
- UI philosophy
- component organization
- state management strategy
- operational workflow rendering
- frontend boundaries
- UI behavior semantics

The purpose of the frontend is NOT:
# marketing-oriented SaaS presentation.

The frontend exists to:
# expose operational workflows to analysts clearly and efficiently.

The UI should behave like:
- internal enterprise tooling
- operational workflow software
- analyst review infrastructure

The frontend intentionally prioritizes:
- clarity
- density
- speed
- predictability
- operational visibility

over:
- decorative interactions
- heavy animations
- visual theatrics
- overdesigned UX patterns

---

# 2. Frontend Philosophy

The frontend should feel:
# operationally alive but functionally disciplined.

Meaning:
- responsive interactions
- smooth workflow transitions
- fast queue visibility
- realtime-feeling operational flow

without becoming:
- visually noisy
- distracting
- animation-heavy

The frontend exists to optimize:
# analyst workflow efficiency.

---

# 3. Core Frontend Responsibilities

The frontend owns:
- upload interactions
- operational visibility
- review queues
- suspicious indicators
- analyst actions
- workflow rendering

The frontend does NOT own:
- normalization logic
- validation rules
- ingestion orchestration
- business workflows
- transactional rules

Those responsibilities remain:
# backend-owned.

---

# 4. Architectural Philosophy

The frontend should behave like:
# a thin operational interface layer.

The frontend must never become:
- business-logic heavy
- workflow-orchestration heavy
- transformation-heavy

The architecture intentionally centralizes operational rules inside the backend.

Reason:
- operational consistency
- deterministic workflows
- easier debugging
- reduced duplication

---

# 5. Technology Stack

---

# Core Framework

```text id="a1front"
React
```

---

# Styling

```

```

```
TailwindCSS
```

---

# Data Fetching

```

```

```
React Query
```

---

# Routing

```

```

```
React Router
```

---

# HTTP Client

```

```

```
Axios
```

---

# Why This Stack Was Chosen

The frontend requires:

-   
operational dashboards  

-   
asynchronous API workflows  

-   
queue rendering  

-   
table-heavy interfaces  

-   
upload handling  


React provides:

-   
predictable component architecture  

-   
mature ecosystem  

-   
operational flexibility  


TailwindCSS provides:

-   
rapid UI implementation  

-   
visual consistency  

-   
low CSS maintenance overhead  


React Query provides:

-   
caching  

-   
retry behavior  

-   
API synchronization  

-   
loading state management  


without introducing unnecessary complexity.

---

# 6. Why Redux Was Rejected

The MVP intentionally avoids:

```

```

```
Redux
MobX
Complex global stores
```

Reason:  
  
the frontend state complexity does not justify:

-   
boilerplate-heavy state orchestration  

-   
reducer complexity  

-   
global mutation architecture  


Most state belongs either:

-   
locally inside components  
  
OR  

-   
inside backend APIs  


React Query is sufficient.

---

# 7. Repository Structure

Expected structure:

```

```

```
frontend/
    src/
        components/
        pages/
        services/
        hooks/
        layouts/
        types/
```

This separation intentionally isolates:

-   
rendering  

-   
API communication  

-   
reusable workflows  

-   
operational layouts  


---

# 8. Folder Responsibilities

---

# components/

Owns:

-   
reusable UI primitives  

-   
operational widgets  

-   
tables  

-   
upload components  

-   
badges  

-   
status indicators  


Examples:

```

```

```
UploadZone.jsx
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
UploadPage.jsx
ReviewQueuePage.jsx
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
auditService.js
```

---

# hooks/

Owns:

-   
reusable operational logic  

-   
React Query wrappers  

-   
UI interaction hooks  


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
application structure  

-   
sidebar layout  

-   
navigation shells  


---

# types/

Owns:

-   
shared TypeScript interfaces  
  
OR  

-   
shared frontend contracts  


---

# 9. UI Philosophy

The UI should feel like:

# operational software.

NOT:

# sales-oriented SaaS dashboards.

The frontend should prioritize:

-   
queue visibility  

-   
operational speed  

-   
high information density  

-   
fast analyst scanning  


Avoid:

-   
excessive whitespace  

-   
decorative panels  

-   
large empty dashboards  

-   
unnecessary motion  


---

# 10. Dashboard Philosophy

The dashboard exists to expose:

# operational state.

The dashboard should immediately answer:

-   
how many uploads exist  

-   
how many suspicious records exist  

-   
how many pending approvals exist  

-   
where operational attention is needed  


The dashboard should optimize:

# operational triage.

---

# Expected Dashboard Sections

Examples:

-   
upload summary  

-   
suspicious records count  

-   
pending review queue  

-   
recent operational activity  


---

# 11. Upload UI Architecture

# Responsibilities

The upload UI owns:

-   
file selection  

-   
drag-and-drop interaction  

-   
upload progress visibility  

-   
upload error visibility  


The upload UI does NOT own:

-   
parsing  

-   
normalization  

-   
ingestion orchestration  


---

# Expected Flow

```

```

```
Select File
    ↓
Choose Source Type
    ↓
Upload File
    ↓
Show Upload Status
    ↓
Redirect to Review Queue
```

---

# Required UI States

The upload flow must support:

-   
uploading  

-   
success  

-   
failure  

-   
retry  

-   
validation errors  


---

# 12. Review Queue Architecture

The review queue is:

# the operational heart of the frontend.

Analysts primarily interact through:

-   
pending queues  

-   
suspicious queues  

-   
approval workflows  


The review queue must optimize:

-   
scanning speed  

-   
operational visibility  

-   
anomaly identification  


---

# Expected Table Columns

Examples:

```

```

```
Source Type
Scope
Category
Quantity
Suspicious Status
Review Status
```

---

# Required Interactions

Analysts must be able to:

-   
approve records  

-   
reject records  

-   
inspect suspicious reasons  

-   
filter operational data  


quickly.

---

# 13. Suspicious Record UX

Suspicious records should remain:

# visually prominent.

Examples:

-   
warning badges  

-   
highlighted rows  

-   
suspicious icons  


The platform should never hide anomalies visually.

---

# Why This Matters

The operational workflow is:

```

```

```
ingest
    ↓
flag
    ↓
review
```

The frontend must reinforce:

# anomaly visibility.

---

# 14. API Communication Strategy

The frontend communicates exclusively through:

# REST APIs.

The frontend should never:

-   
directly manipulate persistence  

-   
embed business rules  

-   
bypass workflow endpoints  


---

# Expected Service Example

```

```

```
export const fetchRecords = async () => {
    return axios.get("/api/records/")
}
```

---

# 15. React Query Philosophy

React Query owns:

-   
server caching  

-   
loading states  

-   
retries  

-   
synchronization  


The frontend intentionally avoids:

-   
manual request orchestration  

-   
duplicated loading logic  

-   
custom caching infrastructure  


---

# Expected Pattern

```

```

```
const { data, isLoading } = useQuery({
    queryKey: ["records"],
    queryFn: fetchRecords
})
```

---

# 16. Error Handling Philosophy

Frontend failures should remain:

-   
visible  

-   
graceful  

-   
operationally understandable  


The UI should never:

-   
silently fail  

-   
freeze  

-   
lose workflow context  


---

# Examples

---

## Upload Failure

Expected UX:

-   
visible error message  

-   
retry option  

-   
preserved UI stability  


---

## API Timeout

Expected UX:

-   
loading timeout feedback  

-   
retry handling  


---

## Empty Review Queue

Expected UX:

-   
operational empty state  

-   
no broken layouts  


---

# 17. Loading State Philosophy

Operational systems must communicate:

# system activity clearly.

The frontend should expose:

-   
upload progress  

-   
table loading  

-   
approval execution  

-   
API synchronization states  


The frontend should never appear:

# frozen or unresponsive.

---

# 18. Component Philosophy

Components should remain:

-   
small  

-   
explicit  

-   
operationally focused  


Avoid:

-   
giant multi-purpose components  

-   
deeply nested rendering logic  

-   
hidden workflow behavior  


---

# Bad Example

```

```

```
MegaDashboardComponent.jsx
```

Forbidden.

---

# Correct Example

```

```

```
ReviewQueueTable.jsx
SuspiciousSummaryCard.jsx
UploadDropzone.jsx
```

---

# 19. Frontend State Rules

Use:

-   
local component state for UI interactions  

-   
React Query for server state  


Avoid:

-   
duplicating backend state locally  

-   
global state overengineering  


---

# 20. Frontend Performance Philosophy

The frontend should optimize:

-   
operational responsiveness  

-   
fast table rendering  

-   
quick analyst workflows  


The MVP intentionally avoids:

-   
virtualization complexity  

-   
websocket synchronization  

-   
realtime subscriptions  


Reason:  
  
the operational scale does not justify it.

---

# 21. Frontend Edge Cases

---

# Empty Operational Data

Expected Behavior:  
  
Graceful empty-state rendering.

---

# Network Failure

Expected Behavior:  
  
Visible retry/error messaging.

---

# Slow APIs

Expected Behavior:  
  
Loading states remain visible.

---

# Duplicate Click Actions

Expected Behavior:  
  
Button disable during mutation.

---

# Upload Interruption

Expected Behavior:  
  
Visible upload failure state.

---

# 22. Responsive Design Philosophy

The platform primarily targets:

# desktop operational workflows.

Mobile responsiveness is secondary.

Reason:  
  
analyst workflows involve:

-   
tables  

-   
review queues  

-   
operational dashboards  


which are desktop-oriented by nature.

---

# 23. Styling Philosophy

The visual system should remain:

-   
clean  

-   
dark-modern  

-   
operationally focused  

-   
minimally distracting  


The UI should feel:

# alive but disciplined.

Use:

-   
subtle transitions  

-   
lightweight hover states  

-   
operational status colors  


Avoid:

-   
flashy gradients everywhere  

-   
oversized cards  

-   
decorative animation overload  


---

# 24. Frontend Invariants

The following guarantees must never be violated.

---

# Invariant 1

```

```

```
Business workflows remain backend-owned.
```

---

# Invariant 2

```

```

```
Suspicious records remain visually prominent.
```

---

# Invariant 3

```

```

```
Operational state remains clearly visible.
```

---

# Invariant 4

```

```

```
Frontend failures remain graceful and visible.
```

---

# Invariant 5

```

```

```
UI interactions must remain operationally predictable.
```

---

# 25. Final Frontend Philosophy

This frontend should ultimately feel like:

-   
operational enterprise software  

-   
analyst workflow tooling  

-   
ingestion-focused dashboards  

-   
audit-sensitive operational systems  


The frontend intentionally prioritizes:

-   
operational clarity  

-   
workflow efficiency  

-   
deterministic interactions  

-   
high information density  

-   
implementation simplicity  


over:

-   
marketing aesthetics  

-   
excessive animation  

-   
frontend complexity  

-   
state-management theatrics  


The strongest frontend is not the most visually impressive UI.

It is the UI that makes operational workflows easiest to execute.