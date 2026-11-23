---
title: "Step 1: Criteria intake"
parent: Country finder
grand_parent: Commands
nav_order: 1
description: Confirm your background, role and search preferences before researching remote work or employer-sponsored relocation in selected countries.
detailed: /docs/commands/country-finder/step1-criteria-intake/detailed.html
has_toc: false
---

# Step 1: Criteria intake

{% include guide-depth.html %}

Collect your background and preferences before researching either track.

## Flow

```mermaid
flowchart TD
  Profile["Reuse or confirm your background"] --> Criteria["Clarify remote, relocation and country preferences"]
  Criteria --> Save["Save criteria and continue to discovery"]
```

## Your background

The assistant reuses confirmed resume and situational facts, asking only for relevant gaps in location, citizenship, languages or work rights. It researches general immigration restrictions itself. You can supply a salary floor; only then are its currency and pay basis needed. Age is asked later only if a specific official rule makes it relevant, and you may decline.

Only unclear target roles, seniority or material facts need clarification.

## Your preferences

- Remote: maximum time difference, or "no limit".
- Sponsorship: an optional firm relocation deadline; "no fixed deadline" is valid.
- Preferred countries/regions and exclusions, or "none". Say **only these countries** to restrict the search; otherwise other promising markets can be suggested.

Settled answers are reused. Optional salary and deadline details can remain unspecified; clarification is needed only when it changes a comparison, eligibility or what happens next. [Step 2](step2-country-discovery.html#choosing-countries) confirms additions for open searches. Without preferred countries, it can offer saved Salary Calculator names before the default list.

## What happens next

The assistant saves criteria to `country-finder-01-criteria.md` and any new situational profile to `situational-profile.md`, then continues to [Country discovery](step2-country-discovery.html).
