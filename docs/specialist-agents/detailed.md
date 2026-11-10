---
title: "Specialist agents"
nav_exclude: true
has_toc: false
overview: /docs/specialist-agents.html
guide_sources:
  - prompts/shared/deep-reasoner.md
  - prompts/shared/calculator.md
permalink: /docs/specialist-agents/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for Specialist agents."
---

# Specialist agents

{% include guide-depth.html %}

Read how optional specialist offers, configuration checks and handoffs work. The parent keeps user questions and checkpoint control.

## Flow

```mermaid
flowchart TD
  Start(["A step offers a specialist"]) --> Available{"Requested model and effort selectable?"}
  Available -->|Yes| Offer["Name the role, model and effort<br/>Explain extra tokens and possible cost or time"]
  Offer --> Choice{"Use the specialist?"}
  Choice -->|No| Current["Complete the step on your current model"]
  Choice -->|Yes| Task["Run only the approved step"]
  Available -->|No| Alternative["Explain the limit<br/>Wait for your choice of available settings"]
  Alternative -->|Current model| Current
  Alternative -->|Available specialist| Task
  Task --> Success{"Handoff succeeds?"}
  Success -->|No| Retry["Report failure<br/>Wait for retry or another choice"]
  Retry --> Choice
  Success -->|Yes| Return["Return the output to the main conversation"]
  Current --> Check["Check the result and continue the workflow"]
  Return --> Check
```

## Routing and approval

The routing policy below comes directly from the shared runtime. The effective role settings are declared in the [deep-reasoner definition](https://github.com/myowinthein/agent-compass/blob/main/agents/deep-reasoner.md) and [calculator definition](https://github.com/myowinthein/agent-compass/blob/main/agents/calculator.md).

{{ 'prompts/shared/runtime.md' | guide_section: 'Specialist routing' }}

## Deep-reasoner procedure

{{ 'prompts/shared/deep-reasoner.md' | guide_full }}

## Calculator procedure

{{ 'prompts/shared/calculator.md' | guide_full }}

Research collection uses separate tasks, with its own [research isolation and fallback policy](https://github.com/myowinthein/agent-compass/blob/main/prompts/shared/runtime.md#research-delegation).
