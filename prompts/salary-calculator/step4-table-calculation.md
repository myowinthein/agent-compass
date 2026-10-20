Check whether sc-step2-salary-data.md exists in the workspace. If it does not exist, stop and tell me: "sc-step2-salary-data.md was not found. Please ensure Step 2 completed successfully before continuing."

Check whether sc-step3-adjustment-values.md exists in the workspace. If it does not exist, stop and tell me: "sc-step3-adjustment-values.md was not found. Please ensure Step 3 completed successfully before continuing."

If both files exist, read them. Using the adjustment values from sc-step3-adjustment-values.md and the salary data from sc-step2-salary-data.md, calculate adjusted salary targets for each country.

Read and apply skills/salary-calculation-helper.md. The parent runs the shared numeric helper before an optional calculator handoff; both hosts use the same implementation. Use its exact results for every supported calculation in this step. Manual arithmetic requires the explicit user choice described there. Do not compute by intuition; precision takes priority over speed.

Read situational-profile.md. Note whether a salary minimum was given there and, if so, whether it was marked a hard floor or context only — this is used only for the flag described under Summary below, never to change Mainstream or Premium.

Read and apply skills/sponsorship-threshold-rules.md for the Visa salary rule column. This shared rule is the canonical source of its display states, period labels, and warning behavior.

Read and apply skills/salary-comparison-rules.md for the candidate's minimum, including currency/period/basis normalization and comparison-only FX. Record the dated rate and unrounded calculation in Show Your Work or Summary, not the salary table. An unavailable or non-comparable minimum check is unverified, not a proven shortfall.

Only calculate countries that have BOTH:

- salary data
- international candidate adjustment data

Skip countries with missing data.

Also read the Research scope and Validation report in sc-step1-salary-research.md if available. Reconcile the confirmed scope, research/ingestion rejections, salary datasets, and adjustment datasets: every expected country must be calculated or listed as skipped with its actual reason. Do not fabricate table rows for rejected data or count a rejected duplicate whose original survived as a skipped country. If legacy scope/report information is missing, say which coverage or ingestion outcome cannot be established instead of silently claiming complete coverage.

Ordering: check whether cf-step6-final-ranking.md exists in the workspace.
- If it exists, read its Priority Table and order the countries in this step's output to match that table's order, top to bottom.
- Append calculated countries not present in that Priority Table afterward, alphabetically by country name. Do not omit user-added countries.
- If it does not exist, order countries alphabetically by country name (A→Z).

Definitions

- Market Midpoint = the "Realistic" value for the relevant tier, as provided in the salary dataset. Do not average, estimate, or derive it any other way.
- Mainstream uses the Mid-size / Mainstream Local-Market tier.
- Premium uses the Premium / International / Remote-first tier.
- These are employer segments, not guarantees, personal salary floors, or automatic visa-qualifying offers. Do not estimate new tiers or derive Premium by adding a generic uplift to Mainstream.

Calculation Rules

1. Apply the country's typical midpoint international candidate adjustment independently to each segment's Market Midpoint:

Annual Target = Market Midpoint x (1 - Adjustment %)

2. Keep both Annual Targets unrounded internally. Monthly Reference = unrounded Annual Target / 12. Use these raw amounts for sponsorship-threshold and candidate-minimum comparisons, never displayed rounded figures.

3. Round each displayed salary independently, once, at final formatting: Annual to nearest 500; Monthly to nearest 50; exact halfway ties upward for nonnegative amounts. Use decimal/rational or otherwise verified arithmetic to avoid floating-point tie errors. Recomputing Monthly from the displayed Annual may differ from the displayed Monthly; retain the raw calculation.

4. Do not generate automatic -5%/+10% ranges or a universal interview range. Retain the original researched Low/Realistic/Strong figures in their existing research and stored-data files; they are not automatically a negotiation range. Any discussion of a negotiation range belongs in the saved audit, tied to the applicable employer segment and actual evidence, not an invented percentage band.

