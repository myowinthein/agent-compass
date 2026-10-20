---
layout: default
title: Specialist agents
nav_exclude: true
permalink: /docs/specialist-agents.html
---

# Specialist agents

Country Finder and Salary Calculator can offer a specialist agent for steps that involve judgement or calculations. You can accept the offer or keep using your current model.

## Requested models

| Specialist | Claude | Codex |
|---|---|---|
| `deep-reasoner` | Opus, high effort | `gpt-6.1-sol`, high effort |
| `calculator` | Opus, max effort | `gpt-6.1-sol`, max effort |

The `deep-reasoner` handles country scoring, final ranking, international salary adjustment and final salary verification. The `calculator` handles the salary table calculations.

These are the settings Agent Compass requests, not a guarantee that every client or account can use them. Matching effort labels do not imply equal capability or token usage across providers. Codex requests the model and effort explicitly rather than inheriting session defaults.

## Your choice

Before each handoff, the assistant names the specialist, model and effort. It explains that delegation uses additional tokens and that higher effort may increase cost and response time, then asks for your approval.

If you decline, the current model completes the step. Final ranking and salary verification still run, and arithmetic still requires calculation tools or step-by-step verification.

If delegation or the requested settings are unavailable, the assistant explains the limitation and waits for you to choose an alternative or your current model. It does not silently substitute settings. A failed handoff also requires your choice before continuing.

Specialist routing does not change your main conversation's model or persistent settings. Research tasks are handled separately and do not inherit these specialist settings.
