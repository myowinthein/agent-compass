---
title: "Step 3: International adjustment"
parent: salary-calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step3-international-adjustment.html
guide_source: prompts/salary-calculator/step3-international-adjustment.md
permalink: /docs/commands/salary-calculator/step3-international-adjustment/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Step 3: International adjustment."
---

# Step 3: International adjustment

{% include guide-depth.html %}

Estimate a supported reduction from local benchmarks for your circumstances. This models negotiation, not legal pay rules or guaranteed offers.

## Flow

```mermaid
flowchart TD
  Start(["Read stored salary evidence and confirmed profiles<br/>Clarify material missing context"]) --> Model["Offer the optional deep-reasoner<br/>Or use your current model"]
  Model --> Review["Review each country's evidence<br/>Use the confirmed employment path and actual status"]
  Review --> Basis{"One common percentage supported for both tiers?"}
  Basis -->|Yes| Estimate["State the range, typical reduction and evidence basis<br/>Assign label and confidence"]
  Estimate --> Check["Check bounds, midpoint and confidence limits<br/>The helper does not judge evidence quality"]
  Basis -->|No| Unknown["Record Adjustment not estimable<br/>Name the gap; do not substitute 0 percent"]
  Check --> Save["Save salary-calculator-03-adjustments.md"]
  Unknown --> Save
  Save --> Next(["Show estimated and unestimable counts<br/>Continue to Step 4"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
