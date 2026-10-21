# country-finder

Run the full Country Finder pipeline, resuming from where it left off if a state file exists.

## Before starting

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Canonical names below use those resolved paths on legacy runs.

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
