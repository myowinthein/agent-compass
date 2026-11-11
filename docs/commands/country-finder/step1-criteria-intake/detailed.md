---
title: "Step 1: Criteria intake"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step1-criteria-intake.html
permalink: /docs/commands/country-finder/step1-criteria-intake/detailed.html
title_category: Details
description: "Criteria intake turns your background and preferences into a usable research brief. It separates facts about the candidate from choices about the search, so later findings can explain why each track fits or does not."
source_files:
  - prompts/country-finder/step1-criteria-intake.md
---

# Step 1: Criteria intake

{% include guide-depth.html %}

Criteria intake turns your background and preferences into a usable research brief. It separates facts about the candidate from choices about the search, so later findings can explain why each track fits or does not.

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

The confirmed resume profile supplies professional experience, role and seniority. Saved situational facts are reused; the agent asks only for material gaps or ambiguity rather than extracting the same resume repeatedly.

Situational context includes location, citizenship, known immigration issues, languages and existing work rights. A country where you can already work may need different analysis from one where an employer must obtain sponsorship. Unknown status remains unknown instead of becoming assumed eligibility.

An optional salary minimum needs an amount, currency and gross/net basis, plus whether it is a hard floor or context only. An unexplained number cannot support a valid exclusion. Age or birth-date context can help with age-dependent routes, but disclosure may be declined and the resulting limitation must remain visible.

## Your preferences

Remote uses your maximum time difference, or **no limit**. Sponsorship uses your relocation timeline, including **no rush**. These choices constrain different tracks; a timezone restriction should not become a relocation exclusion.

State countries or regions to include and exclude, or say none. Clear choices do not need a duplicate confirmation, while vague regions and contradictory boundaries require clarification before they become the candidate scope.

For example, a preference for Europe does not tell the researcher whether you mean the EU, the EEA or a broader region. Resolving that once is more useful than silently choosing a definition for every later step.

## What happens next

The agent saves the criteria and any newly confirmed situational profile, then continues to [Country discovery](../step2-country-discovery.html#choosing-countries).

Your own include list takes precedence. Without one, discovery can offer Salary Calculator's saved country names for your decision before using a default list. That offer transfers names only, not another workflow's salary or eligibility conclusions.

Material changes later can require revisiting affected research. Earlier files and decisions are preserved rather than relabeled as if they were produced from the new profile.

## Explore the source

For implementation details, read [prompts/country-finder/step1-criteria-intake.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/country-finder/step1-criteria-intake.md).
