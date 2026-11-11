---
title: "Step 2: Data validation"
parent: salary-calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step2-data-validation.html
permalink: /docs/commands/salary-calculator/step2-data-validation/detailed.html
title_category: Details
description: "Validation checks whether salary research has the structure needed for later calculation. It preserves accepted evidence unchanged and records rejected or missing data without treating completeness as proof of market accuracy."
source_files:
  - prompts/salary-calculator/step2-data-validation.md
---

# Step 2: Data validation

{% include guide-depth.html %}

Validation checks whether salary research has the structure needed for later calculation. It preserves accepted evidence unchanged and records rejected or missing data without treating completeness as proof of market accuracy.

## Flow

```mermaid
flowchart TD
  Start(["Read salary-calculator-01-research.md"]) --> Bounds{"Country boundaries clear?"}
  Bounds -->|No| Ask["Ask for clarification<br/>Wait before storing"]
  Ask --> Bounds
  Bounds -->|Yes| Review["Review each country<br/>Both employer tiers and their sources"]
  Review --> Accept{"Complete and not already stored?"}
  Accept -->|Yes| Store["Copy accepted data verbatim"]
  Accept -->|No| Skip["Record the reason<br/>Keep originals for duplicates"]
  Store --> Save["Save stored data and Validation report<br/>Account for missing expected countries"]
  Skip --> Save
  Save --> Usable{"Any country stored?"}
  Usable -->|Yes| Next(["Show consolidated counts and reasons<br/>Continue to Step 3"])
  Usable -->|No| Repair(["Record the validation outcome<br/>Offer missing-evidence repair or stop"])
```

## Required data

Each country needs both employer tiers with their required amounts and sources. A figure in an unrelated example or another section cannot silently fill a missing tier field. Clear older labels receive semantic review rather than mechanical rejection based only on their spelling.

Missing visa-rule information or an evidence grade does not automatically reject otherwise usable salary data. An absent grade stays not provided; an unknown rule stays a limitation for later comparison.

Malformed or incomplete blocks are skipped with reasons. Duplicates preserve the stored original, which means a retained original is still a usable country rather than a missing result.

## Country boundaries

Generated input uses top-level `Country:` fields. If the boundary between countries is ambiguous, clarify it before ingestion instead of attaching a paragraph to whichever country appears closest.

Accepted bytes are preserved. The helper performs structural checks and saving; commentary and validation status stay outside the source blocks. Failed or partial saves leave the checkpoint pending until actual state is reconciled.

For example, a country can have complete salary tiers but no usable adjustment evidence. Validation can accept that research; the later adjustment step must still decide whether a numeric reduction is supported. Acceptance here does not authorize an assumed zero.

## What happens next

The validated-data file holds accepted research. The original research file retains the raw findings and separate Validation report, including rejected inputs and missing-country reasons.

With stored countries, continue to [International adjustment](../step3-international-adjustment.html). If none remain usable, the workflow offers evidence repair or stop before specialist questions, career-ladder intake or an empty final table.

Structural validation does not verify market claims, select salary targets or establish visa eligibility. Those require their later evidence and calculation steps.

## Explore the source

For implementation details, read [prompts/salary-calculator/step2-data-validation.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/salary-calculator/step2-data-validation.md).
