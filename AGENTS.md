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
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake test` | Full plugin/helper checks, site JavaScript and isolated Chrome tests, Jekyll build and internal HTML/link/image/script checks. |
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake plugin_test` | Plugin validation and offline Python/Ruby helper regressions. |
| `ruby scripts/validate_plugin.rb` | Four skill entries, shared resources/icon and a relocated package with a separate consumer workspace. |
| `ruby scripts/test_plugin.rb` | Validation edge cases, published arithmetic/table examples, archive attributes and deployment contracts. |
| `ruby scripts/test_salary_targets.rb` | Salary CLI checks against an independent Ruby Rational oracle. |
| `python3 -B scripts/test_compass.py` | Offline consumer checks, golden outputs, legacy names, ingestion/retry, state, encoding and relocation. |
| `python3 -B scripts/test_workflow_replay.py --host claude` or `--host codex` | Optional acceptance replays through the host CLI with fictional data and simulated web evidence. It calls the model and is not part of `rake test`. |
| `cd docs && bundle install && npm ci --ignore-scripts` | Install the locked Ruby and Node docs dependencies. Chrome is required; `COMPASS_DOCS_CHROME` selects a nonstandard executable. |
| `cd docs && bundle exec jekyll serve` | Local documentation preview. |
| `BUNDLE_GEMFILE=docs/Gemfile bundle exec rake client_test` | Optional native discovery regression; requires both Claude and Codex CLIs, uses temporary installations and makes no model calls. |
| `ruby scripts/check_clients.rb --installed` | Inspect inventories after separately updating installed copies. |

Choose local checks from the changed behavior and affected consumers, using the individual scripts and tasks above and in `docs/tasks.rb`. A prose-only guide correction does not require salary or workspace regressions. Broaden to the full suite when focused coverage is insufficient or impact is uncertain. Preserve required CI and publication checks.

When the Claude CLI is available, native validation uses `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate skills`. Offline checks use fictional fixtures; passing them does not establish live research accuracy or model/workflow compliance.

## Architecture Pointers

- `.claude-plugin/plugin.json` owns shared identity/version metadata; `.codex-plugin/plugin.json` mirrors it and adds Codex presentation. Packaging checks require exact shared-field parity. Keep `agent-compass` and all four workflow names stable. The marketplace references this package without duplicating its version or description.
- `skills/<command>/SKILL.md` are the four portable entry points. Each only loads the shared runtime and its workflow. Omit `commands` from both manifests and keep `commands/` absent; legacy adapters and generated `source-command-*` entries create duplicate discovery.
- `workflows/<command>.md` owns orchestration; `prompts/<command>/` owns step behavior, judgment and output instructions. Flat `skills/*.md` files are explicitly loaded rule/interface references, not discoverable skills.
- `prompts/shared/runtime.md` owns installed-resource resolution, parent/checkpoint responsibilities, research isolation/fallback and user-controlled model/effort. `prompts/shared/question-mechanism.md` adapts existing questions to actual host capabilities without adding approval gates.
- Analysis, calculation review and final audits run on the current agent with the user's selected model/effort. No bundled model-selecting agents or routing questions are used; research tasks inherit current settings where supported under the shared runtime.
- `helpers/compass.py` and `helpers/compass_lib/` supply shared mechanics, routed through `skills/helper-runtime.md`; `portals.py` owns profile-free country-report listing, retrieval and immutable saves. `workspace-base` resolves the fixed home storage base and creates it only on request; `run-start` creates that base when absent, isolated chat/person/command run folders and optional confirmed profile copies; `ingest` writes research/stored-data files. Run listing and state checks are read-only. Semantic decisions remain in prompts.
- `helpers/salary_targets.py` retains its v1 consumer interface and is reused by the shared renderer. `data/output-contracts.json` alone defines fixed display tokens, rounding/bounds and batching size for Python and approved manual runs.
- `data/workspace-files.json` is the sole current/legacy artifact registry. `helpers/compass_lib/files.py` and `skills/workspace-files.md` implement the same read-only resolution policy.
- Bundled resources come from the actual installed plugin root. New searches use the fixed `Path.home() / "Agent Compass"` base resolved by `workspace-base`; CF/SC/JS have isolated run folders, including profiles; Portal Finder has separate country-scoped report history. Keep legacy files in place; explicit saved-run handoffs do not change the base for new searches.
- Setup content lives in `docs/_includes/setup/`, composed by `docs/_includes/setup-tabs.html`; the JavaScript and legacy redirects preserve desktop/terminal deep links. Check their tests when changing setup navigation.
- `.github/workflows/docs.yml` runs checks on main pushes, pull requests and manual runs, with no schedule. Its Python matrix spans Linux/macOS/Windows; the site build waits for it. Only successful main builds deploy. Hosted Pages must use GitHub Actions as its source.
- `docs/_config.yml` uses `just-the-docs@latest`. CI resolves the latest stable release and temporarily pins it for that build; failed lookup stops the build. Local builds resolve through the remote-theme plugin; restart the preview to fetch a newer release. `docs/_plugins/frontend.rb` selects the initial stylesheet, generates a search worker from the theme's index/query rules, loads its data on interaction and renders sized Mermaid SVGs through `docs/scripts/render-diagrams.mjs`. The build uses locked Node dependencies and installed Chrome on loopback, caching derived diagrams in `docs/.jekyll-cache/`.

