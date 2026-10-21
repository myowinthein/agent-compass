---
layout: default
title: Specialist agents
nav_exclude: true
permalink: /docs/specialist-agents.html
---

# Specialist agents

Country Finder and Salary Calculator can offer an optional specialist for judgement-heavy or calculation steps. You can accept or keep using your current model.

## Requested models

| Specialist | Claude | Codex | Used for |
|---|---|---|---|
| `deep-reasoner` | Opus, high effort | `gpt-6.1-sol`, high effort | Country scoring and final ranking; salary adjustment and final verification |
| `calculator` | Opus, max effort | `gpt-6.1-sol`, max effort | Checking salary inputs and preparing the table |

These are requested settings, not guaranteed availability. Matching effort labels do not imply equal capability or token usage across providers.

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

## Your choice

Approval applies to the offered step unless you explicitly choose a wider scope. Unavailable settings and failed handoffs are reported; the assistant does not silently substitute another model.

Declining a specialist never skips scoring, final ranking or final salary verification. It also does not change your main conversation's model or persistent settings.

## Calculator versus Python helper

The calculator is an AI specialist, not the arithmetic engine. Both hosts use the same local Python helpers whether or not you accept it.

The main conversation prepares numeric results, and the specialist checks them against the saved inputs. If more calculation is needed, it returns the request before completing the step.

Unavailable Python execution needs a separate manual-fallback choice. See [Calculation runtime]({{ '/docs/commands/salary-calculator/step4-table-calculation.html#calculation-runtime' | relative_url }}).

Research tasks are separate from these specialists and do not inherit their model settings.
