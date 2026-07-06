# claude-compass

Trust your compass.

<img src="docs/images/banner.png" alt="claude-compass" width="600">

A Claude Code plugin for globally-minded job seekers. Slash commands to discover countries for remote hire or visa sponsorship, calculate realistic local-market salaries, and ground every decision in real research — not guesswork.

## Installation

### Install

1. Open Claude Desktop and switch to the Cowork tab.
2. Open Customize (left sidebar), then the Plugins tab.
3. Click the + button under Personal plugins, then select "Add marketplace."
4. Paste this repository: myowinthein/claude-compass
5. Once added, find claude-compass in the plugin browser and click Install.

### Update

1. Open Customize, then the Plugins tab.
2. Find the claude-compass-marketplace entry and click "Update" to pull the latest version from this repository.
3. If you've edited any plugin files locally, Cowork will warn you before an update overwrites those changes.

### Uninstall

1. Open Customize, then the Plugins tab.
2. Open the installed claude-compass plugin.
3. Click "Uninstall."

### Usage

Once installed, type / in a Cowork task. Both commands appear listed under the Claude Compass section:

- country-finder
- salary-calculator

Select the one you want to run.

## Commands

| Command | What it does |
|---|---|
| `/claude-compass:country-finder` | Discover countries for remote hire and visa sponsorship, scored against your criteria. |
| `/claude-compass:salary-calculator` | Calculate realistic local-market salaries for your target role. Runs standalone or scoped to a single country handed off from Country Finder. |

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
