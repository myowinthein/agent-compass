---
title: "Step 1: Research prompt generator"
parent: salary-calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step1-research-prompt-generator.html
guide_source: prompts/salary-calculator/step1-research-prompt-generator.md
permalink: /docs/commands/salary-calculator/step1-research-prompt-generator/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Step 1: Research prompt generator."
---

# Step 1: Research prompt generator

{% include guide-depth.html %}

Confirm countries and collect sourced local salary benchmarks for your role and level.

## Flow

```mermaid
flowchart TD
  Start(["Read or collect your situational profile<br/>Settle any unclear role or level"]) --> CF{"Usable Country Finder result?"}
  CF -->|Yes| Offer["Offer countries with a final Strong or Moderate fit<br/>Use the post-audit Summary"]
  CF -->|No| ManualList["Ask for your target countries<br/>Explain any draft or incompatible source"]
  Offer --> Confirm["Wait for your country choice<br/>Use, add, remove or start fresh"]
  ManualList --> Confirm
  Confirm --> Scope["Use local-employee salary benchmarks<br/>Research visa salary rules as a separate reference"]
  Scope --> Brief["One self-contained brief per country<br/>Two employer tiers, sources and visa salary rules"]
  Brief --> Cap{"Separate research context<br/>with web access available?"}
  Cap -->|Yes| Tasks["Research each country separately"]
  Cap -->|No| Manual["Show prompts<br/>Wait for manual results"]
  Tasks --> Collect["Save scope and country findings<br/>Resolve missing results"]
  Manual --> Collect
  Collect --> Next(["Save salary-calculator-01-research.md<br/>Continue to Step 2"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
