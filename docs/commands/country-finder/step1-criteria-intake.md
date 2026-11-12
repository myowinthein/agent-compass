---
title: "step 1: criteria intake"
parent: country-finder
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

Saved situational facts are reused. Otherwise, provide location, citizenship, known visa issues, languages and work rights/status. An optional salary minimum needs currency, gross/net basis and a hard-floor or context-only choice. Age or birth date supports age-dependent visa rules; you may decline disclosure.

Only unclear target roles, seniority or material facts need clarification.

## Your preferences

- Remote: maximum time difference, or "no limit".
- Sponsorship: relocation timeline, including "no rush".
- Countries/regions to include and exclude, or "none".

Unclear answers need clarification. Without an include list, [Step 2](step2-country-discovery.html#choosing-countries) can offer saved Salary Calculator countries for confirmation before the default list.

## What happens next

The assistant saves criteria to `country-finder-01-criteria.md` and any new situational profile to `situational-profile.md`, then continues to [Country discovery](step2-country-discovery.html).
