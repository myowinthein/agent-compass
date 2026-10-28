---
name: Shared Helper Runtime
description: Execution, shared formatting contract and explicit fallback for the local Python helpers in both hosts.
---

# Shared helper runtime

Read bundled `data/output-contracts.json` as data when a step needs presentation tokens or mechanical bounds. It is the single source for those literals, including during an approved manual run. Semantic decisions remain in the step prompts. Do not copy the contract into an adapter or create another constants file.

Check an available Python 3.11+ interpreter in the current environment. The desktop, terminal and specialist may differ. `python3` is an example; use an available `python` or `py -3` on Windows if appropriate. Never install Python/tzdata, change permissions or switch models automatically.

Invoke the resolved installed `helpers/compass.py` path with `-I -B` and one subcommand. Send JSON through stdin, not shell-interpolated candidate text. Every request includes `schema_version: 1`; other fields are defined in the relevant reference. Success returns `{schema_version, input, result}`. Check echoed inputs against the original sources. Do not save the transient JSON in the workspace or installation.

Keep helper payloads/results in memory or pipes; do not create named JSON scratch files elsewhere in the filesystem either. The run metadata under skills/run-workspaces.md, Markdown deliverables and checkpoint files are durable workflow records.

```text
python3 -I -B "<plugin-root>/helpers/compass.py" <subcommand>
```

Read only the applicable interface:

- Chat/person run selection: `skills/run-workspaces.md`; `run-list` is read-only, while parent-only `run-start` creates an isolated run and optional confirmed profile copies.
- Current/legacy artifact paths: `skills/workspace-files.md`; `resolve-files` takes `{workspace, workflow}` and writes nothing.
- Research scope, blocks and storage: `skills/research-helper.md`; read-only `research-scope` can extract a saved country list without requiring completed research.
- Exact salary/range/FX or dated timezone arithmetic: `skills/comparison-helper.md`.
- Country Finder/Salaries rendering and saved-output checks: `skills/output-helper.md`.
- Existing per-country salary arithmetic: `skills/salary-calculation-helper.md`.

`ingest` writes only existing research/report and stored-data files; `run-start` creates only new run metadata and optional profile copies. The parent invokes both. Other operations are read-only; the parent normally runs them too. A specialist with execution may use a read-only operation, except Salary Calculator's numeric preparation still belongs to the parent. A specialist without execution returns the exact pending helper request to the parent, never guesses, asks the user or saves a partial final deliverable. Continue the approved assignment under the shared runtime's pending-request rule.

Failure handling:

- Exit 2 `invalid_input`: correct the malformed/contradictory input from its source or ask for missing facts. Never bypass it with manual arithmetic.
- Exit 3 `runtime_unavailable`, absent execution or a failed runtime: explain the limitation and ask whether to fix execution or proceed manually under the existing prompts and this same readable contract. Wait for the choice. Reuse an explicitly run-scoped choice instead of asking for each helper/JD; record its scope in the existing notes/audit. State honestly which automated checks did not run.
- Exit 4 `needs_clarification`: resolve ambiguous boundaries, fields or local times with the parent; no guessing.
- Exit 5 `conflict`: preserve files, inspect the changed data and rescan before an explicitly justified retry.
- Exit 6 `io_error`: report the actual failure, including any `written_paths`. State remains unchanged. Per-file atomic replacement is not a two-file transaction; inspect a partial ingestion and retry with fresh verified hashes, never blindly repeat a write.
- Exit 7 `internal_error`: stop and report a helper defect. It is not a data correction or permission to bypass checks.
- Missing bundled code or contract is a broken installation: report its resolved path and stop for repair. A CLI usage error is not a successful helper run.

Local tool-permission prompts remain the host's decision; one run-scoped fallback choice cannot grant extra filesystem access. No helper validates the truth of research, human approval, legal eligibility or that a saved output belongs to a changed profile.

For an unfinished Country Finder or Salary Calculator resume, and after a stage output is saved but before the parent advances state, use `state-check` with `{workspace, workflow}` in the selected run. It resolves current/legacy filenames and checks the existing two-field checkpoint without writing. Its `files`, `naming` and `existing_outputs` fields expose resolved paths and orphan outputs even when state is missing. At a just-finished stage it reports the old checkpoint; the parent must still inspect the new output and obtain required confirmations before updating it. After the user chooses View previous results, completed runs replay saved finals without migration. If state-check is unavailable, use the explicitly approved manual checks; it never becomes permission to skip a checkpoint.
