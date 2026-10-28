---
title: "Step 2: Country discovery"
parent: country-finder
grand_parent: Commands
nav_order: 2
---

# Step 2: Country discovery

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
  Batch --> Cap{"Separate research context<br/>with web access available?"}
  Cap -->|Yes| Research["Research both tracks for every country<br/>Use self-contained candidate briefs"]
  Cap -->|No| Manual["Show batch prompts<br/>Wait for manual results"]
  Research --> Coverage["Collect results and check every country<br/>Resolve missing results"]
  Manual --> Coverage
  Coverage --> TZ["Apply your remote timezone limit, if any<br/>Check relevant hubs and seasonal changes"]
  TZ --> Save(["Save country-finder-02-candidates.md<br/>Continue to Step 3"])
```

## Choosing countries

Your include list comes first. Otherwise, [Salary Calculator](../salary-calculator/step1-research-prompt-generator.html#choosing-countries)'s saved research scope can supply a proposed list. You can keep, edit, replace it or choose the default. The assistant waits for your answer before researching.

Salary research need not be complete: only country names are reused, including targets whose salary data was skipped. No salary or visa conclusions transfer. Missing scope leaves your own list or the default available.

Regions expand into countries before exclusions apply. Clear supplied lists need no second confirmation; ambiguous boundaries do. Accepted choices are saved in criteria and retained on resume.

## What gets checked

- **Remote:** hiring, pay and engagement evidence applicable to your working location. Domestic remote policies do not prove cross-border hiring.
- **Sponsorship:** a named employer-sponsored route and relevant hiring evidence. Nomad/self-sponsored visas do not qualify, and sponsor registration alone proves no willingness to hire.

Dated sources support each finding. Missing evidence is not rejection. Only a valid comparison proving pay below a hard floor can cause a salary-based Remote exclusion.

## Timezone preference

Unless you specify another period, relevant hubs are checked over the next 12 months, including DST. Partial passes retain conditions; uncertain coverage stays unverified.

This affects Remote only and is skipped for "no limit".

## What happens next

`country-finder-02-candidates.md` saves the scope and findings; chat shows counts. Once results are complete, continue to [Detailed research](step3-research-prompt-generator.html).
