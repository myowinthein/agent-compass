---
title: Commands
nav_order: 2
has_children: true
permalink: /docs/commands
---

# Commands

Claude Compass is built for globally-minded IT/tech job seekers. It provides five slash commands: [`/country-finder`](commands/country-finder.html), [`/salary-calculator`](commands/salary-calculator.html), [`/salary-calculator-v2`](commands/salary-calculator-v2.html), [`/portal-finder`](commands/portal-finder.html), and [`/job-screener`](commands/job-screener.html). Country Finder, both Salary Calculator versions, and Job Screener require a resume: on first run, Claude prompts you to upload one and extracts it to `profile.md` in your workspace. Country Finder and both Salary Calculator versions are multi-step pipelines that resume from where they left off if interrupted. Portal Finder, which needs only a country, and Job Screener, which reuses your saved profile, each run in a single step with no state to resume.
