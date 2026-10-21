---
layout: default
title: My Obsidian workflow
parent: Examples
nav_order: 1
permalink: /docs/examples/obsidian-workflow.html
---

# My Obsidian workflow

This is how I organise my job search. Obsidian and this folder structure are optional, not requirements for Agent Compass. The people, companies and salary targets in the examples are fictional; the visa salary rules are sourced below.

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
| 🇳🇱 Netherlands (EUR) | 5,942/mo ⚠️ | 65,000 | 84,000 | 5,400 | 7,000 |

2026 visa salary rules, checked on 21 October 2026:

- 🇩🇪 Germany: [standard EU Blue Card threshold](https://www.arbeitsagentur.de/vor-ort/zav/working-and-living-in-germany/iss-en/issue-03-2026/blue-card), gross annual pay.
- 🇳🇱 Netherlands: [highly skilled migrant threshold for a first application at age 30 or over](https://ind.nl/en/documents/01-2026/business-newsletter-18-december-2025.pdf), gross monthly pay excluding holiday allowance.

The example assumes 12 equal monthly base payments. ⚠️ marks a Mainstream target below the selected rule. Other routes and applicant categories can have different thresholds.

### Saved portal searches

I use [`portal-finder`]({{ '/docs/commands/portal-finder.html' | relative_url }}) to discover relevant portals, then save links to searches filtered for my role and target country.

For example, this section of `Profile.md` might look like:

```markdown
## Portals

- 🇩🇪 Germany
    - [x] [LinkedIn](https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Germany&sortBy=DD) (Northstar Labs)
    - [ ] [Arbeitnow](https://www.arbeitnow.com/jobs/php?sort_by=newest)
- 🇳🇱 Netherlands
    - [ ] [LinkedIn](https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Netherlands&sortBy=DD)
```

## My daily job search

Each day, I work through the saved portal links:

1. Open a portal search with results sorted newest first.
2. Copy the company marker from my note and find it in the results.
3. Review the newer jobs above that company. If I cannot find the marker, I keep reviewing the available results rather than assuming there are no new jobs.
4. When finished, replace the marker with the company at the top of the latest results and tick the portal's checkbox.

The marker records where my search reached, not a company I necessarily applied to. Some searches, such as LinkedIn AI Search, do not use company markers.

## My application history

Before applying, I use [`job-screener`]({{ '/docs/commands/job-screener.html' | relative_url }}) to compare the job with my profile. After I apply, I add the company under the relevant portal in its country note so I do not apply to the same company again by mistake.

For example, `1. 🇩🇪 Germany.md` might contain:

```markdown
## LinkedIn

- [ ] Northstar Labs
- [x] Cedar Systems

## Arbeitnow

- [ ] Lantern Studio
```

I leave the company unchecked while the application is open. If I receive a rejection or decide not to continue, I tick its checkbox to mark it closed.

This history is separate from the portal checkboxes: reviewing a search is not the same as applying to a job.
