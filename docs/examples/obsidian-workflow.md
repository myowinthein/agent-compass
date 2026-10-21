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

### Salary expectations

I save the final table from [`salary-calculator`]({{ '/docs/commands/salary-calculator.html' | relative_url }}) as a reference for applications and salary discussions.

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |
|---|---|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | 50,700/yr | 60,000 | 78,000 | 5,000 | 6,500 |
| 🇳🇱 Netherlands (EUR) | 71,304/yr | 65,000 | 84,000 | 5,400 | 7,000 |

### Saved portal searches

I use [`portal-finder`]({{ '/docs/commands/portal-finder.html' | relative_url }}) to discover relevant portals, then save links to searches filtered for my role and target country.

For example, this section of `Profile.md` might look like:

```markdown
## Portals

- 🇩🇪 Germany
    - [x] [Example Jobs](https://example.invalid/germany/backend) (Northstar Labs)
    - [ ] [Example Tech](https://example.invalid/germany/software) (Lantern Studio)
- 🇳🇱 Netherlands
    - [ ] [Example Jobs](https://example.invalid/netherlands/backend) (Cedar Systems)
```

## My daily job search

I follow these steps each day:

1. Open each saved portal link.
2. Copy the marked company name from my note.
3. Find it in the portal's results and review the newer jobs.
4. Update the company marker and tick the checkbox when I finish.

The checkbox tracks whether a search has been reviewed. I use the company name in parentheses as a reference point for my next search, so I can focus on newer jobs.

## My application history

Each country note groups companies by the portal where I applied.

Before applying, I use [`job-screener`]({{ '/docs/commands/job-screener.html' | relative_url }}) to compare the job with my profile. After applying, I add the company under the relevant portal so I do not apply to the same company again by mistake.

For example, `1. 🇩🇪 Germany.md` might contain:

```markdown
## LinkedIn

- [ ] Northstar Labs
- [x] Cedar Systems

## Arbeitnow

- [ ] Lantern Studio
```

An unchecked company means the application is still open. A checked company means it is closed. I tick the company's checkbox when I receive a rejection or decide not to continue.

This history is separate from the portal checkboxes: reviewing a search is not the same as applying to a job.
