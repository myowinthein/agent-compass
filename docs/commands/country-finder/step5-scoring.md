---
title: Step 5 — Scoring
parent: /country-finder
grand_parent: Commands
nav_order: 5
---

# Step 5 — Scoring

Scores every stored country against your criteria, keeping Remote and Sponsorship tracks completely separate. Before running, Claude asks whether to use the **deep-reasoner** subagent (Opus, high effort) for higher reasoning accuracy. If you decline, the step runs with your current model.

## Flow

```mermaid
flowchart TD
  Start([Step 5 begins]) --> OpusQ{Use Opus for\nhigher accuracy?}
  OpusQ -->|yes| DeepReasoner[Route to deep-reasoner\nOpus / high effort]
  OpusQ -->|no| CurrentModel[Run with your\ncurrent model]
  DeepReasoner --> Remote
  CurrentModel --> Remote[Score all Remote-track countries first]
  Remote --> SalCheck{Salary minimum\nspecified?}
  SalCheck -->|yes| RSalary{Salary meets\nthe minimum?}
  SalCheck -->|no| RClassify
  RSalary -->|no| RExclude[Exclude — state specific gap]
  RSalary -->|yes| RClassify[Classify: Strong / Moderate / Weak\nAssign confidence: High / Medium / Low]
  RClassify --> RVague{Evidence vague\nor unquantified?}
  RVague -->|yes| RLower[Lower confidence\nstate reason]
  RVague -->|no| RNext
  RLower --> RNext
  RExclude --> RNext{More Remote\ncountries?}
  RNext -->|yes| Remote
  RNext -->|no| Spons[Score all Sponsorship-track countries]
  Spons --> SClassify[Classify: Strong / Moderate / Weak\nAssign confidence: High / Medium / Low]
  SClassify --> SVague{Evidence vague\nor unquantified?}
  SVague -->|yes| SLower[Lower confidence\nstate reason]
  SVague -->|no| SNext
  SLower --> SNext
  SNext{More Sponsorship\ncountries?}
  SNext -->|yes| Spons
  SNext -->|no| Save[Save full results\nto cf-step5-scoring-results.md]
  Save --> Brief[Tell user a brief\nscored/excluded count per track]
  Brief --> Done([Step complete\nWait for main command])
```

## What it reads

- `cf-step4-country-data.md` — all country data from Step 4
- `cf-step1-criteria.md` — timezone limit (informational, already applied in Step 2)
- `situational-profile.md` — salary minimum (optional, skipped if not specified) and citizenship-specific friction
- `sc-step4-salary-table.md` — Salary Calculator's final figures, if present, used to check Sponsorship-track visa salary thresholds

## Batching rule

All Remote-track countries are scored first, all the way through, before Sponsorship scoring begins for any country. Tracks are never interleaved.

## Remote track scoring

For each country with Remote data stored:

1. If a minimum monthly salary was specified in the situational profile, check whether the confirmed salary meets or exceeds it. If not, exclude with the specific gap stated (e.g. "confirmed salary $X, below your minimum of $Y"). If no minimum was specified, skip this check.
2. If it passes: classify Remote fit as **Strong**, **Moderate**, or **Weak**.
3. Assign confidence: **High**, **Medium**, or **Low**.
4. Give brief reasoning referencing actual stored evidence, not assumption.

## Sponsorship track scoring

For each country with Sponsorship data stored:

1. If a visa minimum salary threshold was reported, check whether `sc-step4-salary-table.md` exists and covers this country. If it does, note whether those figures clear the threshold. If it doesn't exist or doesn't cover this country, note the threshold as informational only.
2. Classify Sponsorship fit as **Strong**, **Moderate**, or **Weak**.
3. Assign confidence: **High**, **Medium**, or **Low**.
4. Give brief reasoning referencing actual stored evidence, including any citizenship-specific friction from the situational profile.

## Evidence quality rule

If the stored research uses vague or unquantified language ("sometimes," "generally friendly," "fairly common"), confidence is lowered and the reason is stated. Vague claims are never treated as strong evidence.

## Exclusion transparency rule

Every country actually scored on a track but excluded from the results must be listed separately with a specific, evidence-based reason. "General reputation" is not an acceptable reason. If no data was ever stored for that country and track, that is stated plainly. Checking the full Step 2 candidate list for countries that never reached scoring at all is Step 6's Missing Candidate Check, not this rule — Step 5 never reads `cf-step2-candidates.md`.

## File format

This structure is written to `cf-step5-scoring-results.md` — it is not what Claude shows in chat (see Output below):

```
Remote Track Results
- [Scored countries: fit, confidence, brief reasoning]
- [Excluded countries: specific reason]

Sponsorship Track Results
- [Scored countries: fit, confidence, brief reasoning]
- [Excluded countries: specific reason]

Summary
- Remote: [N] scored, [N] excluded
- Sponsorship: [N] scored, [N] excluded
```

## Output

Full results are saved to `cf-step5-scoring-results.md` in the workspace. Step 6 reads this file directly and always runs next to produce the curated, human-facing result — so Claude does not reproduce this detailed breakdown in chat. Instead, it tells you in a few lines how many countries were scored and excluded on each track, and confirms the file is saved.

## Stop condition

After outputting results, Claude stops and waits for the main command, which then proceeds to Step 6 (Final Ranking) — it always runs and is never asked about.
