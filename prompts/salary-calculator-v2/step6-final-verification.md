# Step 6: Final Verification

Read `profile.md`, `scv2-step1-positioning.md`, `scv2-step2-salary-research.md`, `scv2-step3-audited-data.md`, `scv2-step4-adjustments.md`, `scv2-step5-salary-table.md`, and `skills/salary-calculator-v2-rules.md`. Base this audit only on those files and reopened decisive sources.

Audit every final row for:

1. source integrity and continued accessibility;
2. correct target role, level, geography, employer market, and compensation basis;
3. allowed adjustment, evidence support, and the `12%` cap;
4. threshold route, candidate applicability, age rule, effective date, and compensation-basis comparability;
5. exact formula, floor selection, rounding direction, monthly conversion, and interview-range derivation; and
6. semantic correctness of `None`, `N/A`, and `?`.

Change a value only for one of the correction reasons allowed by the v2 rules. Record the old value, new value, source or calculation proving the correction, and affected final cells. If a decisive source cannot be verified, lower the evidence grade or mark the country incomplete; do not defend the number from memory.

Save the complete audit, corrections, unresolved caveats, evidence grades, and final table to `scv2-step6-final-verification.md`. The final table must use exactly:

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

Show that final table in chat, followed by one short completion sentence stating the number of countries audited, whether corrections were applied, and the saved file path. Update the state to Step 6 complete and stop.
