---
title: Known issues
nav_exclude: true
permalink: /docs/known-issues.html
description: Problems you may see when using Agent Compass in Claude or Codex, and what you can do about them.
---

# Known issues

Observations from maintainer testing and use on macOS, alongside documented platform limitations.

## Across agents

<div id="repeated-reviews-may-keep-producing-findings"></div>

<details id="answers-may-vary-between-fresh-runs" markdown="block">
<summary>Starting again can give different answers</summary>

<div class="known-issue__body" markdown="block">

Running commands such as country-finder or salary-calculator in separate sessions can produce [different results](https://platform.claude.com/docs/en/about-claude/glossary#temperature), even with the same profile and answers.

**What you can do:** Choose a more capable model with higher reasoning effort, and give clear, specific answers to the agent's questions.

</div>
</details>

## Codex CLI

<details id="questions-appear-as-plain-text-in-default-mode" markdown="block">
<summary>You may need to type your answers</summary>

<div class="known-issue__body" markdown="block">

In our testing with Codex in a terminal, some Compass questions appeared as chat messages without answer buttons. Its [Default-mode instructions](https://github.com/openai/codex/blob/main/codex-rs/collaboration-mode-templates/templates/default.md) limit when those buttons appear.

**What you can do:** Type your country, a correction to your profile or your choice to continue. You don't need to switch modes. An option shown as selected, or a question you haven't answered, does not count as your confirmation.

</div>
</details>

## Claude Desktop

<details id="the-plugin-icon-is-missing" markdown="block">
<summary>The plugin icon is missing</summary>

<div class="known-issue__body" markdown="block">

Compass supplies an icon for Codex. Its Claude package leaves out the icon setting so it can be installed in Claude Desktop. A missing icon alone does not mean Compass failed to load.

**What you can do:** Find Agent Compass by name in the plugin list. Check that it is turned on, shows the expected version and lists four skills: Country Finder, Salary Calculator, Portal Finder and Job Screener.

</div>
</details>

<details id="code-and-terminal-installations-do-not-appear-in-chatcowork" markdown="block">
<summary>Installing in Code or the terminal does not add it to Chat/Cowork</summary>

<div class="known-issue__body" markdown="block">

Claude [copies plugins one way](https://support.claude.com/en/articles/13837440-use-plugins-in-claude), from your Claude account to Claude Code. Installing Compass in the Code tab or a terminal does not add it to Chat/Cowork.

**What you can do:** Install Compass through [the plugin menu in Claude]({{ '/docs/setup/claude.html#desktop-install' | relative_url }}). Make sure it is turned on and shows four skills, then start a new chat.

</div>
</details>
