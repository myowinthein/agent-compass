---
title: "Step 4: Data validation"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step4-data-validation.html
guide_source: prompts/country-finder/step4-data-validation.md
permalink: /docs/commands/country-finder/step4-data-validation/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Step 4: Data validation."
---

# Step 4: Data validation

{% include guide-depth.html %}

Store structurally complete research unchanged. This checks required content, not the truth of claims.

## Flow

```mermaid
flowchart TD
  Start(["Read Step 3 research and eligible tracks"]) --> Bounds{"Country blocks clear?"}
  Bounds -->|No| Ask["Ask for clarification<br/>Wait before storing"]
  Ask --> Bounds
  Bounds -->|Yes| Check["Review each block<br/>One recognisable country<br/>Required track fields present<br/>Eligible under Step 2"]
  Check --> Valid{"Valid and not already stored?"}
  Valid -->|No| Skip["Record the skip reason<br/>Keep the original for duplicates"]
  Valid -->|Yes| Store["Copy accepted data verbatim"]
  Skip --> Report["Save stored data and one validation report<br/>Account for missing expected countries"]
  Store --> Report
  Report --> Saved{"Files saved successfully?"}
  Saved -->|No| Failure(["Report failure<br/>Inspect before retrying; do not advance"])
  Saved -->|Yes| Next(["Show consolidated counts and reasons<br/>Continue to Step 5"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
