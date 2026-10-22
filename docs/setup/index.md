---
layout: default
title: Setup
nav_order: 2
has_children: true
permalink: /docs/setup/
---

# Setup

Agent Compass works with Claude and Codex. For either platform, you can install, update and uninstall the plugin through the desktop app or terminal. Choose whichever you prefer.

The desktop guides were tested on macOS. The steps should be similar on other supported operating systems, though menus and buttons may move as the apps are updated. Terminal commands tend to stay more consistent across releases and operating systems.

If you use the terminal on Windows, run the examples in a Bash-compatible shell with `grep` available.

## Requirements

| Client | Minimum supported CLI version |
|---|---|
| Claude terminal | 2.1.292 |
| Codex terminal | 0.163.0 |

Verified on 22 October 2026 through package and startup/preflight checks. These are our support baselines, not the first versions that introduced plugins. Older versions may work but are not covered by those checks. Full workflow results also depend on the available tools and model access.

Desktop apps have separate version numbers. Use a current desktop release with plugin support; the CLI versions above do not apply to desktop apps.

Check your terminal versions with:

```bash
claude --version
codex --version
```

The shared helpers need Python 3.11+ and code execution. If these are unavailable, the workflow asks before using its manual fallback. Research steps also need browsing or their documented manual research path.

## Run a command

Type the prefix in the chat input, then select an Agent Compass command.

| Client | Prefix |
|---|---|
| Claude desktop and terminal | `/` |
| Codex terminal | `$` |
| Codex desktop | `/` or `$` |

## Plugin names

The guides use these names to identify the source, marketplace and plugin.

| Name | Value | Purpose |
|---|---|---|
| Repository | `myowinthein/agent-compass` | GitHub source used to add the marketplace. |
| Marketplace | `agent-compass-marketplace` | Catalog containing the plugin. |
| Plugin | `agent-compass` | Package containing the four workflows. |
