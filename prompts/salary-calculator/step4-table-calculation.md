Check that `sc-step2-salary-data.md` and `sc-step3-adjustment-values.md` exist. Stop and report the missing prerequisite if either is absent.

Read both files, `situational-profile.md`, and `skills/sponsorship-threshold-rules.md`.

Use a calculator or code tool for every calculation when available. Do not rely on mental arithmetic. Preserve unrounded values until the display step.

Only calculate countries with validated salary data and an allowed recruiter-attraction adjustment.

## Definitions

- Market Low: verified lower bound from Step 2.
- Market Midpoint: verified Realistic midpoint from Step 2.
- Market Strong: verified upper practical figure from Step 2.
- Raw Target: the deliberately discounted midpoint.
- Expected Salary: the one recruiter-friendly number to enter in application forms.
- Interview Range: a short range beginning at Expected Salary and ending at the verified midpoint or strong figure, as defined below.

## Calculation

For each country:

```text
Raw Target = Market Midpoint × (1 − Adjustment %)
```

Build the Required Floor from applicable evidence:

1. Market Low.
2. A verified sponsorship threshold when the chosen path requires sponsorship.
3. A user-declared hard salary floor when it can be compared reliably in the same currency. If conversion is required, use a current authoritative exchange-rate source and record its date. Historical/context-only salary is never a floor.

```text
Expected Salary before display rounding = max(Raw Target, Required Floor)
```

If a verified legal threshold determines the result, round upward, never downward.

Interview Range:

- Lower bound = Expected Salary.
- If Market Midpoint is at or above Expected Salary, upper bound = Market Midpoint.
- Otherwise, if Market Strong is at or above Expected Salary, upper bound = Market Strong.
- Otherwise, show Expected Salary as a single figure and record a `market / visa conflict` for the final audit.
- Never construct a range using arbitrary percentage padding.

Monthly Equivalent:

```text
Expected Monthly Equivalent = Expected Annual ÷ 12
```

This is a comparison aid, not necessarily a payslip amount in countries using 13th/14th-month pay or mandatory allowances.

## Display rounding

Use clean increments appropriate to the currency and magnitude. Examples:

- EUR, GBP, USD, CAD, AUD, NZD, SGD: usually 500 annually and 50 monthly.
- THB, TWD, HKD, MYR, SEK, AED, SAR: use a locally sensible increment that keeps roughly three significant digits.
- JPY and KRW: use larger locally conventional increments.

Apply one consistent rule per currency. Record the rule in the shown work. Threshold-driven targets must be rounded upward enough to remain eligible.

## Visa Minimum display

Follow `skills/sponsorship-threshold-rules.md`:

- verified numeric: show the amount and official period,
- no fixed threshold: `None`,
- not applicable to chosen path: `N/A`,
- unknown or unverified: `?`.

## Ordering

Use the confirmed country order from Step 1. If it is unavailable, use the Priority Table order from `cf-step6-final-ranking.md`; otherwise sort alphabetically.

## File output

Write `sc-step4-salary-table.md` with:

1. Show Your Work: inputs, formulas, unrounded result, applied floors, conflict checks, and rounding for every country.
2. The final compact table:

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

Formatting:

- Put the flag before the country and include the currency code.
- Salary cells contain plain local-currency numbers without repeated currency symbols.
- Expected Annual is the single application-form answer.
- Expected Monthly is its monthly equivalent.
- Interview Range is the concise answer for a recruiter conversation.
- Do not expose company-type scenarios in the final table.
- Do not add confidence, methodology, or long notes to this table; those stay in the underlying files and final audit.

Finish the file with:

- Countries calculated
- Countries skipped and reasons
- Countries where a legal or personal floor changed the target
- Countries with a market / visa conflict

In chat, report only the calculated/skipped counts and confirm that Step 4 is saved. Continue automatically to Step 5 final verification.
