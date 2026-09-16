---
title: Step 4: Target calculation
parent: /salary-calculator
grand_parent: Commands
nav_order: 4
---

# Step 4: Target calculation

Uses deterministic arithmetic to turn verified market data and the capped adjustment into one practical expected-salary answer.

## Formula

```
Raw Target = Market Midpoint x (1 - Adjustment)
Expected Salary = max(Raw Target, Required Floor)
```

The Required Floor can include:

- verified Market Low,
- an applicable legal sponsorship threshold,
- a user-declared hard salary floor when reliably comparable.

A historical or context-only salary is never treated as a floor.

## Interview range

The lower bound is Expected Salary. The upper bound is the verified midpoint when it remains above the target, otherwise the verified Strong figure. The calculator never creates a range using arbitrary percentage padding.

## Visa status

The Visa Minimum column distinguishes:

- verified numeric amount,
- `None`, no fixed threshold,
- `N/A`, not applicable to the chosen path,
- `?`, unknown or unverified.

If the legal threshold exceeds Market Strong, the target remains visa-compliant and the audit records a market and visa conflict.

## Final table

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

Expected Annual is the application-form number. Expected Monthly is an annual divided by 12 comparison value. The interview range is the short recruiter answer.

Detailed calculations and currency-aware rounding rules are saved to `sc-step4-salary-table.md`. The table is shown to the user only after Step 5 verifies it.
