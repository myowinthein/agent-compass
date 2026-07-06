---
name: Salary Calculator
description: Runs the full Salary Calculator pipeline — research prompt generation, data ingestion, international adjustment, final table calculation, and optional reality check. Can run standalone or scoped to a single country handed off from Country Finder.
---

# /claude-compass:salary-calculator

Run the full Salary Calculator pipeline, resuming from where it left off if a state file exists.

## Before starting

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it first. Wait for my resume and my confirmation of the extracted profile before continuing.

If this command was invoked with a single country already specified (for example, handed off from Country Finder), record it as target_country in the state file and skip asking for a country list in Step 1.

## State tracking

Check for .salary-calculator-state.json in the workspace.

- If it exists, read it to find the last completed step. Tell me which step you are resuming from, then continue from the next step.
- If it does not exist, create it with last_completed_step set to 0 and target_country set to null, and start from Step 1.

State file format:
{
  "last_completed_step": 0,
  "target_country": null,
  "updated_at": ""
}

After finishing each step below, update last_completed_step and updated_at in the state file before moving to the next one.

## Sequence

1. Read prompts/salary-calculator/step1-research-prompt-generator.md and follow it exactly.
2. Read prompts/salary-calculator/step2-data-ingestion.md and follow it exactly.
3. Use the deep-reasoner subagent to read prompts/salary-calculator/step3-international-adjustment.md and complete this step, using the data already gathered in the workspace.
4. Use the calculator subagent to read prompts/salary-calculator/step4-final-table-calculation.md and complete this step, using the data already gathered in the workspace.
5. Ask me if I want to run the reality check. If I say yes, use the deep-reasoner subagent to read prompts/salary-calculator/step5-reality-check.md and complete it.

## Important

- If any step file tells you to stop and wait for me, actually stop and wait. Never fill in a placeholder, answer a question, or assume data on my behalf.
- If uncertain whether you are following a rule correctly, ask me rather than proceeding on a best guess.
- Do not skip, combine, or summarize steps to save time.
