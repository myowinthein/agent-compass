Check that `profile.md`, `situational-profile.md`, and `sc-step5a-career-ladder.md` exist. Stop and report the missing file if any is absent.

## Select countries

Prefer `cf-step6-final-ranking.md` when it exists.

- Read its Priority Table and Effort Allocation.
- Propose the countries above the active-application cutoff; when medals are used, default to the 🥇 countries.
- Preserve the Priority Table order.
- Show the proposed list and ask: "Use these countries as-is, add or remove countries, or start fresh?"
- Wait for confirmation.

If no Country Finder output exists, ask for the target-country list.

Record the confirmed list and the employment basis from `situational-profile.md`. Salary Calculator returns one answer per country, so never blend local-relocation compensation with cross-border remote compensation.

## Research goal

Research one broad, practical salary market for the confirmed target role and level in each country. The final target should work for mass applications without requiring the candidate to identify whether every employer is a startup, enterprise, local company, or multinational.

Use a balanced market sample:

- mainstream employers,
- established startups and scale-ups,
- ordinary international employers,
- sponsor-capable employers when relocation is the chosen basis.

Exclude:

- FAANG-only and elite-company-only data,
- levels.fyi,
- Glassdoor US as a primary source,
- equity-heavy total compensation,
- executive or management-heavy roles when the target is an individual-contributor role,
- contractor or freelance rates unless cross-border contracting is the confirmed employment basis,
- global-remote compensation that is unavailable to candidates in the current location,
- obvious low-wage outliers, internships, and junior roles.

## Evidence requirements

Use current web research from scratch. Prefer evidence from the last 12 months; allow an older annual salary guide only when it remains the latest edition and record its date.

Aim for at least three independent usable sources per country when available, including at least one of:

- a current direct-employer posting with a disclosed salary,
- a reputable recruiter salary guide,
- an official or well-documented local salary dataset.

Every source record must include URL, publisher or employer, publication or access date, location, role/level, salary figure, period, and whether it is base salary or total compensation.

Do not silently convert net salary, total compensation, hourly pay, or contractor rates into annual gross base salary. If a conversion is necessary and valid, show it.

Read and apply `skills/sponsorship-threshold-rules.md`. Research the candidate-applicable route, not a generic country minimum.

## Required country result

Use this exact structure:

```text
Country: [name]
Employment basis: [local employment / relocation OR cross-border remote from current location]
Target benchmark: [role and level]
Currency: [ISO code]
Market coverage: [national or named city/region]
Compensation basis: [annual gross base salary or clearly stated alternative]

Broad-market evidence:
- Low: [amount]
- Realistic midpoint: [amount]
- Strong: [amount]

Sponsorship threshold:
- Status: [verified numeric / no fixed threshold / not applicable to chosen path / unknown or unverified]
- Route: [name or N/A]
- Amount and period: [value or status]
- Effective date: [date or unknown]
- Official source: [URL or none]
- Conditions and compensation basis: [brief]

Sources:
- [URL] — [publisher/employer], [date], [role/level/location], [figure and basis]
- [repeat]

Notes:
- [13th/14th-month pay, holiday allowance, city variation, conflicting evidence, or other material limitation]
```

The figures must satisfy `Low ≤ Realistic midpoint ≤ Strong`. Do not invent a complete range from one salary datapoint.

## Isolated research execution

Run one isolated research task per country when subagents are available. Each agent receives only:

- the confirmed candidate benchmark,
- relevant situational facts,
- one country,
- the required schema above.

Agents must return their result to the main agent; they must not append concurrently to a shared file.

The main agent writes each completed result serially to `sc-research/[country-slug].md`, updates `.salary-calculator-state.json`, and then assembles the country files in confirmed order into `sc-step1-salary-research.md`.

If isolated research is unavailable, show the ready-to-copy prompts and stop for the user to bring back results.

After all results are assembled, report only the researched count and any failed countries, then continue automatically to Step 2.
