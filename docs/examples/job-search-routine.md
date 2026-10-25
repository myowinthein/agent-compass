---
layout: default
title: My job search routine
parent: Examples
nav_order: 2
permalink: /docs/examples/job-search-routine.html
---

# My job search routine

See [My Obsidian setup]({{ '/docs/examples/obsidian-workflow.html' | relative_url }}) for how I organise my job search notes in Obsidian.

## Opening my saved searches

I start in the `Portals` section of `Profile.md` and follow the links from top to bottom.

1. Open each saved portal link in the browser.
2. Copy the company name in parentheses next to the link.
3. Find that company in the job listings and review the newer jobs.
4. At the end of the listings, update the marker next to the link with the last company reviewed.
5. Tick the checkbox to mark the search as reviewed, then close the tab.

## Screening and tracking applications

1. When a job looks interesting, use [`job-screener`]({{ '/docs/commands/job-screener.html' | relative_url }}) to compare it with my profile.
2. Read the detailed analysis and apply if the job seems like a good match.
3. Add the company name under the relevant portal in that country's note in the `Applications` folder.

This history helps me track my applications. If I am unsure whether I have already applied to a company, I check here before applying again.

I tick the company's checkbox when I receive a rejection or decide not to continue.

## Resetting portal checkboxes

I used to uncheck all the portal links by hand before starting each day's search. It was a small task, but repeating it every day became annoying.

Obsidian supports [community plugins](https://obsidian.md/help/community-plugins) and lets you [build your own](https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin), so I created a plugin called **Portal Daily Reset** to uncheck my portal checkboxes automatically each day.

An agent with permission to edit the vault's plugin files can help build a plugin like this.

## Keeping our notes visually distinct

Obsidian supports [CSS snippets](https://obsidian.md/help/snippets), which let me customise how my notes look.

One use case is using different background colours for notes when a vault has multiple profiles. This helps identify whose notes are open and avoid editing the wrong file.

Another use case is colour-coding the `Strong`, `Moderate` and `Weak` ratings in my [Countries to target]({{ '/docs/examples/obsidian-workflow.html' | relative_url }}#countries-to-target) table, making stronger and weaker matches easier to spot.

An agent with permission to edit the vault's CSS snippets can help set this up.
