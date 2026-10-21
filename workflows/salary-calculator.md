# salary-calculator

Run the full Salary Calculator pipeline, resuming from where it left off if a state file exists.

## Before starting

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it first. Wait for my resume and my confirmation of the extracted profile before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .salary-calculator-state.json in the workspace.
- Final step: 5 (career ladder and final verification together).
- Final output: sc-step5b-final-verification.md in the workspace.

## Presentation compatibility

The literal table contract lives in data/output-contracts.json; prompts/salary-calculator/step4-table-calculation.md owns its semantic procedure, and Step 5b audits and presents it. Read the contract as data even during approved manual fallback. Do not duplicate its columns or formulas in host adapters. Keep research field names, output filenames, and pipeline state unchanged. Unfinished legacy runs are interpreted by Step 5b's compatibility rule; completed runs replay the saved final result without migration or new research.

## Sequence

After validation or calculation, if no country has usable estimates, save the required report/output and its completed checkpoint, explain why nothing is calculable, and offer missing-evidence repair or stop. Do not continue to a specialist, career-ladder question or empty final table. Apply this guard on unfinished resumes too. If all adjustments are unestimable, the parent writes Step 4's skip-only record without a calculator handoff. For a repair, explain the affected steps and get the user's choice; before rewriting an affected output, move the checkpoint to immediately before the earliest step being rerun so an interruption cannot mark unchecked files as complete. Preserve valid originals/reports and the existing duplicate policy; never reset a completed run automatically.

1. First read and apply skills/situational-profile-questions.md on the calling model, so situational-profile.md exists before threshold research. Read prompts/salary-calculator/step1-research-prompt-generator.md and follow it exactly.
2. Read prompts/salary-calculator/step2-data-validation.md and follow it exactly.
3. Reuse situational-profile.md; on a legacy resume that lacks it, apply skills/situational-profile-questions.md on the calling model before handoff. Use the specialist routing rule in prompts/shared/runtime.md for Step 3 (international adjustment), role deep-reasoner, prompt prompts/salary-calculator/step3-international-adjustment.md.
4. Read prompts/salary-calculator/step4-table-calculation.md and prepare the parent-executed numeric results under skills/salary-calculation-helper.md. Resolve any execution/fallback choice before handoff. Then use the specialist routing rule in prompts/shared/runtime.md for Step 4 (table calculation), role calculator, supplying those inputs/results with the step prompt.
5. Step 5 (final verification) always runs when at least one country was calculated. First read prompts/salary-calculator/step5a-career-ladder.md and follow it on the calling model, including the user's confirmation before any handoff. Use the specialist routing rule in prompts/shared/runtime.md for Step 5, role deep-reasoner, prompt prompts/salary-calculator/step5b-final-verification.md. Handle pending numeric requests under skills/salary-calculation-helper.md before accepting a final output. Routing is optional; the career ladder and final verification are mandatory for a calculable run.

A Step 5 evidence-refresh request is a blocked return, not a pending helper calculation. The parent offers refresh, continue on the dated snapshot with the limitation, or stop, then waits. On an approved refresh, obtain the specific evidence through available research or user-supplied sources and pass its source, access/as-of dates and scope as task context to the audit continuation; preserve earlier files. The final audit records those citations. Resume the same approved assignment without advancing state while blocked. If required refresh evidence is still unavailable, explain the remaining gap and ask for snapshot or stop rather than looping or claiming verification.
