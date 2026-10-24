---
layout: default
title: Home
nav_order: 1
permalink: /
---

# Agent Compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="agent-compass" width="600">

Agent Compass is a plugin for IT and tech job seekers who use Claude or Codex.

It helps you figure out which countries suit your profile for remote work or visa sponsorship, where to look for jobs and what salary to ask for. When you find an interesting role, it compares the job description with your profile to help you decide whether to apply.

**[Documentation site](https://myowinthein.github.io/agent-compass)**

## Why I built this

When it was time to start a new job search, I used AI to research my options. But getting clear, useful information took more than simply asking a few questions.

I kept refining prompts to get better answers. I also had to save those prompts and run them again whenever I repeated a process. I wanted a way to reuse that work without starting over each time.

That’s why I built Agent Compass. I wanted to turn those prompts into workflows I could use throughout my job search and share with others starting a similar journey.

You can install Agent Compass in Claude or Codex by following the [setup guide](https://myowinthein.github.io/agent-compass/docs/setup/).

## How I use it

```text
country-finder
```

I start here to [find countries that match my profile](https://myowinthein.github.io/agent-compass/docs/commands/country-finder.html) for remote work or visa sponsorship, so I know where to focus my search.

It asks a few questions about your profile and preferences, then researches the countries and returns a priority table.

If you ran `salary-calculator` first, it can suggest your saved target countries for you to confirm or edit.

```text
portal-finder
portal-finder <country>
```

Once I know which countries to target, I use this command to [find verified job portals](https://myowinthein.github.io/agent-compass/docs/commands/portal-finder.html) for IT and tech roles. From there, I can create accounts and start looking for opportunities.

Provide one country name, or leave it out and the command will ask before finding its job portals.

```text
salary-calculator
```

I use this command to [explore realistic local-market salaries](https://myowinthein.github.io/agent-compass/docs/commands/salary-calculator.html) for my role and experience. This gives me a clearer idea of what to ask for when discussing salary expectations.

If you’ve already run `country-finder`, it suggests countries from your results. You can keep the list, add or remove countries or start fresh. Otherwise, it asks which countries you want to research.

```text
job-screener
```

When I find an interesting job, I use this command to [compare its requirements with my profile](https://myowinthein.github.io/agent-compass/docs/commands/job-screener.html). Its Apply, Maybe, or Skip recommendation helps me decide whether to apply.

Start a dedicated chat and run this command once. Then paste job descriptions one at a time. If the responses stop following the screening format, run the command again.

I also use Obsidian to organise my research and track applications. [See my Obsidian workflow](https://myowinthein.github.io/agent-compass/docs/examples/obsidian-workflow.html) for an optional example.

## Help me improve it

If something does not work or you have an idea that would make your job search easier, [share it on GitHub](https://github.com/myowinthein/agent-compass/issues).

Agent Compass is open source under the [MIT license](https://github.com/myowinthein/agent-compass/blob/main/LICENSE).
