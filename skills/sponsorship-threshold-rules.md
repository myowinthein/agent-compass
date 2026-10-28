---
name: Sponsorship Threshold Rules
description: Shared candidate-specific employer-sponsored visa salary states, research and eligible-pay comparison rules for Salary Calculator and Country Finder.
---

# Sponsorship Threshold Rules

## What counts as a threshold

A threshold is the legal minimum salary an employer must pay to sponsor this candidate's work-visa relocation. Keep it separate from market benchmarks and negotiation adjustments. Cross-border remote or independent-contractor work outside that route does not qualify; an international/remote-first employer alone establishes neither employment path nor work location. Unknown intent is not Not applicable.

Salary Calculator always researches an employer-sponsored route as reference information alongside local employee salary benchmarks. This reference assessment does not require or establish a personal relocation plan. Do not ask the user to select an employment path or omit the reference research because they currently work remotely or have not decided to relocate. Apply known candidate facts to the relevant category and disclose material unknowns; lack of a relocation choice alone is not Not applicable. Country Finder still assesses its actual Remote and Sponsorship tracks separately.

A usable number must be a confirmed fixed local-currency amount or a computable national-average multiple resolved to an actual amount. Classify each assessed country/path into exactly one state:

- **Verified numeric:** a specific amount is confirmed, including a resolved multiple.
- **No fixed threshold:** a route exists without a fixed numeric minimum, such as an unstated prevailing-wage test.
- **Not applicable:** the confirmed path does not use employer-sponsored relocation.
- **Unknown:** a plausible route exists, but its current number or whether it has one cannot be confirmed.
- **Blocked:** official rules make a real route unavailable to this candidate now, such as a closed quota, pause or unmet age/occupation/status cutoff. State the concrete reason. The route may have a known or unknown threshold; this is neither missing evidence nor an inapplicable path.

Never guess an amount or collapse Unknown/Blocked into Not applicable. If the legal amount includes compensation absent from the researched base pay, such as allowances or guaranteed bonuses, and no comparable base portion can be isolated, use Unknown.

## What to collect

Read the situational profile before research. Embed relevant citizenship, residence, target-country rights/status and supplied age/date of birth with reference date literally in each brief. Infer neither rights from citizenship/residence nor future filing age from an undated age. Use a supplied birth date at the official rule's relevant date.

Establish the actual pathway/category, age/status conditions and applicable event date. Record category, assumptions, official source and effective date in the existing threshold field or Notes. Never choose the cheapest age category automatically. Respect declined age disclosure; missing material facts leave candidate-specific amounts Unknown, with conditional categories explained. Unknown eligibility is not Blocked.

Record each country's:

- Figure or explicit nonnumeric state.
- Original annual/monthly period.
- Official government source and recency.
- Monthly eligible-pay components/schedule and whether researched annual base / 12 is legally comparable; retain missing/incompatible basis.
- Concrete Blocked reason when applicable.

## How to compare

Compare Mainstream and Premium Annual Targets using unrounded computed values, never display-rounded salaries. Equality clears this salary-minimum comparison.

Use the original verified period and comparable eligible components. Compare annual rules directly. For a monthly rule X, compare raw Annual Target / 12 with X only when the official definition and researched pay schedule support it. Extra guaranteed payments or a different monthly-base definition may prevent comparison; a display reference proves no legal comparability.

Keep the official basis/conversion in shown work, not a second compact-cell number. If unknown or incompatible with the helper's annual/12 method, render Unknown and omit numeric visa requests to the helper/renderer. Retain any known figure, period, source and reason in shown work. Do not change the original period or imply a different legal formula was checked. Salary targets and monthly display references remain unchanged.

Completed legacy outputs replay unchanged. Establish this comparability before claiming a verified numeric result in an unfinished legacy monthly check.

## Result states

Read `data/output-contracts.json` for exact `salary.visa_labels`, numeric state, period suffixes and warning token; render through `skills/output-helper.md`. The same contract supports approved manual processing. Keep the original five research-state names without new dataset fields.

For No fixed threshold, preserve prevailing-wage and other pay conditions in shown work: no fixed number does not mean no pay rules. Not applicable needs a confirmed path outside sponsored relocation. Unknown is neither a dash, guess nor claimed block. Blocked retains its concrete reason and reference-only note even when a number is known; do not extend it to unassessed routes.

Display a verified figure exactly in its original period with the contract suffix, without rounding or both period equivalents. Category, source, effective date and additional conditions stay in shown work. Append one warning when either raw target misses the minimum; identify affected segments and exact shortfalls in Summary. A pass is not overall visa eligibility.

Never change targets to meet a visa minimum. A shortfall is not Blocked: a higher offer may qualify. A Blocked route leaves estimates unchanged as reference-only salaries for sponsorship through that route.

## Legacy display compatibility

For unfinished audits, Safe means Mainstream, Stretch means Premium and Legal Requirement is the old column label. Recover meaning from stored research, not shorthand: a dash cannot distinguish No fixed threshold from Not applicable. Unestablished state/category/period renders Unknown with its limitation. Preserve research and pre-audit tables; completed finals replay without migration.
