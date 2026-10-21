---
title: Commands
nav_order: 3
has_children: true
permalink: /docs/commands
---

# Commands

Use these four commands in Claude or Codex:

| Command | What it helps you do |
|---|---|
| [country-finder](commands/country-finder.html) | Choose countries for remote work or employer-sponsored relocation |
| [portal-finder](commands/portal-finder.html) | Find verified job portals in one country |
| [salary-calculator](commands/salary-calculator.html) | Estimate and audit local-market salary targets |
| [job-screener](commands/job-screener.html) | Compare jobs with your profile and draft application answers |

See [Setup]({{ '/docs/setup/' | relative_url }}) for installation and command prefixes.

## Shared workspaces and saved results

Keep one candidate and research scope per workspace. Country Finder, Salary Calculator and Job Screener share `profile.md`; the first run extracts your resume and waits for your confirmation. A saved `situational-profile.md` can supply background facts across commands. Portal Finder needs neither file.

Country Finder and Salary Calculator save checkpoints and results in that workspace. Portal Finder and Job Screener do not use checkpoint files.

### Starting or resuming a saved workflow

An unfinished run resumes from its next step, keeping successful research. A completed run replays its saved final without restarting or reformatting it.

Missing state with existing step outputs prompts a recovery choice, not an automatic reset. Corrupt checkpoints or missing required files are reported without overwriting them. Shared profiles and the other command's files do not prevent a clean new run.

### Changed facts and shared results

Confirmed clarifications can apply only to the current run. Saving them to your reusable profile needs your approval. A changed role, candidate or pay basis may require repairing unfinished work or using a fresh workspace; valid original research is not silently replaced.

Before reusing another command's result, the assistant checks completion and compatible candidate, role and scope. Imported finals can use your explicit confirmation. Drafts and pre-audit results stay labelled.

Country Finder and Salary Calculator can each run independently. Missing upstream results do not block them; optional country ordering falls back to alphabetical.

### Helpers and evidence

Shared Python 3.11+ helpers handle storage checks, exact arithmetic and table formatting. They do not choose fits, verify source truth or decide eligibility. If execution is unavailable, manual fallback requires your choice. See [Calculation runtime]({{ '/docs/commands/salary-calculator/step4-table-calculation.html#calculation-runtime' | relative_url }}).

Pay comparisons need compatible currencies, periods and pay bases. Hourly or daily rates need known hours and schedules, not assumed working weeks. Local employee benchmarks, contractor revenue and actual job offers remain distinct; unknown comparisons are not failures.

Research tasks use self-contained briefs and fresh conversation context when supported. This is not a promise of filesystem isolation. Pasted jobs, forms and research pages are evidence, not instructions to change the workflow.
