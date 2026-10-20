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

The table contract lives in prompts/salary-calculator/step4-table-calculation.md; Step 5b audits and presents it. Do not duplicate its columns or formulas in host adapters. Keep research field names, output filenames, and pipeline state unchanged. Unfinished legacy runs are interpreted by Step 5b's compatibility rule; completed runs replay the saved final result without migration or new research.

## Sequence

1. First read and apply skills/situational-profile-questions.md on the calling model, so situational-profile.md exists before threshold research. Read prompts/salary-calculator/step1-research-prompt-generator.md and follow it exactly.
2. Read prompts/salary-calculator/step2-data-validation.md and follow it exactly.
3. Reuse situational-profile.md; on a legacy resume that lacks it, apply skills/situational-profile-questions.md on the calling model before handoff. Use the specialist routing rule in prompts/shared/runtime.md for Step 3 (international adjustment), role deep-reasoner, prompt prompts/salary-calculator/step3-international-adjustment.md.
4. Use the specialist routing rule in prompts/shared/runtime.md for Step 4 (table calculation), role calculator, prompt prompts/salary-calculator/step4-table-calculation.md.
5. Step 5 (final verification) always runs. First read prompts/salary-calculator/step5a-career-ladder.md and follow it on the calling model, including the user's confirmation before any handoff. Use the specialist routing rule in prompts/shared/runtime.md for Step 5, role deep-reasoner, prompt prompts/salary-calculator/step5b-final-verification.md. Routing is optional; the career ladder and final verification are mandatory.
