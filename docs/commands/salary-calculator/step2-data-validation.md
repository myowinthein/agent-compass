---
title: "step 2: data validation"
parent: salary-calculator
grand_parent: Commands
nav_order: 2
description: Store accepted salary research unchanged after structural checks, preserving sources and original duplicates without claiming market verification.
detailed: /docs/commands/salary-calculator/step2-data-validation/detailed.html
has_toc: false
---

# Step 2: Data validation

{% include guide-depth.html %}

Store accepted salary research unchanged, without verifying market claims or calculating targets.

## Flow

```mermaid
flowchart TD
  Check["Check country blocks and both salary tiers"] --> Save["Store accepted research without rewriting it"]
  Save --> Next["Continue with usable data or offer repair"]
```

## Required data

Each country needs both employer tiers and their sources. Other sections or quoted examples cannot supply missing tier fields.

Missing visa rules or evidence grades do not reject a country; an absent grade stays "not provided". Malformed/incomplete blocks are reported and skipped. Duplicates preserve stored originals; clear legacy labels receive semantic review.

## Country boundaries

Generated blocks use top-level `Country:` fields. Ambiguity needs clarification. Helpers preserve accepted bytes and check coverage; failed or partial saves leave the checkpoint pending until reconciled.

## What happens next

- `salary-calculator-02-validated-data.md`: accepted data.
- `salary-calculator-01-research.md`: raw findings and separate Validation report.

The report retains rejection and missing-country reasons. A duplicate with a retained original is not a failed country.

With stored countries, continue to [International adjustment](step3-international-adjustment.html). Otherwise, offer evidence repair or stop before specialists or career-ladder intake.
