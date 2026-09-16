---
name: Salary Calculator v2
description: Runs an evidence-audited salary search that produces one recruiter-friendly expected salary and a short interview range per country.
---

# /claude-compass:salary-calculator-v2

Run the evidence-audited Salary Calculator v2 pipeline, resuming from where it stopped when a state file exists.

## Before starting

If `profile.md` does not exist in the workspace, read `prompts/shared/resume-extraction-prompt.md` and follow it. Do not continue until the user has confirmed the extracted profile.

## State

Use `.salary-calculator-v2-state.json`:

```json
{
  "schema_version": 2,
  "last_completed_step": 0,
  "input_fingerprint": "",
  "completed_countries": [],
  "updated_at": ""
}
```

Leave `input_fingerprint` empty until Step 1 is confirmed. After Step 1, set it to a SHA-256 hash of the exact bytes of `profile.md`, followed by one newline, followed by the exact bytes of `scv2-step1-positioning.md`; that positioning file contains the ordered country list. On every resume after Step 1, recompute and compare the hash before doing more work. If inputs changed, explain the mismatch and ask whether to restart v2 or restore the prior inputs. Never resume against changed inputs. If no state exists, create it and start at Step 1.

After each completed step, update the step number, completed countries where relevant, fingerprint, and timestamp before continuing.

## Sequence

1. Read `prompts/salary-calculator-v2/step1-intake-positioning.md` completely and follow it.
2. Read `prompts/salary-calculator-v2/step2-grounded-research.md` completely and follow it.
3. Read `prompts/salary-calculator-v2/step3-audit-normalization.md` completely and follow it.
4. Read `prompts/salary-calculator-v2/step4-recruiter-adjustment.md` completely and follow it.
5. Read `prompts/salary-calculator-v2/step5-calculation.md` completely and follow it.
6. Read `prompts/salary-calculator-v2/step6-final-verification.md` completely and follow it.

## Execution rules

- Never skip or merge steps.
- Read `skills/salary-calculator-v2-rules.md` whenever a step requires it.
- Stop only at an explicit user-input checkpoint or when current web research is unavailable.
- Keep the user-facing result simple: one expected annual number, its monthly equivalent, and one short interview range per country. Evidence and calculations stay in files.
- Use current web research. Do not substitute model memory for salary, immigration, exchange-rate, or legal facts.
- When parallel agents are available, use one isolated task per country in Step 2. Each agent returns its result to the parent and never writes a shared file. The parent alone writes consolidated files serially.
- Use only v2 state and output names. Never read a v1 `sc-step*` file as completed v2 work and never overwrite v1 files.
- Never silently reuse stale output. If an output exists but state marks its step incomplete, ask whether to overwrite it or start a clean v2 run.
- Salary Calculator v2 never edits an Obsidian vault, profile, application tracker, or portal list automatically. Apply external changes only after the user asks.
