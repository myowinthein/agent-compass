---
title: "country-finder"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/country-finder.html
permalink: /docs/commands/country-finder/detailed.html
title_category: Details
description: "Country Finder helps decide where to spend your application effort. It investigates cross-border Remote work and employer-sponsored relocation separately, then turns the evidence into priorities for your confirmed profile."
source_files:
  - workflows/country-finder.md
---

# country-finder

{% include guide-depth.html %}

Country Finder helps decide where to spend your application effort. It investigates cross-border Remote work and employer-sponsored relocation separately, then turns the evidence into priorities for your confirmed profile.

## Flow

```mermaid
flowchart TD
  Start["Select the chat, person and command"] --> Existing{"Matching run?"}
  Existing -->|Completed| View{"View results or start fresh?"}
  View -->|View| Replay["Show the saved final result"]
  Existing -->|Unfinished| Resume{"Resume or start fresh?"}
  View -->|Fresh| New["Create a separate run; preserve earlier work"]
  Resume -->|Fresh| New
  Existing -->|No| New
  New --> Profile{"Confirmed profile reusable for this person?"}
  Profile -->|No| Extract["Extract resume; wait for confirmation before saving"]
  Profile -->|Yes| Ready["Use this run's confirmed profile"]
  Extract --> Ready
  Resume -->|Resume| Check["Validate saved inputs and the next unfinished step"]
  Ready --> Steps["Continue the pipeline below"]
  Check -->|Valid| Steps
  Check -->|Unusable or changed| Repair["Explain the issue; wait for the applicable repair choice"]
```

```mermaid
flowchart TD
  Criteria["1. Confirm background and search criteria"] --> Scope["2. Choose countries and research Remote/Sponsorship suitability"]
  Scope --> Empty{"Any countries in scope?"}
  Empty -->|No| Ask["Ask for a revised list or stop"]
  Empty -->|Yes| Research["3. Collect detailed research for eligible tracks; or save a scope-only record"]
  Research --> Data["4. Validate and store accepted research without rewriting it"]
  Data --> Saved{"Required outputs saved and checked?"}
  Saved -->|No| Hold["Preserve results; reconcile failure without advancing"]
  Saved -->|Yes| Assess["5. Assess fit/confidence per track; optional specialist"]
  Assess --> Audit["6. Audit every candidate, exclusions and gaps; optional specialist"]
  Audit --> Final["Save the audit and Priority Table; show the table in chat"]
```

## Start the command

Run country-finder in a chat for the person being assessed. If a profile is missing, provide a resume and confirm the extraction before research continues. Relevant situational facts are confirmed separately rather than guessed from job titles or nationality.

A new chat starts a fresh search. In the same chat, a completed matching search offers View previous results or Start fresh; an unfinished search offers Resume or Start fresh. Earlier runs remain preserved, and another person's profile is not selected by recency.

## What to expect

### Confirm the criteria and country scope

[Criteria intake](step1-criteria-intake.html) clarifies role, timezone tolerance, relocation timing and include/exclude preferences. Your own country list comes first. Without one, [Country discovery](step2-country-discovery.html#choosing-countries) can offer Salary Calculator's saved country names for confirmation or show the default list.

That optional transfer uses names only. An unfinished salary search or a skipped salary estimate does not remove a country from the offer, and salary conclusions are not silently inherited.

### Investigate the two tracks independently

Remote evidence must apply to hiring someone in your actual working location. A company's domestic work-from-home policy does not establish cross-border hiring or pay. Sponsorship needs an employer-sponsored route and relevant willingness to hire; nomad or self-sponsored routes do not satisfy that track.

[Detailed research](step3-research-prompt-generator.html) follows tracks found eligible at discovery. Research tasks receive the needed profile facts directly and are kept separate from each other. If suitable research access is unavailable, you receive prompts and the workflow waits for supplied results rather than inventing findings.

### Validate, assess and audit

[Validation](step4-data-validation.html) checks structure and preserves accepted research unchanged. It does not certify the truth of every claim. [Scoring](step5-scoring.html) assigns categorical fit and confidence independently to each supported track.

The [final audit](step6-final-ranking.html) checks missing candidates, confidence and misuse of evidence before assigning priorities. Optional specialists can perform scoring or the audit; declining one leaves the required work on the current model.

## Your result

Chat shows a Priority Table with each country, application priority, both track fits and the main limitation. The saved final report contains the fuller audit and effort guidance. Unknown evidence, a known Weak fit and an explicit Exclusion remain different outcomes.

For example, strong Remote evidence can justify pursuing a country while Sponsorship remains unknown. That is not a reason to invent a sponsorship fit. When neither track supports a positive assessment and evidence is missing, Pending evidence is more accurate than a negative ranking.

A nonempty country scope can still reach an audit when no tracks receive detailed research: exclusions and gaps are accounted for without fabricated scores. An empty country list instead needs a revised scope or a stop.

The final Summary records the audited fits. Salary Calculator can use compatible results for its own country selection; [Portal Finder](../portal-finder.html) can help find job boards for one chosen country. Neither follow-up happens automatically.

## Explore the source

For implementation details, read [workflows/country-finder.md](https://github.com/myowinthein/agent-compass/blob/main/workflows/country-finder.md).
