---
title: /country-finder-v2
parent: Commands
nav_order: 2
---

# /country-finder-v2

Runs an automated, evidence-audited country search for two separate goals: remote work from the candidate's current country and employer-sponsored relocation.

## Usage

```text
/claude-compass:country-finder-v2
```

The command resumes from `.country-finder-v2-state.json` if interrupted.

## What is different

- Research is performed during the pipeline instead of requiring the user to run one prompt per country.
- Remote eligibility must explicitly include the candidate's country, region, or worldwide. Domestic-only remote work does not qualify.
- A legal visa route and a sponsor register do not count as proof that an employer will sponsor the target occupation.
- Each track receives a numeric score from 0 to 100.
- A separate audit reopens decisive sources and can revise provisional scores.
- Parallel agents use separate batch files, avoiding shared-file append conflicts.
- Final rankings show two cutoffs: Gold for custom application effort and Silver for broad active monitoring.

## Flow

1. **Intake:** reads the profile and collects only missing candidate, compensation, remote, relocation, and country-scope facts.
2. **Grounded research:** searches official immigration sources and current job evidence for every country and both tracks.
3. **Audit and scoring:** verifies decisive claims, corrects evidence inflation, and calculates final numeric scores.
4. **Final ranking:** produces the full country table, cutoffs, effort allocation, salary positioning, portal strategy, and source register.

## Output files

| File | Contents |
|---|---|
| `cfv2-step1-criteria.md` | Confirmed candidate and search criteria |
| `cfv2-step2-country-universe.md` | Ordered country scope |
| `cfv2-step2-research.md` | Consolidated sourced research |
| `cfv2-step3-audited-scores.md` | Authoritative audited numeric scores |
| `cfv2-step4-final-report.md` | Final reusable report |

The command does not edit an Obsidian vault or external profile automatically.

