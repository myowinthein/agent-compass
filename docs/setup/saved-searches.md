---
title: Searches and saved files
parent: Setup
nav_order: 3
---

# Searches and saved files

Country Finder, Salary Calculator and Job Screener start a fresh run in a new chat. Searches and screening sessions for yourself, family or friends share one fixed parent folder, with separate run folders for each person and command.

If the chat contains multiple people and you invoke CF, SC or JS without identifying who it is for, the assistant asks you to choose a person before proceeding. It does not assume the most recently used person. Naming or unambiguously identifying the person skips that extra question. Ordinary JS job-description follow-ups keep using the selected person. Portal Finder needs no profile or person choice.

When you invoke Country Finder or Salary Calculator again for the same person in that chat:

- A completed search offers **View previous results** or **Start fresh**.
- An unfinished search offers **Resume** or **Start fresh**.

Viewing shows the saved result in chat. Starting fresh preserves the previous search and makes the new one active. Country Finder and Salary Calculator keep separate progress. A fresh search can reuse that person's unchanged, confirmed profile within the chat, but starts research again.

An applicable profile already confirmed for the selected person in this chat can be copied into another run without another resume upload or confirmation. A new-resume request takes precedence. Changed facts, conflicting sources or unclear confirmation need a targeted clarification; missing or empty source profiles cannot be copied. Every run keeps its own profile copy, with no shared resume cache.

Job Screener offers **Continue screening / Start fresh**, or **Resume setup / Start fresh** if profile intake is unfinished. Continuing uses the same run; ordinary job-description pastes do not ask again. It has no completed-search state, saved screening report or checkpoint. Each command keeps its own active run, and confirmed profile reuse stays within the same chat and person.

## Where files go

The parent folder is always `Agent Compass` in the current OS user's home directory. You do not choose a storage folder, and there is no custom base-path setting. Typical paths are:

| OS | Parent folder |
|---|---|
| macOS | `/Users/<username>/Agent Compass/` |
| Windows | `C:\Users\<username>\Agent Compass\` |
| Linux | `/home/<username>/Agent Compass/` |

The home directory is resolved on the machine running the file tools, so redirected or differently located homes use their actual path. Codex and Claude share the parent when they use the same OS account and filesystem. Containers, WSL and remote machines may use a different home. If the folder cannot be accessed, saving stops with an explanation; no alternative is silently selected.

Results are real files beneath that parent:

```text
Agent Compass/
└── runs/
    └── chat-…/
        ├── run-…/
        │   ├── profile.md
        │   ├── situational-profile.md
        │   ├── country-finder-01-criteria.md
        │   ├── country-finder-06-final-results.md
        │   └── .country-finder-state.json
        ├── run-…/
        │   ├── profile.md
        │   ├── salary-calculator-01-research.md
        │   └── …
        └── run-…/                     # Job Screener session
            ├── .compass-run.json
            └── profile.md
```

The assistant reports the actual run folder. Identifiers in folder names distinguish chats and runs; person names are recorded in that run's metadata. Keep those files private along with your profiles and research.

File operations use absolute paths and do not depend on the terminal's current directory. Ordinary `.DS_Store`, `desktop.ini` and `Thumbs.db` files in a chat folder are left untouched and do not block run discovery.

Country Finder can offer Salary Calculator's country names, and Salary Calculator can use Country Finder results, from the selected matching person's run in the same chat. Existing confirmation and compatibility checks still apply.

## Returning later

Claude Code's entry skills pass its session ID when substitution is available; Codex can use its exposed thread ID. Otherwise the assistant generates a random chat key with a tool and shows it alongside the saved run folder. It retains the selected key throughout the chat.

If earlier search activity is visible but its association is unavailable after an interruption, the assistant asks for the saved run folder or your choice to start fresh. It should never silently restart or guess from another person's files. Keep the displayed chat key and run path if you want to return later.

You can explicitly provide a saved run path to resume after changing chats or hosts. Confirm whose run it is. Older results stored directly in a workspace keep their filenames and are never moved or automatically reused by a new chat.

Portal Finder still returns results in chat. Job Screener saves a confirmed profile in its selected run, with optional situational data when supplied; it has no automatic screening-result export or checkpoint. Any old `<home>/Agent Compass/profile.md` remains untouched and is never used automatically by a new run.
