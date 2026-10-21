---
title: "Step 2: Data validation"
parent: salary-calculator
grand_parent: Commands
nav_order: 2
---

# Step 2: Data validation

Checks the research structure and stores accepted salary data unchanged. It does not verify market claims or calculate targets.

## Flow

```mermaid
flowchart TD
  Start(["Read sc-step1-salary-research.md"]) --> Bounds{"Country boundaries clear?"}
  Bounds -->|No| Ask["Ask for clarification<br/>Wait before storing"]
  Ask --> Bounds
  Bounds -->|Yes| Review["Review each country<br/>Both employer tiers and their sources"]
  Review --> Accept{"Complete and not already stored?"}
  Accept -->|Yes| Store["Copy accepted data verbatim"]
  Accept -->|No| Skip["Record the reason<br/>Keep originals for duplicates"]
  Store --> Save["Save stored data and Validation report<br/>Account for missing expected countries"]
  Skip --> Save
  Save --> Usable{"Any country stored?"}
  Usable -->|Yes| Next(["Show consolidated counts and reasons<br/>Continue to Step 3"])
  Usable -->|No| Repair(["Keep the report and checkpoint<br/>Offer missing-evidence repair or stop"])
```

## Required data

Each country needs both the Mainstream and Premium tiers, with salary figures and sources for each. A source in another tier or a quoted example cannot fill a missing field.

A missing sponsorship threshold does not reject a country. Neither does a missing evidence grade; it is recorded as "not provided".

Malformed or incomplete blocks are skipped with exact reasons. Duplicates keep the first stored original. Clear older field wording can be accepted after review without rewriting the research.

## Country boundaries

Generated blocks start at a top-level `Country:` field. Blank lines alone do not separate datasets. Genuinely ambiguous boundaries require clarification, not guessed parsing.

The shared helper copies accepted blocks byte-for-byte and checks coverage. If saving fails, the checkpoint does not advance; any partial write is inspected before retrying.

## What happens next

- `sc-step2-salary-data.md` contains accepted data.
- `sc-step1-salary-research.md` retains the original research and a separate Validation report.

The report carries missing-country and rejection reasons into later summaries. A duplicate whose original was kept is not a failed country.

If at least one country was stored, continue to [Step 3: International adjustment](step3-international-adjustment.html). Otherwise, the assistant offers evidence repair or stop before another specialist or career-ladder question.
