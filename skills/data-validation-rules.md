---
name: Data Validation Rules
description: Governs data validation behavior across Country Finder and Salary Calculator — duplicate detection, missing-field detection, and rejection handling whenever real research data is being stored.
---

# Data Validation Rules

Use `skills/research-helper.md` for parent-run `research-scan` and `ingest`. Python checks boundaries/coverage and copies approved raw slices; it does not verify findings. Approved manual processing follows the same rules without claiming automation ran.

## Country-block boundaries

Generated blocks start with `Country: [name]` at the beginning of a line outside quotes or code fences. They end before the next such field, a top-level `## Validation report`, or end of file. Blank lines and horizontal rules do not define boundaries. A leading `## Research scope` is metadata, not a dataset.

Successive top-level Country fields define separate blocks. Honor explicitly supplied fences or other clear dataset delimiters; a single explicitly bounded block containing multiple datasets is malformed. Accept unambiguous legacy boundaries without rewriting content. The parent clarifies ambiguity rather than guessing. Country mentions in evidence, quotations or source titles do not start blocks.

During collection, append findings before any existing Validation report. Preserve original country content verbatim; framing and generated audit metadata are not research.

## Validation report

Save one consolidated `## Validation report` at the end of the original aggregate file. Preserve research and stored datasets; reruns update only the existing generated report. Record:

- Stored countries.
- Every rejected block's country, or index if unrecognizable, and exact reason.
- Duplicates whose original was retained.
- Expected countries not supplied.

A rejected duplicate is not missing data when its original survives. Use the calling step's existing files without new profile, state or dataset fields. Readers exclude the report from country data; downstream audits use its skip reasons.

For legacy files without a report, inspect available blocks and saved outputs. Distinguish an unknown ingestion outcome from never-researched data; do not invent a reason.

## Validation behavior

- Require one recognizable item per block. Reject explicitly bounded multi-dataset or unrecognizable blocks with reasons, following the calling step's batch skip/report policy. Ambiguous boundaries need clarification.
- Identify exact missing required fields or sections; never store incomplete data as complete.
- Check canonical fields within their own track/tier, outside quoted or fenced examples. Other sections and trailing Notes cannot supply missing Sources. Legacy wording needs semantic review, not automatic rejection or rewritten research.
- Retain stored originals, skip duplicates and report them at the end. Follow any stronger calling-step requirement to ask before overwrite; never silently replace an original.
- Preserve values and formatting exactly. Do not correct, improve, reinterpret, analyze, summarize or score during ingestion; analysis belongs to a later step.
