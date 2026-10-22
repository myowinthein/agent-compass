---
name: Research Helper
description: Shared batching, country-block scanning and byte-preserving ingestion interface.
---

# Research helper

Apply `skills/helper-runtime.md` first. All requests below also include `schema_version: 1`.

## Read a saved country list

Run `research-scope` with `{workspace, workflow: "salary-calculator"}` for Country Finder's optional names-only handoff. It resolves current/legacy research filenames through the shared registry and reads only the leading `## Research scope` as country labels. The result contains `status` (`available`, `missing_file`, `missing_scope` or `empty`), `source`, `naming`, `countries`, `human_confirmation_checked: false` and a `source_hash` when a file exists. It does not read checkpoint contents, infer completion or approve reuse.

Fresh scopes use one country per bullet line. The reader also accepts older plain country lines/comma-separated lists, UTF-8 BOM and CRLF; it removes repeated flag/case variants while preserving first-seen labels and order. Optional `aliases` uses the same explicitly confirmed mapping as batching. It stops at the next research block, fence or section, never taking countries from salary results or a generated report. Review labels semantically as country names before offering them; structural parsing cannot establish their truth or interpret an ambiguous comma in a legacy name. Ambiguous metadata needs clarification, not silent repair or a truncated suggestion.

The parent still prioritizes an explicit Include list, waits for a keep/edit/replace/default choice, applies exclusions and records an accepted choice in Country Finder's existing criteria. Missing/unrecoverable scope falls back to asking for countries or the default list, not extracting a partial list from the final salary table. Declining the optional source never blocks standalone Country Finder. A recorded list can be used before salary research finishes because no salary findings or eligibility conclusions transfer. On resume, preserve the already confirmed Country Finder scope.

This operation writes nothing and requires no new consumer file. Under explicitly approved manual fallback, inspect the same resolved research preface, preserve every selected country and apply the same confirmation and missing/ambiguous-source rules. Never invent completion or rename a legacy file to make it readable.

## Batching

Run `batch-partition` with `groups: [{region, countries: [name, ...]}, ...]` after the user confirms the scope. For an ungrouped list, use one numbered region label. Optional `aliases` maps explicitly confirmed spellings directly to canonical names. Regions and country order are preserved, with contiguous chunks bounded by the contract's `batch_maximum`; do not balance or drop countries. Use returned `expected` for coverage and embed each returned batch's literal countries in its research brief. No prompt generation or research happens in Python.

## Scan and review

Resolve current/legacy paths under skills/workspace-files.md first. Scanning and ingestion use the same registry and preserve the run's existing names; they never create current-name copies of legacy datasets.

Run `research-scan` with:

```json
{"schema_version":1,"workspace":"<absolute consumer directory>","workflow":"salary-calculator","expected":["Germany"]}
```

`workflow` is `country-finder` or `salary-calculator`. Expected is the confirmed scope, or `null` only when legacy coverage genuinely cannot be established. Country Finder research requires explicit `required_tracks: {"Germany": ["remote", "sponsorship"]}` from Step 2's eligible tracks, or an empty object when none are eligible. Omitting that field is an input error, not permission to reject every country. Supply only eligible countries there. Optional `aliases` uses the same mapping as batching. For the earlier Country Finder discovery collection, add `stage: "discovery"`; it scans `country-finder-02-candidates.md` read-only instead of the later country research, without requiring tracks.

The normal scan reads the workflow's existing aggregate research and stored-data files, returning `source_hash`, `stored_hash` (null if absent), block indices/line numbers/hashes, structural issues, missing canonical labels, duplicates and missing coverage. It follows `skills/data-validation-rules.md`. A standalone manual dataset fence may use `research`, `text`, `markdown`, `md` or no language; quotes and ordinary inner code examples are not new countries. An explicit `research` fence denotes a separate dataset. Ambiguous mixed/legacy boundaries need clarification.

Generated reports have bounded ownership/hash comments inside their existing section. A legacy/edited report or research appended after it requires clarification before any replacement; no tail is discarded. Keep findings before that section. An explicit fence with substantive pre-Country content also needs clarification rather than silently dropping that text.

For legacy reports, the parent shows the affected region and asks what is generated metadata versus substantive findings. Only after explicit user confirmation may it reframe/remove the old generated metadata with normal file tools, preserving findings and prior rejection reasons in the existing aggregate file, then rescan with fresh hashes. Alternatively the user may choose manual ingestion of the now-clarified format under the same validation rules, disclosed as not helper-generated. Never infer consent from the helper error, bypass invalid data checks or silently delete a report. Completed runs need no such conversion.

Check every block against the step's required fields. Missing labels can be a formatting variation, not proof that the data is absent: inspect the raw block. Reject genuinely incomplete data with its exact reason. Only after confirming all required content exists under an unambiguous legacy label may you set `reviewed_fields: true`. This is the model's semantic review, not independent verification of source claims. An unrecognized country cannot be made valid merely by accepting its block.

Field checks are scoped to each CF track or SC tier, outside quoted/fenced examples; SC's trailing threshold, evidence grade and Notes do not supply tier Sources. A newly flagged legacy layout uses the same semantic-review path, not automatic rejection. A country-only Research scope may contain `none` for an empty eligible set; do not add candidate context or origin prose to that block-free preface. Supply context in the brief for the researcher's Notes, or save it later in parent-authored criteria/shown work/audit prose under the shared runtime. Never edit collected Notes or append parent context to raw research.

## Store

Only the parent runs `ingest`. Reuse the scan request plus its exact `source_hash` and `stored_hash`, and `decisions: [{index: 0, accept: true}, {index: 1, accept: false, reason: "missing Premium sources"}]`, one per block. `reviewed_fields` is an optional boolean on a decision. Discovery scanning cannot ingest. The helper refuses structurally malformed or ineligible Country Finder blocks even if accepted, keeps existing valid originals and reports duplicates. Do not add an out-of-scope salary rejection that the salary step does not require.

Accepted raw slices are copied without retyping or reformatting. The helper writes only the existing stored-data file and the generated Validation report in its aggregate research file. It does not verify facts, calculate, rank or advance state. Optional sponsorship/evidence fields remain optional; explain missing informational evidence in the audit rather than changing raw research.

Read back both named files. Reconcile `stored`, `rejected`, `expected_not_stored` and the returned report with the current scope. Present the calling step's consolidated report from this inventory, including a reason for each skip. A duplicate whose original survived is not a missing country. On a rerun, exact originals already present are retained without duplication. If a partial write failed, inspect which half was saved, rescan and retry only after checking that the stored originals remain intact.

The helper already persists the report. Do not append a second consolidated review, edit its generated body or add prose after the closing marker to satisfy older generic persistence instructions. Any additional chat formatting stays in chat. Preserve substantive audit interpretation for its later step.

Hash guards are optimistic checks, not multi-writer locking. Do not ingest concurrently with another writer. Existing file modes are preserved; new files are private by default. Temporary staging files are cleaned after handled failures; a process crash can leave a staging file, which must not be treated as a workflow record or deleted without identifying it.

Collection still belongs to the parent: append researcher results before any existing report, then scan for coverage. Never run ingestion or a later checkpoint while a research result/question is still pending.
