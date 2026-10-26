# portal-finder

Find verified job portals for IT/tech roles in a specified country, grouped by type.

## Question points

Use [QM](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern prompts/portal-finder/step1-portal-research.md; ask only when its existing conditions require it.

| Trigger | Preferred form and answer needed |
|---|---|
| Country argument missing | Input for one country; no preset shortlist or profile intake. |
| More than one country named | Single among all named countries; Input for clarification if the country identity is ambiguous. Preserve all choices when the native picker is too small. |
| Live verification unavailable or supplied sources insufficient | Use the common research map: Input for sources/access information or Single for the actual available remedies. Keep partial successes, evidence dates and verification limits; no confirmation can turn unverified portals into verified ones. |

## Before starting

**Country:** If a country was provided as an argument, use it. If not, ask: "Which country do you want to find job portals for?" and wait for my answer before continuing. If more than one country is named at any point, ask me to pick one before proceeding — this command runs for one country at a time.

## Sequence

1. Read prompts/portal-finder/step1-portal-research.md and follow it exactly.
