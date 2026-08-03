---
title: Home
nav_order: 1
permalink: /
---

# claude-compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="claude-compass" width="600">

A Claude Cowork plugin for globally-minded IT/tech job seekers: find remote-hire countries, visa sponsors, and local-market salaries.

**[Documentation site](https://myowinthein.github.io/claude-compass)**

## Installation

### Install

1. Open **Claude Desktop** and switch to the **Cowork** tab.
2. Open **Customize** (left sidebar), then the **Plugins** tab.
3. Click the **Add** button and select **Add marketplace**.
4. Click **Add from a repository** and paste `myowinthein/claude-compass`.
5. Once the marketplace is added, find the **claude-compass** card and click **+** to install.

### Update / Uninstall

1. Open **Customize** (left sidebar), then the **Plugins** tab.
2. Click the **Browse** button, then navigate to **Plugins → Personal** tab.
   _You'll see the marketplace entry at the top and your installed plugins as cards below._
3. To **update**:
   - Click **3 dots (…)** on the marketplace entry and select **Check for updates** (or enable **Sync automatically**).
   - Click the settings icon on the **claude-compass** card, then click **Update**.
     _The Update button only appears after the marketplace has been synced._
4. To **uninstall**: click **3 dots (⋮)** on the **claude-compass** card and click **Uninstall**.

## Usage

Type `/` in a **Cowork** task. All four commands appear listed under the **Claude Compass** section.

| Command | What it does |
|---|---|
| [`/country-finder`](https://myowinthein.github.io/claude-compass/docs/commands/country-finder.html) | Discover countries for remote hire and visa sponsorship, scored against your criteria. |
| [`/salary-calculator`](https://myowinthein.github.io/claude-compass/docs/commands/salary-calculator.html) | Calculate realistic local-market salaries for your target role. |
| [`/portal-finder`](https://myowinthein.github.io/claude-compass/docs/commands/portal-finder.html) | Find verified job portals for IT/tech roles in a specific country, grouped by type. |
| [`/job-screener`](https://myowinthein.github.io/claude-compass/docs/commands/job-screener.html) | Screen a job description against your resume and get a structured apply / maybe / skip verdict. |

Judgment-heavy and arithmetic-heavy steps can be routed to specialist subagents — Claude asks at each step whether to use Opus.

| Agent | Model | Steps |
|---|---|---|
| `deep-reasoner` | Opus / high effort | Country scoring, final ranking, international salary adjustment, final verification |
| `calculator` | Opus / max effort | Salary table calculation |

## Contributing

Issues and pull requests are welcome at [github.com/myowinthein/claude-compass/issues](https://github.com/myowinthein/claude-compass/issues).

## License

[MIT](https://github.com/myowinthein/claude-compass/blob/main/LICENSE)

<!-- last-reviewed: df9b354442e3e01790ae59f7c6eda2757e6008bf -->
