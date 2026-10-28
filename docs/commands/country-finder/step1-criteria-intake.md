---
title: "Step 1: Criteria intake"
parent: country-finder
grand_parent: Commands
nav_order: 1
---

# Step 1: Criteria intake

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

## Your background

Saved situational facts are reused. Otherwise, provide location, citizenship, known visa issues, languages and work rights/status. An optional salary minimum needs currency, gross/net basis and a hard-floor or context-only choice. Age or birth date supports age-dependent visa rules; you may decline disclosure.

Only unclear target roles, seniority or material facts need clarification.

## Your preferences

- Remote: maximum time difference, or "no limit".
- Sponsorship: relocation timeline, including "no rush".
- Countries/regions to include and exclude, or "none".

Unclear answers need clarification. Without an include list, Step 2 can offer saved Salary Calculator countries for confirmation before the default list.

## What happens next

The assistant saves criteria to `country-finder-01-criteria.md` and any new situational profile to `situational-profile.md`, then continues to [Country discovery](step2-country-discovery.html).
