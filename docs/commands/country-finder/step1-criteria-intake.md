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

The assistant reuses confirmed facts, asking only for relevant gaps. Citizenship/passport nationality and existing country-specific status or work rights are separate. One language question asks which languages you are willing and able to use at work. A salary floor is optional; its currency and pay basis are needed only when supplied. Age is asked later only if a specific official rule makes it relevant, and you may decline.

Only unclear target roles, seniority or material facts need clarification.

## Your preferences

- Remote: maximum time difference, or "no limit".
- Sponsorship: an optional firm relocation deadline; "no fixed deadline" is valid.
- Countries/regions to research, a previous CF/SC list, or the default list. A supplied list is used exactly; removals are handled as list edits rather than a separate exclusion question.

Settled answers are reused. Optional salary and deadline details can remain unspecified. The [shared country choice](step2-country-discovery.html#choosing-countries) offers the previous CF/SC scope for this person in this chat when you have not supplied countries, with own/default-list alternatives. Every proposed country is shown before the choice; clear supplied or confirmed lists need no second approval in Step 2.

## What happens next

The assistant saves criteria to `country-finder-01-criteria.md` and any new situational profile to `situational-profile.md`, then continues to [Country discovery](step2-country-discovery.html).
