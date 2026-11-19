---
title: "Step 3: Research prompt generator"
parent: Country-finder
grand_parent: Commands
nav_order: 3
description: Collect detailed country research for eligible remote and sponsorship tracks, account for missing results and preserve successful research.
detailed: /docs/commands/country-finder/step3-research-prompt-generator/detailed.html
has_toc: false
---

# Step 3: Research prompt generator

{% include guide-depth.html %}

Compare each country's non-excluded tracks, including gaps left by discovery.

## Flow

```mermaid
flowchart TD
  Scope["Identify non-excluded tracks and discovery gaps"] --> Research["Compare the same factors; follow up promising gaps"]
  Research --> Save["Account for the scope and save findings"]
```

## What each brief covers

Both briefs compare market demand, role match, international access and pay feasibility. Remote research applies to your working location; Sponsorship research adds the employer-sponsored route and candidate-specific conditions. Checked sources and unresolved questions remain visible.

Promising tracks with important gaps receive targeted follow-up before collection finishes. Unpublished or inaccessible evidence can remain unknown after substantive checks.

Each brief contains the confirmed role and relevant background directly. Researchers use current dated sources; unknown facts do not become assumed eligibility.

## Countries without an eligible track

Only an explicit supported [discovery exclusion](step2-country-discovery.html#what-gets-checked) skips a track. Both positive leads and no-evidence findings receive detailed research. With every track excluded, a scope-only record preserves the reasons without inventing research.

## What happens next

The assistant saves `country-finder-03-research.md`, checks expected countries and tracks, and shows a brief count before [Data validation](step4-data-validation.html).
