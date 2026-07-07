---
title: Step 4 — Data ingestion
parent: /country-finder
grand_parent: Commands
nav_order: 4
---

# Step 4 — Data ingestion

A strict silent-storage mode. Claude reads and stores research data you paste in, one country at a time, with no analysis until you explicitly request it.

## What it reads

- Candidate lists from Step 2 (to validate that each pasted country was expected)

## Rules

Every rule below applies to every message received in this step:

| Situation | Claude's response |
|---|---|
| Valid, complete data for one country | `Received: N` (running count only, no names) |
| Message contains multiple countries | Stops and explains — nothing stored |
| Message contains no recognizable country | Stops and explains — nothing stored |
| Required field or section missing | States exactly what is missing — nothing stored |
| Country not on either Step 2 candidate list | Asks whether to store or reject — waits for answer |
| Country already stored | Asks whether to overwrite or keep original — waits for answer |

Claude preserves all values, wording, and formatting exactly as provided. It does not correct, improve, or reinterpret the data.

## Progress check

Type `list countries` at any point and Claude replies with the country names stored so far and which track(s) each covers. No other data is shown.

## What Claude does not do in this step

- No analysis, scoring, or ranking
- No summaries or tables
- No opinions or recommendations
- No additional actions unless explicitly instructed

## Moving to Step 5

Tell Claude you are done pasting data and want to proceed to scoring.
