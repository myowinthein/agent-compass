---
title: "Step 6: Final ranking"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step6-final-ranking.html
guide_source: prompts/country-finder/step6-final-ranking.md
permalink: /docs/commands/country-finder/step6-final-ranking/detailed.html
title_category: Detailed guide
description: "Complete procedure, choices, constraints and outcomes for Step 6: Final ranking."
---

# Step 6: Final ranking

{% include guide-depth.html %}

Audit the assessments and assign practical application priorities. This step runs even without a specialist.

## Flow

```mermaid
flowchart TD
  Start(["Offer the optional deep-reasoner<br/>Or use your current model"]) --> C1["Check confidence<br/>Is it backed by specific, dated evidence?"]
  C1 --> C2["Check missing countries and tracks<br/>Preserve early exclusions<br/>Distinguish missing from rejected research"]
  C2 --> C3["Check evidence use<br/>Local remote is not cross-border hiring<br/>A visa route is not employer willingness<br/>One vacancy is not a deep market"]
  C3 --> Verdict{"Evidence supports a revision?"}
  Verdict -->|Yes| Revise["Revise affected fits or confidence<br/>Explain the evidence"]
  Verdict -->|No| Keep["Keep supported assessments<br/>Name inconclusive findings"]
  Revise --> Summary["Build the post-audit Summary<br/>Account for every candidate on both tracks"]
  Keep --> Summary
  Summary --> Priority["Assign application priorities and limitations<br/>Check the saved Summary and table agree"]
  Priority --> Save["Save audit, Summary, Priority Table<br/>and Effort Allocation"]
  Save --> End(["Show the Priority Table in chat<br/>Confirm completion and saved file"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
