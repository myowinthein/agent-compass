---
title: "Step 3: International adjustment"
parent: salary-calculator
grand_parent: Commands
nav_order: 3
---

# Step 3: International adjustment

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

## What supports an estimate

Use observed local-versus-overseas offers or a labelled inference supported by relevant evidence. General market difficulty or sponsorship costs alone do not quantify a reduction.

Factors follow actual location, work rights and intended employment path without double-counting. Race, ethnicity and passport prestige never price adjustments. Formal degree recognition remains a process caveat, not a penalty.

## Numeric limits

One supported reduction applies independently to both tiers, within 0–15%. Its typical midpoint sets the label:

| Typical reduction | Label |
|---|---|
| 0–5% | Small |
| Above 5% through 10% | Moderate |
| Above 10% through 15% | Significant |

Above 10% needs concrete evidence. Low salary evidence caps confidence at Medium; missing grades stay disclosed.

Supported zero is valid. Unsupported percentages become **Adjustment not estimable**, with reasons, and Step 4 skips them rather than substituting 0%.

## What happens next

The assistant saves estimates, confidence and gaps to `salary-calculator-03-adjustments.md`; chat shows counts. An optional [specialist]({{ '/docs/specialist-agents.html' | relative_url }}) can run the step before [Table calculation](step4-table-calculation.html).
