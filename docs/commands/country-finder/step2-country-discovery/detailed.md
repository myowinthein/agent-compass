---
title: "step 2: country discovery"
parent: country-finder
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder/step2-country-discovery.html
permalink: /docs/commands/country-finder/step2-country-discovery/detailed.html
title_category: Details
description: "Discovery establishes the candidate countries and the evidence for each employment track. Its job is to decide what deserves deeper research while preserving the difference between an explicit exclusion and information that has not been found."
source_files:
  - prompts/country-finder/step2-country-discovery.md
---

# Step 2: Country discovery

{% include guide-depth.html %}

Discovery establishes the candidate countries and the evidence for each employment track. Its job is to decide what deserves deeper research while preserving the difference between an explicit exclusion and information that has not been found.

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

## Choosing countries

An explicit include list comes first. Otherwise the agent can offer Salary Calculator's saved research country names, including countries whose salary data was skipped. You can keep, edit, replace or decline that list. Salary research need not be complete, and none of its conclusions transfer with the names.

If using the default is an option, the full country list is printed by continent before you answer. A question control is not the only place you should be able to inspect it. A clear list you supplied is used directly; uncertain region boundaries need clarification. Exclusions apply after regions have been expanded into countries.

Once chosen, the scope is saved and retained on resume. An empty result needs revised countries or a stop, not an invented research set.

## What gets checked

Research looks at Remote and Sponsorship together for each country, but reaches separate conclusions.

| Track | Evidence that matters |
|---|---|
| Remote | Cross-border hiring, engagement and pay arrangements applicable to your actual working location. |
| Sponsorship | A named employer-sponsored route and relevant evidence that employers hire candidates through it. |

Domestic work-from-home rules do not establish cross-border Remote access. Likewise, a nomad or self-sponsored visa is not an employer-sponsored route. Sponsor registration alone does not prove an employer is willing to hire this candidate.

Findings use dated sources and retain their limits. Missing evidence is not a rejection. A salary-based Remote exclusion needs a valid comparable range entirely below a confirmed hard floor; context-only minima or incomplete comparisons cannot support that decision.

## Timezone preference

Timezone suitability affects Remote only and is skipped for no limit. Unless you choose another period, the check covers relevant hubs over the next twelve months, including daylight-saving changes.

A country with multiple employment hubs can have mixed results. A partial pass keeps the relevant hub or seasonal condition; incomplete coverage remains unverified. One favorable timezone observed today does not establish a full-year result.

## What happens next

The candidate file records scope, track findings, reasons, timezone conditions and evidence gaps. Chat gives brief counts rather than the full research body.

[Detailed research](../step3-research-prompt-generator.html) follows the eligible yes tracks. Exclusions and no-evidence cases remain in the record for the final audit even when they receive no detailed research.

## Explore the source

For implementation details, read [prompts/country-finder/step2-country-discovery.md](https://github.com/myowinthein/agent-compass/blob/main/prompts/country-finder/step2-country-discovery.md).
