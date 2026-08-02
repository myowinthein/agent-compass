---
title: Step 4 — Data validation
parent: /country-finder
grand_parent: Commands
nav_order: 4
---

# Step 4 — Data validation

A strict silent-storage mode. Claude reads `cf-step3-country-research.md` written by Step 3 and processes each country's data autonomously — no pasting required. If the file is missing, Claude stops and reports it rather than waiting for manual input.

## Flow

```mermaid
flowchart TD
  Start([Step 4 begins]) --> FileCheck{cf-step3-country-research.md\nexists?}
  FileCheck -->|no| Error[Stop — report missing file\nAsk user to rerun Step 3]
  FileCheck -->|yes| ReadFile[Read file — process\neach country in order]
  ReadFile --> MultiCheck{Multiple countries\nor none in block?}
  MultiCheck -->|yes| Err1[Skip — record issue\nNothing stored]
  Err1 --> ReadFile
  MultiCheck -->|no| FieldCheck{Required fields\ncomplete?}
  FieldCheck -->|no| Err2[Skip — record missing fields\nNothing stored]
  Err2 --> ReadFile
  FieldCheck -->|yes| ListCheck{Country on\nStep 2 candidate list?}
  ListCheck -->|no| Unlisted[Skip — never auto-store\nRecord for manual review]
  Unlisted --> ReadFile
  ListCheck -->|yes| DupCheck{Already\nstored?}
  DupCheck -->|yes| SkipDup[Skip — keep original\nRecord as duplicate]
  DupCheck -->|no| Store[Store verbatim]
  SkipDup --> ReadFile
  Store --> ReadFile
  ReadFile --> Done{File\nexhausted?}
  Done -->|no| ReadFile
  Done -->|yes| Report[Reply with one consolidated report:\nstored count + all skips by reason]
  Report --> End([Step complete\nWait for main command])
```

## What it reads

- `cf-step3-country-research.md` — written by Step 3 sub-agents
- `cf-step2-candidates.md` — used to validate that each country was marked suitable for at least one track

## Rules

This runs fully automated, with no pause between countries — bad items are skipped and recorded, never halted on.

| Situation | Claude's response |
|---|---|
| File not found | Stops — reports missing file, asks user to ensure Step 3 completed |
| Block contains multiple countries | Skips it and records the issue — nothing stored |
| Block contains no recognizable country | Skips it and records the issue — nothing stored |
| Required field or section missing | Skips it and records what's missing — nothing stored |
| Country not marked suitable for any track in Step 2 | Never stored automatically — skipped and recorded for manual review |
| Country already stored | Skips it, keeps original, records it as a duplicate |
| Valid, complete data for one country | Stored silently |

Claude preserves all values, wording, and formatting exactly as provided. It does not correct, improve, or reinterpret the data.

## What Claude does not do in this step

- No analysis, scoring, or ranking
- No summaries or tables
- No opinions or recommendations
- No additional actions unless explicitly instructed

## Stop condition

Once all countries from `cf-step3-country-research.md` have been processed, Claude writes all successfully stored countries to `cf-step4-country-data.md` (which Step 5 scores next), replies with one consolidated report (stored count, plus every skip grouped by reason — malformed, missing fields, duplicate, not marked suitable for any track), then stops and waits for the main command.
