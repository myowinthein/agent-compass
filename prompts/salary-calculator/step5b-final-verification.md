Read:

- `sc-step4-salary-table.md`
- `sc-step2-salary-data.md`
- `sc-step3-adjustment-values.md`
- `profile.md`
- `situational-profile.md`
- `sc-step5a-career-ladder.md`
- `skills/sponsorship-threshold-rules.md`

This is an independent evidence and calculation audit. Do not automatically defend or lower the numbers.

## Audit checks

### 1. Candidate benchmark

Confirm that every country uses the confirmed target role and level rather than the highest historical title or a management-heavy role the candidate is not targeting.

### 2. Evidence integrity

For every country, verify:

- decisive source URLs support the recorded figures,
- role, seniority, location, currency, and compensation basis align,
- sources are sufficiently current,
- elite-company, contractor, total-compensation, and remote-first outliers were not mixed into a broad local benchmark,
- Low ≤ Midpoint ≤ Strong,
- the evidence grade is justified.

Perform a fresh web check only where a source is weak, inaccessible, contradictory, stale, or produces an outlier. Do not replace sound evidence merely to make the table look more uniform.

### 3. Adjustment integrity

Confirm that:

- the adjustment is one of 0%, 3%, 5%, 7%, 10%, or 12%,
- it is supported by concrete candidate-specific friction,
- passport rankings and presumed nationality prestige were not used,
- hiring difficulty was not automatically converted into a large discount,
- the adjustment cap was respected,
- existing residence or independent work authorization was handled correctly.

### 4. Calculation integrity

Recalculate every country independently:

- Raw Target,
- Required Floor,
- Expected Salary,
- Monthly Equivalent,
- Interview Range,
- currency-aware rounding.

Confirm that historical/context-only salary was not treated as a hard floor.

### 5. Immigration integrity

Confirm the threshold route, candidate applicability, amount, period, compensation basis, effective date, and official source.

Ensure that:

- verified thresholds act as floors,
- unknown is shown as `?`, not as no threshold,
- remote-path countries show `N/A`,
- period conversion is valid,
- any threshold above Market Strong is flagged as a market / visa conflict.

## Corrections

Correct a country only when supported by:

- a verified source,
- a unit, role, level, currency, or compensation-basis correction,
- a deterministic arithmetic error,
- a threshold-applicability correction.

Do not recalibrate based only on intuition, generic recruiter language, or a desire to improve interview conversion.

Record every correction with the old value, new value, and reason. If the evidence remains too weak, keep the country out of the final table and state what must be researched; do not invent a number.

## Output file

Write all audit checks, corrections, unresolved issues, and the resulting final table to `sc-step5b-final-verification.md`.

Use the same compact table and country order as Step 4:

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

The table is the user's practical result:

- Expected Annual: single number for application forms.
- Expected Monthly: monthly equivalent when a form asks monthly.
- Interview Range: short answer for recruiter or interview conversations.

## Chat response

Show the final table exactly as saved, followed by one completion sentence:

- If corrected: `Salary Calculator is complete. [N] countries audited; evidence-backed corrections were applied. Full audit saved to sc-step5b-final-verification.md.`
- If unchanged: `Salary Calculator is complete. [N] countries audited; no corrections were needed. Full audit saved to sc-step5b-final-verification.md.`

Do not reproduce the detailed audit in chat.
