# Claude Compass

A Claude Code plugin for globally-minded job seekers — find countries that hire remotely or sponsor visas, then calculate realistic local-market salaries.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Background

Claude Compass is a markdown-only Claude Code plugin. There is no runtime code. Each command is a sequenced pipeline of prompt files that Claude reads and executes step by step, grounded entirely in research you provide — never in Claude's assumptions or training data.

Two pipelines:

- **Country Finder** — collects your criteria, discovers candidate countries for remote hire and visa sponsorship as two separate tracks, researches each one, scores them against your requirements, and offers an optional reality check.
- **Salary Calculator** — generates ready-to-copy research prompts for local-market salary data, ingests your research results, applies international adjustments, and produces a final salary table. Can run standalone or scoped to a single country handed off from Country Finder.

Both pipelines resume from where they left off if interrupted, using state files written to your workspace.

## Install

Requires [Claude Code](https://claude.ai/code).

In any Claude Code workspace, install the plugin:

```
/plugin install https://github.com/myowinthein/claude-compass
```

Or install from a local clone:

```
/plugin install /path/to/claude-compass
```

## Usage

Both commands require a resume. On first run, Claude will prompt you to upload one and extract it to `profile.md` in your workspace. This file is reused on all subsequent runs.

**Run the Country Finder pipeline:**

```
/claude-compass:country-finder
```

Steps: criteria intake → candidate discovery → per-country research generation → data ingestion → scoring → reality check (optional, confirm to run).

**Run the Salary Calculator pipeline:**

```
/claude-compass:salary-calculator
```

Steps: research prompt generation → data ingestion → international adjustment → final table calculation → reality check (optional, confirm to run).

**Hand off a single country from Country Finder to Salary Calculator:**

After Country Finder step 5, Claude will offer to run the Salary Calculator scoped to one country. Accept the offer or invoke the command directly:

```
/claude-compass:salary-calculator Germany
```

**State files written to your workspace:**

| File | Purpose |
|------|---------|
| `profile.md` | Extracted resume profile, shared by both pipelines |
| `situational-profile.md` | Location, citizenship, and language preferences (Country Finder) |
| `.country-finder-state.json` | Last completed step for resume support |
| `.salary-calculator-state.json` | Last completed step and target country for resume support |

## Contributing

This is a solo project. Issues and pull requests are welcome for bug reports or prompt improvements.

## License

[MIT](LICENSE)

<!-- last-reviewed: b72f7478ac3b5641272717696951a533c5579303 -->
