---
name: Run Workspaces
description: Select isolated Country Finder, Salary Calculator and Job Screener runs by chat, person and command before reading profiles or checkpoints.
---

# Run workspaces

Apply this before CF/SC/JS profile intake, artifact resolution or completed replay. Resolve the fixed **base workspace** under the shared runtime's File locations rule: `Path.home() / "Agent Compass"`. There is no custom base-folder option or folder question. Every new search or screening session gets its own **run workspace** beneath it; all existing artifact/profile names and checkpoint schemas stay unchanged inside that directory. Never interpret a new chat as a request to resume whatever is in the base folder.

## Bind the chat and person

Retain an already selected chat key throughout this chat; do not switch keys when a native ID becomes available later. Otherwise use a trusted current conversation/session identifier exposed by the host, prefixed with its host name. In Codex, `CODEX_THREAD_ID`, when exposed to the parent, can provide it; do not launch another model or inspect private client transcripts to obtain one. In Claude, the entry skill's actually substituted session hint supplies `claude:<session-id>` when available. An unresolved substitution, workspace path, person name or previous chat's ID is not a chat identifier.

If no reliable host identifier is available, first check this conversation for earlier Compass activity. If activity or a compaction summary indicates an earlier run but its association is missing, ask for the saved run path or an explicit Start fresh choice before generating another key. Never silently treat lost context as a new chat or search other chats to guess.

When a fallback key is needed for a genuinely new chat, or after that Start fresh choice, use the available Python interpreter to execute `import uuid; print("local:" + str(uuid.uuid4()))` with `-I -B -c`. Retain the exact tool output; never invent, reuse an example or manually compose the UUID. If execution is unavailable, use the helper-runtime repair/manual choice; approved manual handling still requires a host/tool-generated unique identifier. Show `Chat key: <key>` and the selected run path in the chat, and retain the key, base workspace, person IDs and active run paths in continuation summaries. Reuse them for later invocations in this chat, not across new chats. Disclose that automatic rediscovery requires this association. Never change native client settings.

Before profile intake, identify the requested person from the invocation or its directly associated request. An established single-person identity can supply the person only when the multiple-person rule below does not apply. If neither establishes the person, ask for a short person label; a full extracted profile is not needed to start. Reuse that person's returned `person_id` and exact stored `person_label`; a different person gets a new ID. If the ID is missing from context, use the unfiltered chat listing below to recover candidates and ask only if their identity remains unresolved, including two people with the same name. A label alone never proves that an old profile belongs to a new candidate. Do not read root-level or another person's profiles as automatic intake.

## Select the search

Apply `skills/helper-runtime.md`. At the start of each CF/SC/JS invocation and before any `run-start`, the parent calls `run-list` with the base `workspace` and `chat_id`, initially without person or workflow filters so existing identities and all three commands are visible. Bind the requested person from that listing and retained context before narrowing by `person_id`/`workflow`. Do not omit a known person's ID to bypass an existing run choice. This reads only the selected chat's run metadata and checks matching active runs; it writes nothing. No matching person/command means a fresh run, without a resume question.

On every CF, SC or JS invocation, inspect this unfiltered listing before selecting a person, even when a person ID is retained. Count each distinct person once across commands, and include established candidate identities in this chat. If more than one person is known and the invocation or its directly associated request does not unambiguously identify one, ask **Who is this for?** Show each known person once, with an option to identify another person, and wait for the answer before reading/copying profiles, selecting producer data or offering that person's run choices. Do not default to the most recent person, command, active run or previously selected profile. Distinguish identical labels with minimal run/date context; an ambiguous explicit name still needs clarification. An unambiguous explicit person choice needs no extra picker. Keep the answer for this invocation and its normal continuations; ordinary JS JD/application pastes and answers to pending run questions do not trigger another person picker. Portal Finder is outside this rule because it does not use a profile.

For an existing active CF/SC run belonging to this person and command, show its label, command and path, then ask:

- **Completed:** report completion and offer **View previous results / Start fresh**. View displays that run's saved final in chat and ends without new research or writes.
- **Unfinished:** report the saved step, or that no checkpoint exists yet, and offer **Resume / Start fresh**. Resume keeps that run workspace and continues the next unfinished step after the existing consistency and orphan-output checks.
- **Inconsistent/corrupt:** explain the actual problem; preserve files and offer the existing repair route or Start fresh. Never claim completion or silently reset it.

