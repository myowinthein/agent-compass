---
title: "country-finder"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder.html
guide_source: workflows/country-finder.md
permalink: /docs/commands/country-finder/detailed.html
title_category: Detailed guide
description: "Complete procedure, choices, constraints and outcomes for country-finder."
---

# country-finder

{% include guide-depth.html %}

Find countries worth targeting for remote work or employer-sponsored relocation. Each path is assessed separately against your profile and current evidence.

## Flow

The run setup comes first. Saved results are replayed only after the matching chat and person have been established.

```mermaid
flowchart TD
  Start["Select the chat, person and command"] --> Existing{"Matching run?"}
  Existing -->|Completed| View{"View results or start fresh?"}
  View -->|View| Replay["Show the saved final result"]
  Existing -->|Unfinished| Resume{"Resume or start fresh?"}
  View -->|Fresh| New["Create a separate run; preserve earlier work"]
  Resume -->|Fresh| New
  Existing -->|No| New
  New --> Profile{"Confirmed profile reusable for this person?"}
  Profile -->|No| Extract["Extract resume; wait for confirmation before saving"]
  Profile -->|Yes| Ready["Use this run's confirmed profile"]
  Extract --> Ready
  Resume -->|Resume| Check["Validate saved inputs and the next unfinished step"]
  Ready --> Steps["Continue the pipeline below"]
  Check -->|Valid| Steps
  Check -->|Unusable or changed| Repair["Explain the issue; wait for the applicable repair choice"]
```

The six steps keep the two tracks independent. Exclusions and missing evidence still reach the final audit; an empty country scope needs a new list or a stop.

```mermaid
flowchart TD
  Criteria["1. Confirm background and search criteria"] --> Scope["2. Choose countries and research Remote/Sponsorship suitability"]
  Scope --> Empty{"Any countries in scope?"}
  Empty -->|No| Ask["Ask for a revised list or stop"]
  Empty -->|Yes| Research["3. Collect detailed research for eligible tracks; or save a scope-only record"]
  Research --> Data["4. Validate and store accepted research without rewriting it"]
  Data --> Saved{"Required outputs saved and checked?"}
  Saved -->|No| Hold["Preserve results; reconcile failure without advancing"]
  Saved -->|Yes| Assess["5. Assess fit/confidence per track; optional specialist"]
  Assess --> Audit["6. Audit every candidate, exclusions and gaps; optional specialist"]
  Audit --> Final["Save the audit and Priority Table; show the table in chat"]
```


## Complete procedure

{{ page.guide_source | guide_full }}
