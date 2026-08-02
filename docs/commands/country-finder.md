---
title: /country-finder
parent: Commands
nav_order: 1
has_children: true
---

# /country-finder

Runs the full Country Finder pipeline. Collects your criteria, discovers candidate countries for remote hire and visa sponsorship as two separate tracks, generates per-country research prompts, validates and stores your results, scores each country against your requirements, and produces a final priority ranking. Resumes from the last completed step if interrupted.

## Usage

```
/claude-compass:country-finder
```

Run it once per session. Claude resumes automatically if a `.country-finder-state.json` file already exists.

## Flow

```mermaid
flowchart TD
  Start([User runs /country-finder]) --> Profile{profile.md\nexists?}
  Profile -->|no| Extract[Resume extraction —\nwait for upload and confirmation]
  Profile -->|yes| Sit
  Extract --> Sit

  Sit{situational-profile.md\nexists?} -->|no| SitQ[Collect location, citizenship,\nlanguage, optional salary minimum — save to file]
  Sit -->|yes| State
  SitQ --> State

  State{.country-finder-state.json\nexists?} -->|yes| Resume[Inform user: resuming from step N]
  State -->|no| S1
  Resume --> S1

  S1[Step 1: Criteria intake\ntimezone · timeline · preferences] --> S2
  S2[Step 2: Country discovery\npreferred/wealth-tier universe · region-batch sub-agents · timezone mark] --> S3
  S3[Step 3: Research prompt generator\nready-to-copy prompts per country] --> S4
  S4[Step 4: Data validation\none country at a time] --> S5
  S5[Step 5: Scoring\ndeep-reasoner agent] --> S6
  S6[Step 6: Final ranking\ndeep-reasoner agent — always runs]
  S6 --> Done([Results delivered])
```

## Steps

### Profile check

Checks for `profile.md` in the workspace. If absent, reads `prompts/shared/resume-extraction-prompt.md`, waits for the user to upload their resume, and waits for explicit confirmation of the extracted profile before continuing. The profile is reused on all subsequent runs without re-extraction.

### Situational profile

Checks for `situational-profile.md`. If absent, asks six questions: current location, citizenship, any known immigration friction tied to that citizenship, languages spoken, required work language, and minimum acceptable monthly salary (or "not specified"). Saves answers to `situational-profile.md` for reuse across sessions and pipelines.

### State check

Checks for `.country-finder-state.json`. If found, reads `last_completed_step` and informs the user which step will resume. If absent, creates the file with `last_completed_step: 0` and starts from Step 1. Updates the file after each step completes.

### [Step 1 — Criteria intake](country-finder/step1-criteria-intake.html)

Collects requirements for both tracks. Remote track: maximum timezone difference (or "no limit" to skip). Sponsorship track: relocation timeline. Relocation is assumed — the question is not asked. Country preferences: any countries or regions to include or exclude from both tracks. Vague answers are rejected — specific values or explicit "no limit" / "not specified" are required.

### [Step 2 — Country discovery](country-finder/step2-country-discovery.html)

Builds a single candidate universe — your saved `data/preferred-countries.md` if it exists, otherwise your Step 1 Include list, otherwise Claude stops and asks you to list the countries you want considered — then researches it in region-batched sub-agents that check each country for Remote and Sponsorship suitability together. A timezone limit from Step 1 marks (not removes) out-of-range countries as unsuitable for Remote only; a salary minimum from the situational profile is folded into the Remote check.

### [Step 3 — Research prompt generator](country-finder/step3-research-prompt-generator.html)

Generates ready-to-copy research prompts for each candidate country on each track. The user copies these prompts and runs them in separate research sessions to gather real-world data. Claude does not generate the research itself.

### [Step 4 — Data validation](country-finder/step4-data-validation.html)

Reads `cf-step3-country-research.md` written by Step 3's sub-agents and stores each country's data automatically. Validates each block: one country per block, all required fields present, duplicates skipped and noted. Data is preserved verbatim — no analysis, scoring, or summarizing during ingestion. Stored data is written to `cf-step4-country-data.md` for later steps.

### [Step 5 — Scoring](country-finder/step5-scoring.html)

Claude asks whether to use the **deep-reasoner** subagent (Opus, high effort) for higher reasoning accuracy — if declined, the step runs with your current model. Scores each stored country against the criteria from Step 1, keeping remote hire and sponsorship tracks completely separate. Salary minimum check is only applied if a minimum was specified. Each country receives a fit classification (Strong / Moderate / Weak) and a confidence level (High / Medium / Low). Every excluded country requires a specific, evidence-based reason.

### [Step 6 — Final Ranking](country-finder/step6-final-ranking.html)

Always runs after Step 5 completes — this is the only step in the pipeline with no skip option, since it produces the final result. Claude asks whether to use the **deep-reasoner** subagent (Opus, high effort) — if declined, the step runs with your current model. Audits the scoring output across two checks (confidence calibration and a missing-candidate check), then produces the Priority Table — a country-by-country ranking with a usable-track label and a holistic priority medal.

## Stop conditions

- **Profile not yet uploaded.** Claude waits — it does not proceed or fill in placeholder data.
- **Any step instructs Claude to wait.** Claude stops and waits. No guessing, no assumptions.
- **Vague answer to a criteria question.** Claude asks again for a specific value before continuing.
- **Data validation receives multiple countries, missing fields, or a country not on either Step 2 candidate list.** Claude never stops mid-batch — it skips the item and records the reason. Duplicates, malformed items, missing-field items, and unlisted candidates are all reported together in one consolidated report at the end of Step 4, rather than stopping the run.

## See also

- [`/salary-calculator`](salary-calculator.html) — calculate local-market salaries for countries discovered here
- [`/portal-finder`](portal-finder.html) — find verified job portals for a specific country
- [`/job-screener`](job-screener.html) — screen job descriptions against your resume profile
