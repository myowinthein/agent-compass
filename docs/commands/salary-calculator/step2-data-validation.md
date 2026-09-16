---
title: Step 2: Evidence validation
parent: /salary-calculator
grand_parent: Commands
nav_order: 2
---

# Step 2: Evidence validation

Verifies and normalizes the research instead of storing it passively.

## Checks

For each country, Claude confirms:

- one country and one employment basis,
- confirmed target role and level,
- currency and annual gross base-salary basis,
- numerical order, `Low <= Midpoint <= Strong`,
- source support for role, level, location, date, and amount,
- separation of base salary from bonuses, equity, allowances, net pay, and contractor rates,
- city variation where material,
- candidate-specific sponsorship threshold details.

Duplicate reposts do not count as independent sources.

## Repair behavior

Missing, stale, inaccessible, or contradictory evidence triggers targeted research. A country is skipped only when a defensible midpoint still cannot be established.

Each stored country receives a High, Medium, or Low evidence grade.

## Output

Validated and normalized records are saved to `sc-step2-salary-data.md` in confirmed country order, including repair notes and verified sources.
