---
title: Commands
nav_order: 3
has_children: true
has_toc: false
permalink: /docs/commands
description: Explore four Agent Compass workflows for finding countries and job portals, estimating local salary targets and screening jobs against your profile.
---

# Commands

Guides to using Agent Compass for your job search. Each command page explains how to start, what happens along the way and what results to expect.

| When you want to… | Command |
|---|---|
| Compare countries for remote work or employer-sponsored relocation | [country-finder]({{ '/docs/commands/country-finder.html' | relative_url }}) |
| Estimate local salary targets for your role | [salary-calculator]({{ '/docs/commands/salary-calculator.html' | relative_url }}) |
| Find verified tech job portals in one country | [portal-finder]({{ '/docs/commands/portal-finder.html' | relative_url }}) |
| Screen a job or draft an application from confirmed facts | [job-screener]({{ '/docs/commands/job-screener.html' | relative_url }}) |

## Where files are saved

Country Finder and Salary Calculator save profiles, research and results in a folder named `Agent Compass` in your home directory. Job Screener uses the same base for profiles; its screening reports stay in chat. Portal Finder saves no automatic exports.

| OS | Folder |
|---|---|
| macOS | `/Users/<username>/Agent Compass/` |
| Windows | `C:\Users\<username>\Agent Compass\` |
| Linux | `/home/<username>/Agent Compass/` |

Each person and search gets its own run folder under `runs/`. Claude and Codex share the folder on the same OS account. Containers, WSL and remote machines may use a different home directory.
