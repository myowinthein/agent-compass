# claude-compass

Trust your compass.

<img src="docs/images/banner.png" alt="claude-compass" width="600">

A Claude Code plugin for globally-minded job seekers. Slash commands to discover countries for remote hire or visa sponsorship, calculate realistic local-market salaries, and ground every decision in real research — not guesswork.

## Install

```bash
# Register this repo as a marketplace on your machine. Runs once.
/plugin marketplace add myowinthein/claude-compass

# Install the claude-compass plugin from the registered marketplace.
/plugin install claude-compass@claude-compass

# Pull the latest version when a new release ships.
/plugin update claude-compass@claude-compass

# Remove the plugin from your machine.
/plugin uninstall claude-compass@claude-compass

# Apply changes after install, update, or uninstall.
/reload-plugins
```

## Usage

Both commands require a resume. On first run, Claude prompts you to upload one and extracts it to `profile.md` in your workspace. This file is reused on all subsequent runs. Both pipelines resume from where they left off if interrupted.

### Commands

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
