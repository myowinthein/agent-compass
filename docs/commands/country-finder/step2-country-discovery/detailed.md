---
title: "Step 2: Country discovery"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step2-country-discovery.html
guide_source: prompts/country-finder/step2-country-discovery.md
permalink: /docs/commands/country-finder/step2-country-discovery/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Step 2: Country discovery."
---

# Step 2: Country discovery

{% include guide-depth.html %}

Check which countries have evidence of remote hiring or employer-sponsored relocation for your role.

## Flow

```mermaid
flowchart TD
  Start(["Read your profile and criteria"]) --> List{"Countries specified?"}
  List -->|Yes| Scope["Expand regions and apply exclusions<br/>Clarify ambiguous boundaries"]
  List -->|No| Salary{"Saved Salary Calculator country list?"}
  Salary -->|Yes| Offer["Offer the saved target countries, names only<br/>Wait: keep, edit, replace or choose default"]
  Offer -->|Keep, edit or replace| Confirm["Save your country choice in criteria"]
  Confirm --> Scope
  Offer -->|Default| Default["Show the default list<br/>Wait for your list or approval"]
  Salary -->|No usable list| Default
  Default --> Scope
  Scope --> Empty{"Any countries left?"}
  Empty -->|No| Revise(["Ask for a revised list or stop"])
  Empty -->|Yes| Batch["Save the country scope<br/>Split into batches of at most 15"]
  Batch --> Continue["Continue below with the saved country scope"]
```

Research covers both tracks in every selected country, with explicit handling for unavailable research access and missing results.

```mermaid
flowchart TD
  Batch["Use the saved country batches"] --> Cap{"Separate research context<br/>with web access available?"}
  Cap -->|Yes| Research["Research both tracks for every country<br/>Use self-contained candidate briefs"]
  Cap -->|No| Manual["Show batch prompts<br/>Wait for manual results"]
  Research --> Coverage["Collect results and check every country<br/>Resolve missing results"]
  Manual --> Coverage
  Coverage --> TZ["Apply your remote timezone limit, if any<br/>Check relevant hubs and seasonal changes"]
  TZ --> Save(["Save country-finder-02-candidates.md<br/>Continue to Step 3"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