## Domain Rules

Before changing intake, evidence handling, scoring, sponsorship, arithmetic or output formatting, read the affected step prompt and its referenced shared rules. Keep behavioral instructions in these shared sources rather than platform adapters or Python judgment code.

- CF/SC/JS select their chat/person/command run through `skills/run-workspaces.md` before profile or checkpoint access. New chats start fresh; same-chat repeats offer the command's view/resume/continue choice versus a separate fresh run. JS remains profile-only, without screening exports or checkpoints. Keep existing flat runs untouched and accept them only through explicit selection.
- In chats with multiple people, CF/SC/JS invocations without an unambiguous explicit person choice ask who the run is for; never default to recency. Ordinary JS follow-ups retain their selected person. PF stays profile-free.
- New CF/SC/JS runs reuse a profile already confirmed for the selected person in the same chat, copied through `profile_source_run`, unless the user asks for a new resume. Never copy research, outputs or checkpoints. Chat keys are host-prefixed (`claude:`, `codex:` or a tool-generated `local:<UUID4>`) and are never invented. Several distinct confirmed versions need a choice among them, never recency; a byte-identical `profile.md` plus optional `situational-profile.md` counts as one version.
- Each person and command has one active run. Start fresh chains from its ID; superseded runs are read-only and are listed (`run-list` `include_history`) or used as sources only on explicit request, except the retained immediate predecessor's names-only country offer on Start fresh. A consumer's View or Resume keeps its recorded producer and confirmed scope and never rebinds to a newer active producer. An unfinished active producer never silently falls back to an older completed run.
- Preserve `profile.md`, `situational-profile.md`, the existing two-field checkpoint schema and saved artifacts. Existing current/legacy runs keep their resolved filenames, including missing later artifacts; duplicate spellings for one artifact require clarification rather than migration, merging or copies. Completed runs replay saved finals.
- The parent owns questions, confirmations, aggregate research and checkpoint advancement. Fresh research tasks receive literal candidate facts/rules; fresh context is not a filesystem sandbox.
- For research collection/validation changes, read `skills/data-validation-rules.md` and `skills/research-helper.md`. Accepted bytes and original duplicates are preserved; validation metadata stays outside country blocks. Ingestion is atomic per file, not across both files, so partial failures require readback and fresh hashes before retry.
- `skills/country-selection.md` owns CF/SC's common supplied-list, previous-scope and default-country question. Supplied countries are exact scope; otherwise offer the last CF/SC scope for the same person in this chat across all four pairings. Retain the source before a same-command Start fresh supersedes it. Show every proposed country outside the question panel; reuse transfers names only, including excluded/skipped countries, without requiring producer completion. CF reads its full Step 2 candidate scope, SC its Step 1 research scope. Keep this separate from substantive readiness/compatibility; optional sources never block own/default choices or change a resumed scope.
- Country Finder assesses Remote and Sponsorship independently across all Step 2 countries. Missing evidence differs from weak fit and explicit exclusion. Scoring either track requires stored research, even when the other track is excluded. Discovery gaps proceed to detailed research; only supported explicit exclusions skip a track. `skills/country-assessment-rules.md` owns consistent factors, targeted follow-up and fit/access/pay separation. New finals have independent Remote and Relocation priority tables; the post-audit Summary still owns final fits. Salary presentation uses Relocation order, retaining combined-table fallback for legacy outputs.
- Salary Calculator researches two independent local-employee gross annual base-pay tiers, not cross-border remote offers. Unsupported adjustments remain unverified; comparable researched midpoints continue as clearly disclosed unadjusted benchmark references rather than invented 0% adjustments. SC uses obtained evidence without requesting manual research, another evidence search or a refresh choice; missing salary data remains skipped and missing visa evidence remains unverified. `skills/salary-comparison-rules.md` and `skills/sponsorship-threshold-rules.md` own comparable currency/pay basis/period, unrounded comparisons and official monthly legal-pay support; targets, hard floors and visa rules stay separate.
- `skills/timezone-rules.md` owns hub and seasonal/DST coverage; helper offsets only describe supplied dates. Portal Finder needs opened relevant sources. Job Screener needs an explicit mandatory condition plus confirmed inability for each blocker, and retains its exact conditional report format.
- Portal Finder lists Global, Local & regional, and IT & tech niche job boards, requiring current target-country IT coverage before grouping. Exclude aggregation-focused services and Indeed; omit unqualified portals without warning lists. Stars mark the strongest evidence-supported choices per group with genuine peers allowed, never a quota. Discovery stays IT-wide without profile tailoring. Portal Finder saves immutable country reports through `skills/portal-results.md`, without profiles or checkpoints. It offers the latest saved report before fresh research; older history is available only on request. Job Screener has no automatic screening exports or checkpoints.

