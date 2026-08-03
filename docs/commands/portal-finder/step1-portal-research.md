---
title: Step 1 — Portal research
parent: /portal-finder
grand_parent: Commands
nav_order: 1
---

# Step 1 — Portal research

Researches job portals for IT/tech roles in the target country online. Each portal's existence and activity is confirmed directly on its own site — not from blog posts or listicle articles.

## Flow

```mermaid
flowchart TD
  Start([Step 1 begins]) --> Research[Research portals online\nfor the target country]
  Research --> Group[Organize by type into 3 groups\ngeneral · tech · networks]
  Group --> Flag[Flag top 2–3 per group with ⭐\nFlag caveats with ⚠️]
  Flag --> Output([Output all groups — stop])
```

## What it uses

- Country — established before this step runs

## Groups

Portals are organized **by type** into these three mutually exclusive groups, in this order:

1. **General job boards** — broad portals that list many fields including tech
2. **Tech-specific boards** — boards built for IT, software, data, or related tech roles
3. **Professional & community networks** — professional networks and community-run boards where tech roles are posted (e.g. LinkedIn, Wellfound, startup "who's hiring" boards, active local developer communities)

Government and official employment-service portals are deliberately excluded — they tend to be citizen/PR-oriented or geared toward expat/relocation information rather than reliable third-party job listings.

Each portal goes in exactly one group. Geographic scope (country-dedicated vs global/multi-country) is not a group — it is noted per portal, since it changes how much of a portal's listings are relevant. Remote-first boards are placed under General or Tech-specific by their focus, not a separate group. If a portal fits none of the three, it gets its own clearly named group rather than being forced in. If no portals fit a group, that group is omitted rather than padded with weak entries.

## Per-portal output

For each portal:
- Name, with its official URL in parentheses right after (e.g. LinkedIn (linkedin.com)) — the portal's own domain, not a search engine result or aggregator link
- Scope — country-dedicated or global/multi-country
- One-line description of its real strength for an IT/tech job seeker

Within each group, ⭐ marks the 2–3 portals to start with first.

## Warning flags

⚠️ flags anything outside the structure but worth knowing:
- Portal is dead or deprecated despite still ranking in searches
- Two portals in the list are owned by the same parent company
- Portal is restricted to citizens or residents and not open to foreign applicants
- Any significant caveat affecting an international candidate

## Stop condition

Claude outputs all groups in a single response, in order from group 1 to 3, then stops. No follow-up advice or recommendations are added.
