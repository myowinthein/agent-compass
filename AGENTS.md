# Agent Compass

## Project

This repository packages the same four career research workflows for Claude and Codex. Plugin identity and version are maintained only in `.claude-plugin/plugin.json`. Keep the plugin name `agent-compass` and existing workflow command names stable.

Project configuration:

```text
git-strategy: solo
git-auto-commit: true
readme-style: custom
```

## Shared sources

- `skills/<command>/SKILL.md`: portable entry points. These only reference the shared runtime and their corresponding workflow.
- `commands/<command>.md`: Claude command adapters. These only reference the portable entry points and pass through arguments.
- `workflows/<command>.md`: the single source of orchestration for each workflow.
- `prompts/<command>/`: canonical step instructions, output formats, and domain decisions.
- `prompts/shared/runtime.md`: packaged resource paths, workspace state tracking, host-specific delegation, and research fallback.
- `prompts/shared/deep-reasoner.md` and `prompts/shared/calculator.md`: canonical specialist procedures. `agents/*.md` select Claude models, declare each role's effort once for both hosts, and reference these files. Codex model selection and fallback behavior belong in the shared runtime, not a second agent definition.
- `skills/*.md`: shared rule references; these flat files are explicitly read by step prompts, not discoverable Agent Skills.
- `skills/salary-comparison-rules.md` and `skills/timezone-rules.md`: canonical currency/pay-basis and timezone/DST policies. Research briefs embed applicable rules as literal text so isolated researchers do not need workspace or package access.
- `data/default-preferred-countries.md`: shipped Country Finder default search scope.
- `.claude-plugin/marketplace.json`: shared Claude-compatible marketplace. Do not duplicate the manifest's description or version here.

Keep behavioral instructions in those sources, never copy them into platform adapters. For a change to scoring, evidence handling, sponsorship thresholds, profile intake, or output formatting, read the relevant step and its referenced shared rules before editing. Preserve the existing file names and schemas for candidate profiles, state, and step outputs so users can resume across hosts.

Bundled resources are read from the installed plugin root. Candidate data and output files belong to the consumer's selected workspace. The plugin is a set of Markdown instructions, not an API application or service.

## Verification

- `ruby scripts/validate_plugin.rb`: check entry names, shared references, and a relocated package with a separate consumer workspace. No external dependencies required.
- `ruby scripts/test_plugin.rb`: regress non-UTF-8 validation, check the compact salary table, threshold states and published arithmetic examples, check Country Finder's table contract and documentation edge cases, and verify Git archive exclusions. These contributor checks use Git and are not live model/workflow tests.
- `bundle exec rake test`: validate the plugin, build the Jekyll site, and check its internal HTML links/images/scripts. Required after documentation or site configuration changes.
- `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate skills`: native manifest and skill validation when the `claude` CLI is available.

`docs/` is both user documentation and the GitHub Pages site. Update affected pages whenever behavior changes; search references across `docs/`, `workflows/`, `prompts/`, and `skills/`. Keep documentation summaries explanatory; runtime rules belong in prompts. Prose in `docs/` avoids em dashes.

## Maintenance boundaries

Preserve unrelated user edits. Do not create or modify `.claude/rules` without an explicit request. Do not inspect or edit `.claude/helm/*-log.json` during feature work; these are tool ledgers, not source code. Repository contributor instructions are not automatically installed as consumer workflow context; runtime requirements must be reachable from the skill entry points.
