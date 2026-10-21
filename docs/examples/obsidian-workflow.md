---
layout: default
title: My Obsidian workflow
parent: Examples
nav_order: 1
permalink: /docs/examples/obsidian-workflow.html
---

# My Obsidian workflow

This is how I organise my job search. Obsidian and this folder structure are optional, not requirements for Agent Compass. All examples below use fictional data.

## Why I use Obsidian

I tried several note-taking apps before moving to Obsidian. Its notes are Markdown files, so Claude and Codex can read and update them when I give them access. I can also customise the workspace with plugins and CSS snippets.

I keep my job search in a separate vault called `Career`.

## How I organise it

Inside the vault, each person has their own folder:

```text
Career/
└── Alex/
    ├── Profile.md
    └── Applications/
        ├── 1. 🇩🇪 Germany.md
        └── 2. 🇳🇱 Netherlands.md
```

`Profile.md` is my dashboard. The `Applications` folder holds my application history.

For someone pursuing multiple roles, I separate the histories into folders such as `Applications - PD` for product design and `Applications - PO` for product owner roles.

## My profile dashboard

### Countries to target

I save the final priority table from [`country-finder`]({{ '/docs/commands/country-finder.html' | relative_url }}) so I can see where to focus my search.

| Country | Priority | Remote Fit | Sponsorship Fit | Main limitation |
|---|---|---|---|---|
| 🇩🇪 Germany | 🥇 Focus | Moderate | Strong | Fewer remote roles accept the candidate's location |
| 🇳🇱 Netherlands | 🥈 Selective | Strong | Unknown | Sponsorship evidence needs further checking |

These are fictional examples, not country recommendations.

### Salary expectations

I save the final table from [`salary-calculator`]({{ '/docs/commands/salary-calculator.html' | relative_url }}) as a reference for applications and salary discussions.

Gross base salary in local currency. Monthly figures are annual ÷ 12 references, not necessarily payslips; targets are market estimates, not visa-eligibility guarantees.

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |
|---|---|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | Unknown | 60,000 | 78,000 | 5,000 | 6,500 |
| 🇳🇱 Netherlands (EUR) | Unknown | 65,000 | 84,000 | 5,400 | 7,000 |

These figures are fictional and do not represent current salaries or visa rules.

### Saved portal searches

I use [`portal-finder`]({{ '/docs/commands/portal-finder.html' | relative_url }}) to discover relevant portals, then save links to searches filtered for my role and target country.

For example, this section of `Profile.md` might look like:

```markdown
## Portals

- 🇩🇪 Germany
    - [x] [Example Jobs](https://example.invalid/germany/backend) (Northstar Labs)
    - [ ] [Example Tech](https://example.invalid/germany/software)
- 🇳🇱 Netherlands
    - [ ] [Example Jobs](https://example.invalid/netherlands/backend)
```

The checkbox tracks whether a search has been reviewed. The company in parentheses marks where the previous scan reached, helping me avoid repeatedly reviewing older results. It does not mean I applied there.

My dashboard also holds useful background information and reusable answers to common application questions.

## My application history

Each country note groups companies by the portal where I applied.

For example, `1. 🇩🇪 Germany.md` might contain:

```markdown
## Example Jobs

- [ ] Northstar Labs
- [x] Cedar Systems

## Example Tech

- [ ] Lantern Studio
```

An unchecked company means the application is still open. A checked company means it is closed.

This history is separate from the portal checkboxes: reviewing a search is not the same as applying to a job.

## How the commands fit into my routine

I start with `country-finder`, then use `portal-finder` and `salary-calculator` for my target countries. I collect the useful results in my dashboard.

When I find an interesting opening, I use [`job-screener`]({{ '/docs/commands/job-screener.html' | relative_url }}) to compare it with my profile. After I apply, I record the company in the relevant country note.

I also use a separate personal `job-scan` skill to review saved portal searches and identify jobs worth considering. It checks my application history and updates search progress, but does not apply for me or add companies to my application history. It is not included in Agent Compass.

## Keep the dashboard separate from workflow files

My Obsidian `Profile.md` is a personal dashboard, not Agent Compass's generated `profile.md`. I keep the command workspace separate and preserve its generated filenames. Names that differ only by capitalisation can conflict on macOS.
