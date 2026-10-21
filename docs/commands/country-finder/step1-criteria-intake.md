---
title: "Step 1: Criteria intake"
parent: country-finder
grand_parent: Commands
nav_order: 1
---

# Step 1: Criteria intake

Collects your preferences before researching countries for remote work or visa sponsorship.

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
  CriteriaClear -->|Yes| Save["Save preferences and target role<br/>cf-step1-criteria.md<br/>Confirm it was saved"]
  Save --> Continue(["Continue automatically to Step 2<br/>Country discovery"])
```

## Your background

If you already have a saved situational profile, it is reused. Otherwise, the assistant asks about:

- Your current location, citizenship and any known visa complications.
- Languages you speak and want to use at work.
- Existing work rights or immigration status.
- Minimum monthly salary and currency, whether it is before or after tax and whether it is a strict minimum or just context.
- Age or date of birth for age-dependent visa salary rules.

You can skip the salary minimum or choose not to share your age. If your target role or seniority is unclear, it asks you to clarify.

## Your preferences

- Remote work: the maximum time difference you accept from your current location, or "no limit".
- Visa sponsorship: your relocation timeline, such as "within 12 months" or "no rush".
- Countries or regions you want included, or "none".
- Countries or regions you want excluded, or "none".

If an answer is unclear, the assistant asks for clarification before continuing.

## What happens next

Your preferences are saved to `cf-step1-criteria.md`. A new situational profile is saved to `situational-profile.md` for reuse.

The workflow then continues to [Step 2: Country discovery](step2-country-discovery.html).
