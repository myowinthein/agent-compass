# job-screener

Screen job descriptions against your resume profile.

## Question points

Use [QM](../prompts/shared/question-mechanism.md) and the shared runtime's common question map. These forms also govern prompts/job-screener/step1-match-analysis.md; ask only when its existing conditions require it.

| Trigger | Preferred form and answer needed |
|---|---|
| No job description supplied | Input for the JD via normal chat/paste or a supplied readable file; resume extraction/confirmation follows the common map. |
| Multiple distinct jobs or an ambiguous job/form mixture | Single among the actual jobs to handle first, Input if the intended boundary is unclear. Do not turn one-job application follow-ups into a new selection. |
| Material missing/conflicting candidate facts or an unsupported claimed blocker | Input for only the necessary facts; preserve unknown where allowed. Optional situational-profile absence does not trigger full intake. Saving an existing-profile correction follows the common Review rule. |
| Application answers or drafts need facts | Input for missing facts, or retain the prompt's visible placeholder when appropriate. Drafting is not submission approval; do not add a submit action or persistence. |

## Before starting

Read skills/run-workspaces.md and select this chat/person's Job Screener run before reading any profile. A new chat or person starts fresh. On re-invocation in this chat, offer Continue screening / Start fresh for a ready profile, or Resume setup / Start fresh when intake is unfinished. Use the returned run workspace for profiles; never reuse the base folder's profile automatically. Once selected, ordinary JD/application follow-ups stay in that run without repeating run selection. JS has no completed-search state, saved screening reports or checkpoint.

A request to screen for a different person must select that person's run before screening, even without command re-invocation. Do not carry another person's candidate facts or application drafts into the selected run.

A replacement resume or different profile version for this person starts a fresh JS run under skills/run-workspaces.md, preserving the current profile; ordinary JD/application follow-ups and approved dated clarifications stay in the selected run.

Check if profile.md exists in the workspace. If it does not, read prompts/shared/resume-extraction-prompt.md and follow it. Wait for the resume and confirmation of the extracted profile, and for profile.md to be saved, before continuing.

## Sequence

1. Read prompts/job-screener/step1-match-analysis.md and follow it exactly.
