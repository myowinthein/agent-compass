---
name: Sponsorship Threshold Rules
description: Governs collection and use of candidate-specific salary thresholds for employer-sponsored work authorization.
---

# Sponsorship Threshold Rules

## Scope

A sponsorship salary threshold is a legally mandated pay floor for a specific work-authorization route. It is not a market salary, recruiter preference, or international-candidate discount.

Apply a threshold only when the chosen employment basis is local employment or relocation and the route is plausibly applicable to this candidate. Cross-border remote or independent-contractor work normally has no destination-country sponsorship threshold.

## Required threshold record

For each country, store:

- Status: `verified numeric`, `no fixed threshold`, `not applicable to chosen path`, or `unknown / unverified`
- Visa or permit route
- Candidate-applicability conditions, including age, occupation, experience, education, residence, and new-entrant rules where relevant
- Amount and local currency
- Reported period: hourly, monthly, or annual
- Compensation basis: base salary, guaranteed cash compensation, allowances, holiday allowance, or another legally defined basis
- Effective date or validity period
- Official government source URL and access date

Never use an abstract passport ranking. Citizenship matters only through concrete eligibility rules, restrictions, processing requirements, or documented employer obligations.

## What counts as verified numeric

A threshold is usable only when an official source provides:

- a fixed numeric amount, or
- a formula that can be resolved into a numeric amount for this candidate, role, location, and date.

An occupation-specific prevailing wage may be used when the official system provides a verifiable numeric figure for the target occupation and location. If the amount cannot be resolved, mark it `unknown / unverified`, not `no fixed threshold`.

Do not combine base salary with allowances, bonuses, equity, or benefits unless the legal rule explicitly counts those components and the salary dataset uses the same basis.

## Period conversion

Convert a monthly threshold to an annual equivalent only when multiplying by 12 is legally and economically comparable to the researched annual base salary. Do not assume this when holiday allowance, 13th/14th-month salary, hourly rules, or guaranteed allowances change the basis.

When a clean conversion is not possible, preserve the official period and compare on that same basis. Record any limitation.

## Use in the final target

The verified threshold is a hard floor for a sponsorship-based expected salary:

- Compare it with the unrounded recruiter-friendly target.
- If the target is below the threshold, raise the displayed target to the threshold and round upward using the country's normal salary increment.
- If the threshold exceeds the researched strong-market figure, keep the visa-compliant target but flag a `market / visa conflict` in the audit.
- Never lower the market evidence or claim the market midpoint changed merely because a legal floor applies.

Display states:

- Verified numeric: show the figure and period.
- No fixed threshold: `None`.
- Not applicable to chosen path: `N/A`.
- Unknown or unverified: `?`.

These states must never be collapsed into a single em dash.
