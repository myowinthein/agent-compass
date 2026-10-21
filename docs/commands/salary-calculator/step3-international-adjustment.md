---
title: "Step 3: International adjustment"
parent: salary-calculator
grand_parent: Commands
nav_order: 3
---

# Step 3: International adjustment

Estimates a supported reduction from local salary benchmarks for your circumstances as an international candidate. It is a negotiation estimate, not a legal salary rule or guaranteed outcome.

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

The assistant uses observed local-versus-overseas offers, or a clearly labelled inference supported by candidate-applicable evidence. Generic market difficulty or sponsorship cost alone does not quantify a pay reduction.

Relevant factors include employer hiring practices, sponsorship friction, language, relocation and local-market familiarity. They apply only where relevant to your actual location, work rights and intended path. The same issue is not counted twice.

Race, ethnicity, passport prestige and generic nationality rankings are never adjustment factors. Formal degree recognition is a process caveat, not a priced penalty.

## Numeric limits

Reductions stay within 0–15%. A supported 0% is allowed. One common percentage applies independently to both employer tiers; evidence for only one tier cannot automatically justify both.

The typical midpoint determines the display label:

| Typical reduction | Label |
|---|---|
| 0–5% | Small |
| Above 5% through 10% | Moderate |
| Above 10% through 15% | Significant |

A midpoint above 10% needs specific concrete evidence. A Low salary evidence grade caps adjustment confidence at Medium. Missing grades stay disclosed rather than becoming an invented grade.

If no defensible common percentage exists, the result is **Adjustment not estimable**, with the missing evidence. Step 4 skips that country rather than assuming no reduction.

## What happens next

`salary-calculator-03-adjustments.md` saves each country's estimate, confidence and reasoning, or its unestimable reason. Chat shows brief counts.

You can choose a [specialist agent]({{ '/docs/specialist-agents.html' | relative_url }}) or keep your current model. The workflow then continues to [Step 4: Table calculation](step4-table-calculation.html).
