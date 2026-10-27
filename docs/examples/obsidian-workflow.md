---
layout: default
title: My Obsidian setup
parent: Examples
nav_order: 1
permalink: /docs/examples/obsidian-workflow.html
---

# My Obsidian setup

This is how I organise my job search. Obsidian and this folder structure are optional, not requirements for Agent Compass. All examples below use fictional data.

## Why I use Obsidian

After trying several note-taking apps, I chose Obsidian because it stores notes as Markdown files. This lets my agents read and update them when I give them access. I can also customise the workspace with plugins and CSS snippets.

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

For someone pursuing multiple roles, I separate the histories into folders such as `Applications - FS` for full-stack and `Applications - PO` for product owner roles.

## My profile dashboard

### Countries to target

I save the final [priority table]({{ '/docs/commands/country-finder/step6-final-ranking.html' | relative_url }}#priority-table) from `country-finder` so I can see where to focus my search.

```markdown
## Countries to target

| Country | Priority | Remote Fit | Sponsorship Fit | Main limitation |
|---|---|---|---|---|
| 🇩🇪 Germany | 🥇 Focus | Moderate | Strong | Fewer remote roles accept the candidate's location |
| 🇳🇱 Netherlands | 🥈 Selective | Strong | Unknown | Sponsorship evidence needs further checking |
```

### Salary expectations

I save the final [table]({{ '/docs/commands/salary-calculator/step4-table-calculation.html' | relative_url }}#table-format) from `salary-calculator` as a reference for applications and salary discussions.

```markdown
## Salary expectations

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |
|---|---|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | 50,700/yr | 60,000 | 78,000 | 5,000 | 6,500 |
| 🇳🇱 Netherlands (EUR) | 71,304/yr | 65,000 | 84,000 | 5,400 | 7,000 |
```

### Saved portal searches

I use [`portal-finder`]({{ '/docs/commands/portal-finder.html' | relative_url }}) to discover relevant portals, then save links to searches filtered for my role and target country.

```markdown
## Portals

- 🇩🇪 Germany
    - [x] [LinkedIn](https://www.linkedin.com/jobs/search/?location=Germany&keywords=full%20stack) (Northstar Labs)
    - [ ] [Arbeitnow](https://www.arbeitnow.com/?search=full%20stack) (Lantern Studio)
- 🇳🇱 Netherlands
    - [ ] [LinkedIn](https://www.linkedin.com/jobs/search/?location=Netherlands&keywords=full%20stack) (Cedar Systems)
```

The company name in parentheses is the last company I saw during my previous job search. It helps me find where I left off and focus on newer jobs.

## My application history

I keep a note for each country and organise my applications by job portal.

For example, `1. 🇩🇪 Germany.md` might contain:

```markdown
## LinkedIn

- [ ] Northstar Labs
- [x] Cedar Systems

## Arbeitnow

- [ ] Lantern Studio
```

An unchecked company means I have applied and the application is still open. I tick the checkbox when I receive a rejection email or decide not to continue.

See [My job search routine]({{ '/docs/examples/job-search-routine.html' | relative_url }}) for how I use these notes during my daily job search.
