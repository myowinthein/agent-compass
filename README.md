---
title: Home
nav_order: 1
permalink: /
---

# claude-compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="claude-compass" width="600">

A plugin for Claude Cowork, Claude Code, and Codex, built for globally-minded IT/tech job seekers: find remote-hire countries, visa sponsors, and local-market salaries.

**[Documentation site](https://myowinthein.github.io/claude-compass)**

## Installation

### Claude Cowork

1. Open **Claude Desktop** and switch to the **Cowork** tab.
2. Open **Customize** (left sidebar), then the **Plugins** tab.
3. Click the **Add** button and select **Add marketplace**.
4. Click **Add from a repository** and paste `myowinthein/claude-compass`.
5. Once the marketplace is added, find the **claude-compass** card and click **+** to install.

### Claude Code

```text
/plugin marketplace add myowinthein/claude-compass
/plugin install claude-compass@claude-compass-marketplace
```

### Codex

Add the same repository marketplace and install the plugin:

```bash
codex plugin marketplace add myowinthein/claude-compass
codex plugin add claude-compass@claude-compass-marketplace
```

Then start a new chat in a writable folder for your career research. In the desktop app, you can also open the Plugins directory, select the added marketplace, and install Claude Compass there.

For local development, replace `myowinthein/claude-compass` in the marketplace-add command with the absolute path to this checkout. Local changes must be refreshed/reinstalled before the installed copy sees them.

The existing Claude-compatible manifest is shared by both platforms; there is no second plugin metadata source. See the [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins) for compatibility and marketplace support.

### Update / Uninstall in Claude Cowork

1. Open **Customize** (left sidebar), then the **Plugins** tab.
2. Click the **Browse** button, then navigate to **Plugins → Personal** tab.
   _You'll see the marketplace entry at the top and your installed plugins as cards below._
3. To **update**:
   - Click **3 dots (…)** on the marketplace entry and select **Check for updates** (or enable **Sync automatically**).
   - Click the settings icon on the **claude-compass** card, then click **Update**.
     _The Update button only appears after the marketplace has been synced._
4. To **uninstall**: click **3 dots (⋮)** on the **claude-compass** card and click **Uninstall**.

### Update / Uninstall in Codex

```bash
codex plugin marketplace upgrade claude-compass-marketplace
codex plugin add claude-compass@claude-compass-marketplace
```

For uninstalling, run `codex plugin remove claude-compass@claude-compass-marketplace` or remove the plugin in the desktop Plugins directory.

## Usage

The four command names are the same on both platforms. In Cowork or Claude Code, type `/` and choose the command under Claude Compass, or use `/claude-compass:country-finder`. In Codex CLI, type `$` and choose the matching skill (for example `country-finder`, which may be displayed with the `claude-compass:` namespace), or open `/skills`. In the desktop app, select the skill from the composer. The host controls the invocation prefix: Claude uses `/`, Codex CLI uses `$`. See [Codex skill invocation](https://learn.chatgpt.com/docs/build-skills) and [Cowork plugin commands](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

| Command | What it does |
|---|---|
| [`/country-finder`](https://myowinthein.github.io/claude-compass/docs/commands/country-finder.html) | Discover countries for remote hire and visa sponsorship, scored against your criteria. |
| [`/salary-calculator`](https://myowinthein.github.io/claude-compass/docs/commands/salary-calculator.html) | Calculate realistic local-market salaries for your target role. |
| [`/portal-finder`](https://myowinthein.github.io/claude-compass/docs/commands/portal-finder.html) | Find verified job portals for IT/tech roles in a specific country, grouped by type. |
| [`/job-screener`](https://myowinthein.github.io/claude-compass/docs/commands/job-screener.html) | Screen a job description against your resume and get a structured apply / maybe / skip verdict. |

Judgment-heavy and arithmetic-heavy steps can be routed to specialist subagents. Claude offers Opus at each eligible step; Codex offers a specialist using your current or configured Codex model and reasoning settings. Delegation is optional, and final ranking and salary verification always run. If the host cannot delegate, the current model runs the step.

| Agent | Claude | Codex | Steps |
|---|---|---|---|
| `deep-reasoner` | Opus / high effort | Current or configured model/effort | Country scoring, final ranking, international salary adjustment, final verification |
| `calculator` | Opus / max effort | Current or configured model/effort | Salary table calculation |

Use one workspace for one candidate. Both hosts read and write the same `profile.md`, `situational-profile.md`, `.country-finder-state.json`, `.salary-calculator-state.json`, and `cf-*` / `sc-*` output files, so you can resume a completed step on either host. Run one pipeline at a time in a workspace.

Country Finder, Salary Calculator, and Portal Finder require live web access. When isolated research agents or browsing are unavailable, the research pipelines provide prompts for you to run manually. Portal Finder reports when live verification is unavailable. A resume can be pasted or supplied as a readable local file when your client does not support attachments.

## Shared source

`commands/` contains Claude entry points and `skills/<command>/SKILL.md` contains portable entry points. Both load the same orchestrators in `workflows/`, the same step instructions in `prompts/`, and the same shared rule files. Specialist procedures also live once in `prompts/shared/`; Claude agent files only select their model and point to those procedures. Install the complete plugin, not individual skill folders, because the entry points reference its shared resources.

## Contributing

Run `ruby scripts/validate_plugin.rb` to check entry points, resource references, and a relocated installation. Run `bundle exec rake test` for the documentation site. Contributor guidance lives in `AGENTS.md`; `CLAUDE.md` imports it.

Issues and pull requests are welcome at [github.com/myowinthein/claude-compass/issues](https://github.com/myowinthein/claude-compass/issues).

## License

[MIT](https://github.com/myowinthein/claude-compass/blob/main/LICENSE)

<!-- last-reviewed: 0db57abc536b929c52e12ed4aa460d700b71c8c7 -->
