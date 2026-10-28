---
title: "Step 4: Data validation"
parent: country-finder
grand_parent: Commands
nav_order: 4
---

# Step 4: Data validation

Store structurally complete research unchanged. This checks required content, not the truth of claims.

## Flow

```mermaid
flowchart TD
  Start(["Read Step 3 research and eligible tracks"]) --> Bounds{"Country blocks clear?"}
  Bounds -->|No| Ask["Ask for clarification<br/>Wait before storing"]
  Ask --> Bounds
  Bounds -->|Yes| Check["Review each block<br/>One recognisable country<br/>Required track fields present<br/>Eligible under Step 2"]
  Check --> Valid{"Valid and not already stored?"}
  Valid -->|No| Skip["Record the skip reason<br/>Keep the original for duplicates"]
  Valid -->|Yes| Store["Copy accepted data verbatim"]
  Skip --> Report["Save stored data and one validation report<br/>Account for missing expected countries"]
  Store --> Report
  Report --> Saved{"Files saved successfully?"}
  Saved -->|No| Failure(["Report failure<br/>Inspect before retrying; do not advance"])
  Saved -->|Yes| Next(["Show consolidated counts and reasons<br/>Continue to Step 5"])
```

## What is accepted

Each country needs the fields for its Step 2 eligible tracks. Malformed, incomplete, duplicate and unlisted data is skipped with reasons; duplicates preserve stored originals. Older labels are accepted after review when their meaning is clear.

Generated blocks use top-level `Country:` delimiters. Ambiguous boundaries need clarification.

## What you see

One report accounts for stored countries, rejected blocks and missing results. Retained duplicates are not missing countries. Helpers preserve accepted bytes; manual processing needs explicit approval when execution is unavailable.

## What happens next

- `country-finder-04-validated-data.md`: accepted data.
- `country-finder-03-research.md`: original findings and separate Validation report.

Empty eligible scope can still proceed to an audit of exclusions/gaps. Failed saves leave progress pending. After successful saving, continue to [Scoring](step5-scoring.html).