## Instruction authoring

This covers Compass's agent-facing instructions. General prose follows `.claude/rules/writing.md`.

- Keep non-obvious guidance that changes decisions. Rewrite affected passages instead of accumulating exceptions, tutorials or repeated explanations.
- Define shared rules once per loaded context; brief reminders at consequential actions may repeat. Preserve required literal context in isolated research briefs and dependencies needed by standalone references.
- Keep routine paths concise and load required specialized detail at its owning step. Moving text into another file alone is not trimming.
- Preserve research coverage, source quality, independent tracks/tiers, uncertainty distinctions, QM capabilities, approvals, checkpoints and final audits. Brevity never justifies premature research stops or unsupported conclusions; word quotas do not establish quality.
- Reuse unchanged instructions and matching verified evidence only under the runtime and owning step's rules. Keep required fresh checks and readback; a prior success does not verify changed inputs.
- Verify proportionately with existing checks. Measure source size, loaded context and runtime separately; speed or token-saving claims need comparable measurements, and structural checks do not establish research accuracy.

## Documentation

Website files and documentation checks live under `docs/`; run Jekyll there. `docs/_plugins/repository_content.rb` renders the root README and shared plugin icon while retaining published URLs, and reads the header version from `.claude-plugin/plugin.json`, so release bumps need no docs edit. `docs/_includes/header_custom.html` places the version after the theme chooser, with a link to the matching GitHub release tag, so tags must stay `vX.Y.Z`. The site serves all its resources itself and its privacy policy says so; adding an external host needs a matching update to `docs/legal/privacy-policy.md`. Canonical agent instructions stay at their package paths.

Before editing the following content, read and follow its standard alongside the project's active Writing rule:

