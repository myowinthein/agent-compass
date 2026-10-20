---
title: Commands
nav_order: 3
has_children: true
permalink: /docs/commands
---

# Commands

Agent Compass helps IT and tech job seekers research their options with Claude and Codex. It provides four workflows with the same names on both platforms: [`/country-finder`](commands/country-finder.html), [`/portal-finder`](commands/portal-finder.html), [`/salary-calculator`](commands/salary-calculator.html) and [`/job-screener`](commands/job-screener.html). Country Finder, Salary Calculator, and Job Screener require a resume: on first run, the assistant prompts you to upload one and extracts it to `profile.md` in your workspace. Country Finder and Salary Calculator are multi-step pipelines that resume from where they left off if interrupted. Portal Finder, which needs only a country, and Job Screener, which reuses your saved profile, each run in a single step with no state to resume.

For platform-specific installation and invocation, see [Setup]({{ '/docs/setup/' | relative_url }}). Claude uses slash commands; Codex CLI uses skill mentions or `/skills`. All four entry points share the same workflow and rule sources.
