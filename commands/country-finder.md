---
name: Country Finder
description: Runs the full Country Finder pipeline — criteria intake, grounded country discovery, per-country research, scoring, and a final priority ranking.
---

# /claude-compass:country-finder

Run the full Country Finder pipeline, resuming from where it left off if a state file exists.

## Before starting

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it. Wait until profile.md is output before continuing.

## State tracking

Check for .country-finder-state.json in the workspace.

- If it exists, read it to find the last completed step. Tell me which step you are resuming from, then continue from the next step.
- If it does not exist, create it with last_completed_step set to 0, and start from Step 1.

State file format:
{
  "last_completed_step": 0,
  "updated_at": ""
}

After finishing each step below, update last_completed_step and updated_at in the state file before moving to the next one.

## Sequence

1. Read prompts/country-finder/step1-criteria-intake.md and follow it exactly.
2. Read prompts/country-finder/step2-country-discovery.md and follow it exactly.
3. Read prompts/country-finder/step3-research-prompt-generator.md and follow it exactly.
4. Read prompts/country-finder/step4-data-validation.md and follow it exactly.
5. Before running this step, ask me: "Step 5 (scoring) can run on Claude Opus for higher reasoning accuracy, which may cost more. Use Opus for this step? (yes/no)" — If I say yes, use the deep-reasoner subagent to read prompts/country-finder/step5-scoring.md. If I say no, read prompts/country-finder/step5-scoring.md yourself and follow it exactly using your current model.
6. Step 6 (final ranking) always runs — it produces the pipeline's final result, so it is never skipped. Before running it, ask me: "Step 6 (final ranking) can run on Claude Opus for higher reasoning accuracy, which may cost more. Use Opus for this step? (yes/no)" — If I say yes, use the deep-reasoner subagent to read prompts/country-finder/step6-final-ranking.md. If I say no, read it yourself and follow it exactly using your current model.

## Important

- If any step file tells you to stop and wait for me, actually stop and wait. Never fill in a placeholder, answer a question, or assume data on my behalf.
- If uncertain whether you are following a rule correctly, ask me rather than proceeding on a best guess.
- Do not skip, combine, or summarize steps to save time.
