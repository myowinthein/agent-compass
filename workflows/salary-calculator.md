# salary-calculator

Run the full Salary Calculator pipeline in a search isolated by chat, person and command.

## Before starting

First read [skills/run-workspaces.md](../skills/run-workspaces.md). Select or create the run before any profile, artifact or checkpoint access; keep its returned workspace for this whole pipeline. New chats start fresh. In this chat, a matching completed run offers View previous results / Start fresh; an unfinished run offers Resume / Start fresh. Preserve earlier runs when starting fresh.

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Resolve Country Finder separately when its optional results are used. Canonical names below use those resolved paths on legacy runs.

Check if profile.md exists in the workspace. If it does not, read [prompts/shared/resume-extraction-prompt.md](../prompts/shared/resume-extraction-prompt.md) and follow it first. Wait for my resume and my confirmation of the extracted profile before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .salary-calculator-state.json in the workspace.
- Final step: 5 (career ladder and final verification together).
- Final output: salary-calculator-05b-final-results.md in the workspace.

## Presentation compatibility

data/output-contracts.json owns the literal table contract, Step 4 its semantic procedure, and Step 5b its audit, presentation and unfinished-legacy compatibility. Read the contract even during approved manual fallback; do not duplicate columns/formulas in host adapters or change research field names. Shared runtime rules govern filename resolution, checkpoints and completed replay.

## Sequence

After validation or calculation, including resumed runs, if no country has usable estimates, save the required report/output and completed checkpoint, explain why, and offer missing-evidence repair or stop. Do not continue to a career ladder or empty final table. If all adjustments are unestimable, write Step 4's skip-only record without numeric/rendering calls. Repairs and changed inputs follow the shared runtime's preservation/rewind rule.

1. First read and apply [skills/situational-profile-questions.md](../skills/situational-profile-questions.md) on the calling model, so situational-profile.md exists before threshold research. Read [prompts/salary-calculator/step1-research-prompt-generator.md](../prompts/salary-calculator/step1-research-prompt-generator.md) and follow it exactly.
2. Read [prompts/salary-calculator/step2-data-validation.md](../prompts/salary-calculator/step2-data-validation.md) and follow it exactly.
3. Reuse situational-profile.md; on a legacy resume that lacks it, apply skills/situational-profile-questions.md first. Read [prompts/salary-calculator/step3-international-adjustment.md](../prompts/salary-calculator/step3-international-adjustment.md) and follow it exactly on the current agent.
4. Read [prompts/salary-calculator/step4-table-calculation.md](../prompts/salary-calculator/step4-table-calculation.md) and follow it exactly on the current agent, using [skills/salary-calculation-helper.md](../skills/salary-calculation-helper.md) for numeric results and their review.
5. Step 5 (final verification) always runs when at least one country was calculated. First read [prompts/salary-calculator/step5a-career-ladder.md](../prompts/salary-calculator/step5a-career-ladder.md) and follow it, including the user's confirmation. Saving the confirmed ladder completes only substep 5a; keep `last_completed_step` at 4 until the final audit is saved and its required checks succeed. Then read [prompts/salary-calculator/step5b-final-verification.md](../prompts/salary-calculator/step5b-final-verification.md) and follow it exactly on the current agent. Complete any additional numeric work under skills/salary-calculation-helper.md before accepting a final output. The career ladder and final verification remain mandatory for a calculable run.

Missing essential current evidence blocks the Step 5 audit separately from helper calculations. The parent offers refresh, continue on the dated snapshot with the limitation, or stop, then waits. On an approved refresh, obtain the specific evidence through available research or user-supplied sources and retain its source, access/as-of dates and scope as cited context for the continuing audit; preserve earlier files. The final audit records those citations. Continue the audit without advancing state while blocked. If required refresh evidence is still unavailable, explain the remaining gap and ask for snapshot or stop rather than looping or claiming verification.

## Question points

Use [question mechanism (QM)](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern the named supporting prompts; ask only when their existing conditions require it.

| Trigger and owner | Preferred form and answer needed |
|---|---|
| New situational profile; skills/situational-profile-questions.md | Reuse applicable confirmed profile facts and saved answers, including those copied from Country Finder. Input for missing location, passport nationality, willing-and-able working languages or country/status/work-condition pairs. Pay is optional; collect its units/basis only when supplied and clarify firm minimum versus context only when ambiguous. Do not ask for expected salary, generic immigration-risk judgments or upfront age. Preserve unknown/none/not specified and declined disclosure. |
| Material official age-dependent reference route rule; skills/sponsorship-threshold-rules.md | Explain the affected country/source/event and ask only for the needed age or band. Respect declined disclosure; keep the affected visa check conditional without blocking other research or salary targets. Later persistence uses the shared runtime's existing dated-note approval. |
| Target role/level; prompts/salary-calculator/step1-research-prompt-generator.md | Input only for unresolved role/level. Local employee salary benchmarks and separate reference visa salary research are the fixed scope, not a user choice. Do not ask for an employment path or offer a remote/relocation/sponsorship menu. Explain the limitation only for an explicit cross-border-pay request. |
| Country Finder provenance and proposed countries; prompts/salary-calculator/step1-research-prompt-generator.md | Use the common upstream map, then Single for use/add/remove/choose a new list with the full list visible. Add uses Input; remove uses Multi explicitly naming countries to remove; a new list or absent results uses Input. An empty eligible list offers a target list or stop without reviving older ratings. |
| Research collection, validation and unusable estimates; prompts/salary-calculator/step1-research-prompt-generator.md, prompts/salary-calculator/step2-data-validation.md and Sequence below | Use the common research/helper map. Single for missing-evidence repair versus stop when nothing is usable; Input for missing results or facts. Preserve required reports/checkpoints and do not ask a career-ladder question on this exit. |
| Adjustment/calculation missing context, invalid units or changed scope; prompts/salary-calculator/step3-international-adjustment.md and prompts/salary-calculator/step4-table-calculation.md | Input for material facts; use the common repair/helper forms for affected work or unavailable execution. Show actual manual-calculation limits; existing unknown/skipped outcomes do not force intake or extra approvals. |
| Career ladder; prompts/salary-calculator/step5a-career-ladder.md | Review of the full proposed ladder before saving; Input for corrections or material mismatch with a saved ladder, then show the revision for confirmation. Reuse an established confirmed ladder for the same target. |
| Evidence-refresh blocked return; prompts/salary-calculator/step5b-final-verification.md and Sequence below | Single for refresh, dated snapshot with limitation, or stop; Input for supplied evidence when needed. If refresh remains unavailable, ask snapshot/stop without looping. Preserve earlier files and leave the audit checkpoint pending. |
