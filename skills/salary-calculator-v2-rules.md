---
name: Salary Calculator v2 Rules
description: Shared evidence, market-scope, recruiter-positioning, visa-threshold, calculation, and audit rules for Salary Calculator v2.
---

# Salary Calculator v2 Rules

## Purpose

Produce a practical salary answer for mass applications and interviews. The target is a credible value proposition: neither a low-ball figure nor premium-employer pricing. It should be attractive to an ordinary sponsor-capable employer while remaining consistent with the candidate's demonstrated level and current market evidence.

## Market benchmark

Research one broad practical employer market per country. Include mainstream employers, established startups or scaleups, and ordinary international or sponsor-capable employers. Weight evidence toward employers that could realistically interview the candidate.

Exclude:

- FAANG-only, elite-only, or `levels.fyi` data
- expatriate or relocation premiums
- contractor and freelance rates unless the confirmed employment basis is contracting
- equity-heavy total compensation when base salary cannot be isolated
- junior roles, management-heavy roles when the candidate targets individual-contributor work, and clearly mismatched specialties
- global remote pay that is not applicable to the confirmed hiring location
- unexplained aggregator estimates or extreme outliers

Use annual gross base salary. If a source reports monthly salary, 13th-month pay, guaranteed bonus, allowance, or total compensation, preserve that basis and normalize only when the conversion is explicit and comparable.

## Evidence standard

Aim for at least three independent sources per country, including where available:

1. direct job postings with salary ranges;
2. reputable local recruiter salary guides or local compensation datasets; and
3. official immigration sources for sponsorship thresholds.

For every material figure record the source title, URL, publication or access date, location, role and level, figure, currency, and compensation basis. Aggregators may corroborate but should not be the sole basis for a high-confidence result.

Grade the evidence:

- **High:** multiple current, mutually consistent direct or authoritative sources.
- **Medium:** useful current evidence with a material coverage or comparability limitation.
- **Low:** sparse, old, indirect, or conflicting evidence. Low confidence must remain visible and must never justify a large adjustment.

## Practical market points

Derive three evidence-supported annual base points in local currency:

- **Market Low:** lower edge for a credible candidate at the confirmed target level, not the bottom of all advertised roles.
- **Market Midpoint:** the best single estimate for the broad practical employer market.
- **Market Strong:** a realistic upper point for a strong match, not elite-only compensation.

Do not create these points by averaging incompatible data. Explain the weighting and resolve role, level, city, and compensation-basis mismatches first.

## Recruiter-attraction adjustment

This is a positioning concession for concrete costs or risks that the employer must absorb. It is not a nationality discount and must never be based on race, ethnicity, passport prestige, or a generic country ranking.

Allowed values are `0%`, `3%`, `5%`, `7%`, `10%`, and `12%`. The hard cap is `12%`.

- **0-3%:** candidate is already local or has independent work rights, or friction is minimal.
- **5-7%:** routine international hiring, sponsorship, relocation, or onboarding friction supported by current evidence.
- **10-12%:** substantial, documented employer cost, delay, uncertainty, or unusual relocation risk.

Use only candidate-applicable evidence. Separate market hiring difficulty from salary positioning; a difficult market does not automatically justify a larger concession. If evidence is insufficient, use `5%` with Low confidence, not a larger value. If the candidate is already local with independent work rights, do not exceed `3%` without specific contrary evidence.

## Sponsorship threshold

A usable threshold is an official minimum compensation rule for the specific employer-sponsored route reasonably applicable to this candidate and target role. Record:

- route name and candidate applicability;
- exact figure and currency;
- annual or monthly period;
- base salary or total-remuneration basis;
- age or new-entrant rule, if applicable;
- effective date; and
- official government URL.

Use one of four states:

- **Verified numeric:** an exact, current, comparable figure is confirmed.
- **No fixed threshold:** the route has no fixed numeric minimum or relies on an unresolved prevailing-wage test.
- **Not applicable:** the confirmed employment path does not use employer-sponsored relocation.
- **Unknown:** the route or current figure could not be confirmed.

Never turn `Unknown` into zero or `Not applicable`. Never use a general immigration route that does not fit the candidate. Convert monthly and annual figures only when their compensation basis is comparable. If a threshold includes components that cannot be compared with base salary, keep the status `Unknown` and explain why.

## Deterministic calculation

Use exact, unrounded values for every comparison:

```text
Raw Target = Market Midpoint × (1 - adjustment)
Required Floor = max(Market Low, verified applicable visa threshold, comparable user hard floor)
Expected Salary = max(Raw Target, Required Floor)
```

Include the user salary figure only when the intake labels it a hard floor and it can be reliably converted to the country's annual gross base basis. Historical salary and context-only targets are evidence about positioning, never automatic floors.

When a verified threshold determines the target, round upward so the displayed figure cannot fall below it. Otherwise use conservative, currency-aware display rounding and document the increment. Calculate monthly as annual divided by 12; label it as an equivalent when local pay commonly uses 13 or 14 installments.

Interview range:

- Lower bound = Expected Salary.
- Upper bound = Market Midpoint when it is at least Expected Salary.
- Otherwise use Market Strong when it is at least Expected Salary.
- If neither is at least Expected Salary, show the Expected Salary as a single figure and flag a market/visa or hard-floor conflict.

Do not generate a range by applying arbitrary percentages around Expected Salary.

## Final output semantics

Use this exact compact table:

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

In `Visa Minimum`, show the verified local-currency number, `None` for No fixed threshold, `N/A` for Not applicable, or `?` for Unknown. Keep detailed route and evidence notes in the audit file, not in the final table.

## Audit constraints

The final audit may change a number only for:

- a verified source correction;
- a role, level, location, currency, period, or compensation-basis correction;
- a deterministic arithmetic or rounding error; or
- corrected applicability of an official visa threshold.

Do not recalibrate from intuition, generic recruiter psychology, or an unsupported desire to make the result look safer. Record every correction and retain the pre-audit value.
