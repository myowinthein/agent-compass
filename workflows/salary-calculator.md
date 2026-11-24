# salary-calculator

Run the full Salary Calculator pipeline in a search isolated by chat, person and command.

## Before starting

First read [skills/run-workspaces.md](../skills/run-workspaces.md). Select or create the run before any profile, artifact or checkpoint access; keep its returned workspace for this whole pipeline. New chats start fresh. In this chat, a matching completed run offers View previous results / Start fresh; an unfinished run offers Resume / Start fresh. Preserve earlier runs when starting fresh.

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Resolve the selected prior CF/SC source separately for country names; any substantive CF ordering read retains its own readiness checks. Canonical names below use those resolved paths on legacy runs.

Check if profile.md exists in the workspace. If it does not, read [prompts/shared/resume-extraction-prompt.md](../prompts/shared/resume-extraction-prompt.md) and follow it first. Wait for my resume and my confirmation of the extracted profile before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .salary-calculator-state.json in the workspace.
- Final step: 5 (career ladder and final verification together).
- Final output: salary-calculator-05b-final-results.md in the workspace.

## Presentation compatibility

data/output-contracts.json owns the literal table contract, Step 4 its semantic procedure, and Step 5b its audit, presentation and unfinished-legacy compatibility. Read the contract even during approved manual fallback; do not duplicate columns/formulas in host adapters or change research field names. Shared runtime rules govern filename resolution, checkpoints and completed replay.

## Sequence

Use the evidence collected in the initial research pass. Complete the initial country briefs with their full source verification and independent tier coverage before classifying a gap; normal searches and opened-source checks within that assignment remain required. Do not ask the user to supply research data manually, approve another evidence search or choose repair/refresh versus stop because online evidence is insufficient. Do not launch follow-up research merely to fill an evidence gap. Record unavailable browsing, failed tasks and uncollected countries honestly; preserve successful findings and continue through validation with what was obtained. Every scheduled initial task must have an outcome before collection ends; a missing/failed outcome is a disclosed process gap, never successful coverage. Intake, candidate-fact confirmations and tool/file-integrity failures retain their own rules.

A supported international adjustment is optional. When it cannot be estimated, use each comparable tier's researched Realistic value as an unadjusted local-market benchmark reference, with the overseas adjustment explicitly unverified. Never substitute a verified 0% or invent missing salary data. If validation or calculation leaves no country with usable salary benchmarks, save the required reports/output and completed stage checkpoint, explain the no-result outcome and end without a research-retry/manual-data question, career ladder or empty final table. Repairs to changed inputs remain user-directed under the runtime's preservation rule.

1. First read and apply [skills/situational-profile-questions.md](../skills/situational-profile-questions.md) on the calling model, so situational-profile.md exists before threshold research. Read [prompts/salary-calculator/step1-research-prompt-generator.md](../prompts/salary-calculator/step1-research-prompt-generator.md) and follow it exactly.
2. Read [prompts/salary-calculator/step2-data-validation.md](../prompts/salary-calculator/step2-data-validation.md) and follow it exactly.
3. Reuse situational-profile.md; on a legacy resume that lacks it, apply skills/situational-profile-questions.md first. Read [prompts/salary-calculator/step3-international-adjustment.md](../prompts/salary-calculator/step3-international-adjustment.md) and follow it exactly on the current agent.
4. Read [prompts/salary-calculator/step4-table-calculation.md](../prompts/salary-calculator/step4-table-calculation.md) and follow it exactly on the current agent, using [skills/salary-calculation-helper.md](../skills/salary-calculation-helper.md) for numeric results and their review.
5. Step 5 (final verification) always runs when at least one country was calculated. First read [prompts/salary-calculator/step5a-career-ladder.md](../prompts/salary-calculator/step5a-career-ladder.md) and follow it, including the user's confirmation. Saving the confirmed ladder completes only substep 5a; keep `last_completed_step` at 4 until the final audit is saved and its required checks succeed. Then read [prompts/salary-calculator/step5b-final-verification.md](../prompts/salary-calculator/step5b-final-verification.md) and follow it exactly on the current agent. Complete any additional numeric work under skills/salary-calculation-helper.md before accepting a final output. The career ladder and final verification remain mandatory for a calculable run.

Step 5 audits the saved dated evidence without offering a refresh question. Keep supported dated facts with their as-of limitations; an unsupported current visa state/amount becomes Unknown, not a guessed pass or block. Missing market calibration stays inconclusive. Continue with defensible values and record remaining gaps. Only an explicit user-initiated evidence update may introduce fresh sources; preserve earlier files and cite its source, access/as-of dates and scope in the final audit.

## Question points

Use [question mechanism (QM)](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern the named supporting prompts; ask only when their existing conditions require it.

| Trigger and owner | Preferred form and answer needed |
|---|---|
| New situational profile; skills/situational-profile-questions.md | Reuse applicable confirmed profile facts and saved answers, including those copied from Country Finder. Input for missing location, passport nationality, willing-and-able working languages or country/status/work-condition pairs. Pay is optional; collect its units/basis only when supplied and clarify firm minimum versus context only when ambiguous. Do not ask for expected salary, generic immigration-risk judgments or upfront age. Preserve unknown/none/not specified and declined disclosure. |
| Material official age-dependent reference route rule; skills/sponsorship-threshold-rules.md | Explain the affected country/source/event and ask only for the needed age or band. Respect declined disclosure; keep the affected visa check conditional without blocking other research or salary targets. Later persistence uses the shared runtime's existing dated-note approval. |
| Target role/level; prompts/salary-calculator/step1-research-prompt-generator.md | Input only for unresolved role/level. Local employee salary benchmarks and separate reference visa salary research are the fixed scope, not a user choice. Do not ask for an employment path or offer a remote/relocation/sponsorship menu. Explain the limitation only for an explicit cross-border-pay request. |
| Country scope; skills/country-selection.md and prompts/salary-calculator/step1-research-prompt-generator.md | Use the shared previous-list/own/default question and show every proposed country in ordinary chat first. Supplied countries are exact scope; retain excluded/skipped countries in a reused list. Names-only selection never confirms producer completion, fits or salary conclusions. Resume keeps its confirmed list/source. |
| Research collection, validation and unusable estimates; prompts/salary-calculator/step1-research-prompt-generator.md, prompts/salary-calculator/step2-data-validation.md and Sequence above | Report missing/failed collection outcomes and proceed with obtained evidence. No manual-research request, retry/refresh choice or missing-evidence repair menu. If no salary benchmark is usable, save the required outcome and end without career-ladder intake. Structural ambiguity and tool/file-integrity failures retain the shared helper/repair rules. |
| Adjustment/calculation context, invalid units or changed scope; prompts/salary-calculator/step3-international-adjustment.md and prompts/salary-calculator/step4-table-calculation.md | Ask only for material candidate facts or genuine input/file repair. Missing evidence is recorded as unverified or skipped; missing adjustment alone uses benchmark references. Existing execution/manual-arithmetic choices remain separate from research collection. |
| Career ladder; prompts/salary-calculator/step5a-career-ladder.md | Review of the full proposed ladder before saving; Input for corrections or material mismatch with a saved ladder, then show the revision for confirmation. Reuse an established confirmed ladder for the same target. |
| Audit evidence gaps; prompts/salary-calculator/step5b-final-verification.md | Continue on supported dated evidence with explicit uncertainty; do not ask for refreshed/manual evidence or a retry choice. User-initiated updates follow the existing preservation and provenance rules. |
