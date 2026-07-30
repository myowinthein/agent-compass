---
name: Data Validation Rules
description: Governs data ingestion behavior across Country Finder and Salary Calculator — duplicate detection, missing-field detection, and rejection handling whenever real research data is being stored.
---

# Data Validation Rules

Whenever ingesting or storing data provided by the user, apply these rules:

- Each block is expected to contain data for exactly one item (one country, one dataset). If it contains multiple items or nothing recognizable, stop and explain the issue rather than guessing which part to use.
- If required fields or sections are missing from what was provided, state exactly what is missing. Do not store incomplete data as if it were complete.
- If an item was already stored earlier, keep the original, skip the duplicate, and note it in a warning at the end of processing. Never silently overwrite the original. (A calling step may instead require stopping to ask before overwriting — follow the calling step's rule when it specifies one.)
- Preserve values and formatting exactly as provided. Do not correct, improve, or reinterpret the data.
- Do not analyze, summarize, or score data during ingestion — that happens in a later, separate step.
