---
title: Step 5 — Scoring
parent: /country-finder
grand_parent: Commands
nav_order: 5
---

# Step 5 — Scoring

Scores every stored country against your criteria from Step 1, keeping Remote and Sponsorship tracks completely separate. Routed to the **deep-reasoner** subagent (Opus, high effort).

## What it reads

- All country data stored in Step 4
- Criteria, salary minimum, time zone limit, and dealbreakers from Step 1

## Batching rule

All Remote-track countries are scored first, all the way through, before Sponsorship scoring begins for any country. Tracks are never interleaved.

## Remote track scoring

For each country with Remote data stored:

1. Does the confirmed salary meet or exceed your Step 1 minimum? If not, the country is excluded with the specific gap stated (e.g. "confirmed salary $X, below your minimum of $Y").
2. If it passes: classify Remote fit as **Strong**, **Moderate**, or **Weak**.
3. Assign confidence: **High**, **Medium**, or **Low**.
4. Give brief reasoning referencing actual stored evidence, not assumption.

## Sponsorship track scoring

For each country with Sponsorship data stored:

1. Does the stored data directly conflict with any dealbreaker from Step 1? If yes, the country is excluded with the specific conflict stated.
2. If a visa minimum salary threshold was reported and Salary Calculator figures exist, note whether they clear the threshold. If no figures exist, the threshold is noted as informational only.
3. If it passes: classify Sponsorship fit as **Strong**, **Moderate**, or **Weak**.
4. Assign confidence: **High**, **Medium**, or **Low**.
5. Give brief reasoning referencing actual stored evidence, not assumption.

## Evidence quality rule

If the stored research uses vague or unquantified language ("sometimes," "generally friendly," "fairly common"), confidence is lowered and the reason is stated. Vague claims are never treated as strong evidence.

## Exclusion transparency rule

Every country that was on a Step 2 candidate list but does not appear in the final results must be listed separately with a specific, evidence-based reason. "General reputation" is not an acceptable reason. If no data was ever stored for that country and track, that is stated plainly.

## Output format

```
Remote Track Results
- [Scored countries: fit, confidence, brief reasoning]
- [Excluded countries: specific reason]

Sponsorship Track Results
- [Scored countries: fit, confidence, brief reasoning]
- [Excluded countries: specific reason]

Summary
- Remote: [N] scored, [N] excluded
- Sponsorship: [N] scored, [N] excluded
```

## After scoring

Claude asks whether you want salary data for any of the results. If yes, it offers to run `/salary-calculator` scoped to a single named country. If you want to run the optional reality check first, proceed to Step 6.
