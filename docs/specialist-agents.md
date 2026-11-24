---
layout: default
title: Model and effort
nav_exclude: true
permalink: /docs/specialist-agents.html
description: Compass uses your current model and effort for analysis and audits, with separate research tasks and shared Python arithmetic helpers.
detailed: /docs/specialist-agents/detailed.html
has_toc: false
---

# Model and effort

{% include guide-depth.html %}

Country Finder and Salary Calculator use your current model and reasoning effort for analysis, calculation review and final audits. Choose those settings in your client; Compass continues without asking you to select another model between steps.

## Flow

```mermaid
flowchart TD
  Evidence["Collect and validate evidence"] --> Analyse["Analyse on your current model and effort"]
  Analyse --> Audit["Run the required final audit and saved-output checks"]
  Audit --> Results["Present the results"]
```

<span id="specialist-agents"></span>
<span id="requested-models"></span>

## Your model and effort

Compass does not prescribe a higher model or effort. Your selection leaves the required research, analysis and audits in place.

## Your choice

The workflow still asks for necessary candidate facts, scope decisions and confirmations. Salary Calculator's career ladder needs your confirmation before its audit; ordinary step transitions need no model approval.

<span id="calculator-versus-python-helper"></span>

## Calculations and research

Shared Python helpers calculate exact salary amounts. Your current agent checks their inputs and results against saved evidence. Unavailable execution needs the existing [manual-fallback choice]({{ '/docs/commands/salary-calculator/step4-table-calculation.html#calculation-runtime' | relative_url }}).

Research can use separate tasks to keep each brief isolated. These inherit your current model and effort where supported; otherwise the workflow uses its existing manual-research fallback. Compass does not offer a different research configuration.