- Documentation or instruction changes that affect the guides: [docs/standards/documentation.md](docs/standards/documentation.md).
- README content: [docs/standards/readme.md](docs/standards/readme.md).
- Project descriptions in GitHub About, plugin manifests, README/site metadata or related variants: [docs/standards/project-description.md](docs/standards/project-description.md).
- Mechanical helper development or review, including callers: [docs/standards/mechanical-helper-audit.md](docs/standards/mechanical-helper-audit.md).

<!-- shared-standards-maintenance:start -->
### Shared standards maintenance

The four files in `docs/standards/` are maintained together with the sibling Agent Helm/Agent Compass checkout. Changes may originate in either project; neither copy automatically wins a conflict. Before changing a standard or its checker/tests, read the sibling project's instructions and compare current contents.

Keep `documentation.md`, `readme.md` and `project-description.md` byte-for-byte identical. In `mechanical-helper-audit.md`, keep the marked shared core identical and review each project's local requirements against its own runtime/helper contracts. Preserve intentional local differences and unrelated edits. The two checker/test scripts and this marked maintenance instruction stay identical too.

For authorized shared changes, update both repositories, run `ruby scripts/check_standards.rb` from either root, and run each project's affected required checks before committing. The checker accepts an explicit sibling path when needed and only reads local files; it does not fetch, copy, commit or publish. Missing/unreadable sibling content leaves synchronization unverified. Report synchronization status, retained local adaptations and any outstanding file; do not silently certify one-sided work. Loading these instructions starts no synchronization scan or workflow. These are project-only standards, outside Adopt.
<!-- shared-standards-maintenance:end -->

## Contributor Review Preference

When consulting Claude for a project review/discussion or running Claude workflow tests, request `claude --model claude-sonnet-5-5 --effort high`. Record the requested settings and check returned model metadata; ask before substituting an unavailable configuration. This contributor preference does not change workflow model selection or global client settings.

## Known Traps

- Keep the two client manifests in the same package, sharing all skills and resources. Do not add a root manifest or another marketplace. Cross-platform symlink installation needs actual native discovery testing.
- `assets/icon.svg` supplies Codex `interface.logo`/`composerIcon`. Omit `icon` and `interface` from the Claude manifest for Desktop importer compatibility; this forgoes Anthropic directory icon metadata. Keep Codex branding in its own manifest.
- Native discovery tests inspect Codex's actual `skills/list` catalog for duplicate-free discovery and `plugin/read` for display metadata. They also check Claude's four skills and absence of bundled agents; they do not establish model behavior.
- `.gitattributes` excludes canonical `.helm/` and legacy `.claude/helm/` records from Git archives. Preserve both exclusions; `scripts/test_plugin.rb` checks nested canonical paths in an isolated synthetic archive.
- Overview and Details are independently authored human guides under `docs/`. Details expands the Overview journey with explanations, examples and meaningful decisions; it never embeds raw agent instructions. `source_files` records reference sources and each page links to the existing repository for implementation depth. `docs/tests/test_human_guides.rb` checks this separation and view pairing; built-site checks preserve the selector, sidebar activation and navigation. The Model and effort guide retains its published specialist-agents URLs. Adding or removing a pair requires updating the fixed pair count (18) in `docs/tests/guide_pairs.rb`, which both guide tests share.
- `docs/_plugins/frontend.rb` patches Just the Docs output by exact match and raises `Just the Docs theme changed` when its markup or scripts move. Because the theme follows `@latest`, a theme release can fail the build until the matching patch is updated.
- Diagram colours are set in `docs/scripts/render-diagrams.mjs` and re-checked as literal values in `docs/tests/check-theme-colors.mjs`, which inspects rendered pixels in light and dark. Change both together.

## Rules

For repository contributor work, read and follow these shared local rules on both Claude and Codex:

- .claude/rules/git.md
- .claude/rules/safety.md
- .claude/rules/writing.md
- .claude/rules/design.md
- .claude/rules/interaction.md

These contributor copies are not dependencies of the Compass workflows.

<!-- last-reviewed: 4c6e3c0c5ee6b9082fe16db28ec91d8e73d7556e -->
