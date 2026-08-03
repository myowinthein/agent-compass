Check whether sc-step2-salary-data.md exists in the workspace. If it does not exist, stop and tell me: "sc-step2-salary-data.md was not found. Please ensure Step 2 completed successfully before continuing."

Check whether sc-step3-adjustment-values.md exists in the workspace. If it does not exist, stop and tell me: "sc-step3-adjustment-values.md was not found. Please ensure Step 3 completed successfully before continuing."

If both files exist, read them. Using the adjustment values from sc-step3-adjustment-values.md and the salary data from sc-step2-salary-data.md, calculate adjusted expected salary ranges for each country.

Read and apply skills/sponsorship-threshold-rules.md for the Legal Requirement column described below.

Only calculate countries that have BOTH:

- salary data
- international candidate adjustment data

Skip countries with missing data.

Ordering: check whether cf-step6-final-ranking.md exists in the workspace.
- If it exists, read its Priority Table and order the countries in this step's output to match that table's order, top to bottom.
- If it does not exist, order countries alphabetically by country name (A→Z).

Definitions

- Market Midpoint = the "Realistic" value for the relevant tier, as provided in the salary dataset. Do not average, estimate, or derive it any other way.
- Safe = Market Midpoint from the Mid-size / Mainstream Local-Market tier.
- Stretch = Market Midpoint from the Premium / International / Remote-first tier.

Do not estimate new salary tiers. Use only the salary data already provided.

Calculation Rules

1. Apply the international candidate adjustment independently to both the Safe and Stretch Market Midpoints.

Adjusted Midpoint = Market Midpoint x (1 - Adjustment %)

2. Fixed Value

Fixed = Adjusted Midpoint

3. Range Calculation (Annual only)

For each Annual Fixed value:

- Lower Range = Fixed x 0.95
- Upper Range = Fixed x 1.10

4. Monthly Calculation

Monthly = Annual Fixed / 12 — a single reference value, not a range. Monthly values are a reference only and may not represent actual monthly payslips in countries using 13th or 14th salary payments.

5. Legal Requirement Comparison

For each country with a usable sponsorship salary threshold (per skills/sponsorship-threshold-rules.md), compare it against the unrounded Fixed values for both Safe and Stretch — this comparison happens before the display rounding in the Formatting Rules below, never after, since rounding could flip a borderline result. Convert the threshold to match whichever period (Annual or Monthly) the comparison needs.

File format (write this structure to sc-step4-salary-table.md — this is not what you show in chat, see below):

Show Your Work

Before producing the table, work through the calculation for each country: Market Midpoint, Adjustment % applied, and resulting Adjusted Midpoint, for both Safe and Stretch.

Formatting Rules

- After showing the calculations, format the final salary data as ONE Markdown table with ONE row per country.
- Use ONLY these columns, in this exact order:

| Country | Legal Requirement | 🛡️ Safe Annual | 🚀 Stretch Annual | 🛡️ Safe Monthly | 🚀 Stretch Monthly |

- Place the country's flag emoji before its name, and include the currency code. Example: `🇩🇪 Germany (EUR)`.
- In each Annual column, show the Fixed target first, then its Range in parentheses. Example: `65,500 (62,000–72,000)`.
- Each Monthly column shows only the single Monthly value (Annual Fixed ÷ 12) — no range.
- Right-align the Legal Requirement, Safe Annual, Stretch Annual, Safe Monthly, and Stretch Monthly columns.
- Do not add footnotes, revision markers, notes, explanations, or additional columns.

Legal Requirement column:
- Em dash (—) if there is no usable sponsorship salary threshold for this country (per skills/sponsorship-threshold-rules.md — this covers both "no threshold exists" and "could not confirm one").
- Otherwise, show both period equivalents in one cell: the Annual figure first, then the Monthly figure in parentheses with a "/mo" suffix — e.g. `45,300 (3,775/mo)`. Neither figure is rounded.
- If either Safe or Stretch Fixed value falls short of the threshold (at either period), append a single ⚠️ at the end of the cell — the warning applies to the country as a whole, not to one period only.
- Never adjust Safe or Stretch because of this column — the two facts are shown side by side, never merged.

Do NOT repeat currency symbols or currency codes inside salary values.

Safe and Stretch salary values must:

- use local currency only
- contain plain formatted numbers only
- not convert to USD
- round cleanly for readability
- use consistent formatting across all countries

Recommended rounding:

- Annual (Fixed and Range): nearest 500
- Monthly: nearest 50

Example:

| Country | Legal Requirement | 🛡️ Safe Annual | 🚀 Stretch Annual | 🛡️ Safe Monthly | 🚀 Stretch Monthly |
|---|---:|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | 45,300 (3,775/mo) | 59,500 (56,500–65,500) | 74,500 (71,000–82,000) | 4,950 | 6,200 |
| 🇳🇱 Netherlands (EUR) | 63,972 (5,331/mo) ⚠️ | 56,500 (53,500–62,000) | 70,000 (66,500–77,000) | 4,700 | 5,850 |
| 🇺🇸 United States (USD) | — | 140,000 (133,000–154,000) | 175,000 (166,500–192,500) | 11,650 | 14,600 |

After the table, output:

Summary

- Countries calculated: X
- Countries skipped: Y

If any countries are skipped, list them with the reason.

Save the shown work, table, and summary to sc-step4-salary-table.md in the workspace.

In your chat response, do not reproduce the shown calculations or the table — Step 5 always runs next and is the point where the final table is presented to me. Instead, tell me in a few lines: how many countries were calculated and skipped, and that the full results are saved to sc-step4-salary-table.md.

Do not perform any additional analysis, ranking, recommendations, or commentary.

Step complete — stop here and wait for the main command.
