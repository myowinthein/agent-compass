---
layout: default
title: Terminal
parent: Codex
grand_parent: Setup
nav_order: 2
permalink: /docs/setup/codex/terminal.html
---

# Codex terminal

Read the [Setup notes]({{ '/docs/setup/' | relative_url }}) before starting.

## Install

```bash
codex plugin marketplace add myowinthein/agent-compass
codex plugin add agent-compass@agent-compass-marketplace
codex plugin list --marketplace agent-compass-marketplace
```

Start a fresh Codex session in your job search folder. Type `$` and filter by `country`, `portal`, `salary`, or `job` to find the workflows.

## Update

```bash
codex plugin marketplace upgrade agent-compass-marketplace
codex plugin add agent-compass@agent-compass-marketplace
codex plugin list --marketplace agent-compass-marketplace
```

Check the installed version and enabled state, then start a fresh session.

## Uninstall

```bash
codex plugin remove agent-compass@agent-compass-marketplace
codex plugin list --marketplace agent-compass-marketplace
```

Check that Compass is absent from the installed list. In a fresh session, its workflows should no longer appear. An older chat may retain loaded instructions.
