---
title: "Step 3: Research prompt generator"
parent: country-finder
grand_parent: Commands
nav_order: 3
---

# Step 3: Research prompt generator

Collect detailed research for each country's eligible tracks.

## Flow

```mermaid
flowchart TD
  Start(["Read Step 2 suitability findings"]) --> Eligible{"Any tracks marked yes?"}
  Eligible -->|No| Empty["Save an empty research scope<br/>Keep early exclusions and evidence gaps for the audit"]
  Eligible -->|Yes| Brief["One brief per country<br/>Include only tracks marked yes<br/>Embed relevant profile and criteria facts"]
  Brief --> Cap{"Separate research context<br/>with web access available?"}
  Cap -->|Yes| Tasks["Run a separate research task per country"]
  Cap -->|No| Manual["Show ready-to-copy prompts<br/>Wait for manual results"]
  Tasks --> Collect["Collect findings<br/>Check country and track coverage"]
  Manual --> Collect
  Collect --> Missing{"Any expected result missing?"}
  Missing -->|Yes| Resolve["Retry missing work or collect it manually<br/>Keep successful results"]
  Resolve --> Collect
  Missing -->|No| Save["Save country-finder-03-research.md"]
  Empty --> Save
  Save --> Next(["Continue to Step 4"])
```

## What each brief covers

Remote briefs cover pay, hiring and payment arrangements for your working location. Sponsorship briefs cover the employer-sponsored route, salary rules, employer willingness, processing, quotas and relevant candidate restrictions.

Each brief contains the confirmed role and relevant background directly. Researchers use current dated sources; unknown facts do not become assumed eligibility.

## Countries without an eligible track

Only Step 2 "yes" tracks receive detailed research. Explicit rejections and missing evidence remain distinct. With none eligible, a scope-only record lets later steps account for exclusions and gaps without inventing research.

## What happens next

The assistant saves `country-finder-03-research.md`, checks expected countries and tracks, and shows a brief count before [Data validation](step4-data-validation.html).
