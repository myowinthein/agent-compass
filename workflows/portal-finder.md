# portal-finder

Find usable country-relevant IT/tech portals in exactly three groups: Global job boards, Local & regional job boards, and IT & tech niche job boards. Apply the research prompt's aggregator exclusion and evidence-based star criteria; omit problematic/unverified candidates without warning lists.

## Before starting

**Country:** If a country was provided as an argument, use it. If not, ask: "Which country do you want to find job portals for?" and wait for my answer before continuing. If more than one country is named at any point, ask me to pick one before proceeding — this command runs for one country at a time.

## Sequence

1. Read [Portal results](../skills/portal-results.md) and look up reports for the established country. If none exists, continue to research. Otherwise show the latest report's saved/evidence dates, verification kind and coverage, then ask **View saved results / Run a fresh search**. Honor an explicit fresh-search or saved-report choice without asking again. Viewing reads the selected report unchanged, labels it as historical and ends the command. Offer older history only on request.
2. For a fresh search, read [prompts/portal-finder/step1-portal-research.md](../prompts/portal-finder/step1-portal-research.md) and follow it exactly. Save each completed report through Portal results, preserving earlier runs. No profile or checkpoint is created.

## Question points

Use [question mechanism (QM)](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern prompts/portal-finder/step1-portal-research.md; ask only when its existing conditions require it.

| Trigger | Preferred form and answer needed |
|---|---|
| Country argument missing | Input for one country; no preset shortlist or profile intake. |
| More than one country named | Single among all named countries; Input for clarification if the country identity is ambiguous. Preserve all choices when the native picker is too small. |
| A saved report exists for the established country | Single for View saved results / Run a fresh search, showing its saved/evidence dates, verification kind and coverage. Reuse an explicit choice. Offer older reports only on request. |
| Live verification unavailable or supplied sources insufficient | Use the common research map: Input for sources/access information or Single for the actual available remedies. Keep partial successes, evidence dates and verification limits; no confirmation can turn unverified portals into verified ones. |
