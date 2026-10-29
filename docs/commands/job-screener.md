---
title: job-screener
parent: Commands
nav_order: 4
has_children: true
---

# job-screener

Compare job descriptions with your profile and receive an Apply, Maybe or Skip report. You can also request application drafts.

## Start the command

```text
job-screener
```

Use the prefix from [Setup]({{ '/docs/setup/' | relative_url }}#run-a-command). Run once in a dedicated chat, then paste one job at a time.

## Flow

```mermaid
flowchart TD
  Start(["Run job-screener"]) --> Profile["Load profile.md<br/>Or extract your resume and wait for confirmation"]
  Profile --> Context["Reuse situational-profile.md if present<br/>Clarify only material missing or conflicting facts"]
  Context --> Wait(["Profile loaded<br/>Wait for your paste"])
  Wait --> Kind{"What did you send?"}
  Kind -->|One job description| Screen["Screen this job using the fixed report format"]
  Kind -->|Application questions or writing| Draft["Draft from confirmed facts<br/>Ask or use placeholders for missing details"]
  Kind -->|Several jobs or unclear mix| Ask["Ask which to handle first"]
  Screen --> Wait
  Draft --> Wait
  Ask --> Wait
```

## Your result

Each report gives a verdict, pros, cons and missing information. Salary and application method appear only when stated. 🚫 marks confirmed hard blockers, not every profile gap.

Saved situational facts are reused without requiring new intake. Drafts use confirmed facts and compact English; nothing is submitted automatically.

The profile is stored at `<home>/Agent Compass/profile.md`. Screening results stay in chat. See [Searches and saved files](../setup/saved-searches.html).

See [Match analysis](job-screener/step1-match-analysis.html) for verdict rules and the exact report format.

## Continuing the chat

Keep pasting jobs or application questions. Each job is assessed independently without a checkpoint. If a long chat drifts, rerun the command to reload its instructions and profile.
