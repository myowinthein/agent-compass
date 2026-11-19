---
title: Portal-finder
parent: Commands
nav_order: 2
has_children: true
description: Find verified job portals for IT and tech roles in one country, with official links, grouped results and disclosed verification limits.
detailed: /docs/commands/portal-finder/detailed.html
has_toc: false
---

# Portal-finder

{% include guide-depth.html %}

Finds verified job portals for IT/tech roles in one country. It needs a country, not your resume or a completed Country Finder run.

## Flow

```mermaid
flowchart TD
  Country["Choose one country"] --> Saved{"Saved report available?"}
  Saved -->|View saved results| View["Show the dated report and stop"]
  Saved -->|Fresh search or no report| Research["Verify relevant portals on their own sites"]
  Research --> Result["Save a new report and show grouped links"]
```

## Start the command

```text
portal-finder Germany
```

Or leave out the country and answer when asked:

```text
Codex → $portal-finder    Claude → /portal-finder
```

Use the prefix shown in [Setup]({{ '/docs/setup/' | relative_url }}#run-a-command). If you name several countries, the assistant asks you to pick one.

## Saved reports

If a report exists for your country, choose **View saved results** or **Run a fresh search**. The assistant shows its saved date, evidence date and verification limits before you choose. With no saved report, research starts directly.

Each completed search saves a separate report under your home directory’s `Agent Compass/portal-finder/` folder. Previous reports are kept; older history is available on request. Viewing a report keeps its original evidence and dates, without checking the portals again.

## Your result

Portals are grouped into general job boards, tech-specific boards, and professional or community networks. Each entry includes an official link, geographic scope and a short description.

⭐ marks verified starting picks. ⚠️ highlights access limits or other important caveats. A blocked or login-only site is not called dead merely because it could not be checked.

The command shows the report in chat with its saved location, then stops. Partial results keep their coverage notes. No profile or checkpoint is created.

See [Step 1: Portal research](portal-finder/step1-portal-research.html) for verification and partial-result handling.
