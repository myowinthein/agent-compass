---
layout: default
title: Terminal
parent: Claude
grand_parent: Setup
nav_order: 2
permalink: /docs/setup/claude/terminal.html
---

# Claude terminal

Read the [Setup notes]({{ '/docs/setup/' | relative_url }}) before starting.

## Install

```bash
claude plugin marketplace add myowinthein/agent-compass
claude plugin install agent-compass@agent-compass-marketplace --scope user
claude plugin list --json | grep -F -A3 '"id": "agent-compass@agent-compass-marketplace"'
```

Start a fresh Claude session in your job search folder. Type `/` and filter by `country`, `portal`, `salary`, or `job` to find the workflows.

## Update

```bash
claude plugin marketplace update agent-compass-marketplace
claude plugin update agent-compass@agent-compass-marketplace --scope user
claude plugin list --json | grep -F -A3 '"id": "agent-compass@agent-compass-marketplace"'
```

Check the installed version and enabled state, then start a fresh session.

## Uninstall

```bash
claude plugin uninstall agent-compass@agent-compass-marketplace --scope user --keep-data
claude plugin list --json | grep -F -A3 '"id": "agent-compass@agent-compass-marketplace"'
```

Check that the CLI-managed entry is gone. In a fresh session, its workflows should no longer appear unless an account-synced copy is also installed.
