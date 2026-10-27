---
name: Output Helper
description: Shared final Country Finder and Salary Calculator rendering and saved-section checks, without semantic Markdown parsing.
---

# Output helper

Apply `skills/helper-runtime.md` and read `data/output-contracts.json` as data. Every request includes `schema_version: 1`. All decisions/facts come from the model's source review; the helper does not read semantic profile/audit prose or decide evidence quality.

## Salary

Run `render-salary` with `rows: [{country, calculation, visa}, ...]` and optional `priority_order: [countryName, ...]` transcribed from Country Finder's Priority Table. Each display country contains one researched flag and its name; flag position is normalized. `calculation` is the existing complete schema-version-1 input in `skills/salary-calculation-helper.md`, not a fabricated helper result. The renderer reuses that same salary calculation and returns exact `calculations`, `markdown`, `table_markdown`, `notes` and `calculated`.

Both renderers optionally accept `aliases`, the same explicit direct alias mapping used for research matching. Never fuzzy-merge countries. Numeric visa display requires an exact terminating amount; if official precision for a recurring legal amount cannot be established, preserve the uncertainty rather than inventing rounded legal pay.

`visa` contains `state` from the contract's underlying visa states. For its numeric state also supply `{amount, period, currency, pay_basis}`: exact amount, annual/monthly, same target currency and confirmed gross_base components. First establish comparability under skills/sponsorship-threshold-rules.md; a monthly rule needs a verified official/pay-schedule basis compatible with annual/12. Otherwise use Unknown without numeric fields or a numeric calculation comparison, and retain the known threshold and limitation in shown work. Raw targets determine the warning only after that semantic check. For other nonnumeric states also omit numeric fields and comparisons. A Blocked state requires `reason`; retain its reference-only returned note in Summary. Underlying eligibility and any other wage conditions stay in the audit, not the compact cell. Country order follows the supplied priority order, with extra calculated countries appended alphabetically.

Save `markdown` verbatim where the step requests the caption/table, surrounded only by that step's existing shown work and Summary. Preserve `calculations` as readable exact shown work, not a JSON sidecar. Follow `skills/salary-comparison-rules.md` separately for candidate-minimum FX/ranges; recurring normalized comparisons use `compare`, not truncated input to the older salary CLI.

## Country Finder

Run `render-cf` after the audit with:

- `expected`: the full Step 2 candidate universe, not additional expected-but-absent audit suggestions.
- `early_exclusions`: `{countryName: {remote: "exact earlier reason", sponsorship: "exact earlier reason"}}`; include only actual excluded tracks, or an empty object. Read these from Step 2, do not infer them from missing research.
- `decisions`: one object per expected country, in the model's evidence-led within-priority order: `{country, remote, sponsorship, priority, limitation, ingestion}`. Use the contract's Summary fit labels, not the table-only missing display. For an excluded/missing track include `remote_reason` or `sponsorship_reason`; preserve each early reason exactly. `ingestion` is stored/not_supplied/rejected/unknown; wholly missing countries also need `ingestion_reason`.

Scoring either track requires stored research, even when the other track is excluded. Correct a contradictory request before saving or completing the step.

The helper returns `summary_markdown`, `table_markdown`, combined `markdown`, `counts` and `audit_notes`. Preserve the separate notes for wholly unresearched/rejected research. Put `audit_notes` with the three file-only audit checks, then copy the complete `markdown` verbatim as contiguous Summary and Priority Table sections, followed by the existing Effort Allocation. It counts each candidate once per track and rejects contradictions; the model still chooses fits/priorities and within-bucket order. It sorts priority buckets stably and Pending evidence alphabetically ignoring flags. Show only `table_markdown` in chat, then the step's completion message.

## Verify the saved file

Apply skills/workspace-files.md first. `check-saved` accepts either registered spelling of an allowed artifact and checks its resolved existing file, not a second copy. Duplicate aliases stop with a conflict even when their contents match.

After saving a newly rendered result, run `check-saved` with `{workspace, file, kind, render_input}`. File is the existing Step 4 or final salary file for kind salary, or the final Country Finder file for kind country. `render_input` is the exact renderer request without its outer schema_version. The helper regenerates only its own canonical sections and compares against the actual saved text, including row coverage. It writes nothing and does not verify audit truth. Correct a save/rendering mismatch before the parent advances state; do not rewrite raw research or pre-audit files to make a check pass.

Saved-table checks ignore only CRLF versus LF and an absent final newline; cell contents, columns and row coverage must still match. Research ingestion remains byte-preserving and does not use this line-ending normalization.

Existing completed results are replayed as saved. For an unfinished legacy run the model reads old Summary/audit prose and supplies typed decisions or recovered raw inputs; ambiguous legacy facts require clarification. There is no legacy Markdown migration engine. Under approved manual fallback, read the same contract, follow the step's checks and disclose that rendering/saved-output automation did not run.