For an existing JS run, `ready` means a nonempty profile exists, not verified profile content or a completed search. After checking this person's retained intake/confirmation context, offer **Continue screening / Start fresh**. For `profile_missing`, offer **Resume setup / Start fresh**; an empty or partly written profile requires the normal intake/confirmation repair before screening, not automatic reuse. A saved file alone never proves intake was confirmed when that context is unavailable; clarify only the unresolved confirmation. Resume/Continue keeps the workspace and applies the existing profile and candidate checks. An `inconsistent` JS run uses the repair/Start fresh rule. Do not call `state-check`, write a JS checkpoint, label the run complete, or offer a saved final report. Repeated JD/application messages after run selection continue within that run without another picker.

Starting fresh creates a new run and makes it the active baseline for this person and command. Keep all earlier runs unchanged. CF, SC and JS maintain separate active baselines. Do not reopen old results or profiles as the default after a newer run has started, even if that newer run is incomplete.

## Start and retain a run

The parent calls `run-start` with:

```json
{"schema_version":1,"workspace":"<workspace-base result>","chat_id":"<host:actual-chat-id or local:UUID>","workflow":"country-finder","person_label":"<confirmed person>"}
```

For an existing person, include their exact returned `person_id`. After a Start fresh choice, also include the exact active `previous_run_id`; missing/stale baselines fail instead of silently replacing a search. Before `run-start`, check for an applicable unchanged profile already confirmed for the selected person in this chat, including another command's run. Reuse it via `profile_source_run` without another resume upload or confirmation; honor an explicit request for a new resume instead. Prior confirmation must be established in this chat, not inferred from file existence. If changed facts, conflicting sources or missing confirmation leave reuse versus new intake unresolved, use the shared question map once and wait; do not choose by recency, merge profiles or repeatedly reopen a settled choice. With no suitable source, collect and confirm the person's resume in the new run.

`profile_source_run` copies that source's confirmed `profile.md` and optional `situational-profile.md` byte-for-byte. Check that both remain applicable; if circumstances changed, choose new intake or an explicitly reviewed correction instead of copying stale answers. The helper rejects a missing resume profile or any empty source profile file without creating a run. Nonempty or partial content alone does not prove a valid confirmed extraction; the parent still checks it. Never copy research, outputs or checkpoints. A fresh search restarts research, not necessarily unchanged profile intake.

For a new JS screening session, set `workflow` to `job-screener` and use the same identity/baseline/profile-copy rules. JS runs contain run metadata and the confirmed profile, plus optional confirmed situational data; they do not export screening reports. A new chat cannot automatically copy an earlier chat's profile or the top-level legacy `profile.md`.

The result supplies the new run ID, person ID and absolute `workspace`. Retain them in chat context and show the chat key and actual saved directory after every start. Use that run workspace for every subsequent helper, specialist, profile and checkpoint operation. The metadata filename and root directory come from `data/workspace-files.json`; `run-start` creates the fixed base if absent and alone writes the new run metadata and optional profile copies. It rejects other bases. It does not establish human approval or advance a workflow checkpoint.

The helper uses `runs/chat-<chat-key>/run-<run-id>/` with private directory/file permissions where supported. Names contain no candidate names or raw chat IDs. Immutable metadata links prior runs; conflicting active runs stop automatic selection for reconciliation. Do not edit metadata, delete prior runs or switch workspaces to bypass a conflict.

## Cross-workflow reuse and legacy files

Before a CF/SC producer lookup, use `run-list` without a workflow filter for this chat/person, then bind the relevant producer's active run workspace separately. Use it for producer `resolve-files`, `research-scope`, readiness and evidence reads. Consumer files stay in the consumer run. Preserve the existing names-only confirmation and substantive compatibility rules. A missing matching producer is normal; never search another person's or chat's runs or the base folder to fill it. Explicit user-selected external/legacy sources retain the existing provenance and compatibility checks.

Existing flat workspaces are not migrated, renamed, copied or auto-resumed. The user may explicitly select a saved run path, current or legacy, for viewing or resuming, including a host handoff, after confirming its person and command. For a managed run, read its registry-named metadata to check the person and command, and validate its source catalog with `run-list` when the original chat key is known; metadata is not proof of human identity. Missing/corrupt managed metadata needs repair, not legacy fallback. Keep the original metadata, names and checkpoint policy. This explicit selection is not automatic discovery for a new chat and does not reassign the saved run to that chat.

If helper execution is unavailable, offer the existing repair/manual choice. Under approved manual handling, create a new uniquely named private run folder and keep its chat/person/command association in this conversation. Reuse only explicit paths retained for that chat/person; never infer ownership from files or improvise a metadata schema. Report unavailable automatic catalog checks. A broken package, invalid metadata or conflicting association is a blocker, not permission for manual bypass.
