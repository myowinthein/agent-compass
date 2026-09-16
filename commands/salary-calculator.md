---
name: Salary Calculator
description: Researches and verifies local-market salaries, applies a capped recruiter-attraction adjustment, and returns one practical expected-salary target plus a short interview range per country.
---

# /claude-compass:salary-calculator

Run the full Salary Calculator pipeline, resuming safely when a compatible state file exists.

The final result is intentionally simple: one recruiter-friendly expected salary for forms, one monthly equivalent, and one short interview range per country. Detailed evidence and calculations stay in workspace files.

## Before starting

1. Check whether `profile.md` exists. If it does not, read `prompts/shared/resume-extraction-prompt.md` and follow it first. Wait for the resume and confirmation before continuing.
2. Read and apply `skills/situational-profile-questions.md` so `situational-profile.md` exists before salary research. This is required because citizenship, age, residence, work authorization, language, salary floor, and employment path can affect the benchmark or visa threshold.
3. Read `prompts/salary-calculator/step5a-career-ladder.md`, confirm the target role and level with the user, and save the result to `sc-step5a-career-ladder.md`. Salary research must not begin until this is confirmed.

## State tracking

Check for `.salary-calculator-state.json` in the workspace.

- If it does not exist, create it using the schema below and start from Step 1.
- If it exists, verify that `schema_version` is `2` and that its recorded profile, situational-profile, career-positioning, and country-list fingerprints still match the current inputs.
- If the schema is older or an input changed, explain which input changed and restart from the earliest affected step. Never silently reuse stale salary research for a different candidate, target level, country list, or employment path.
- If it is compatible, tell the user which step and countries are being resumed, then continue.

State file format:

```json
{
  "schema_version": 2,
  "last_completed_step": 0,
  "completed_country_research": [],
  "profile_fingerprint": "",
  "situational_profile_fingerprint": "",
  "career_positioning_fingerprint": "",
  "country_list_fingerprint": "",
  "updated_at": ""
}
```

Update the state after each completed country-research task and after each completed pipeline step.

## Sequence

1. Read `prompts/salary-calculator/step1-research-prompt-generator.md` and follow it exactly.
2. Read `prompts/salary-calculator/step2-data-validation.md` and follow it exactly.
3. Ask once: "Step 3 can use the deep-reasoner for a stricter recruiter-attraction assessment, which may cost more. Use it? (yes/no)" If yes, use the deep-reasoner subagent for `prompts/salary-calculator/step3-international-adjustment.md`. If no, run that prompt with the current model.
4. Read `prompts/salary-calculator/step4-table-calculation.md` and follow it with the current model. Use a calculator or code tool for all arithmetic when available; model choice is not a substitute for deterministic calculation.
5. Ask once: "Final verification can use the deep-reasoner for a stricter independent audit, which may cost more. Use it? (yes/no)" If yes, use the deep-reasoner subagent for `prompts/salary-calculator/step5b-final-verification.md`. If no, run that prompt with the current model.

## Important

- Embedded prompts are workflow instructions, not evidence. Salary and immigration claims still require cited, current sources.
- The calculator produces a strategic expected-salary answer, not a prediction or guarantee of an offer.
- Never use an abstract passport ranking or presumed nationality prestige. Use only concrete, sourced immigration rules and documented employer sponsorship friction relevant to the candidate.
- Never combine local employment, relocation, and cross-border remote compensation into one research market. Use the employment basis confirmed in `situational-profile.md`.
- If any step explicitly requires user confirmation, stop and wait.
- Do not skip validation or final verification to save time.
