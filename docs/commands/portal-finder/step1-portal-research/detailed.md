---
title: "step 1: portal research"
parent: portal-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/portal-finder/step1-portal-research.html
permalink: /docs/commands/portal-finder/step1-portal-research/detailed.html
title_category: Details
description: "Portal research checks where someone can actually look for country-relevant tech roles. It uses the portal's own deeper pages, deduplicates the results and makes incomplete access visible instead of filling a recommendation quota."
source_files:
  - prompts/portal-finder/step1-portal-research.md
---

# Step 1: Portal research

{% include guide-depth.html %}

Portal research checks where someone can actually look for country-relevant tech roles. It uses the portal's own deeper pages, deduplicates the results and makes incomplete access visible instead of filling a recommendation quota.

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

The result uses three types: **General job boards**, **Tech-specific boards**, and **Professional & community networks**. Each portal appears once. Country-only versus global coverage is noted per entry, not used as a competing group.

A remote-first board belongs under General or Tech-specific according to its focus. A genuine exception may have a clearly named additional group. Empty groups do not need filler, and government employment-service portals are excluded from this workflow.

Redirects and rebrands of the same portal are deduplicated. Distinct boards are not merged merely because a parent company owns both.

## What you receive

Each entry includes its official URL, geographic scope and a short explanation of its practical strength. The researcher opens official country, category, search or job pages to establish current local tech coverage. A homepage, marketing banner or search-engine snippet alone does not pass.

The live result includes a verification date. Within each group, ⭐ marks two or three useful starting picks, or fewer if fewer qualify. Picks follow observed coverage and usable access, not reputation or invented numerical rankings.

A specific caveat can be marked with ⚠️, such as restricted access, deprecated service or shared ownership. Account access and eligibility for an individual job remain different facts.

## Partial or unavailable access

If one official page fails, another relevant public page on the same domain may establish useful coverage. If it still cannot be checked, move the portal out of the verified groups and explain the access limitation. Adding a caveat does not make an otherwise unverified entry a verified pick.

For example, a working homepage with a login-only job search does not prove current openings. An accessible search page with limited visible listings can support that observed coverage, with the limit stated.

If browsing is unavailable, wait for access or supplied evidence. User-supplied material retains its date and the label **user-supplied; not live verified**, separate from live-verified recommendations. It cannot receive a star that implies live checking.

Preserve successful partial results. When nothing can be verified, explain the specific gap rather than returning an empty success. The final grouped response ends the command; no profile, output file or checkpoint is created.

## Explore the source

For implementation details, read [prompts/portal-finder/step1-portal-research.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/portal-finder/step1-portal-research.md).
