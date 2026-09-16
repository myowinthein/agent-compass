---
name: Country Finder v2
description: Runs an evidence-audited country search with numeric remote and sponsorship scores, explicit cutoffs, and a reusable final report.
---

# /claude-compass:country-finder-v2

Run the evidence-audited Country Finder v2 pipeline, resuming from where it stopped when a state file exists.

## Before starting

If `profile.md` does not exist in the workspace, read `prompts/shared/resume-extraction-prompt.md` and follow it. Do not continue until the user has confirmed the extracted profile.

## State

Use `.country-finder-v2-state.json`:

```json
{
  "last_completed_step": 0,
  "updated_at": ""
}
```

If the file exists, tell the user which step is being resumed. Otherwise create it with step 0. After each completed step, update the number and timestamp before continuing.

## Sequence

1. Read `prompts/country-finder-v2/step1-intake.md` completely and follow it.
2. Read `prompts/country-finder-v2/step2-grounded-research.md` completely and follow it.
3. Read `prompts/country-finder-v2/step3-audit-scoring.md` completely and follow it.
4. Read `prompts/country-finder-v2/step4-final-ranking.md` completely and follow it.

## Execution rules

- Never skip or merge steps.
- Read `skills/country-finder-v2-scoring-rules.md` whenever a step requires it.
- Stop only at an explicit user-input checkpoint or when live web research is unavailable.
- When parallel agents are available, use them for country batches in Steps 2 and 3. Every agent writes to a unique batch file. Agents must never append to one shared file.
- The parent process validates and consolidates batch files. It owns every final step output.
- Never silently reuse stale output. If a step output exists but the state says that step is incomplete, ask whether to overwrite it or start a clean v2 run.
- Country Finder v2 never edits an Obsidian vault, profile, or job-portal list automatically. It may recommend changes in the report; apply them only after the user asks.

