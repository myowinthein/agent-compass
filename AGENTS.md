# Agent Compass

## Project Identity

Agent Compass packages four career research workflows for Claude and Codex: `country-finder`, `salary-calculator`, `portal-finder` and `job-screener`. It is a Markdown instruction plugin with standard-library Python mechanics, plus a Jekyll documentation site, rather than an API application or service.

## Project Config

- ship-method: direct
- git-auto-commit: true
- git-merge-strategy: squash
- readme-style: custom

## Dev Commands

Run commands from the repository root. Helpers require Python 3.11+; Ruby checks use REXML and Bundler, and site checks also need Node. CI uses Ruby 3.4 and Python 3.11/3.14.

| Command | Purpose |
|---|---|
| `bundle exec rake test` | Full plugin/helper checks, site JavaScript tests, Jekyll build and internal HTML/link/image/script checks; required after documentation or site configuration changes. |
| `bundle exec rake plugin_test` | Plugin validation and offline Python/Ruby helper regressions. |
| `ruby scripts/validate_plugin.rb` | Four skill entries, shared resources/icon and a relocated package with a separate consumer workspace. |
| `ruby scripts/test_plugin.rb` | Validation edge cases, published arithmetic/table examples, archive attributes and deployment contracts. |
| `ruby scripts/test_salary_targets.rb` | Salary CLI checks against an independent Ruby Rational oracle. |
| `python3 -B scripts/test_compass.py` | Offline consumer checks, golden outputs, legacy names, ingestion/retry, state, encoding and relocation. |
| `bundle exec jekyll serve` | Local documentation preview. |
| `bundle exec rake client_test` | Optional native discovery regression; requires both Claude and Codex CLIs, uses temporary installations and makes no model calls. |
| `ruby scripts/check_clients.rb --installed` | Inspect inventories after separately updating installed copies. |

When the Claude CLI is available, native validation uses `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate skills`. Offline checks use fictional fixtures; passing them does not establish live research accuracy or model/workflow compliance.

## Architecture Pointers

- `.claude-plugin/plugin.json` is the sole identity/version source. Keep `agent-compass` and all four workflow names stable. The marketplace references this package without duplicating its version or description.
- `skills/<command>/SKILL.md` are the four portable entry points. Each only loads the shared runtime and its workflow. Keep `commands: []`; legacy command adapters and generated `source-command-*` entries create duplicate discovery.
- `workflows/<command>.md` owns orchestration; `prompts/<command>/` owns step behavior, judgment and output instructions. Flat `skills/*.md` files are explicitly loaded rule/interface references, not discoverable skills.
- `prompts/shared/runtime.md` owns installed-resource resolution, parent/checkpoint responsibilities, research isolation/fallback and host-specific specialist routing. `prompts/shared/question-mechanism.md` adapts existing questions to actual host capabilities without adding approval gates.
- `prompts/shared/deep-reasoner.md` and `calculator.md` are the specialist procedures. `agents/*.md` selects Claude models and declares each role's effort for both hosts; Codex model selection belongs in the shared runtime.
- `helpers/compass.py` and `helpers/compass_lib/` supply shared mechanics, routed through `skills/helper-runtime.md`. Only `ingest` writes research/stored-data files; state checks are read-only. Semantic decisions remain in prompts.
- `helpers/salary_targets.py` retains its v1 consumer interface and is reused by the shared renderer. `data/output-contracts.json` alone defines fixed display tokens, rounding/bounds and batching size for Python and approved manual runs.
- `data/workspace-files.json` is the sole current/legacy artifact registry. `helpers/compass_lib/files.py` and `skills/workspace-files.md` implement the same read-only resolution policy.
- Bundled resources come from the actual installed plugin root. Candidate profiles, research, workflow outputs and checkpoints belong to the consumer's separately selected workspace.

## Domain Rules

Before changing intake, evidence handling, scoring, sponsorship, arithmetic or output formatting, read the affected step prompt and its referenced shared rules. Keep behavioral instructions in these shared sources rather than platform adapters or Python judgment code.

