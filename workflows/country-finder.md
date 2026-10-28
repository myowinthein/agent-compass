# country-finder

Run the full Country Finder pipeline, resuming from where it left off if a state file exists.

## Question points

Use [QM](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern the named supporting prompts; ask only when their existing conditions require it.

| Trigger and owner | Preferred form and answer needed |
|---|---|
| Target role/seniority ambiguity; prompts/country-finder/step1-criteria-intake.md | Input for the missing role/level; reuse a clear target. |
| New situational profile; skills/situational-profile-questions.md | Input for location, citizenship, immigration context, languages, salary amount/currency/pay basis, country/status pairs and age/date reference. Single for hard floor versus context-only when a minimum is supplied. Preserve none, unknown, not specified and declined age as different answers; no invented candidate options. |
| Track criteria and preferences; prompts/country-finder/step1-criteria-intake.md | Input for timezone hours/no limit, relocation timeline and Include/Exclude countries or regions. Multi only for an actual displayed finite country set; Input for additions and precise clarification of vague answers. Keep track labels and independent Include/Exclude intent. |
| Salary research-scope offer; prompts/country-finder/step2-country-discovery.md | Single for keep/edit/replace/default with all proposed countries visible. Edit uses Multi explicitly naming countries to retain or exclude, plus Input for additions; replace uses Input. Missing scope offers own/default list. Names-only selection never confirms salary conclusions or completion. |
| Default list, ambiguous region or empty country scope; prompts/country-finder/step2-country-discovery.md | For the default offer, print the complete list grouped by continent in ordinary chat before asking Single for default versus own list or invoking a native question tool. Follow Step 2's display rule. Input for custom countries or an ambiguous expansion, Review only when that expansion needs confirmation. Empty scope asks Input for a revised list or Single to stop. Explicit clear lists need no repeated confirmation. |
| Research collection, boundary ambiguity and missing-country repair; prompts/country-finder/step2-country-discovery.md, prompts/country-finder/step3-research-prompt-generator.md and prompts/country-finder/step4-data-validation.md | Use the common research/helper map: Input for missing results or boundaries; Single for actual repair routes. A no-eligible-track scope-only record and a reported rejection do not themselves require a question. |
| Scoring/final-audit missing facts, optional salary provenance or contradicted exclusions; prompts/country-finder/step5-scoring.md and prompts/country-finder/step6-final-ranking.md | Use the common clarification, upstream and repair forms. Parent resolves questions before specialist continuation; no extra approval of ordinary scores, ranking or final output. |

## Before starting

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Canonical names below use those resolved paths on legacy runs.

Step 2 may offer Salary Calculator's saved research scope as an optional country list when no explicit Include list was supplied. Resolve that producer separately only when needed; missing salary files never block Country Finder. Reuse names only after confirmation, not salary-based fit or eligibility conclusions.

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it. Wait for the resume and confirmation of the extracted profile, and for profile.md to be saved, before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .country-finder-state.json in the workspace.
- Final step: 6.
- Final output: country-finder-06-final-results.md in the workspace.

## Sequence

Apply the shared runtime's changed-input and repair rule on unfinished resumes. Zero eligible tracks, all rejected detailed research and all-Pending evidence are distinct from an empty country scope. A nonempty candidate universe still reaches the final audit with its exclusions/gaps accounted for, using Step 3's scope-only record when necessary; do not invent scores or automatically research every no-evidence track. An empty scope asks for revised countries or stop before research. Contradicted early exclusions return to the parent for a repair choice rather than being silently overridden.

1. Read prompts/country-finder/step1-criteria-intake.md and follow it exactly.
2. Read prompts/country-finder/step2-country-discovery.md and follow it exactly.
3. Read prompts/country-finder/step3-research-prompt-generator.md and follow it exactly.
4. Read prompts/country-finder/step4-data-validation.md and follow it exactly.
5. Use the specialist routing rule in prompts/shared/runtime.md for Step 5 (scoring), role deep-reasoner, prompt prompts/country-finder/step5-scoring.md. Run the step on the chosen agent or current model.
6. Step 6 (final ranking) always runs. Use the specialist routing rule in prompts/shared/runtime.md for Step 6, role deep-reasoner, prompt prompts/country-finder/step6-final-ranking.md. Routing is optional; this final step is mandatory.
