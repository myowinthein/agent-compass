---
name: Output Helper
description: Shared final Country Finder and Salary Calculator rendering and saved-section checks, without semantic Markdown parsing.
---

# Output helper

Apply `skills/helper-runtime.md` and read `data/output-contracts.json` as data. Every request includes `schema_version: 1`. All decisions/facts come from the model's source review; the helper does not read semantic profile/audit prose or decide evidence quality.

For both renderers, each display `country` in `rows` or `decisions` must contain exactly one researched country flag and its full name, such as `🇩🇪 Germany`; flag position is normalized. Matching names in `expected`, `orders` and `priority_order` may omit flags.

## Salary

Run `render-salary` once for the complete eligible `rows: [{country, calculation, visa}, ...]`, with optional `priority_order: [countryName, ...]` transcribed from Country Finder's Relocation priorities table for new results, or its legacy combined Priority Table. `calculation` is the complete schema-version-1 input in skills/salary-calculation-helper.md, not a fabricated result. This one call performs the arithmetic and returns exact `calculations`, `markdown`, `table_markdown`, `notes` and `calculated`; no separate per-country CLI calls are required first. `check-saved` remains a fresh required check of the actual saved file.

Both renderers optionally accept `aliases`, the same explicit direct alias mapping used for research matching. Never fuzzy-merge countries. Numeric visa display requires an exact terminating amount; if official precision for a recurring legal amount cannot be established, preserve the uncertainty rather than inventing rounded legal pay.

`visa` contains `state` from the contract's underlying visa states. For its numeric state also supply `{amount, period, currency, pay_basis}`: exact amount, annual/monthly, same target currency and confirmed gross_base components. First establish comparability under skills/sponsorship-threshold-rules.md; a monthly rule needs a verified official/pay-schedule basis compatible with annual/12. Otherwise use Unknown without numeric fields or a numeric calculation comparison, and retain the known threshold and limitation in shown work. Raw targets determine the warning only after that semantic check. For other nonnumeric states also omit numeric fields and comparisons. A Blocked state requires `reason`; retain its reference-only returned note in Summary. Underlying eligibility and any other wage conditions stay in the audit, not the compact cell. Country order follows the supplied priority order, with extra calculated countries appended alphabetically.

Save `markdown` verbatim where the step requests the caption/table, surrounded by that step's shown work, Summary and any required benchmark-reference notice. Keep that notice outside the canonical caption/table; do not alter the returned Markdown. Preserve `calculations` as readable exact shown work, not a JSON sidecar. Follow `skills/salary-comparison-rules.md` separately for candidate-minimum FX/ranges; recurring normalized comparisons use `compare`, not truncated input to the older salary CLI.

## Country Finder

New Country Finder results call `render-cf` with `format: "tracks"` and:

- `expected`: the complete Step 2 candidate universe; `early_exclusions` and optional direct `aliases` retain their existing meanings. Each early exclusion maps a country to remote/sponsorship exact reasons; never infer it from absent research.
- `orders: {remote: [countryName, ...], sponsorship: [countryName, ...]}`: each contains every expected country exactly once, in the model's independently chosen evidence-led order. The helper sorts priority buckets stably and Pending evidence alphabetically, preserving the supplied order within other buckets.
- `decisions`: one object per country with `{country, remote, sponsorship, ingestion, tracks}`. Fits use the contract's Summary labels. Missing/excluded fits require `remote_reason` / `sponsorship_reason`; `ingestion` remains stored/not_supplied/rejected/unknown and wholly missing countries need `ingestion_reason`. Scored tracks require stored applicable research even when the other track is excluded.
- `tracks` contains both `remote` and `sponsorship`, each `{priority, confidence, access, pay, limitation, next_action}`. Read their exact vocabularies from `data/output-contracts.json`. Apply skills/country-assessment-rules.md to select states. The helper rejects contradictions; it does not decide market potential, verify evidence or infer feasibility from a visa route.

The helper returns `summary_markdown`, `table_markdown` (headed Remote priorities and Relocation priorities), contiguous combined `markdown`, `counts` and `audit_notes`. Keep audit notes with the three checks and save `markdown` verbatim as Summary and Priority Table sections, followed by Effort Allocation. Show only both headed tables in chat and the completion message. Missing fits display as Unknown; the Summary and counts retain their original schema.

Without `format: "tracks"`, the existing combined renderer remains available for pinned unfinished/legacy verification: decisions instead use the original `priority` and `limitation`, without tracks/orders. Its five-column output and decision boundaries are unchanged. Do not use this compatibility path to avoid the new workflow, rewrite completed results or mix formats within a report. Completed results replay as saved without a new render.

## Verify the saved file

Apply skills/workspace-files.md first. `check-saved` accepts either registered spelling of an allowed artifact and checks its resolved existing file, not a second copy. Duplicate aliases stop with a conflict even when their contents match.

After saving a newly rendered result, run `check-saved` with `{workspace, file, kind, render_input}`. File is the existing Step 4 or final salary file for kind salary, or the final Country Finder file for kind country. `render_input` is the exact renderer request without its outer schema_version. The helper regenerates only its own canonical sections and compares against the actual saved text, including row coverage. It writes nothing and does not verify audit truth. Correct a save/rendering mismatch before the parent advances state; do not rewrite raw research or pre-audit files to make a check pass.

Saved-table checks ignore only CRLF versus LF and an absent final newline; cell contents, columns and row coverage must still match. Research ingestion remains byte-preserving and does not use this line-ending normalization.

After run selection and the user's View previous results choice, completed results are replayed as saved. For an unfinished legacy run the model reads old Summary/audit prose and supplies typed decisions or recovered raw inputs; ambiguous legacy facts require clarification. There is no legacy Markdown migration engine. Under approved manual fallback, read the same contract, follow the step's checks and disclose that rendering/saved-output automation did not run.
