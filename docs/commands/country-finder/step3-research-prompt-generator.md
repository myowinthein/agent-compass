---
title: Step 3 — Research prompt generator
parent: /country-finder
grand_parent: Commands
nav_order: 3
---

# Step 3 — Research prompt generator

Generates one ready-to-copy research prompt per candidate country, then runs each as an isolated sub-agent. Claude does not answer the research questions itself in this step.

## Flow

```mermaid
flowchart TD
  Start([Step 3 begins]) --> ForEach[For each candidate country]
  ForEach --> TrackCheck{Appeared in\nwhich list?}
  TrackCheck -->|Remote only| RemoteP[Remote Track\nprompt only]
  TrackCheck -->|Sponsorship only| SponP[Sponsorship Track\nprompt only]
  TrackCheck -->|Both| Combined[Combined prompt\nwith both sections]
  RemoteP --> RunAgent[Run as isolated sub-agent\none country only]
  SponP --> RunAgent
  Combined --> RunAgent
  RunAgent --> Isolate{Isolation\nguaranteed?}
  Isolate -->|yes| Append[Append results to\ncf-step3-country-research.md]
  Isolate -->|no| Manual[Show prompt\nWait for manual results]
  Manual --> Append
  Append --> More{More\ncountries?}
  More -->|yes| ForEach
  More -->|no| Done([Step complete\nWait for main command])
```

## What it reads

- `cf-step2-remote-candidates.md` and `cf-step2-sponsorship-candidates.md` from Step 2
- `profile.md` and `situational-profile.md`

## Prompt structure per country

Each prompt covers only the track(s) that country appeared in:

| Country appeared in | Prompt contains |
|---|---|
| Remote list only | Remote Track section only |
| Sponsorship list only | Sponsorship Track section only |
| Both lists | Both sections in one combined prompt |

**Remote Track section asks for:**
- Confirmed realistic remote salary range for your role and seniority, in local currency
- Evidence of remote hiring volume (job postings, hiring reports, company policies)
- Typical payment structure (local currency vs USD, contractor vs employee)
- Sources with dates

**Sponsorship Track section asks for:**
- Full name of the specific visa or sponsorship pathway and its official source
- Minimum salary threshold required by that visa
- Realistic employer willingness to sponsor your specific role
- Realistic visa processing time
- Any quota, cap, or annual limit
- Family or dependent sponsorship provisions
- Citizenship-specific complications based on your situational profile
- Sources with dates

## Sub-agents

Each country's prompt is run as a separate isolated sub-agent. Each agent:
- Receives only its own country's prompt
- Has no access to results for other countries
- Returns results that are appended to `cf-step3-country-research.md`

If isolation cannot be guaranteed, Claude shows all prompts and waits for you to bring back the results manually.

## Output

- `cf-step3-country-research.md` — per-country research results, appended as each agent completes

## Stop condition

Once all results are saved to `cf-step3-country-research.md`, Claude stops and waits for the main command before continuing to Step 4.
