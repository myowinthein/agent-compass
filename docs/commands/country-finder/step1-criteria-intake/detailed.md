---
title: "Step 1: Criteria intake"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step1-criteria-intake.html
guide_source: prompts/country-finder/step1-criteria-intake.md
permalink: /docs/commands/country-finder/step1-criteria-intake/detailed.html
title_category: Detailed guide
description: "Complete procedure, choices, constraints and outcomes for Step 1: Criteria intake."
---

# Step 1: Criteria intake

{% include guide-depth.html %}

Collect your background and preferences before researching either track.

## Flow

```mermaid
flowchart TD
  Start(["Read your resume profile<br/>Clarify target role or seniority if needed"]) --> Existing{"Saved situational profile?"}
  Existing -->|Yes| Reuse["Reuse saved background<br/>Ask only for material missing details"]
  Existing -->|No| Background["Collect your background<br/>Location, citizenship and known visa issues<br/>Spoken/work languages and work rights/status<br/>Optional monthly minimum: amount and currency<br/>Gross base or net; strict minimum or context<br/>Optional age or date of birth"]
  Background --> BackgroundClear{"Answers clear?"}
  BackgroundClear -->|No| ClarifyBackground["Ask for clarification<br/>Wait for your answer"]
  ClarifyBackground --> BackgroundClear
  BackgroundClear -->|Yes| SaveBackground["Save situational-profile.md"]

  Reuse --> Criteria["Ask about your search<br/>Remote: timezone limit or no limit<br/>Sponsorship: relocation timeline or no rush<br/>Countries/regions to include, or none<br/>Countries/regions to exclude, or none"]
  SaveBackground --> Criteria
  Criteria --> CriteriaClear{"All criteria answered clearly?"}
  CriteriaClear -->|No| ClarifyCriteria["Ask for clarification<br/>Wait for your answer"]
  ClarifyCriteria --> CriteriaClear
  CriteriaClear -->|Yes| Save["Save preferences and target role<br/>country-finder-01-criteria.md<br/>Confirm it was saved"]
  Save --> Continue(["Continue automatically to Step 2<br/>Country discovery"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
