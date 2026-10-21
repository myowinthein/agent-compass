---
title: Commands
nav_order: 3
has_children: true
permalink: /docs/commands
---

# Commands

Agent Compass helps IT and tech job seekers research their options with Claude and Codex. It provides four workflows with the same names on both platforms: [`/country-finder`](commands/country-finder.html), [`/portal-finder`](commands/portal-finder.html), [`/salary-calculator`](commands/salary-calculator.html) and [`/job-screener`](commands/job-screener.html). Country Finder, Salary Calculator, and Job Screener require a resume: on first run, the assistant prompts you to upload one and extracts it to `profile.md` in your workspace. Country Finder and Salary Calculator are multi-step pipelines that resume from where they left off if interrupted. Portal Finder, which needs only a country, and Job Screener, which reuses your saved profile, each run in a single step with no state to resume.

For platform-specific installation and invocation, see [Setup]({{ '/docs/setup/' | relative_url }}). Claude uses slash commands; Codex CLI uses skill mentions or `/skills`. All four entry points share the same workflow and rule sources.

## Shared workspaces and saved results

Use one candidate and research scope per workspace. Profiles can be reused across commands, but a changed candidate, role or salary basis may invalidate unfinished work. Same-scope repairs preserve valid original research; a fresh workspace avoids mixing changed-scope research with originals that ingestion deliberately keeps.

Country Finder and Salary Calculator check their own saved outputs before creating a missing checkpoint. Existing outputs prompt a recovery choice, not a silent restart. Shared profiles or the other command's files do not prevent a new run. Completed runs replay their saved results unchanged.

A saved final is used as an audited result only when completion can be established, or you explicitly confirm a legacy/imported final. Drafts and pre-audit results stay labelled. Missing or unsuitable upstream results never prevent a standalone run, and optional table ordering falls back to alphabetical.

Confirmed clarifications reach the affected steps and specialists. They can be used for the current run without silently changing your reusable profile; saving a dated profile note requires your approval. Derived experience avoids counting overlapping roles twice and states the date used for current roles.

Salary comparisons need compatible currency, period and pay basis. Hourly or daily amounts need supported hours and payment schedules, not assumed working weeks. Unknown comparisons are not failures. Local employee benchmarks, contractor revenue and actual JD offers remain distinct. Research pages, manual results and pasted forms are evidence, not instructions to change the workflow.
