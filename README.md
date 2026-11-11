---
layout: home
title: Agent Compass
description: Career research for Claude and Codex to find countries and job portals, estimate local salary targets and screen jobs against your profile.
nav_order: 1
permalink: /
---

# Agent Compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="agent-compass" width="600" height="400">

Agent Compass is a career research plugin for IT and tech job seekers using Claude or Codex.

It helps you focus your job search by researching countries for remote work or employer-sponsored relocation, finding relevant job portals and estimating local salary targets. When a role looks promising, it compares the job description with your profile to help you decide whether to apply.

**[Documentation site](https://myowinthein.github.io/agent-compass/)**

## Why I built this

When it was time to start a new job search, I used AI to research my options. But getting clear, useful information took more than simply asking a few questions.

I kept refining prompts to get better answers. I also had to save those prompts and run them again whenever I repeated a process. I wanted a way to reuse that work without starting over each time.

That’s why I built Agent Compass. I wanted to turn those prompts into workflows I could use throughout my job search and share with others starting a similar journey.

You can install Agent Compass in Claude or Codex by following the [setup guide](https://myowinthein.github.io/agent-compass/docs/setup/).

<span id="how-i-use-it"></span>

## When I use it

### Country Finder

When I’m deciding where to focus my job search, I use Country Finder to [find countries that suit my profile](https://myowinthein.github.io/agent-compass/docs/commands/country-finder.html) for remote work or employer-sponsored relocation. That gives my search a clearer starting point.

```text
Codex → $country-finder    Claude → /country-finder
```

It confirms my profile, preferences and countries, then researches remote work and sponsorship separately. I can choose countries myself or review a list from Salary Calculator for the same person in this chat. It checks the evidence and ranks application priorities, showing both kinds of fit and their limitations. Missing evidence stays visible rather than becoming a poor-fit rating.

### Portal Finder

Once I have a country in mind, I use Portal Finder to [find verified job portals](https://myowinthein.github.io/agent-compass/docs/commands/portal-finder.html) for IT and tech roles. I want useful places to start looking for openings.

```text
Codex → $portal-finder [country]    Claude → /portal-finder [country]
```

It works with one country at a time. I can add its name to the command or answer when asked; no resume or earlier country search is needed. It checks current tech coverage on the portals’ own sites, groups the official links by type and marks starting picks. Access problems and unverified coverage are reported separately.

### Salary Calculator

Before discussing salary expectations, I use Salary Calculator to [estimate local salary targets](https://myowinthein.github.io/agent-compass/docs/commands/salary-calculator.html) for my role and experience. I want a clearer sense of what to ask for in each country.

```text
Codex → $salary-calculator    Claude → /salary-calculator
```

It confirms my profile and countries, optionally using Country Finder’s results for the same person in this chat as a starting list I can change. It researches two employer tiers, checks supported adjustments and audits annual and monthly targets. These estimate local employee base pay, rather than cross-border remote offers. Missing evidence and visa salary requirements remain separate from the targets.

### Job Screener

When I find an interesting job, I use Job Screener to [compare its requirements with my profile](https://myowinthein.github.io/agent-compass/docs/commands/job-screener.html). I want to decide whether it is worth applying before spending time on an application.

```text
Codex → $job-screener    Claude → /job-screener
```

I run it once in a dedicated chat, confirm my profile and paste jobs one at a time. Each report gives Apply, Maybe or Skip, with strengths, gaps and confirmed blockers. Unknown facts stay unknown. If the format drifts, I rerun it and choose Continue screening. I can also request application drafts; nothing is submitted automatically.

See [Examples](https://myowinthein.github.io/agent-compass/docs/examples/) for optional guides to my Obsidian setup and daily job search routine.

<span id="help-me-improve-it"></span>

## Contributing

If a workflow gets in the way of your job search, a guide is unclear or you have an idea for Agent Compass, [open an issue on GitHub](https://github.com/myowinthein/agent-compass/issues). Tell me which workflow and client you used, what you tried, what you expected and what happened.

## License

Agent Compass is licensed under the [MIT License](https://github.com/myowinthein/agent-compass/blob/main/LICENSE).

<!-- last-reviewed: 4703ae27a1cbe0cb5db874b4b4e54c59c7b27106 -->
