Check whether `sc-step2-salary-data.md` exists. If it does not, stop and report that Step 2 must finish first.

Read:

- `sc-step2-salary-data.md`
- `profile.md`
- `situational-profile.md`
- `sc-step5a-career-ladder.md`
- relevant Country Finder evidence when available

## Goal

Choose a small, deliberate recruiter-attraction adjustment for each country.

This adjustment reflects the candidate's strategy: ask slightly below the verified local-market midpoint when concrete overseas-hiring friction makes that useful, while avoiding both low-balling and premium pricing.

It is not:

- a claim that foreigners legally or normally deserve lower pay,
- a prediction of the final offer,
- a substitute for the visa salary threshold,
- a penalty based on passport ranking, nationality prestige, race, or ethnicity.

Use citizenship only when a current, sourced immigration rule, restriction, processing obligation, or employer sponsorship requirement actually applies.

## Evidence considered

Consider only factors that plausibly affect the usefulness of a lower initial salary ask:

- whether employer sponsorship is required,
- documented sponsorship cost or administrative burden,
- relocation and cross-border interview friction,
- whether the candidate already lives locally,
- whether the candidate has independent work authorization,
- workplace-language mismatch when the target market genuinely requires it,
- sponsor-capable employer availability,
- direct fit between the candidate's experience and the confirmed target role,
- current hiring-market conditions.

Do not convert general hiring difficulty into a large salary discount. Hiring probability and salary level are separate concepts.

## Adjustment scale

Choose one value from: `0%`, `3%`, `5%`, `7%`, `10%`, or `12%`.

- 0–3%: little practical friction, already local/authorized, or unusually strong direct fit.
- 5–7%: meaningful but routine international-hiring friction.
- 10–12%: substantial, specifically evidenced friction where a more attractive initial ask is strategically reasonable.

Rules:

- 12% is the hard maximum unless the user explicitly authorizes more after seeing evidence.
- Never use a large adjustment merely because evidence is missing. When evidence is insufficient, use 5% with Low confidence.
- If the candidate already lives in the country with independent work authorization, do not exceed 3% without specific evidence.
- Strong role/domain fit may reduce the adjustment; it does not create a negative discount or premium.
- Do not apply the sponsorship threshold or personal hard floor here. Step 4 handles those floors after calculating the raw target.

## Required output per country

```text
Country: [name]
Market midpoint: [amount and currency]
Recruiter-attraction adjustment: [allowed percentage]
Adjustment level: [None / Small / Moderate / Significant]
Confidence: [High / Medium / Low]
Evidence:
- [source-backed factor]
- [source-backed factor]
Reason: [two or three concise sentences]
```

Save all countries to `sc-step3-adjustment-values.md` in the same order as Step 2.

Report only the number completed, confidence counts, and any countries that could not be assessed. Continue automatically to Step 4.
