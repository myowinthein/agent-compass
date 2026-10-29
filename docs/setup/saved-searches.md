---
title: Searches and saved files
parent: Setup
nav_order: 3
---

# Searches and saved files

Country Finder and Salary Calculator start a fresh search in a new chat. Searches for yourself, family or friends share one fixed parent folder, with a separate run folder for each person and search.

When you invoke the same command again for the same person in that chat:

- A completed search offers **View previous results** or **Start fresh**.
- An unfinished search offers **Resume** or **Start fresh**.

Viewing shows the saved result in chat. Starting fresh preserves the previous search and makes the new one active. Country Finder and Salary Calculator keep separate progress. A fresh search can reuse that person's unchanged, confirmed profile within the chat, but starts research again.

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
        └── run-…/
            ├── profile.md
            ├── salary-calculator-01-research.md
            └── …
```

The assistant reports the actual run folder. Identifiers in folder names distinguish chats and runs; person names are recorded in that run's metadata. Keep those files private along with your profiles and research.

Country Finder can offer Salary Calculator's country names, and Salary Calculator can use Country Finder results, from the selected matching person's run in the same chat. Existing confirmation and compatibility checks still apply.

## Returning later

Claude Code's entry skills pass its session ID when substitution is available; Codex can use its exposed thread ID. Otherwise the assistant generates a random chat key with a tool and shows it alongside the saved run folder. It retains the selected key throughout the chat.

If earlier search activity is visible but its association is unavailable after an interruption, the assistant asks for the saved run folder or your choice to start fresh. It should never silently restart or guess from another person's files. Keep the displayed chat key and run path if you want to return later.

You can explicitly provide a saved run path to resume after changing chats or hosts. Confirm whose run it is. Older results stored directly in a workspace keep their filenames and are never moved or automatically reused by a new chat.

Portal Finder still returns results in chat. Job Screener saves a confirmed profile, when needed, at `<home>/Agent Compass/profile.md`; it has no automatic screening-result export or checkpoint.
