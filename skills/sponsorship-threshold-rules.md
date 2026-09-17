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

Classify every country into exactly one of five states, never collapsing them into each other:
- **Verified numeric**: a specific fixed figure (or a computable multiple you resolved into one) is confirmed.
- **No fixed threshold**: an employer-sponsored route exists but has no fixed numeric minimum, e.g. it relies on an unstated "prevailing wage" test instead.
- **Not applicable**: the confirmed employment path doesn't use employer-sponsored relocation (most remote and contractor arrangements).
- **Unknown**: a plausible employer-sponsored route exists but its current figure, or whether it has one at all, couldn't be confirmed.
- **Blocked**: a real employer-sponsored route exists (possibly with its own confirmed or unconfirmed threshold), but current official rules make it unavailable to this specific candidate right now, e.g. an exhausted quota, a paused category, or an eligibility cutoff (age, occupation category, prior status) this candidate doesn't meet. This is different from Unknown (we can't confirm a figure) and from Not applicable (the candidate isn't pursuing sponsorship at all) — a Blocked route is real but currently closed to this candidate specifically. State the concrete reason it's blocked.

Never report a guessed figure to fill the gap, and never report "not applicable" when the real situation is "couldn't confirm" or "blocked" — these are different states with different implications for the candidate and must stay distinguishable in what gets stored.

If the threshold would structurally require including compensation components not reflected in a base-salary figure (e.g. mandatory housing allowance, guaranteed bonus counted toward the legal minimum), and you cannot isolate the base-salary-equivalent portion, report it as Unknown rather than an apples-to-oranges number.

## What to collect

For each country, report:
- The threshold figure (local currency), or which of the four non-numeric states applies (No fixed threshold / Not applicable / Unknown / Blocked)
- Whether that figure is annual or monthly
- The official government source and how recent it is
- If Blocked, the concrete reason (e.g. quota exhausted, category paused, an eligibility cutoff this candidate doesn't meet)

## How to compare

Compare against the Fixed values (not the ranges) for both Safe and Stretch, using the unrounded computed figures — the table's display rounding (nearest 500 annual, nearest 50 monthly) happens only for presentation and must never be applied before this comparison, since it could flip a borderline result.

Convert the threshold to match whichever period (Annual or Monthly) the comparison needs — a monthly threshold reported as X converts to 12×X for an Annual comparison, and vice versa. Since Safe and Stretch each have one Annual Fixed value and one Monthly value, compare both, using whichever conversion matches the threshold's own reported period.

## Result states

- **No fixed threshold** or **Not applicable** — show an em dash (—). Both mean there is genuinely nothing to compare against; render them the same way.
- **Unknown** — show a question mark (?), never an em dash. This means a plausible route exists but its figure couldn't be confirmed, which is materially different from "there is nothing to check" and must stay visually distinct.
- **Blocked** — show the literal word `Blocked`, never an em dash or a number, even if a figure was otherwise confirmed. A blocked route is a live fact the candidate needs to see, not an absence of data.
- **Verified numeric** — show both period equivalents in one cell: the Annual figure first, then the Monthly figure in parentheses with a "/mo" suffix, e.g. `45,300 (3,775/mo)`. Neither figure is rounded — both are specific legal figures, shown exactly as reported or derived from it via the ×12/÷12 conversion.
  - If both Safe and Stretch Fixed values clear it (at the period the threshold was actually reported in), show the cell as above with no warning.
  - If either Safe or Stretch Fixed value falls short, append a single ⚠️ at the end of the cell — the warning applies to the country as a whole, not to one period only.

Never adjust Safe or Stretch to meet the threshold. The threshold failing means the calculated market salary is unlikely to qualify through this sponsorship route, not that the market figure itself is wrong — the two facts are shown side by side, never merged. A Blocked route follows the same principle: it never zeroes or changes Safe or Stretch, it just means those figures aren't a live sponsorship target for this candidate right now, independent of what the numbers themselves say.
