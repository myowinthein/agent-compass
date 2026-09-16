# Step 2: Grounded Country Research

Read `scv2-step1-positioning.md`, `profile.md`, and `skills/salary-calculator-v2-rules.md`. Stop if the positioning file is missing or not confirmed.

Research every confirmed country from scratch using current web sources. Do not use prior conversation conclusions, model memory, or a v1 `sc-step*` file as evidence.

## Isolation and writing

When parallel agents are available, create one isolated task per country. Give each task only `profile.md`, the confirmed positioning facts needed for that country, and the v2 rules. The country task must not research or infer results for another country.

Each country task returns its complete result to the parent. No country task may create, append, or edit a shared file. The parent validates each returned block, writes one file per country under `scv2-research/`, and only then consolidates them in confirmed priority order into `scv2-step2-salary-research.md`.

If isolated web research is unavailable, stop and tell the user which countries remain. Do not fabricate results or silently fall back to memory.

## Required country result

For each country, collect:

- confirmed target role, level, location scope, and employment basis;
- Market Low, Market Midpoint, and Market Strong annual gross base salary in local currency for the broad practical employer market;
- the evidence and weighting used to derive those three points;
- current recruiter-attraction friction evidence relevant to this candidate, without choosing the adjustment yet;
- sponsorship-threshold status, route, applicability, exact figure and basis where verified, effective date, and official URL;
- evidence grade: High, Medium, or Low; and
- conflicts, missing evidence, or comparability caveats.

For every source, record title, direct URL, publication or access date, role and level, location, quoted or paraphrased figure, currency, and whether it is base salary or total compensation. Observe the market exclusions and evidence hierarchy in the v2 rules.

Do not calculate an expected salary and do not choose an adjustment in this step.

After all country files and the consolidated file are written, report only the researched count, incomplete count, and saved path in chat. Update the v2 state, including completed countries, then continue automatically to Step 3.
