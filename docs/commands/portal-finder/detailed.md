---
title: "portal-finder"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/portal-finder.html
guide_source: workflows/portal-finder.md
permalink: /docs/commands/portal-finder/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for portal-finder."
---

# portal-finder

{% include guide-depth.html %}

Finds verified job portals for IT/tech roles in one country. It needs a country, not your resume or a completed Country Finder run.

## Flow

```mermaid
flowchart TD
  Start(["Run portal-finder"]) --> Country{"Exactly one country established?"}
  Country -->|No| Ask["Ask for one country<br/>Wait for your answer"]
  Ask --> Country
  Country -->|Yes| Research["Research portals on their own sites<br/>Check current country-relevant tech coverage"]
  Research --> Output(["Show grouped links and starting picks<br/>Disclose verification limits"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
