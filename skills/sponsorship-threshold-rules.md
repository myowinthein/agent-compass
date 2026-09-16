---
name: Sponsorship Threshold Rules
description: Governs how Salary Calculator collects and compares government-mandated minimum salary thresholds for employer-sponsored work visas. Applies to Salary Calculator steps 1, 4, and 5b.
---

# Sponsorship Threshold Rules

## What counts as a threshold

A sponsorship salary threshold is a legally mandated minimum salary a country requires an employer to pay in order to sponsor this candidate's work visa. It is a hard eligibility rule, not a market benchmark and not the same thing as an international-candidate negotiation adjustment.

It is scoped to employer-sponsored work-visa relocation only. It does not apply to remote or independent-contractor arrangements — most remote hiring uses one of these, so most countries and roles will have no threshold to report at all.

Only report a threshold as a usable number if it is:
- A specific fixed figure in local currency, or
- A clearly computable multiple of a stated national average that you can resolve into an actual number

If the threshold is occupation-specific with no fixed figure, based on an unstated "prevailing wage," or you cannot confirm one exists at all, do not report a number — report "not applicable." Do not guess a figure to fill the gap.

If the threshold would structurally require including compensation components not reflected in a base-salary figure (e.g. mandatory housing allowance, guaranteed bonus counted toward the legal minimum), and you cannot isolate the base-salary-equivalent portion, report "not applicable" rather than an apples-to-oranges number.

## What to collect

For each country, report:
- The threshold figure (local currency), or "not applicable"
- Whether that figure is annual or monthly
- The official government source and how recent it is

## How to compare

Compare against the Fixed values (not the ranges) for both Safe and Stretch, using the unrounded computed figures — the table's display rounding (nearest 500 annual, nearest 50 monthly) happens only for presentation and must never be applied before this comparison, since it could flip a borderline result.

Convert the threshold to match whichever period (Annual or Monthly) the comparison needs — a monthly threshold reported as X converts to 12×X for an Annual comparison, and vice versa. Since Safe and Stretch each have one Annual Fixed value and one Monthly value, compare both, using whichever conversion matches the threshold's own reported period.

## Result states

- **No usable threshold** (none exists, or it isn't a comparable number) — show an em dash. Do not distinguish "legally no threshold" from "could not confirm one" — both render the same way.
- **Threshold exists** — show both period equivalents in one cell: the Annual figure first, then the Monthly figure in parentheses with a "/mo" suffix, e.g. `45,300 (3,775/mo)`. Neither figure is rounded — both are specific legal figures, shown exactly as reported or derived from it via the ×12/÷12 conversion.
  - If both Safe and Stretch Fixed values clear it (at the period the threshold was actually reported in), show the cell as above with no warning.
  - If either Safe or Stretch Fixed value falls short, append a single ⚠️ at the end of the cell — the warning applies to the country as a whole, not to one period only.

Never adjust Safe or Stretch to meet the threshold. The threshold failing means the calculated market salary is unlikely to qualify through this sponsorship route, not that the market figure itself is wrong — the two facts are shown side by side, never merged.
