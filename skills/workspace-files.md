---
name: Workspace Files
description: Resolve current and legacy workflow filenames without renaming or duplicating saved results.
---

# Workspace files

Read bundled `data/workspace-files.json` as data. It is the single registry of current/legacy artifact names and checkpoint membership. Shared `profile.md` and `situational-profile.md` are unchanged. Portal Finder and Job Screener have no automatic result exports or checkpoints; do not add them for naming consistency.

Before accessing Country Finder or Salary Calculator artifacts, apply `skills/helper-runtime.md` and run the read-only `resolve-files` operation:

```json
{"schema_version":1,"workspace":"<absolute consumer directory>","workflow":"country-finder"}
```

Use `salary-calculator` for that workflow. Resolve a producer separately before an optional cross-workflow read; one workflow's naming never controls the other. This lookup establishes paths, not completion, profile compatibility or permission to overwrite anything.

The result contains `files` keyed by artifact (`research`, `validated-data`, `final-results`, etc., plus `state`), `existing_outputs`, and `naming` (`current`, `legacy` or `mixed`). Prefix each returned filename with the selected workspace path. Recheck resolution before writes and after a resume; if paths changed since a handoff, stop and reconcile before saving. Pass specialists the resolved absolute input/output paths and this rule, not just canonical names. Completion messages name the actual saved file.

## Resolution policy

1. Check both registered spellings for every artifact of the requested workflow, including Salary Calculator's career ladder. Reject symlinks, non-files and paths outside the workspace; do not read their contents.
2. If both spellings exist for the same artifact, stop for clarification even if their bytes match. Never guess which is authoritative, merge them, delete one or keep writing. An explicitly user-managed resolution must leave a single chosen spelling before resuming.
3. Keep whichever spelling already exists for each artifact. If any legacy artifact exists in this workflow, use legacy names for its missing artifacts too. Otherwise use current names. A nonduplicate mixed workspace is supported: keep each existing name and use legacy names for missing artifacts.
4. Never rename, copy, migrate, create aliases for or duplicate saved outputs merely to adopt the new format. Do not reset state. Existing finals replay as saved. Missing checkpoints with either filename family still require the runtime's recovery/import choice before creating state or writing outputs.

Canonical filenames mentioned in workflows, step prompts and docs are logical artifact references, not instructions to create a second file in an existing run. Replace every such read, existence check and write with its resolved path. Keep original research, prior step outputs and their contents intact under the existing preservation rules. After an approved rewind, retain the resolved naming of the run; do not delete outputs to force a naming switch.

## Without execution

If the helper is unavailable, use the existing explicit manual-fallback choice under `skills/helper-runtime.md`, then apply the same four rules by inspecting file metadata and reading the bundled registry. Do not invent a second mapping or silently default to current names. Missing/unreadable registry data is a broken installation, not a manual-fallback case.

No filename-resolution JSON is saved. The packaged registry is plugin configuration, not a consumer sidecar.
