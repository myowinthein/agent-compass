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
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake test` | Full plugin/helper checks, site JavaScript tests, Jekyll build and internal HTML/link/image/script checks; required after documentation or site configuration changes. |
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake plugin_test` | Plugin validation and offline Python/Ruby helper regressions. |
| `ruby scripts/validate_plugin.rb` | Four skill entries, shared resources/icon and a relocated package with a separate consumer workspace. |
| `ruby scripts/test_plugin.rb` | Validation edge cases, published arithmetic/table examples, archive attributes and deployment contracts. |
| `ruby scripts/test_salary_targets.rb` | Salary CLI checks against an independent Ruby Rational oracle. |
| `python3 -B scripts/test_compass.py` | Offline consumer checks, golden outputs, legacy names, ingestion/retry, state, encoding and relocation. |
| `python3 -B scripts/test_workflow_replay.py --host claude` or `--host codex` | Optional acceptance replays through the host CLI with fictional data and simulated web evidence. It calls the model and is not part of `rake test`. |
| `cd docs && bundle exec jekyll serve` | Local documentation preview. |
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake client_test` | Optional native discovery regression; requires both Claude and Codex CLIs, uses temporary installations and makes no model calls. |
| `ruby scripts/check_clients.rb --installed` | Inspect inventories after separately updating installed copies. |

When the Claude CLI is available, native validation uses `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate skills`. Offline checks use fictional fixtures; passing them does not establish live research accuracy or model/workflow compliance.

## Architecture Pointers

- `.claude-plugin/plugin.json` owns shared identity/version metadata; `.codex-plugin/plugin.json` mirrors it and adds Codex presentation. Packaging checks require exact shared-field parity. Keep `agent-compass` and all four workflow names stable. The marketplace references this package without duplicating its version or description.
- `skills/<command>/SKILL.md` are the four portable entry points. Each only loads the shared runtime and its workflow. Omit `commands` from both manifests and keep `commands/` absent; legacy adapters and generated `source-command-*` entries create duplicate discovery.
- `workflows/<command>.md` owns orchestration; `prompts/<command>/` owns step behavior, judgment and output instructions. Flat `skills/*.md` files are explicitly loaded rule/interface references, not discoverable skills.
- `prompts/shared/runtime.md` owns installed-resource resolution, parent/checkpoint responsibilities, research isolation/fallback and host-specific specialist routing. `prompts/shared/question-mechanism.md` adapts existing questions to actual host capabilities without adding approval gates.
- `prompts/shared/deep-reasoner.md` and `calculator.md` are the specialist procedures. `agents/*.md` selects Claude models and declares each role's effort for both hosts; Codex model selection belongs in the shared runtime.
- `helpers/compass.py` and `helpers/compass_lib/` supply shared mechanics, routed through `skills/helper-runtime.md`. `workspace-base` resolves the fixed home storage base and creates it only on request; `run-start` creates that base when absent, isolated chat/person/command run folders and optional confirmed profile copies; `ingest` writes research/stored-data files. Run listing and state checks are read-only. Semantic decisions remain in prompts.
- `helpers/salary_targets.py` retains its v1 consumer interface and is reused by the shared renderer. `data/output-contracts.json` alone defines fixed display tokens, rounding/bounds and batching size for Python and approved manual runs.
- `data/workspace-files.json` is the sole current/legacy artifact registry. `helpers/compass_lib/files.py` and `skills/workspace-files.md` implement the same read-only resolution policy.
- Bundled resources come from the actual installed plugin root. New searches use the fixed `Path.home() / "Agent Compass"` base resolved by `workspace-base`; CF/SC/JS have isolated run folders, including profiles. Keep legacy files in place; explicit saved-run handoffs do not change the base for new searches.
- Setup content lives in `docs/_includes/setup/`, composed by `docs/_includes/setup-tabs.html`; the JavaScript and legacy redirects preserve desktop/terminal deep links. Check their tests when changing setup navigation.
- `.github/workflows/docs.yml` runs checks on main pushes, pull requests and manual runs, with no schedule. Its Python matrix spans Linux/macOS/Windows; the site build waits for it. Only successful main builds deploy. Hosted Pages must use GitHub Actions as its source.
- `docs/_config.yml` uses `just-the-docs@latest`. CI resolves the latest stable release and temporarily pins it for that build; failed lookup stops the build. Local builds resolve through the remote-theme plugin; restart the preview to fetch a newer release.

## Domain Rules

Before changing intake, evidence handling, scoring, sponsorship, arithmetic or output formatting, read the affected step prompt and its referenced shared rules. Keep behavioral instructions in these shared sources rather than platform adapters or Python judgment code.

- CF/SC/JS select their chat/person/command run through `skills/run-workspaces.md` before profile or checkpoint access. New chats start fresh; same-chat repeats offer the command's view/resume/continue choice versus a separate fresh run. JS remains profile-only, without screening exports or checkpoints. Keep existing flat runs untouched and accept them only through explicit selection.
- In chats with multiple people, CF/SC/JS invocations without an unambiguous explicit person choice ask who the run is for; never default to recency. Ordinary JS follow-ups retain their selected person. PF stays profile-free.
- New CF/SC/JS runs reuse a profile already confirmed for the selected person in the same chat, copied through `profile_source_run`, unless the user asks for a new resume. Never copy research, outputs or checkpoints. Chat keys are host-prefixed (`claude:`, `codex:` or a tool-generated `local:<UUID4>`) and are never invented. Several distinct confirmed versions need a choice among them, never recency; a byte-identical `profile.md` plus optional `situational-profile.md` counts as one version.
- Each person and command has one active run. Start fresh chains from its ID; superseded runs are read-only and are listed (`run-list` `include_history`) or used as sources only on explicit request. A consumer's View or Resume keeps its recorded producer and confirmed scope and never rebinds to a newer active producer. An unfinished active producer never silently falls back to an older completed run.
- Preserve `profile.md`, `situational-profile.md`, the existing two-field checkpoint schema and saved artifacts. Existing current/legacy runs keep their resolved filenames, including missing later artifacts; duplicate spellings for one artifact require clarification rather than migration, merging or copies. Completed runs replay saved finals.
- The parent owns questions, confirmations, aggregate research and checkpoint advancement. Fresh research tasks receive literal candidate facts/rules; fresh context is not a filesystem sandbox.
- For research collection/validation changes, read `skills/data-validation-rules.md` and `skills/research-helper.md`. Accepted bytes and original duplicates are preserved; validation metadata stays outside country blocks. Ingestion is atomic per file, not across both files, so partial failures require readback and fresh hashes before retry.
- Country Finder prioritizes explicit Includes, then offers Salary Calculator's recorded research scope as names only with confirmation, otherwise its shipped default. This scope retains countries omitted from salary tables and requires neither salary completion nor substantive compatibility. Keep this separate from readiness/compatibility gates for substantive transfers; optional upstream data never blocks a standalone workflow or changes a resumed scope.
- Country Finder assesses Remote and Sponsorship independently across all Step 2 countries. Missing evidence differs from weak fit and explicit exclusion. Scoring either track requires stored research, even when the other track is excluded. The post-audit Summary owns final fits; the Priority Table supplies presentation order.
- Salary Calculator researches two independent local-employee gross annual base-pay tiers, not cross-border remote offers. Unsupported adjustments are skipped rather than changed to zero. `skills/salary-comparison-rules.md` and `skills/sponsorship-threshold-rules.md` own comparable currency/pay basis/period, unrounded comparisons and official monthly legal-pay support; targets, hard floors and visa rules stay separate.
- `skills/timezone-rules.md` owns hub and seasonal/DST coverage; helper offsets only describe supplied dates. Portal Finder needs opened relevant sources. Job Screener needs an explicit mandatory condition plus confirmed inability for each blocker, and retains its exact conditional report format.
- Portal Finder and Job Screener intentionally have no automatic exports or checkpoints.

## Instruction authoring

This covers Compass's agent-facing instructions. General prose follows `.claude/rules/writing.md`.

- Keep non-obvious guidance that changes decisions. Rewrite affected passages instead of accumulating exceptions, tutorials or repeated explanations.
- Define shared rules once per loaded context; brief reminders at consequential actions may repeat. Preserve required literal context in isolated research briefs and dependencies needed by standalone references.
- Keep routine paths concise and load required specialized detail at its owning step. Moving text into another file alone is not trimming.
- Preserve research coverage, source quality, independent tracks/tiers, uncertainty distinctions, QM capabilities, approvals, checkpoints and final audits. Brevity never justifies premature research stops or unsupported conclusions; word quotas do not establish quality.
- Reuse unchanged instructions and matching verified evidence only under the runtime and owning step's rules. Keep required fresh checks and readback; a prior success does not verify changed inputs.
- Verify proportionately with existing checks. Measure source size, loaded context and runtime separately; speed or token-saving claims need comparable measurements, and structural checks do not establish research accuracy.

## Documentation

Website files and documentation checks live under `docs/`; run Jekyll there. `docs/_plugins/repository_content.rb` renders the root README and shared plugin icon while retaining published URLs. Canonical agent instructions stay at their package paths.

Before editing the following content, read and follow its standard alongside the project's active Writing rule:

- Documentation or instruction sources rendered into guides: [docs/standards/documentation.md](docs/standards/documentation.md).
- README content: [docs/standards/readme.md](docs/standards/readme.md).
- Project descriptions in GitHub About, plugin manifests, README/site metadata or related variants: [docs/standards/project-description.md](docs/standards/project-description.md).

## Contributor Review Preference

When consulting Claude for a project review/discussion or running Claude workflow tests, request `claude --model claude-sonnet-5-5 --effort high`. Record the requested settings and check returned model metadata; ask before substituting an unavailable configuration. This preference does not change bundled specialist routing or global client settings.

## Known Traps

- Keep the two client manifests in the same package, sharing all skills and resources. Do not add a root manifest or another marketplace. Cross-platform symlink installation needs actual native discovery testing.
- `assets/icon.svg` supplies Codex `interface.logo`/`composerIcon`. Omit `icon` and `interface` from the Claude manifest for Desktop importer compatibility; this forgoes Anthropic directory icon metadata. Keep Codex branding in its own manifest.
- Native discovery tests inspect Codex's actual `skills/list` catalog for duplicate-free discovery and `plugin/read` for display metadata. They also check Claude's four skills and two agents; they do not establish model behavior.
- `.gitattributes` excludes canonical `.helm/` and legacy `.claude/helm/` records from Git archives. Preserve both exclusions; `scripts/test_plugin.rb` checks nested canonical paths in an isolated synthetic archive.
- Detailed guide pages render the canonical `workflows/`, `prompts/<command>/` and `skills/` Markdown through `docs/_plugins/guide_content.rb`, mapping relative links to Detailed pages. `docs/specialist-agents/detailed.md` extracts `## Specialist routing` from `prompts/shared/runtime.md` by exact heading, so renaming it or removing a rendered source fails the site build.

## Rules

For repository contributor work, read and follow these shared local rules on both Claude and Codex:

- .claude/rules/git.md
- .claude/rules/safety.md
- .claude/rules/writing.md

These contributor copies are not dependencies of the Compass workflows.

<!-- last-reviewed: 2100ac476d98d9d63892d23b3d6d8d8265614cdf -->
