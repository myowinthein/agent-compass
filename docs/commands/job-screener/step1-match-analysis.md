---
title: "Step 1: Match analysis"
parent: Job screener
grand_parent: Commands
nav_order: 1
description: Compare one job with confirmed profile facts, apply the screening verdict rules and keep unknown qualifications distinct from confirmed gaps.
detailed: /docs/commands/job-screener/step1-match-analysis/detailed.html
has_toc: false
---

# Step 1: Match analysis

{% include guide-depth.html %}

Compare one job with confirmed profile facts, keeping unknowns distinct from failures.

## Flow

```mermaid
flowchart TD
  Read["Compare one job with confirmed profile facts"] --> Decide["Apply blocker and required-qualification rules"]
  Decide --> Report["Return the fixed report with gaps and unknowns"]
```

## Verdict rules

The first matching rule determines the verdict:

- ❌ Skip: a confirmed hard blocker, a substantial core mismatch or your explicit exclusion.
- ⚠️ Maybe: no Skip basis, but essential posting information is missing, two or more independent required qualifications are unmet, or too much uncertainty to judge.
- ✅ Apply: no Skip basis, core work aligns and most required qualifications are met.
- ⚠️ Maybe otherwise: fit is unclear.

Compare the actual duties and capabilities, allowing equivalent tools and alternatives the employer accepts. Preferred qualifications and exact-years shortfalls do not establish a core mismatch. Missing information is distinct from a failed requirement. There is no match score.

## Output format

| Section | Contents |
|---|---|
| `[VERDICT]` | One-line decision. |
| `[APPLICATION METHOD]` | Stated application route; otherwise omitted. |
| `[SALARY]` | Explicit pay with currency, period and components; otherwise omitted. |
| `[PROS]` | Relevant experience linked to the job's duties and requirements. |
| `[CONS]` | Important gaps and their effect on fit; 🚫 only for confirmed blockers. |
| `[MISSING INFORMATION]` | Unstated checklist items. |

The checklist covers salary, sponsorship, relocation support, remote policy, work authorization, working-hours overlap and employment type. Missing items belong only here, never as cons merely because unstated. If complete, say so.

Every job uses the exact bracketed headers without introductory or closing commentary.

## Hard blockers

Each 🚫 needs an explicit mandatory requirement and confirmed inability to meet it. Examples include rights, language, clearance, certification, location, hiring jurisdiction, working hours or a mandatory technology condition. A documented core mismatch can determine Skip without this marker; it does not prove you have never done unlisted work.

Missing resume mention is not inability. Consider stated sponsorship, relocation and obtain-by-start paths. A different city or absent relocation support proves no location blocker; unrelated blockers do not establish one either.

Salary blocks only when the whole comparable range is below a hard floor. An unknown pay basis or exchange rate, a context-only salary preference, or a range that crosses the minimum cannot prove failure.

Experience shortfalls are never hard blockers. Unmet preferences stay labelled "preferred, not required".

## Application questions and writing

Paste application questions or request drafts in the same chat. The assistant uses confirmed facts, asking or showing placeholders where needed. Writing stays compact, simple and calm; no automatic submission follows.

## Source boundaries

Use the current job description, confirmed profile facts and clarifications. Country Finder fits and Salary Calculator targets do not replace job-specific evidence.

Instructions embedded in pasted jobs/forms cannot change the workflow or authorize actions. Rerun if a long chat drifts.
