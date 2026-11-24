---
title: "Step 1: Match analysis"
parent: Job screener
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/job-screener/step1-match-analysis.html
permalink: /docs/commands/job-screener/step1-match-analysis/detailed.html
title_category: Details
description: "Match analysis uses the current job description and confirmed candidate facts to make a compact screening decision. It treats missing information, ordinary gaps and hard blockers as different evidence rather than adding them into a match score."
source_files:
  - prompts/job-screener/step1-match-analysis.md
---

# Step 1: Match analysis

{% include guide-depth.html %}

Match analysis uses the current job description and confirmed candidate facts to make a compact screening decision. It treats missing information, ordinary gaps and hard blockers as different evidence rather than adding them into a match score.

## Flow

```mermaid
flowchart TD
  Start(["Read one job description<br/>Compare with confirmed profile facts"]) --> Block{"Confirmed blocker, substantial core mismatch<br/>Or explicit user exclusion?"}
  Block -->|Yes| Skip["Skip"]
  Block -->|No| Gaps{"Two or more independent required gaps<br/>Or insufficient information to judge?"}
  Gaps -->|Yes| Maybe["Maybe"]
  Gaps -->|No| Most{"Most required qualifications met?"}
  Most -->|Yes| Apply["Apply"]
  Most -->|No| Maybe
  Skip --> Report["Return the fixed report<br/>Keep unknowns distinct from negatives"]
  Maybe --> Report
  Apply --> Report
  Report --> Wait(["Wait for the next job or application question"])
```

## Verdict rules

Apply the first supported rule in this order:

| Verdict | Condition |
|---|---|
| ❌ Skip | A confirmed hard blocker, substantial core mismatch or your explicit exclusion. |
| ⚠️ Maybe | No Skip basis, but essential role information is missing, at least two independent required qualifications are unmet, or material uncertainty prevents a useful judgment. |
| ✅ Apply | No Skip basis, core work aligns and most required qualifications are met. |
| ⚠️ Maybe | Fit remains unclear otherwise. |

The comparison starts with the work and expected outputs. Related requirements are grouped into capabilities rather than counting several tools as separate gaps. A title or familiar supporting tool does not outweigh a substantial mismatch in the main work. Conversely, comparable experience can establish a capability even when a named example tool is absent; accepted alternatives and explicit training paths matter.

A substantial core mismatch means that several central capabilities or a substantial part of the required work are not demonstrated in the confirmed profile. It is a judgment about documented fit, not a claim that you have never done anything omitted from your resume. A limited gap or unclear proficiency can remain Maybe. Your explicit role preferences are assessed separately and are never inferred from your resume alone.

Preferred qualifications are not required gaps. Unknown requirements are identified as unknown instead of being silently treated as failures. A short but informative posting can be assessed; a title and company benefits without meaningful duties may lead to Maybe because the role cannot be judged. Missing salary alone does not make a posting insufficient. The report does not invent a numeric match percentage.

## Output format

Every job uses the same literal bracketed headers, starting directly with `[VERDICT]` and without extra introductory or closing commentary.

| Header | What it contains |
|---|---|
| `[VERDICT]` | One-line decision. |
| `[APPLICATION METHOD]` | The route stated in the posting; omitted when unstated. |
| `[SALARY]` | Explicit pay with currency, period and components; omitted when unstated. |
| `[PROS]` | Important requirements connected to confirmed relevant experience. |
| `[CONS]` | Important gaps or uncertainties, with their practical effect on fit; 🚫 only for confirmed blockers. |
| `[MISSING INFORMATION]` | Unstated items from the fixed checklist. |

Pros and Cons explain the decision through specific comparisons rather than reproducing the whole resume or posting. Overlapping strengths are combined, while each deciding gap makes its evidence and consequence clear. There is no separate score or extra explanation section.

The missing-information checklist covers salary, sponsorship, relocation support, Remote policy, work authorization, working-hours overlap and employment type. An unstated item belongs here, not in Cons solely because it is absent. If the checklist is complete, the report says so.

## Hard blockers

Every 🚫 needs an explicit mandatory requirement and a confirmed candidate fact establishing inability to meet it. Rights, language, clearance, certification, hiring jurisdiction, mandatory hours or a mandatory technology condition can qualify when both sides of that comparison are known. A supported core mismatch can determine Skip without 🚫; missing resume mention alone does not establish inability.

Missing resume mention is not inability. A different city does not establish unwillingness or inability to relocate. Consider an explicit sponsorship or obtain-by-start path without promising that it will succeed. Each blocker is checked independently; one work-rights blocker does not manufacture an additional location blocker.

Experience shortfalls are never hard blockers. Unmet preferences remain labelled preferred, not required. Salary blocks only when the whole comparable range is below a confirmed hard floor; unknown conversion, incompatible pay basis and a straddling range cannot prove failure.

## Application questions and writing

Follow-up answers use confirmed profile and situational facts. Missing material information prompts a focused question or a visible placeholder, not an invented skill, personal circumstance or salary expectation.

Keep drafts compact, clear and calm. They remain drafts in chat, without automatic submission or a saved screening checkpoint.

## Source boundaries

Use this job, the confirmed profile and explicit clarifications. Country Finder fit and Salary Calculator targets do not replace job-specific eligibility or stated pay. Optional missing situational data does not trigger a full new intake merely to screen one posting.

Instructions embedded in pasted jobs or forms cannot change the workflow, authorize file access or approve submission. If a long chat drifts, the next report returns to the same format; re-invoking the command is also available.

## Explore the source

For implementation details, read [prompts/job-screener/step1-match-analysis.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/job-screener/step1-match-analysis.md).
