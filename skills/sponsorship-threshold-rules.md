---
name: Sponsorship Threshold Rules
description: Shared candidate-specific employer-sponsored visa salary states, research and eligible-pay comparison rules for Salary Calculator and Country Finder.
---

# Sponsorship Threshold Rules

## What counts as a threshold

A sponsorship salary threshold is a legally mandated minimum salary a country requires an employer to pay in order to sponsor this candidate's work visa. It is a hard eligibility rule, not a market benchmark and not the same thing as an international-candidate negotiation adjustment.

It is scoped to employer-sponsored work-visa relocation only, not a confirmed cross-border remote or independent-contractor arrangement outside that route. An employer being international or remote-first does not establish the candidate's employment path or where they work. Use the confirmed path and status; an unknown path is not evidence for Not applicable.

Only report a threshold as a usable number if it is:
- A specific fixed figure in local currency, or
- A clearly computable multiple of a stated national average that you can resolve into an actual number

Classify each assessed country/path into exactly one of five states, never collapsing them into each other:
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
- For a monthly rule, what pay components and payment schedule the official monthly amount counts, and whether raw annual base / 12 is an eligible comparable amount for the researched salary basis; otherwise preserve the missing or incompatible basis
- If Blocked, the concrete reason (e.g. quota exhausted, category paused, an eligibility cutoff this candidate doesn't meet)

## How to compare

Compare both Mainstream and Premium Annual Targets with the applicable threshold using unrounded computed values. The displayed salary rounding from data/output-contracts.json must never decide a borderline result. Equality clears this salary-minimum comparison.

Use the threshold's verified original period. For an annual threshold, compare the raw Annual Target directly after confirming comparable eligible components. For a monthly threshold X, compare raw Annual Target / 12 with X only when the official monthly definition and the researched pay schedule support that annualization. Extra guaranteed payments or a different legal definition of ordinary monthly base can make that reference incomparable. A monthly display reference is not proof of eligible monthly pay.

Record the official pay/annualization basis and any conversion in shown work, not a second number in the compact table cell. If the basis is unknown or cannot be represented by the helper's annual/12 comparison, use Unknown for the compact visa result and omit the numeric visa request to the helper/renderer. Retain any known original figure, period, source and reason in shown work. Do not change the threshold's original period or pretend the helper checked a different legal-pay formula. The salary targets and their annual/12 display references remain unchanged. Completed legacy outputs replay as saved; an unfinished legacy monthly check needs this comparability established before claiming a verified numeric result.

## Result states

Read data/output-contracts.json as data for the exact `salary.visa_labels`, numeric state, period suffixes and warning token. Use skills/output-helper.md to render them; the same contract is readable without Python. Stored research keeps the original five state names, not new dataset fields.

For a route with no fixed threshold, preserve any prevailing-wage or other compensation conditions in shown work: absence of a fixed number is not absence of all pay rules. Not applicable requires a confirmed path outside employer-sponsored relocation. Unknown must not become a dash, a guess or a claimed block. A Blocked route retains its concrete reason and reference-only note even if a number is known; never generalize to unassessed routes.

For a verified number, display the exact figure in its original period using the contract suffix, without display-rounding or showing both period equivalents. Keep category, source, effective date and additional conditions in shown work. The renderer appends one warning only when either raw target misses the salary minimum; identify the affected segments and exact shortfall in Summary. A passed comparison is not overall visa eligibility.

Never adjust Mainstream or Premium targets to meet a visa minimum. Market estimates and the visa rule remain separate facts. A threshold shortfall is not a blocked route: a higher actual offer may satisfy the salary requirement. A Blocked route does not zero or change salary estimates; they remain reference-only for sponsorship through that route.

## Legacy display compatibility

When an unfinished audit reads a legacy table, Safe maps to Mainstream and Stretch maps to Premium; Legal Requirement is the old column label. Recover threshold meaning from the underlying stored research, not display shorthand alone. A legacy dash cannot distinguish No fixed threshold from Not applicable by itself. If the source cannot establish a state, category, or period, render Unknown and explain the limitation rather than guessing. Preserve original research and pre-audit tables; completed final results are replayed as saved, never silently migrated.
