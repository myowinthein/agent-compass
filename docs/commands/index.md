---
title: Commands
nav_order: 2
has_children: true
permalink: /docs/commands
---

# Commands

Agent Compass is built for globally-minded IT/tech job seekers. It provides four workflows with the same names in Claude Cowork, Claude Code, and Codex: [`/country-finder`](commands/country-finder.html), [`/salary-calculator`](commands/salary-calculator.html), [`/portal-finder`](commands/portal-finder.html), and [`/job-screener`](commands/job-screener.html). Country Finder, Salary Calculator, and Job Screener require a resume: on first run, the assistant prompts you to upload one and extracts it to `profile.md` in your workspace. Country Finder and Salary Calculator are multi-step pipelines that resume from where they left off if interrupted. Portal Finder, which needs only a country, and Job Screener, which reuses your saved profile, each run in a single step with no state to resume.

For platform-specific installation and invocation, see the [home page](../index.html#installation). Claude uses slash commands; Codex CLI uses skill mentions or `/skills`. All four entry points share the same workflow and rule sources.
