---
title: Known issues
nav_exclude: true
permalink: /docs/known-issues.html
---

# Known issues

Observations from maintainer testing and use on macOS, alongside documented platform limitations. Platform documentation was checked on **28 October 2026**.

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
