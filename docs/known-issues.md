---
title: Known issues
nav_exclude: true
permalink: /docs/known-issues.html
description: Review observed Agent Compass limitations in Claude and Codex, including instruction following, question handling, plugin display and installation behavior.
---

# Known issues

Observations from maintainer testing and use on macOS, alongside documented platform limitations.

## Across agents

<details id="instructions-and-workflow-steps-may-not-be-followed-consistently" markdown="block">
<summary>Instructions and workflow steps may not be followed consistently</summary>

<div class="known-issue__body" markdown="block">

Claude and Codex have sometimes skipped Compass steps, stopped early or changed a required report format. [Written instructions do not guarantee execution](https://code.claude.com/docs/en/best-practices#deterministic-and-non-deterministic-instructions).

**What you can do:** Point out the missed step and ask the agent to resume from the last verified point. Check that research supports the country recommendations, salary targets or portal links, and that screening answers use your confirmed profile.

</div>
</details>

<div id="repeated-reviews-may-keep-producing-findings"></div>

<details id="answers-may-vary-between-fresh-runs" markdown="block">
<summary>Answers may vary between fresh runs</summary>

<div class="known-issue__body" markdown="block">

Fresh runs can give different country rankings, salary estimates, portal lists or screening answers, even when you repeat the same profile and answers. [Model responses aren't fully repeatable](https://platform.claude.com/docs/en/about-claude/glossary#temperature), and new research can find different sources.

**What you can do:** Compare the profile, preferences, evidence and reasoning behind meaningful differences. To revisit existing research, choose a saved-result view instead of starting fresh. Job Screener results stay in chat.

</div>
</details>

## Codex CLI

<details id="questions-appear-as-plain-text-in-default-mode" markdown="block">
<summary>Questions appear as plain text in Default mode</summary>

<div class="known-issue__body" markdown="block">

In maintainer testing, some Compass intake and confirmation questions in Codex CLI Default mode needed a typed reply. Codex's [Default-mode instructions](https://github.com/openai/codex/blob/main/codex-rs/collaboration-mode-templates/templates/default.md) restrict when its question picker is used.

**What you can do:** Type your country, profile correction or choice to continue. You don't need to change modes. An unanswered question or preselected option isn't confirmation.

</div>
</details>

## Claude Desktop

<details id="the-plugin-icon-is-missing" markdown="block">
<summary>The plugin icon is missing</summary>

<div class="known-issue__body" markdown="block">

Compass includes custom icon metadata for Codex but omits it from the Claude package for Desktop compatibility. A missing icon alone doesn't tell you whether its workflows loaded.

**What you can do:** Find Agent Compass by name and check its enabled state, version and four listed skills: Country Finder, Salary Calculator, Portal Finder and Job Screener.

</div>
</details>

<details id="code-and-terminal-installations-do-not-appear-in-chatcowork" markdown="block">
<summary>Code and terminal installations do not appear in Chat/Cowork</summary>

<div class="known-issue__body" markdown="block">

Anthropic's [one-way plugin sync](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) runs from the Claude account to Claude Code. Installing Compass in Code or the terminal doesn't add it to Chat/Cowork.

**What you can do:** Install Compass through [Claude's plugin interface]({{ '/docs/setup/claude.html#desktop-install' | relative_url }}). Check that it's enabled and lists four skills, then start a fresh chat.

</div>
</details>
