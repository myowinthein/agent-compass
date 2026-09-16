Check whether `sc-step1-salary-research.md` exists. If it does not, stop and report that Step 1 must finish first.

Read `profile.md`, `situational-profile.md`, `sc-step5a-career-ladder.md`, and every country block in `sc-step1-salary-research.md`.

This is an evidence-validation and normalization step, not passive storage.

## Validate each country

Confirm:

1. Exactly one country is represented.
2. The employment basis matches `situational-profile.md`.
3. The role and level match `sc-step5a-career-ladder.md`.
4. Values use one clearly identified currency and compensation basis.
5. Values are comparable annual gross base salary, or any alternative basis is explicit.
6. `Low ≤ Realistic midpoint ≤ Strong`.
7. Sources actually support the recorded role, level, location, period, and compensation type.
8. Source URLs, dates, and figures are present.
9. Contractor, equity, bonus, allowance, net-pay, and elite-employer figures have not been mixed into base salary without justification.
10. City or regional variation is recorded when material.
11. The sponsorship-threshold record follows `skills/sponsorship-threshold-rules.md`.
12. Duplicate sources or reposted copies are not counted as independent evidence.

Open and verify the decisive sources. If a source is inaccessible, stale, contradictory, or does not support the number attributed to it, downgrade or remove it.

## Repair before skipping

When a field or source is missing, perform targeted current research to repair the country record. Record every repaired value and its replacement source.

Skip a country only when there is still insufficient evidence to establish a defensible broad-market midpoint after repair. Never invent missing values.

For duplicates, keep the better-supported and more recent record rather than automatically keeping the first one.

## Evidence grade

Assign:

- High: at least three mutually consistent, current, directly relevant sources, including strong direct-employer or recruiter-guide evidence.
- Medium: at least two usable sources with manageable limitations.
- Low: a usable estimate exists, but evidence is thin, older, indirect, or conflicting.

Low-confidence countries may continue, but the weakness must be visible to the final auditor.

## Normalized output

Write `sc-step2-salary-data.md` in confirmed country order. For every stored country include:

- Country
- Employment basis
- Target role and level
- Currency
- Market coverage
- Compensation basis
- Market Low
- Market Realistic midpoint
- Market Strong
- Sponsorship threshold status, route, amount, period, effective date, conditions, and official source
- Evidence grade
- Verified sources
- Validation or repair notes

Finish with one consolidated report:

- Validated: [count]
- Repaired: [count and countries]
- Low confidence: [count and countries]
- Skipped: [count, countries, and reasons]

Continue automatically to Step 3.