- Preserve `profile.md`, `situational-profile.md`, the existing two-field checkpoint schema and saved artifacts. Existing current/legacy runs keep their resolved filenames, including missing later artifacts; duplicate spellings for one artifact require clarification rather than migration, merging or copies. Completed runs replay saved finals.
- The parent owns questions, confirmations, aggregate research and checkpoint advancement. Fresh research tasks receive literal candidate facts/rules; fresh context is not a filesystem sandbox.
- For research collection/validation changes, read `skills/data-validation-rules.md` and `skills/research-helper.md`. Accepted bytes and original duplicates are preserved; validation metadata stays outside country blocks. Ingestion is atomic per file, not across both files, so partial failures require readback and fresh hashes before retry.
- Country Finder prioritizes explicit Includes, then offers Salary Calculator's recorded research scope as names only with confirmation, otherwise its shipped default. This scope retains countries omitted from salary tables and requires neither salary completion nor substantive compatibility. Keep this separate from readiness/compatibility gates for substantive transfers; optional upstream data never blocks a standalone workflow or changes a resumed scope.
- Country Finder assesses Remote and Sponsorship independently across all Step 2 countries. Missing evidence differs from weak fit and explicit exclusion. The post-audit Summary owns final fits; the Priority Table supplies presentation order.
- Salary Calculator researches two independent local-employee gross annual base-pay tiers, not cross-border remote offers. Unsupported adjustments are skipped rather than changed to zero. `skills/salary-comparison-rules.md` and `skills/sponsorship-threshold-rules.md` own comparable currency/pay basis/period, unrounded comparisons and official monthly legal-pay support; targets, hard floors and visa rules stay separate.
- `skills/timezone-rules.md` owns hub and seasonal/DST coverage; helper offsets only describe supplied dates. Portal Finder needs opened relevant sources. Job Screener needs an explicit mandatory condition plus confirmed inability for each blocker, and retains its exact conditional report format.
- Portal Finder and Job Screener intentionally have no automatic exports or checkpoints.

## Documentation and Distribution

`docs/` is both user documentation and the GitHub Pages site. Update affected pages when behavior changes and search references across `docs/`, `workflows/`, `prompts/` and `skills/`. Documentation summaries explain behavior; runtime rules stay in prompts. New documentation prose avoids em dashes.

Setup content lives in `_includes/setup/`, composed by `_includes/setup-tabs.html`; the JavaScript and legacy redirects preserve desktop/terminal deep links. Check their tests when changing setup navigation.

`.github/workflows/docs.yml` runs checks on main pushes, pull requests and manual runs, with no schedule. Its Python matrix spans Linux/macOS/Windows; the site build waits for it. Only successful main builds deploy. Hosted Pages must use GitHub Actions as its source.

`_config.yml` uses `just-the-docs@latest`. CI resolves the latest stable release and temporarily pins it for that build; failed lookup stops the build. Local builds resolve through the remote-theme plugin; restart the preview to fetch a newer release.

## Contributor Review Preference

When consulting Claude for a project review/discussion or running Claude workflow tests, request `claude --model claude-sonnet-5-5 --effort high`. Record the requested settings and check returned model metadata; ask before substituting an unavailable configuration. This preference does not change bundled specialist routing or global client settings.

## Known Traps

- `.claude-plugin/plugin.json` is the shared Claude manifest and supported Codex compatibility layout. A separate root identity manifest creates competing ownership. Cross-platform symlink installation needs actual native discovery testing.
- `assets/icon.svg` is the single static vector icon, shared by Claude `icon` and Codex `interface.logo`/`composerIcon`. Claude's ignored `interface` field can produce an expected validation warning; its directory icon support does not guarantee custom GitHub-install display.
- Native discovery tests inspect Codex's actual `skills/list` catalog, not merely `plugin/read`. They check discovery, not model behavior.
- Archive exclusions in `.gitattributes` and their regression checks currently cover legacy `.claude/helm/`, but not tracked canonical `.helm/` records. This is a known packaging gap requiring separate maintenance.

## Rules

For repository contributor work, read and follow these shared local rules on both Claude and Codex:

- .claude/rules/git.md
- .claude/rules/safety.md
- .claude/rules/writing.md

These contributor copies are not dependencies of the Compass workflows.

<!-- last-reviewed: 08aafa31bb383277b7f56d12252dbab535c47b07 -->