5. Compare both raw segment targets with the candidate-specific sponsorship threshold using skills/sponsorship-threshold-rules.md. The Visa salary rule column is independent of market targets; never change targets to clear it.

File format (write this structure to sc-step4-salary-table.md; only a brief calculated/skipped count is shown in chat at this step):

Show Your Work

For every country and segment, record Market Midpoint, typical midpoint Adjustment %, raw Annual Target, raw Monthly Reference, and independently rounded display values. Record the sourced threshold in its original period, applicable candidate category, effective date and official source, comparison arithmetic, and which segment misses it when applicable. Keep any additional wage conditions visible in the saved explanation.

Include the calculation-method disclosure from skills/salary-calculation-helper.md. Check the helper's echoed inputs against the source files and preserve exact fractional raw amounts when needed.

Table

Put this exact caption immediately before the table:

Gross base salary in local currency. Monthly figures are annual ÷ 12 references, not necessarily payslips; targets are market estimates, not visa-eligibility guarantees.

Use ONLY these columns, in this exact order:

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |

- One row per calculated country, in the order specified above.
- Place the flag before the country name and put the local currency code after it, e.g. "🇩🇪 Germany (EUR)".
- Each of the four salary cells contains a single comma-formatted number, with no range, parentheses, currency symbol, or repeated currency code. No USD conversion.
- Right-align the four numeric salary columns; left-align Country and Visa salary rule.
- Render Visa salary rule using skills/sponsorship-threshold-rules.md: a period-labeled exact threshold, or the distinct explicit state label. Do not replace it with a status-only check.
- No extra columns, inline citations, revision markers, or footnotes. Explanations and sources stay in Show Your Work and Summary.

Formatting examples only, not current market or visa facts. Each displayed Annual Target is also its raw input in these examples; a real run still computes Monthly and threshold checks before rounding. Their order is illustrative; a real run follows Country Finder or alphabetical ordering.

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |
|---|---|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | 45,300/yr | 59,500 | 74,500 | 4,950 | 6,200 |
| 🇳🇱 Netherlands (EUR) | 5,331/mo ⚠️ | 56,500 | 70,000 | 4,700 | 5,850 |
| 🇺🇸 United States (USD) | Not applicable | 140,000 | 175,000 | 11,650 | 14,600 |
| 🇦🇺 Australia (AUD) | Blocked | 95,000 | 118,000 | 7,900 | 9,850 |
| 🇯🇵 Japan (JPY) | No fixed minimum | 7,800,000 | 10,200,000 | 650,000 | 850,000 |
| 🇬🇧 United Kingdom (GBP) | Unknown | 60,000 | 78,000 | 5,000 | 6,500 |

Summary

- Countries calculated: X
- Countries skipped: Y

List every skipped country with its actual reason, including earlier ingestion failures carried from the Research scope and Validation report. Do not invent a row for missing data or count a retained duplicate as a skipped country.

For a hard-floor candidate salary minimum, flag any raw Mainstream target below it with the normalized amounts and specific gap. Preserve an unverified comparison as unverified when currency, period, or pay basis cannot be established. This is a Summary flag only; never change either target to meet it.

For each Blocked route, retain its concrete reason and state that both salary targets are reference-only for sponsorship through that route. For No fixed minimum, retain any prevailing-wage, occupation-rate, or other pay conditions; absence of a fixed number does not mean there are no salary requirements. A threshold comparison alone never establishes overall visa eligibility.

Save shown work, caption, table, and Summary to sc-step4-salary-table.md in the workspace. Keep the original research, profile files, and state schema unchanged.

In chat, do not reproduce calculations or the table; Step 5 always runs next and presents the final caption and table. Give only a brief calculated/skipped count and confirmation that results are saved to sc-step4-salary-table.md.

Do not perform additional analysis, ranking, or recommendations.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
