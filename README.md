---
title: Home
nav_order: 1
permalink: /
---

# claude-compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="claude-compass" width="600">

A Claude Cowork plugin for globally-minded job seekers: find remote-hire countries, visa sponsors, and local-market salaries.

**[Documentation site](https://myowinthein.github.io/claude-compass)**

## How it works

Both commands follow a structured pipeline. Research steps are intentionally manual: Claude generates ready-to-copy prompts, you run them yourself (in a web search, a separate Claude session, or any research tool), then paste the results back. Claude ingests and processes what you provide.

This design is deliberate. Job market conditions, visa policies, and salary data change faster than any model's training. Grounding every decision in research you supply — with real sources and dates — produces results that are accurate to now, not to whenever Claude was last trained.

**What gets written to your workspace:**
- `profile.md` — your extracted resume profile, reused across sessions
- `situational-profile.md` — your location, citizenship, and language answers
- `.country-finder-state.json` / `.salary-calculator-state.json` — pipeline progress, enables resume on interruption
- `remote-candidates.md`, `sponsorship-candidates.md`, `country-research.md` — research you paste in

All data stays in your Cowork workspace. No information is sent to any external service.

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

Type `/` in a **Cowork** task. Both commands appear listed under the **Claude Compass** section.

| Command | What it does |
|---|---|
| [`/country-finder`](docs/commands/country-finder.md) | Discover countries for remote hire and visa sponsorship, scored against your criteria. |
| [`/salary-calculator`](docs/commands/salary-calculator.md) | Calculate realistic local-market salaries for your target role. Runs standalone or scoped to a single country handed off from Country Finder. |

Judgment-heavy and arithmetic-heavy steps are automatically routed to specialist subagents.

| Agent | Model | Steps |
|---|---|---|
| `deep-reasoner` | Opus / high effort | Country scoring, international salary adjustment, reality checks |
| `calculator` | Opus / max effort | Final salary table calculation |

## Contributing

Issues and pull requests are welcome at [github.com/myowinthein/claude-compass/issues](https://github.com/myowinthein/claude-compass/issues).

## License

[MIT](LICENSE)

<!-- last-reviewed: f008d61141ce661602056e50383ef1f35474c424 -->
