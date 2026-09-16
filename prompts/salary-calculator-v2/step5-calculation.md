# Step 5: Deterministic Calculation

Read `scv2-step1-positioning.md`, `scv2-step3-audited-data.md`, `scv2-step4-adjustments.md`, and `skills/salary-calculator-v2-rules.md`. Calculate only countries with complete audited market data and an allowed adjustment.

Use a calculator or executable arithmetic tool for every calculation. Do not perform long arithmetic by intuition. Apply the exact formula, floor rules, interview-range logic, and currency-aware rounding rules from the v2 skill.

For each country, show in the saved file:

- exact Market Low, Midpoint, and Strong;
- adjustment and exact Raw Target;
- every candidate floor considered and whether it is comparable;
- exact Required Floor;
- exact Expected Salary before rounding;
- display-rounding increment and displayed Expected Annual;
- Expected Monthly calculation;
- Interview Range derivation; and
- any market/visa or hard-floor conflict.

Then produce this exact compact table:

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

Use local currency and place the currency code in the country cell. Use `None`, `N/A`, and `?` with the exact meanings in the v2 rules. Preserve confirmed country order.

Save the shown work and pre-audit table to `scv2-step5-salary-table.md`. Do not show the table in chat yet. Report only calculated and skipped counts, update the v2 state, and continue automatically to Step 6.
