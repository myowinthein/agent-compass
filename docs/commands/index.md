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

## How scripts help

Compass uses existing native tools and fixed bundled helpers for arithmetic, research-file handling, table formatting and saved-run storage. Agents retain the research, interpretation and decisions. They do not create inline programs or temporary helper scripts during a workflow.

When required execution is unavailable, the existing repair or disclosed manual-processing choice applies. Invalid data and broken installations still need resolution; a substitute script cannot bypass them. Maintainer tests and website builds are separate from your search.

## Where files are saved

Compass saves profiles, research and results in your home directory, grouped by person and search. Claude and Codex share these files on the same OS account.

| OS | Folder |
|---|---|
| macOS | `/Users/<username>/Agent Compass/` |
| Windows | `C:\Users\<username>\Agent Compass\` |
| Linux | `/home/<username>/Agent Compass/` |

These files help agents reuse confirmed profiles, resume research and revisit results.
