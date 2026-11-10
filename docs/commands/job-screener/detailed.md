---
title: "job-screener"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/job-screener.html
guide_source: workflows/job-screener.md
permalink: /docs/commands/job-screener/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for job-screener."
---

# job-screener

{% include guide-depth.html %}

Compare job descriptions with your profile and receive an Apply, Maybe or Skip report. You can also request application drafts.

## Flow

```mermaid
flowchart TD
  Start(["Run job-screener"]) --> Run{"Matching chat/person JS session?"}
  Run -->|Continue screening or Resume setup| Profile["Use the selected run's profile<br/>Or extract your resume and wait for confirmation"]
  Run -->|No match or Start fresh| New["Create an isolated run"]
  New --> Profile
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

## Complete procedure

{{ page.guide_source | guide_full }}
