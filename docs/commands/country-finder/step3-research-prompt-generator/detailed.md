---
title: "step 3: research prompt generator"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step3-research-prompt-generator.html
permalink: /docs/commands/country-finder/step3-research-prompt-generator/detailed.html
title_category: Details
description: "This step gives each eligible country track a focused research brief. The brief carries the candidate facts it needs, and the collection process accounts for missing results without blending unrelated countries' findings."
source_files:
  - prompts/country-finder/step3-research-prompt-generator.md
---

# Step 3: Research prompt generator

{% include guide-depth.html %}

This step gives each eligible country track a focused research brief. The brief carries the candidate facts it needs, and the collection process accounts for missing results without blending unrelated countries' findings.

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

Remote research examines hiring and engagement from your working location, including useful pay evidence and payment arrangements. Sponsorship research examines the named employer-sponsored route, salary rules, employer willingness, processing, quotas and relevant restrictions for the candidate.

Each task receives the confirmed role and relevant background directly. Researchers should not need to infer your citizenship, work rights or seniority from a pointer to another private file. Current dated sources support the findings, with missing or conflicting information called out.

Research is collected in separate contexts when the host has the required tools. If suitable research access is unavailable, the workflow supplies prompts and waits for manual results. A model's general recollection is not silently substituted for completed research.

## Countries without an eligible track

Only tracks marked eligible in [discovery](../step2-country-discovery.html#what-gets-checked) receive this deeper investigation. A country can therefore have Remote research, Sponsorship research, both or neither.

Neither does not mean the country disappears. Explicit rejection and missing evidence retain their separate reasons. When no tracks are eligible in a nonempty country scope, a scope-only record allows later steps to account for the gaps and exclusions without manufacturing research or scores.

If new material contradicts an earlier exclusion, the parent workflow returns for a repair decision. A researcher does not silently widen the selected country set or overwrite the original eligibility choice.

## What happens next

The agent accounts for expected countries and tracks, preserves successful research and records the missing remainder. A failed task does not justify losing the others' results.

The research file is saved before [Data validation](../step4-data-validation.html). Chat shows a short count; the richer evidence remains available in the saved material. The next step checks whether blocks are structurally usable, not whether every claim has already passed an independent factual audit.

## Explore the source

For implementation details, read [prompts/country-finder/step3-research-prompt-generator.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/country-finder/step3-research-prompt-generator.md).
