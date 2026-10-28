---
name: Run Workspaces
description: Select isolated Country Finder and Salary Calculator searches by chat, person and command before reading profiles or checkpoints.
---

# Run workspaces

Apply this before CF/SC profile intake, artifact resolution or completed replay. The user's selected folder is the **base workspace**. Every new search gets its own **run workspace** beneath it; all existing artifact/profile names and checkpoint schemas stay unchanged inside that directory. Never interpret a new chat as a request to resume whatever is in the base folder.

## Bind the chat and person

Use a trusted current conversation/session identifier exposed by the host, prefixed with its host name. In Codex, `CODEX_THREAD_ID`, when exposed to the parent, can provide it; do not launch another model or inspect private client transcripts to obtain one. In Claude, use an actual host-provided session identifier only when available. An unresolved substitution, workspace path, person name or previous chat's ID is not a chat identifier.

If no reliable host identifier is available, generate a random UUID once and retain `local:<UUID>` in this chat's working context, together with the base workspace and selected run paths. Reuse it for later invocations in this chat, not across new chats. If this association is lost, ask for the selected run path or begin fresh rather than searching other chats or guessing. Disclose that automatic rediscovery requires the retained association. Never change native client settings.

Identify the requested person from the user's request and confirmed profile. Reuse that person's returned `person_id` within this chat; a different person gets a new ID. Ask only for an unresolved identity, including two people with the same name. A label alone never proves that an old profile belongs to a new candidate. Do not read root-level or another person's profiles as automatic intake.

## Select the search

Apply `skills/helper-runtime.md`. The parent calls `run-list` with the base `workspace`, `chat_id`, and optionally the selected `person_id` and `workflow`. This reads only the selected chat's run metadata and checks matching active runs; it writes nothing. No match means a fresh search, without a resume question.

For an existing active run belonging to this person and command, show its label, command and path, then ask:

- **Completed:** report completion and offer **View previous results / Start fresh**. View displays that run's saved final in chat and ends without new research or writes.
- **Unfinished:** report the saved step, or that no checkpoint exists yet, and offer **Resume / Start fresh**. Resume keeps that run workspace and continues the next unfinished step after the existing consistency and orphan-output checks.
- **Inconsistent/corrupt:** explain the actual problem; preserve files and offer the existing repair route or Start fresh. Never claim completion or silently reset it.

Starting fresh creates a new run and makes it the active baseline for this person and command. Keep all earlier runs unchanged. CF and SC maintain separate active baselines. Do not reopen old results as the default after a newer run has started, even if that newer run is incomplete.

## Start and retain a run

The parent calls `run-start` with:

```json
{"schema_version":1,"workspace":"<absolute base workspace>","chat_id":"<host:actual-chat-id or local:UUID>","workflow":"country-finder","person_label":"<confirmed person>"}
```

For an existing person, include their exact returned `person_id`. After a Start fresh choice, also include the exact active `previous_run_id`; missing/stale baselines fail instead of silently replacing a search. Optionally provide `profile_source_run` from the same chat/person to copy their confirmed `profile.md` and `situational-profile.md` byte-for-byte. Reuse profiles only when still applicable and confirmed; never copy research, outputs or checkpoints into a fresh search. For a new person, collect and confirm their own resume/profile in the new workspace. A fresh search restarts research, not necessarily unchanged profile intake.

The result supplies the new run ID, person ID and absolute `workspace`. Retain them in chat context and show the actual saved directory to the user. Use that run workspace for every subsequent helper, specialist, profile and checkpoint operation. The metadata filename and root directory come from `data/workspace-files.json`; `run-start` alone writes the new run metadata and optional profile copies. It does not establish human approval or advance a workflow checkpoint.

The helper uses `runs/chat-<chat-key>/run-<run-id>/` with private directory/file permissions where supported. Names contain no candidate names or raw chat IDs. Immutable metadata links prior runs; conflicting active runs stop automatic selection for reconciliation. Do not edit metadata, delete prior runs or switch workspaces to bypass a conflict.

## Cross-workflow reuse and legacy files

Before a CF/SC producer lookup, use `run-list` without a workflow filter for this chat/person, then bind the relevant producer's active run workspace separately. Use it for producer `resolve-files`, `research-scope`, readiness and evidence reads. Consumer files stay in the consumer run. Preserve the existing names-only confirmation and substantive compatibility rules. A missing matching producer is normal; never search another person's or chat's runs or the base folder to fill it. Explicit user-selected external/legacy sources retain the existing provenance and compatibility checks.

Existing flat workspaces are not migrated, renamed, copied or auto-resumed. The user may explicitly select a saved run path, current or legacy, for viewing or resuming, including a host handoff, after confirming its person and command; retain its names, original metadata and checkpoint policy. This explicit selection is not automatic discovery for a new chat and does not reassign the saved run to that chat.

If helper execution is unavailable, offer the existing repair/manual choice. Under approved manual handling, create a new uniquely named private run folder and keep its chat/person/command association in this conversation. Reuse only explicit paths retained for that chat/person; never infer ownership from files or improvise a metadata schema. Report unavailable automatic catalog checks. A broken package, invalid metadata or conflicting association is a blocker, not permission for manual bypass.
