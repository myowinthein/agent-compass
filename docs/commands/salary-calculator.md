---
title: salary-calculator
parent: Commands
nav_order: 3
has_children: true
---

# salary-calculator

Estimates salary targets for your role in selected countries, then audits how realistic they are for your profile.

Mainstream and Premium are two local-employee employer segments. Both describe pay for work in the target country, not a cross-border remote offer from your home country.

## Start the command

```text
salary-calculator
```

Use the prefix shown in [Setup]({{ '/docs/setup/' | relative_url }}). There is no country argument; the workflow asks you to choose countries.

It loads your saved resume profile, or extracts your resume and waits for confirmation. Your situational profile is collected or reused before research.

## Flow

```mermaid
flowchart TD
  Start(["Load or confirm your profile"]) --> Status{"Saved run?"}
  Status -->|Completed| Replay(["Show the saved final result"])
  Status -->|Needs recovery or repair| Recover(["Explain the issue<br/>Wait for your choice"])
  Status -->|New or valid unfinished run| Resume["Start or resume the next unfinished step"]
  Resume --> S1["1. Confirm countries and employment path<br/>Research local salaries and visa salary rules"]
  S1 --> S2["2. Validate and store research"]
  S2 --> Stored{"Any country stored?"}
  Stored -->|No| Repair(["Save the report and checkpoint<br/>Offer evidence repair or stop"])
  Stored -->|Yes| S3["3. Estimate supported international adjustments"]
  S3 --> S4["4. Calculate comparable salary targets<br/>Record skipped countries"]
  S4 --> Usable{"Any country calculated?"}
  Usable -->|No| Repair
  Usable -->|Yes| Ladder["5a. Draft or reuse the matching career ladder<br/>Wait for confirmation if needed"]
  Ladder --> Audit["5b. Audit the salary framework<br/>Revise only when evidence supports it"]
  Audit --> End(["Show the final salary table<br/>Save the full audit"])
```

The numbered path shows a new run. An interrupted run continues from its next unfinished step.

## What to expect

[Research](salary-calculator/step1-research-prompt-generator.html) starts with countries you confirm. Country Finder can suggest a list, but is not required. Research covers two employer tiers, your role and level, dated sources and applicable visa salary rules.

[Validation](salary-calculator/step2-data-validation.html) preserves accepted research. [International adjustment](salary-calculator/step3-international-adjustment.html) estimates a supported reduction from local benchmarks; missing evidence is not treated as 0%.

[Calculation](salary-calculator/step4-table-calculation.html) produces annual targets and monthly references. The [final verification](salary-calculator/step5b-final-verification.html) checks positioning and calibration after you confirm the career ladder.

Some steps offer a [specialist agent]({{ '/docs/specialist-agents.html' | relative_url }}). Declining does not skip the step or change the shared arithmetic.

## Your result

Chat shows Country, Visa salary rule, Mainstream Annual, Premium Annual, Mainstream Monthly and Premium Monthly. Targets stay in local currency and are not raised to satisfy a visa rule or your salary minimum.

The full audit is saved to `salary-calculator-05b-final-results.md`. An inconclusive audit is stated plainly rather than presented as verified market advice.

If you run Salary Calculator first, [country-finder](country-finder.html) can offer your saved target countries for confirmation. It reuses the names only and assesses remote work and sponsorship separately.

Interrupted runs use `.salary-calculator-state.json`. See [shared workspaces and saved results]({{ '/docs/commands#shared-workspaces-and-saved-results' | relative_url }}) for recovery and [Calculation runtime](salary-calculator/step4-table-calculation.html#calculation-runtime) for Python requirements.
