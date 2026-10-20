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

Read the candidate's situational profile before generating threshold research. Embed the relevant facts as literal text in the research brief: citizenship, current residence, target-country work rights/status, and supplied age/date of birth with its reference date. Use the supplied date of birth to establish age at the official rule's relevant date; an age without a reliable as-of date does not establish age at a future filing date. Do not infer immigration status from citizenship or residence alone.

Research which official pathway and age/status category actually applies, including whether the rule is based on application date or another event. Record the applicable category, eligibility assumptions, source, and effective date in the existing threshold field or Notes. Do not automatically choose the cheapest age-based threshold. If the candidate declined age disclosure or a material status/date is unknown, report the applicable figure as Unknown when a candidate-specific category cannot be confirmed; explain the conditional categories without inventing the missing fact. Do not classify the route as Blocked merely because eligibility is unknown.

For each country, report:
- The threshold figure (local currency), or which of the four non-numeric states applies (No fixed threshold / Not applicable / Unknown / Blocked)
- Whether that figure is annual or monthly
- The official government source and how recent it is
- If Blocked, the concrete reason (e.g. quota exhausted, category paused, an eligibility cutoff this candidate doesn't meet)

## How to compare

Compare both Mainstream and Premium Annual Targets with the applicable threshold using unrounded computed values. The displayed salary rounding (nearest 500 annual, nearest 50 monthly) must never decide a borderline result. Equality clears this salary-minimum comparison.

Use the threshold's verified original period. For a monthly threshold X, compare each raw Annual Target / 12 with X; for an annual threshold, compare the raw Annual Target directly. Record any annual/monthly conversion in shown work, not a second number in the compact table cell. Check comparable currency and eligible pay components first; an unconfirmable base-pay comparison stays Unknown rather than an invented pass or failure.

## Result states

The following rendering is canonical for the **Visa salary rule** column. Stored research keeps the original five state names; these are presentation labels, not new research fields.

- **No fixed threshold**: show `No fixed minimum`. Preserve any prevailing-wage, occupation-rate, or other compensation conditions in the saved shown work/audit. This is not a claim that no pay requirements apply.
- **Not applicable**: show `Not applicable`, only when the confirmed employment path does not use employer-sponsored relocation.
- **Unknown**: show `Unknown`, never a dash, N/A, a guessed figure, or a claimed block.
- **Blocked**: show `Blocked`, even if a numeric threshold is known. Retain the concrete candidate-specific route-blocking reason in the saved Summary. Do not claim every possible immigration route is blocked from evidence about the assessed route only.
- **Verified numeric**: show the exact verified figure in its original period with `/yr` or `/mo`, e.g. `45,300/yr` or `5,331/mo`. Never display-round a legal threshold, show an unqualified number, or duplicate both period equivalents in the cell. Candidate category, source, effective date, and any additional conditions stay in the existing shown work/audit.
  - If both raw segment targets meet the threshold, show the numeric rule without a warning.
  - If either raw target falls short, append a single ⚠️ and identify the affected segment(s) with the raw comparison in the saved Summary. This warning concerns the salary minimum only, not overall visa eligibility.

Never adjust Mainstream or Premium targets to meet a visa minimum. Market estimates and the visa rule remain separate facts. A threshold shortfall is not a blocked route: a higher actual offer may satisfy the salary requirement. A Blocked route does not zero or change salary estimates; they remain reference-only for sponsorship through that route.

## Legacy display compatibility

When an unfinished audit reads a legacy table, Safe maps to Mainstream and Stretch maps to Premium; Legal Requirement is the old column label. Recover threshold meaning from the underlying stored research, not display shorthand alone. A legacy dash cannot distinguish No fixed threshold from Not applicable by itself. If the source cannot establish a state, category, or period, render Unknown and explain the limitation rather than guessing. Preserve original research and pre-audit tables; completed final results are replayed as saved, never silently migrated.
