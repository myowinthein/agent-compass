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

**Observed:** Claude and Codex have sometimes [skipped rules or command steps](https://github.com/anthropics/claude-code/issues/18454), [stopped before completion](https://github.com/openai/codex/issues/36596), or [changed a required output format](https://github.com/openai/codex/issues/25673).

[Written instructions do not guarantee consistent execution](https://code.claude.com/docs/en/best-practices#deterministic-and-non-deterministic-instructions). Point out the missed requirement and ask the agent to resume from the last verified step. Check the actual result before accepting a completion claim.

</details>

<details id="repeated-reviews-may-keep-producing-findings" markdown="block">
<summary>Repeated reviews may keep producing findings</summary>

**Observed:** Repeating a review in fresh Claude or Codex sessions has produced new findings after earlier fixes.

Studies of specific models report [inconsistent reviews](https://arxiv.org/abs/2502.20747) and [unnecessary corrections](https://link.springer.com/article/10.1007/s10515-026-00638-5). Keep the review scope consistent, require evidence for defects, and separate optional improvements from required fixes. A no-findings result applies only to the checked scope.

</details>

## Codex CLI

<details id="questions-appear-as-plain-text-in-default-mode" markdown="block">
<summary>Questions appear as plain text in Default mode</summary>

**Observed:** Compass's questions appeared as plain text in Default mode, requiring a typed reply. Native single-choice selection and custom text replies worked in Plan mode and the desktop app.

OpenAI describes [Plan mode](https://learn.chatgpt.com/docs/learn/best-practices#plan-first-for-difficult-tasks) as planning before implementation. In Default mode, type your choice or text to continue.

</details>

## Claude Desktop

<details id="the-plugin-icon-is-missing" markdown="block">
<summary>The plugin icon is missing</summary>

**Observed:** Compass's custom icon did not appear in Claude Desktop.

Claude Code ignores the [manifest icon field](https://code.claude.com/docs/en/plugins-reference#directory-listing-fields), which is used for directory listings. The cause in Chat/Cowork remains unconfirmed.

</details>

<details id="code-and-terminal-installations-do-not-appear-in-chatcowork" markdown="block">
<summary>Code and terminal installations do not appear in Chat/Cowork</summary>

**Observed:** Installing a plugin through the desktop app's **Code** tab or the **terminal** does not add it to the account's **Claude (Chat + Cowork)** plugin library.

Anthropic documents [one-way plugin sync](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) from Claude (Chat + Cowork) to Claude Code. Code and terminal installs do not sync back.

</details>
