---
title: "Step 5: Final verification"
parent: salary-calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step5b-final-verification.html
guide_sources:
  - prompts/salary-calculator/step5a-career-ladder.md
  - prompts/salary-calculator/step5b-final-verification.md
permalink: /docs/commands/salary-calculator/step5b-final-verification/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Step 5: Final verification."
---

# Step 5: Final verification

{% include guide-depth.html %}

Audit the framework against your target role and saved evidence whenever at least one country was calculated.

## Flow

```mermaid
flowchart TD
  Start(["Draft the career ladder for your actual role<br/>Or reuse a matching confirmed ladder"]) --> Confirm{"Confirmed for this target?"}
  Confirm -->|No| Edit["Show the ladder<br/>Wait for your confirmation or edits"]
  Edit --> Confirm
  Confirm -->|Yes| Model["Offer the optional deep-reasoner<br/>Or use your current model"]
  Model --> Audit["Audit candidate positioning, framework calibration,<br/>each country and framework recommendations"]
  Audit --> Current{"Essential current visa evidence missing?"}
  Current -->|Yes| Choice["Wait for your choice<br/>Refresh evidence, use the dated snapshot or stop"]
  Choice -->|Approved evidence or snapshot| Verdict
  Current -->|No| Verdict{"Market revision supported?"}
  Verdict -->|Yes| Recal["Revise affected targets from evidence<br/>Recheck visa rules and your salary floor"]
  Verdict -->|No| Keep["Keep valid targets<br/>Distinguish supported from inconclusive"]
  Recal --> Final["Render and check the final table<br/>Record any approved visa-only update separately"]
  Keep --> Final
  Final --> Save["Save checks, verdict, table and skip reasons<br/>Leave earlier research and Step 4 unchanged"]
  Save --> End(["Show the standard caption and final table<br/>Report audited count and any inconclusive findings"])
```

## Career ladder procedure

{{ 'prompts/salary-calculator/step5a-career-ladder.md' | guide_full }}

## Final audit procedure

{{ 'prompts/salary-calculator/step5b-final-verification.md' | guide_full }}
