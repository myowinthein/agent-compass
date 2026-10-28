---
title: "Step 1: Portal research"
parent: portal-finder
grand_parent: Commands
nav_order: 1
---

# Step 1: Portal research

Verify portals on their own sites for the chosen country's IT/tech roles.

## Flow

```mermaid
flowchart TD
  Start(["Use the established country"]) --> Browse{"Live browsing available?"}
  Browse -->|No| Wait["Explain the limit<br/>Wait for access or supplied evidence"]
  Wait --> Supplied["Label supplied evidence and its date<br/>Do not call it live verified"]
  Browse -->|Yes| Check["Check official country, tech or job-search pages<br/>A working homepage alone is insufficient"]
  Check --> Access{"Country-relevant coverage verifiable?"}
  Access -->|No| Retry["Try another relevant public page<br/>On the same official domain"]
  Retry --> Verified{"Now verified?"}
  Verified -->|No| Note["Keep out of verified groups<br/>Name the access or coverage limit"]
  Verified -->|Yes| Keep
  Access -->|Yes| Keep["Keep useful official links and verification date<br/>Deduplicate redirects and rebrands"]
  Keep --> Group["Group verified portals by type<br/>Star useful starting picks"]
  Note --> Result
  Group --> Result(["Return results and coverage notes<br/>Stop after this response"])
  Supplied --> Result
```

## Groups

Each portal appears once by type:

1. General job boards.
2. Tech-specific boards.
3. Professional & community networks.

Geographic scope is noted per entry; remote-first boards follow their subject focus. Genuine exceptions can have another group. Empty groups need no filler. Government employment-service portals are excluded.

## What you receive

Each entry gives an official link, country/global scope and one-line strength. Country/category/search links support verification beyond a homepage.

⭐ marks 2–3 verified starting picks per group, or fewer when fewer qualify. Live results carry a verification date. ⚠️ flags restrictions, deprecated sites, shared ownership or access limits; account access and job eligibility are separate.

## Partial or unavailable access

Failed access becomes a coverage note, not a dead-site claim or verified recommendation. Homepage marketing alone cannot qualify an entry when deeper pages cannot be checked. Other verified results remain usable.

Without browsing, wait for access or supplied evidence. Supplied results are dated and labelled **user-supplied; not live verified**, separate from verified picks. No verified portals means an explicit limitation, not an empty success.
