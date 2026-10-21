# Agent Compass

## Project

This repository packages the same four career research workflows for Claude and Codex. Plugin identity and version are maintained only in `.claude-plugin/plugin.json`. Keep the plugin name `agent-compass` and existing workflow command names stable.

Project configuration:

```text
git-strategy: solo
git-auto-commit: true
readme-style: custom
```

## Contributor review preference

When consulting Claude for project reviews or discussions, explicitly use Claude Opus 5.5 at high effort: `claude --model claude-opus-5-5 --effort high`. Record the requested settings and check the returned model metadata. If the requested configuration is unavailable, ask before substituting another model or effort.

This is the user's preferred pairing with GPT-6.1 Sol at high effort, not a claim of equivalent capability or reasoning budget. It does not change the plugin's bundled specialist routing or global client settings.

## Shared sources

- `skills/<command>/SKILL.md`: portable entry points. These only reference the shared runtime and their corresponding workflow.
- `commands/<command>.md`: Claude command adapters. These only reference the portable entry points and pass through arguments.
- `workflows/<command>.md`: the single source of orchestration for each workflow.
- `prompts/<command>/`: canonical step instructions, output formats, and domain decisions.
- `prompts/shared/runtime.md`: packaged resource paths, workspace state tracking, host-specific delegation, and research fallback.
- `prompts/shared/deep-reasoner.md` and `prompts/shared/calculator.md`: canonical specialist procedures. `agents/*.md` select Claude models, declare each role's effort once for both hosts, and reference these files. Codex model selection and fallback behavior belong in the shared runtime, not a second agent definition.
- `skills/*.md`: shared rule references; these flat files are explicitly read by step prompts, not discoverable Agent Skills.
- `skills/salary-comparison-rules.md` and `skills/timezone-rules.md`: canonical currency/pay-basis and timezone/DST policies. Research briefs embed applicable rules as literal text so isolated researchers do not need workspace or package access.
- `helpers/compass.py` and `helpers/compass_lib/`: shared mechanical operations for both hosts. `skills/helper-runtime.md` routes to concise research, comparison and output interfaces. Only `ingest` writes the existing research/stored-data files; state checks are read-only. Keep semantic judgment in prompts, not code or host adapters.
- `helpers/salary_targets.py`: unchanged v1 consumer interface for salary arithmetic, reused by the shared renderer rather than forked.
- `data/output-contracts.json`: single readable source for fixed display tokens, bounds and batching size. Python and approved manual runs read the same file. Prose may explain semantic predicates and docs may show checked examples, but do not duplicate runtime template/enum definitions.
- `data/default-preferred-countries.md`: shipped Country Finder default search scope.
- `.claude-plugin/marketplace.json`: shared Claude-compatible marketplace. Do not duplicate the manifest's description or version here.
- `assets/icon.png`: the single shared plugin icon. The manifest's Claude `icon` and Codex `interface.logo`/`interface.composerIcon` fields point to this same file. Codex reads `interface` from the shared compatibility manifest; Claude ignores that field with an expected validation warning. Do not add a second identity manifest or duplicate the image to remove that warning. Claude's documented icon support is for Anthropic directory listings, not a guarantee for custom GitHub installs.

Keep behavioral instructions in those sources, never copy them into platform adapters. For a change to scoring, evidence handling, sponsorship thresholds, profile intake, or output formatting, read the relevant step and its referenced shared rules before editing. Preserve the existing file names and schemas for candidate profiles, state, and step outputs so users can resume across hosts.

Bundled resources are read from the installed plugin root. Candidate data and output files belong to the consumer's selected workspace. The plugin uses Markdown instructions and standard-library Python mechanics, not an API application or service. Profiles, state schemas and filenames remain compatible; completed workflows replay without migration.

## Verification

- `ruby scripts/validate_plugin.rb`: check entry names, shared references, and a relocated package with a separate consumer workspace. No external dependencies required.
- `ruby scripts/test_plugin.rb`: regress non-UTF-8 validation, check the compact salary table, threshold states and published arithmetic examples, check Country Finder's table contract and documentation edge cases, and verify Git archive exclusions. These contributor checks use Git and are not live model/workflow tests.
- `ruby scripts/test_salary_targets.rb`: run the shared Python CLI against an independent Ruby Rational oracle, fictional inputs, recalibration, invalid inputs and a relocated read-only package. Requires Python 3.11+. No live research or candidate files.
- `python3 -B scripts/test_compass.py`: offline consumer checks for shared operations, byte-preserving ingestion, golden tables, exact comparisons, read-only state, legacy boundaries, encoding, failure/retry and relocated packaging. Fixtures are temporary and fictional, not live browser evidence.
- `bundle exec rake test`: validate the plugin, build the Jekyll site, and check its internal HTML links/images/scripts. Required after documentation or site configuration changes.
- `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate skills`: native manifest and skill validation when the `claude` CLI is available.

`docs/` is both user documentation and the GitHub Pages site. Update affected pages whenever behavior changes; search references across `docs/`, `workflows/`, `prompts/`, and `skills/`. Keep documentation summaries explanatory; runtime rules belong in prompts. Prose in `docs/` avoids em dashes.

## Documentation deployment

`.github/workflows/docs.yml` runs the full checks on pushes to `main`, pull requests and manual runs. Its Python matrix covers the minimum and current supported Python on Linux, macOS and Windows; the site build waits for these checks. Only successful `main` builds deploy. There is no schedule. `_config.yml` uses `@latest`; each workflow run resolves the latest stable theme release and temporarily pins that tag for its build, without committing a version change. A failed release lookup stops the build rather than falling back to the development branch.

When enabling this workflow, change the repository's **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. Merge the workflow and configuration together before deploying. Locally, `bundle exec rake test` and `bundle exec jekyll serve` resolve `@latest` through the remote-theme plugin; restart the preview to fetch a newer release.

## Maintenance boundaries

Preserve unrelated user edits. Do not create or modify `.claude/rules` without an explicit request. Do not inspect or edit `.claude/helm/*-log.json` during feature work; these are tool ledgers, not source code. Repository contributor instructions are not automatically installed as consumer workflow context; runtime requirements must be reachable from the skill entry points.
