---
title: "Step 1: Research prompt generator"
parent: Salary calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step1-research-prompt-generator.html
permalink: /docs/commands/salary-calculator/step1-research-prompt-generator/detailed.html
title_category: Details
description: "Salary research establishes comparable local benchmarks before any adjustment is calculated. It records how figures were chosen, which employer segment they describe and what the evidence cannot establish."
source_files:
  - skills/country-selection.md
  - prompts/salary-calculator/step1-research-prompt-generator.md
  - skills/situational-profile-questions.md
  - skills/sponsorship-threshold-rules.md
---

# Step 1: Research prompt generator

{% include guide-depth.html %}

Salary research establishes comparable local benchmarks before any adjustment is calculated. It records how figures were chosen, which employer segment they describe and what the evidence cannot establish.

## Flow

```mermaid
flowchart TD
  Start(["Read or collect your situational profile<br/>Settle any unclear role or level"]) --> Countries["Use your own countries, a previous list or the default"]
  Countries --> Confirm["Show every proposed country<br/>Wait for any required choice or edits"]
  Confirm --> Scope["Use local-employee salary benchmarks<br/>Research visa salary rules as a separate reference"]
  Scope --> Brief["One self-contained brief per country<br/>Two employer tiers, sources and visa salary rules"]
  Brief --> Cap{"Separate research context<br/>with web access available?"}
  Cap -->|Yes| Tasks["Research each country separately"]
  Cap -->|No| Manual["Record the collection limitation<br/>Use any available findings"]
  Tasks --> Collect["Save findings and every task outcome<br/>Disclose missing coverage"]
  Manual --> Collect
  Collect --> Next(["Save salary-calculator-01-research.md<br/>Continue to Step 2"])
```

## Starting information

Your confirmed resume and applicable situational answers supply the candidate context. A profile reused from Country Finder does not need another full questionnaire. Location and work rights help distinguish an overseas applicant from someone already able to work in the target market; accepted working languages matter to actual role opportunities. The role and seniority need clarification only when the target is unclear.

You can leave your personal pay minimum unspecified. If supplied, it is a comparison against the researched targets, with its currency, gross/net basis and firm-versus-context meaning kept clear. It is not an expected salary you must invent before the command can help you.

General immigration restrictions and employer behavior come from research. A concrete personal circumstance may need clarification, but you are not asked to estimate citizenship-related hiring risk. Age is requested only when an official rule could change the relevant visa category or salary requirement. An age band can be enough; declining leaves that check conditional without preventing salary research.

## Choosing countries

An explicit list defines the exact research scope. Otherwise, a fresh salary search can offer the preceding Country Finder or Salary Calculator list for the same person in this chat. The complete list transfers, including countries previously excluded or missing usable salary data. A weak fit in Country Finder does not remove a country from this names-only choice.

The assistant identifies the source and displays all its countries before asking whether to reuse them, choose other countries or use the default. Long lists appear in readable groups or short lines above the question. You can supply a replacement or request additions/removals directly. If no usable prior list exists, the same own/default choice remains available. Defaults are shown in full before acceptance; requesting an unseen default does not confirm its contents.

Choosing Start fresh can reuse the preceding country list while preserving earlier files. If the chat does not clearly establish which previous search to use, you choose the source. Resuming an unfinished search keeps its recorded list instead of offering newer countries.

Reusing country names does not require a completed search or adopt its conclusions. A completed Country Finder result may also order the salary table by Relocation priority when it matches the current profile and scope; otherwise the table uses alphabetical order.

## What gets researched

Mainstream represents mid-size or mainstream local-market employers; Premium represents premium, international or remote-first employers. Both describe gross annual base pay for local employees working in the target country. Each receives its own Low, Realistic and Strong amounts, role and level, geography, working-hours basis, dated sources and selection method.

Premium needs actual employer-segment evidence. It is not a percentage uplift applied to Mainstream, and a high compensation package dominated by equity is not automatically a comparable base-pay benchmark. Contractor rates, expat premiums and inflated global-only figures are excluded from the intended comparison.

Published numbers and analyst selections remain distinguishable. If Realistic is inferred from several sources, the method is recorded rather than presented as a quoted market statistic. Quantitative local-versus-overseas evidence is also retained for the later adjustment decision.

The local-employee scope is fixed: this step does not ask you to choose Remote, relocation or sponsorship. Actual cross-border pay while you stay in another country falls outside this calculation.

## Visa salary research

A relevant employer-sponsored salary rule is collected separately using confirmed age, status, residence and citizenship where material. Unknown facts do not select a favorable category. An undecided relocation plan does not, by itself, make the rule Not applicable.

Keep the original amount and period, or an explicit nonnumeric state. A monthly comparison requires official eligible-pay and schedule support; dividing annual base by twelve is not enough to establish that legal basis. [Calculation](../step4-table-calculation.html#visa-salary-rule-comparison) preserves that distinction.

## What happens next

Separate research tasks collect the initial findings. Each scheduled task ends with a collected, missing or failed outcome. Unavailable access and failed collection remain visible gaps; successful findings stay preserved. The workflow proceeds with obtained evidence rather than requesting manual results or another evidence search. It records the full country scope, including countries with missing or rejected data, for later country or salary searches.

After coverage checks, [Data validation](../step2-data-validation.html) checks structure and preserves accepted evidence. Research remains a dated source snapshot, not an offer or an immigration eligibility determination.

## Explore the source

For implementation details, read the [research prompt](https://github.com/myowinthein/agent-compass/blob/main/prompts/salary-calculator/step1-research-prompt-generator.md), [shared intake](https://github.com/myowinthein/agent-compass/blob/main/skills/situational-profile-questions.md) and [visa salary rules](https://github.com/myowinthein/agent-compass/blob/main/skills/sponsorship-threshold-rules.md).

The shared [country-selection rules](https://github.com/myowinthein/agent-compass/blob/main/skills/country-selection.md) define the common previous-list, own-list and default choices.
