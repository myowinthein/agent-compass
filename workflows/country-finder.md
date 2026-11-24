# country-finder

Run the full Country Finder pipeline in a search isolated by chat, person and command.

## Before starting

First read [skills/run-workspaces.md](../skills/run-workspaces.md). Select or create the run before any profile, artifact or checkpoint access; keep its returned workspace for this whole pipeline. New chats start fresh. In this chat, a matching completed run offers View previous results / Start fresh; an unfinished run offers Resume / Start fresh. Preserve earlier runs when starting fresh.

Resolve this workflow's artifact paths using skills/workspace-files.md before accessing saved outputs. Canonical names below use those resolved paths on legacy runs.

Step 1 asks for the countries to research: a supplied list is the exact scope, while no preference leads to the displayed, editable default list in Step 2. Do not automatically suggest extra countries or offer Salary Calculator's list. Its saved research scope remains available on explicit names-only request; missing salary files never block Country Finder and no salary conclusions transfer. Resumes retain their confirmed scope.

Check if profile.md exists in the workspace. If it does not, read [prompts/shared/resume-extraction-prompt.md](../prompts/shared/resume-extraction-prompt.md) and follow it. Wait for the resume and confirmation of the extracted profile, and for profile.md to be saved, before continuing.

## State tracking

Apply the state tracking instructions in prompts/shared/runtime.md with:

- State file: .country-finder-state.json in the workspace.
- Final step: 6.
- Final output: country-finder-06-final-results.md in the workspace.

## Sequence

Apply the shared runtime's changed-input and repair rule on unfinished resumes. All tracks explicitly excluded, all rejected detailed research and wholly unresolved evidence are distinct from an empty country scope. A nonempty candidate universe still reaches the final audit with its exclusions/gaps accounted for, using Step 3's scope-only record only when every track is explicitly excluded; research discovery no-evidence tracks under Step 3, including targeted follow-up for promising gaps; never invent scores. An empty scope asks for revised countries or stop before research. Contradicted early exclusions return to the parent for a repair choice rather than being silently overridden.

1. Read [prompts/country-finder/step1-criteria-intake.md](../prompts/country-finder/step1-criteria-intake.md) and follow it exactly.
2. Read [prompts/country-finder/step2-country-discovery.md](../prompts/country-finder/step2-country-discovery.md) and follow it exactly.
3. Read [prompts/country-finder/step3-research-prompt-generator.md](../prompts/country-finder/step3-research-prompt-generator.md) and follow it exactly.
4. Read [prompts/country-finder/step4-data-validation.md](../prompts/country-finder/step4-data-validation.md) and follow it exactly.
5. Read [prompts/country-finder/step5-scoring.md](../prompts/country-finder/step5-scoring.md) and follow it exactly on the current agent.
6. Read [prompts/country-finder/step6-final-ranking.md](../prompts/country-finder/step6-final-ranking.md) and follow it exactly on the current agent. This final audit always runs and produces independently ordered Remote and Relocation tables.

## Question points

Use [question mechanism (QM)](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern the named supporting prompts; ask only when their existing conditions require it.

| Trigger and owner | Preferred form and answer needed |
|---|---|
| Target role/seniority ambiguity; prompts/country-finder/step1-criteria-intake.md | Input for the missing role/level; reuse a clear target. |
| Missing situational context; skills/situational-profile-questions.md | Reuse confirmed facts; Input for missing location, passport nationality, one combined willing-and-able working-language answer, or country/status/work-condition pairs. Citizenship and current status remain separate; do not request known citizenship twice or infer unrestricted permission. Offer an optional pay floor, collecting amount/currency/basis only when supplied. No generic immigration-risk question or upfront age request; preserve none/unknown/not specified/declined. |
| Material official age-dependent route rule; skills/sponsorship-threshold-rules.md | The parent explains the affected country/source/event and asks only the needed age or band, reusing supplied references. Respect declined disclosure; unresolved checks remain conditional without blocking other research. Saving a later dated profile note uses the runtime's existing Review rule. |
| Track criteria and country scope; prompts/country-finder/step1-criteria-intake.md | Reuse settled answers; batch missing timezone hours/no limit and an optional firm relocation deadline with one Input for the user's countries or default choice. Supplied countries are exact scope; no separate exclusion question or automatic additions. |
| Displayed default or explicitly requested salary names; prompts/country-finder/step2-country-discovery.md | Show the full list in ordinary chat before Single for use/edit/replace; a requested salary source also offers default. Edit uses Multi for displayed countries and Input for additions. Names-only reuse never confirms salary conclusions or completion. Clear supplied or already confirmed lists need no duplicate approval. |
| Ambiguous region, legacy unconfirmed open scope or empty selection; prompts/country-finder/step2-country-discovery.md | Input only for ambiguous boundaries; use the existing repair choice before changing legacy scope intent. Empty scope asks for revised countries or stop. Resumes keep their saved scope. |
| Research collection, boundary ambiguity and missing-country repair; prompts/country-finder/step2-country-discovery.md, prompts/country-finder/step3-research-prompt-generator.md and prompts/country-finder/step4-data-validation.md | Use the common research/helper map: Input for missing results or boundaries; Single for actual repair routes. A no-eligible-track scope-only record and a reported rejection do not themselves require a question. |
| Scoring/final-audit missing facts, optional salary provenance or contradicted exclusions; prompts/country-finder/step5-scoring.md and prompts/country-finder/step6-final-ranking.md | Use the common clarification, upstream and repair forms before continuing; no extra approval of ordinary scores, ranking or final output. |
