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
| `python3 -B scripts/test_workflow_replay.py --host claude` or `--host codex` | Optional acceptance replays through the host CLI with fictional data and simulated web evidence. It calls the model and is not part of `rake test`. |
| `bundle exec jekyll serve` | Local documentation preview. |
| `bundle exec rake client_test` | Optional native discovery regression; requires both Claude and Codex CLIs, uses temporary installations and makes no model calls. |
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

## Domain Rules

Before changing intake, evidence handling, scoring, sponsorship, arithmetic or output formatting, read the affected step prompt and its referenced shared rules. Keep behavioral instructions in these shared sources rather than platform adapters or Python judgment code.

- CF/SC/JS select their chat/person/command run through `skills/run-workspaces.md` before profile or checkpoint access. New chats start fresh; same-chat repeats offer the command's view/resume/continue choice versus a separate fresh run. JS remains profile-only, without screening exports or checkpoints. Keep existing flat runs untouched and accept them only through explicit selection.
- In chats with multiple people, CF/SC/JS invocations without an unambiguous explicit person choice ask who the run is for; never default to recency. Ordinary JS follow-ups retain their selected person. PF stays profile-free.
- New CF/SC/JS runs reuse a profile already confirmed for the selected person in the same chat, copied through `profile_source_run`, unless the user asks for a new resume. Never copy research, outputs or checkpoints. Chat keys are host-prefixed (`claude:`, `codex:` or a tool-generated `local:<UUID4>`) and are never invented.
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

## Documentation and Distribution

Command and step guides, related pages outside navigation and included explanatory content should give people a comfortable understanding of Compass. Follow `.claude/rules/writing.md` for prose and its complete reference-link workflow. This section defines the documentation experience.

- Use **Overview / Detailed guide** for paired command, step and specialist topics. Overview is the default: explain purpose, main phases, meaningful choices, outcomes and constraints comfortably. Detailed expands the same journey with complete procedures, conditions, examples, exceptions and recovery. Headings may differ; keep the sequence of ideas aligned. Do not force a second depth onto indexes, short setup instructions, examples or unrelated policies.
- Put `_includes/guide-depth.html` immediately below the title in both views. Keep the labels, placement and behavior consistent. These are ordinary current-tab navigation links with stable URLs, native browser history and an accessible current-page indication. Preserve existing overview URLs and section anchors, including links through setup tabs and redirects.
- Give Overview a compact Mermaid summary. Detailed diagrams cover the full meaningful routes, questions, approvals, exits and recovery outcomes. Split complex phases into connected diagrams instead of one oversized canvas; do not draw every mechanical action. Use diagrams only when they clarify the subject, and keep essential meaning in text.
- Let text explain more than the diagram. Use connected paragraphs, short lists, comparisons, tables and examples where useful. Detailed writing can be rich and precise without becoming an encyclopedia, diagram transcript or collection of overloaded paragraphs. Remove filler, hype and generic AI phrasing; brevity is not a word, line or node quota.
- Preserve research coverage, evidence quality, independent tracks/tiers, uncertainty, candidate-data boundaries, approvals, checkpoints, arithmetic/output contracts and final audits. Overview can omit internal mechanics while keeping necessary warnings visible. Detailed retains complete behavior, including rare consequential cases. Readers needing implementation detail can follow source links or inspect the code.
- Keep one authoritative plain Markdown instruction source for each workflow, prompt and shared rule. Detailed pages render these sources through `_plugins/guide_content.rb`; wrappers add reading context and diagrams without defining competing policy. Keep website controls and diagrams out of agent instructions. Supporting procedures retain their owners and load conditions. Follow links and includes to affected content outside the menu, and link authoritative references instead of reproducing them.
- Apply the reference-link workflow during docs maintenance: choose useful phrases and relevant verified sections, preserve clear wording, avoid linking every mention, use current-tab defaults and distinguish external destinations with the established icon. Check resulting anchors and interaction with available tools; report gaps. Changes to excluded instruction sources need an explicit site rebuild; renderer/configuration changes need a preview restart.

Setup content lives in `_includes/setup/`, composed by `_includes/setup-tabs.html`; the JavaScript and legacy redirects preserve desktop/terminal deep links. Check their tests when changing setup navigation.

`.github/workflows/docs.yml` runs checks on main pushes, pull requests and manual runs, with no schedule. Its Python matrix spans Linux/macOS/Windows; the site build waits for it. Only successful main builds deploy. Hosted Pages must use GitHub Actions as its source.

`_config.yml` uses `just-the-docs@latest`. CI resolves the latest stable release and temporarily pins it for that build; failed lookup stops the build. Local builds resolve through the remote-theme plugin; restart the preview to fetch a newer release.

### README command entries

Use the same entry structure as Agent Helm while retaining Compass's personal job-search voice. Keep each entry in `README.md`'s **How I use it** section in this order, following `.claude/rules/writing.md` and checking claims against the canonical workflow and its relevant supporting prompts. Retain existing heading anchors.

| Element | Purpose | Expected maximum |
|---|---|---|
| Heading | Identify the command by name alone. | Command name only. |
| First paragraph | Explain when I use it and the benefit I want. Link a meaningful purpose phrase to the command's Overview guide. | 45 words. |
| Invocation block | Show both client invocations in one `text` block, such as `Codex → $country-finder    Claude → /country-finder`. | One line. |
| Closing paragraph | Explain the main actions, concrete result and important choices, approvals or limits without repeating the first paragraph. | 70 words. |

Use two prose paragraphs per entry. These are expected limits, not reasons to remove essential warnings or approval boundaries. Keep deeper explanation and argument examples in the linked guides; add other contextual links only when they help readers take a distinct next step. Keep command names bare in general prose. Follow the reference-link workflow and use absolute `https://myowinthein.github.io/agent-compass/...` documentation URLs so links work on GitHub and the site. This structure is local project guidance, not a dependency on a sibling checkout.

## Contributor Review Preference

When consulting Claude for a project review/discussion or running Claude workflow tests, request `claude --model claude-sonnet-5-5 --effort high`. Record the requested settings and check returned model metadata; ask before substituting an unavailable configuration. This preference does not change bundled specialist routing or global client settings.

## Known Traps

- Keep the two client manifests in the same package, sharing all skills and resources. Do not add a root manifest or another marketplace. Cross-platform symlink installation needs actual native discovery testing.
- `assets/icon.svg` supplies Codex `interface.logo`/`composerIcon`. Omit `icon` and `interface` from the Claude manifest for Desktop importer compatibility; this forgoes Anthropic directory icon metadata. Keep Codex branding in its own manifest.
- Native discovery tests inspect Codex's actual `skills/list` catalog for duplicate-free discovery and `plugin/read` for display metadata. They also check Claude's four skills and two agents; they do not establish model behavior.
- `.gitattributes` excludes canonical `.helm/` and legacy `.claude/helm/` records from Git archives. Preserve both exclusions; `scripts/test_plugin.rb` checks nested canonical paths in an isolated synthetic archive.

## Rules

For repository contributor work, read and follow these shared local rules on both Claude and Codex:

- .claude/rules/git.md
- .claude/rules/safety.md
- .claude/rules/writing.md

These contributor copies are not dependencies of the Compass workflows.

<!-- last-reviewed: e6bb038615747cb01ba80674f2f997a493adad77 -->
