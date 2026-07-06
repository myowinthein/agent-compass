# claude-compass

Trust your compass.

<img src="docs/images/banner.jpg" alt="claude-compass" width="600">

A Claude Code plugin for globally-minded job seekers. Slash commands to discover countries for remote hire or visa sponsorship, calculate realistic local-market salaries, and ground every decision in real research — not guesswork.

## Installation

### Install

1. Open **Claude Desktop** and switch to the **Cowork** tab.
2. Open **Customize** (left sidebar), then the **Plugins** tab.
3. Click the **Add** button and select **Add marketplace**.
4. Click **Add from a repository** and paste `myowinthein/claude-compass`.
5. Once the marketplace is added, find the **claude-compass** card and click **+** to install.

### Update / Uninstall

1. Open **Customize** (left sidebar), then the **Extensions** tab.
2. Click **Browse extensions**, then navigate to **Plugins → Personal** tab. _You'll see the marketplace entry at the top and your installed plugins as cards below._
3. To **update**:
   - Click **...** on the marketplace entry and select **Check for updates** (or enable **Sync automatically**).
   - Open the **claude-compass** card, click **Manage**, then click **Update**. _The Update button only appears after the marketplace has been synced._
4. To **uninstall**: open the **claude-compass** card and click **Uninstall**.

## Commands

Once installed, type `/` in a **Cowork** task. Both commands appear listed under the **Claude Compass** section.

| Command | What it does |
|---|---|
| [`/country-finder`](docs/commands/country-finder.md) | Discover countries for remote hire and visa sponsorship, scored against your criteria. |
| [`/salary-calculator`](docs/commands/salary-calculator.md) | Calculate realistic local-market salaries for your target role. Runs standalone or scoped to a single country handed off from Country Finder. |

### Agents

Judgment-heavy and arithmetic-heavy steps are automatically routed to specialist subagents rather than running on the default model.

| Agent | Model | Steps |
|---|---|---|
| `deep-reasoner` | Opus / high effort | Country scoring, international salary adjustment, reality checks |
| `calculator` | Opus / max effort | Final salary table calculation |

## Contributing

Issues and pull requests are welcome at [github.com/myowinthein/claude-compass/issues](https://github.com/myowinthein/claude-compass/issues).

## License

[MIT](LICENSE)

<!-- last-reviewed: 592aca1d6a71f53cc3273aa66d7602694bd92948 -->
