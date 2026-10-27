# salary-calculator

Run the full Salary Calculator pipeline, resuming from where it left off if a state file exists.

## Question points

Use [QM](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern the named supporting prompts; ask only when their existing conditions require it.

| Trigger and owner | Preferred form and answer needed |
|---|---|
| New situational profile; skills/situational-profile-questions.md | Input for the eight existing situational questions, including units, country/status pairs and age/date reference. Single for hard floor versus context-only if a salary minimum is supplied. Preserve unknown/none/not specified and declined age; reuse saved answers without full intake. |
| Target role/level or intended employment path; prompts/salary-calculator/step1-research-prompt-generator.md | Input for unresolved role/level; Single for sponsored local employment versus local benchmarks without sponsorship assessment when path is unclear. For an actual cross-border-pay request, preserve local-context/stop scope choices. |
| Country Finder provenance and proposed countries; prompts/salary-calculator/step1-research-prompt-generator.md | Use the common upstream map, then Single for as-is/add/remove/start fresh with the full list visible. Add uses Input; remove uses Multi explicitly naming countries to remove; fresh or absent results uses Input. An empty eligible list offers a target list or stop without reviving older ratings. |
| Research collection, validation and unusable estimates; prompts/salary-calculator/step1-research-prompt-generator.md, prompts/salary-calculator/step2-data-validation.md and Sequence below | Use the common research/helper map. Single for missing-evidence repair versus stop when nothing is usable; Input for missing results or facts. Preserve required reports/checkpoints and do not ask a career-ladder or specialist question on this exit. |
| Adjustment/calculation missing context, invalid units or changed scope; prompts/salary-calculator/step3-international-adjustment.md and prompts/salary-calculator/step4-table-calculation.md | Input for material facts; use the common repair/helper forms for affected work or unavailable execution. Show actual manual-calculation limits; existing unknown/skipped outcomes do not force intake or extra approvals. |
| Career ladder; prompts/salary-calculator/step5a-career-ladder.md | Review of the full proposed ladder before saving; Input for corrections or material mismatch with a saved ladder, then show the revision for confirmation. Reuse an established confirmed ladder for the same target. |
| Evidence-refresh blocked return; prompts/salary-calculator/step5b-final-verification.md and Sequence below | Single for refresh, dated snapshot with limitation, or stop; Input for supplied evidence when needed. If refresh remains unavailable, ask snapshot/stop without looping. Preserve earlier files and leave the audit checkpoint pending. |
| Specialist handoffs and new numeric requests; Sequence below | Use the common routing/helper map. Selecting a specialist never confirms the ladder or missing evidence; an approved continuation adds no duplicate routing question. |

## Before starting

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Resolve Country Finder separately when its optional results are used. Canonical names below use those resolved paths on legacy runs.

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it first. Wait for my resume and my confirmation of the extracted profile before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .salary-calculator-state.json in the workspace.
- Final step: 5 (career ladder and final verification together).
- Final output: salary-calculator-05b-final-results.md in the workspace.

## Presentation compatibility

The literal table contract lives in data/output-contracts.json; prompts/salary-calculator/step4-table-calculation.md owns its semantic procedure, and Step 5b audits and presents it. Read the contract as data even during approved manual fallback. Do not duplicate its columns or formulas in host adapters. Keep research field names and pipeline state unchanged; use the shared filename resolution rather than renaming existing outputs. Unfinished legacy runs are interpreted by Step 5b's compatibility rule; completed runs replay the saved final result without migration or new research.

## Sequence

After validation or calculation, if no country has usable estimates, save the required report/output and its completed checkpoint, explain why nothing is calculable, and offer missing-evidence repair or stop. Do not continue to a specialist, career-ladder question or empty final table. Apply this guard on unfinished resumes too. If all adjustments are unestimable, the parent writes Step 4's skip-only record without a calculator handoff. For repairs and materially changed inputs, apply the shared runtime's repair/rewind rule and scope-safe original preservation; a changed-role rerun cannot replace stored originals through ordinary ingestion. Never reset a completed run automatically.

1. First read and apply skills/situational-profile-questions.md on the calling model, so situational-profile.md exists before threshold research. Read prompts/salary-calculator/step1-research-prompt-generator.md and follow it exactly.
2. Read prompts/salary-calculator/step2-data-validation.md and follow it exactly.
3. Reuse situational-profile.md; on a legacy resume that lacks it, apply skills/situational-profile-questions.md on the calling model before handoff. Use the specialist routing rule in prompts/shared/runtime.md for Step 3 (international adjustment), role deep-reasoner, prompt prompts/salary-calculator/step3-international-adjustment.md.
4. Read prompts/salary-calculator/step4-table-calculation.md and prepare the parent-executed numeric results under skills/salary-calculation-helper.md. Resolve any execution/fallback choice before handoff. Then use the specialist routing rule in prompts/shared/runtime.md for Step 4 (table calculation), role calculator, supplying those inputs/results with the step prompt.
5. Step 5 (final verification) always runs when at least one country was calculated. First read prompts/salary-calculator/step5a-career-ladder.md and follow it on the calling model, including the user's confirmation before any handoff. Saving the confirmed ladder completes only substep 5a; keep `last_completed_step` at 4 until the final audit is saved and its required checks succeed. Use the specialist routing rule in prompts/shared/runtime.md for Step 5, role deep-reasoner, prompt prompts/salary-calculator/step5b-final-verification.md. Handle pending numeric requests under skills/salary-calculation-helper.md before accepting a final output. Routing is optional; the career ladder and final verification are mandatory for a calculable run.

A Step 5 evidence-refresh request is a blocked return, not a pending helper calculation. The parent offers refresh, continue on the dated snapshot with the limitation, or stop, then waits. On an approved refresh, obtain the specific evidence through available research or user-supplied sources and pass its source, access/as-of dates and scope as task context to the audit continuation; preserve earlier files. The final audit records those citations. Resume the same approved assignment without advancing state while blocked. If required refresh evidence is still unavailable, explain the remaining gap and ask for snapshot or stop rather than looping or claiming verification.
