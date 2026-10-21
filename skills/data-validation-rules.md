---
name: Data Validation Rules
description: Governs data validation behavior across Country Finder and Salary Calculator — duplicate detection, missing-field detection, and rejection handling whenever real research data is being stored.
---

# Data Validation Rules

Use `skills/research-helper.md` for the parent's `research-scan` and `ingest` operations. The existing policies below still govern semantic review; Python checks boundaries/coverage and copies approved raw slices, not the truth of findings. Under an explicitly approved manual run, apply these same policies without claiming automated ingestion ran.

## Country-block boundaries

Generated research keeps the existing `Country: [name]` field as its delimiter: put it at the start of a line, outside quotes or code fences. A block ends immediately before the next such `Country:` line, before a top-level `## Validation report` section, or at end of file. Blank lines and horizontal rules alone are not country boundaries. Ignore an optional `## Research scope` preface before the first country; it is metadata, not a dataset.

Two successive top-level Country fields mean two blocks, not a malformed multi-country block. If the user explicitly supplies individually fenced or otherwise clearly delimited datasets, honor those boundaries instead; an explicitly bounded block containing multiple country datasets is malformed. Accept unambiguous legacy boundaries without rewriting the supplied content. If boundaries are genuinely ambiguous, the parent asks for clarification rather than inventing separators or guessing. Country mentions in evidence, quotations, and source titles do not create new datasets.

The parent uses these same boundaries when collecting research. Append new country results before any existing Validation report, never after it. Preserve original country content verbatim; framing and generated audit metadata are not research findings.

## Validation report

After ingestion, save the consolidated validation report under `## Validation report` at the end of the original aggregate research file, separate from the country blocks. Preserve the raw research text and stored datasets unchanged; update only a previously generated report when rerunning validation. Record stored countries, every rejected block's country (or block index if unrecognizable), the exact reason, duplicates whose original was retained, and expected countries not supplied. Do not treat a rejected duplicate as a country with no valid data when its original was stored.

The calling step identifies the existing research/output files; no new profile, state, or dataset fields are required. Readers ignore the report as country data, but downstream audits use its skip reasons. On legacy runs without a report, distinguish an unknown ingestion outcome from "never researched"; use the available research blocks and saved outputs to establish what happened rather than inventing a reason.

## Validation behavior

Whenever ingesting or storing data provided by the user, apply these rules:

- Each block is expected to contain data for exactly one item (one country, one dataset). If an identifiable block contains multiple datasets or nothing recognizable, reject it with the reason rather than guessing which part to use. Follow the calling step's skip-and-report policy for batch ingestion; genuinely ambiguous boundaries require parent-side clarification.
- If required fields or sections are missing from what was provided, state exactly what is missing. Do not store incomplete data as if it were complete.
- If an item was already stored earlier, keep the original, skip the duplicate, and note it in a warning at the end of processing. Never silently overwrite the original. (A calling step may instead require stopping to ask before overwriting — follow the calling step's rule when it specifies one.)
- Preserve values and formatting exactly as provided. Do not correct, improve, or reinterpret the data.
- Do not analyze, summarize, or score data during ingestion — that happens in a later, separate step.
