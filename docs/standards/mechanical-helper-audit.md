# Mechanical helper review

Baseline: `a0edc45133fb09849e74ffac26fcb2b92fcd32e4`. This is a maintainer assessment record, not another runtime rule or consumer step.

## Scope and boundary

The inventory covers all 41 tracked Python, Ruby, JavaScript/MJS/CJS and Rake sources, their workflow/build/test callers, CI shell/Ruby blocks and embedded setup/header code. Dependencies and generated website content are excluded. No saved candidate workspace, live Helm record, installed plugin or demo session was changed.

The single execution boundary lives in [Mechanical helpers](../../prompts/shared/runtime.md#mechanical-helpers). Existing native tools and reviewed packaged helpers handle bounded mechanics; agents retain research, judgments, confirmations and checkpoint decisions. Workflow execution cannot create inline programs, temporary helpers or replacements for installed code. Approved Markdown/checkpoint writes retain their existing owners and checks. Maintainer development and website/test code have separate purposes.

## Decisions

| Action | Change and reason |
|---|---|
| Remove | The instruction to generate and execute an inline UUID program. A five-line fixed `chat-key` operation returns a UUID4 fallback identity without storage access, only at the existing missing-host-ID branch. |
| Remove | Mandatory-looking per-country salary preparation before rendering the same rows. The existing `render-salary` call already produces all exact calculations and the table. The standalone v1 arithmetic CLI remains available for isolated work and compatibility. |
| Remove | Redundant `resolve-files` calls around a required fresh `state-check`, which already returns the complete filename resolution. Fresh pre-write/resume resolution and post-save checks remain required. |
| Update | Dispatch imports only the selected mechanical module and its dependencies, rather than eagerly importing every operation family. Command names, JSON input/output and error categories remain stable; `chat-key` is the sole added operation. |
| Remove | Duplicate registry readers and the separate workflow-classification wrapper. Runs, portals and filename resolution use one registry reader; workflow validation reads it once instead of twice. There is no persistent or process-wide cache. |
| Update | State and saved-table checks pass their already loaded registry definition into filename resolution. A salary batch passes its one loaded formatting contract into each calculation. These are local values within one operation, not reusable saved evidence. |
| Update | Salary execution and fallback instructions refer to the shared helper runtime instead of repeating Python setup and failure choices. The source-data, exact-arithmetic and human-review requirements remain. |
| Keep | Byte-preserving research parsing/ingestion, hash checks, per-file atomic writes, immutable reports, run/person separation, legacy filename protection, exact arithmetic and canonical saved-output checks. They replace error-prone manual work without deciding research truth or advancing checkpoints. |
| Keep | Packaging/native-discovery tools, fictional acceptance replays and website code. They serve maintainer/product purposes and add no consumer execution phase. No new runner, dependency, schema, sidecar, framework or model service is needed. |

## Source inventory

All sources remain for the purposes below; the changes above simplify their callers or implementation. Fixed test-only interpreter snippets simulate old interpreters and disposable homes. They are maintained fixture code, not permission for an executing agent to invent programs.

| Source | Purpose |
|---|---|
| `Rakefile` | Compose offline plugin/docs checks; native discovery remains opt-in. |
| `helpers/compass.py` | Dispatch fixed mechanical operations and structured results/errors. |
| `helpers/salary_targets.py` | Exact two-tier salary arithmetic with the retained v1 CLI. |
| `helpers/compass_lib/__init__.py` | Package marker. |
| `helpers/compass_lib/common.py` | Strict bounded data, exact numbers, identities and workspace access. |
| `helpers/compass_lib/files.py` | One registry reader and read-only current/legacy filename resolution. |
| `helpers/compass_lib/money.py` | Exact declared FX/range comparisons and adjustment consistency checks. |
| `helpers/compass_lib/portals.py` | Country-scoped immutable report storage and digest-bound retrieval. |
| `helpers/compass_lib/research.py` | Stable batches, bounded country-block parsing and byte-preserving ingestion. |
| `helpers/compass_lib/runs.py` | Chat/person run metadata, immutable lineage, confirmed profile copies and UUID generation. |
| `helpers/compass_lib/state.py` | Read-only checkpoint/output consistency; never advances state. |
| `helpers/compass_lib/tables.py` | Render supplied decisions/calculations and compare canonical saved sections. |
| `helpers/compass_lib/timezones.py` | Supplied-date offsets and interval overlap, without seasonal certification. |
| `helpers/compass_lib/workspaces.py` | Resolve the fixed home storage base; create only when requested. |
| `scripts/validate_plugin.rb` | Package identity, entries, references, contracts and relocated resources. |
| `scripts/test_plugin.rb` | Packaging, discovery contracts, published examples and protected Git exports. |
| `scripts/test_salary_targets.rb` | Independent Rational oracle for salary CLI arithmetic and boundaries. |
| `scripts/test_compass.py` | Fictional helper, storage, legacy, encoding, isolation and preservation regressions. |
| `scripts/check_clients.rb` | Optional temporary native discovery; no model calls. |
| `scripts/test_workflow_replay.py` | Optional bounded model replays with fictional data and simulated web evidence. |
| `docs/tasks.rb` | Build the site and run its offline source/browser/link checks. |
| `docs/_plugins/asset_digest.rb` | Digest published static assets; reject unpublished targets. |
| `docs/_plugins/frontend.rb` | Initial theme, lazy search and sized static Mermaid assets. |
| `docs/_plugins/repository_content.rb` | Render shared README/icon/version while retaining public URLs. |
| `docs/scripts/render-diagrams.mjs` | Render shipped Mermaid using local dependencies and loopback Chrome. |
| `docs/assets/js/guide-nav.js` | Keep an overview's navigation active on its Details page. |
| `docs/assets/js/setup-tabs.js` | Setup panels and preserved URL fragments. |
| `docs/assets/js/theme-switcher.js` | System/Light/Dark choice and the existing saved preference. |
| `docs/tests/browser_frontend.mjs` | Isolated browser theme, layout, search, navigation and diagram checks. |
| `docs/tests/check-theme-colors.mjs` | Shared computed-color/contrast and diagram assertions. |
| `docs/tests/guide_pairs.rb` | Discover the 18 authored Overview/Details pairs. |
| `docs/tests/test_asset_digest.rb` | Stable digest, content-change and unpublished-asset controls. |
| `docs/tests/test_frontend.rb` | Initial-theme, lazy-search and static-diagram source contracts. |
| `docs/tests/test_guide_nav.cjs` | Details/overview navigation and activation regressions. |
| `docs/tests/test_guide_views.rb` | Built depth selectors, active navigation and guide links. |
| `docs/tests/test_human_guides.rb` | Pair inventory, source references and separation from raw agent prompts. |
| `docs/tests/test_repository_content.rb` | Shared homepage/icon/version inputs and canonical public paths. |
| `docs/tests/test_setup_redirects.cjs` | Historical setup URL and fragment preservation. |
| `docs/tests/test_setup_tabs.cjs` | Panel visibility, heading anchors and keyboard/history behavior. |
| `docs/tests/test_site_navigation.cjs` | Built navigation, legal links and canonical site boundaries. |
| `docs/tests/test_theme_switcher.cjs` | Theme preference, loading failure and cross-tab behavior. |

CI installs locked build dependencies, resolves the chosen documentation theme, runs existing checks and publishes only under its established main-branch trigger. Setup redirects preserve old fragments; header code loads site assets. These are fixed maintainer/site programs, not generated consumer helpers.

## Evidence and limits

Focused regressions first reproduced unnecessary imports, two registry reads per state/workflow check and three formatting-contract reads for a two-row salary batch. They pass after the changes: unrelated operation modules remain unloaded, each check reads its registry once, and the whole batch reads one contract while retaining both exact results. The UUID operation is checked for canonical UUID4 output, rejected extra fields and no storage access.

For a complete salary table with N eligible countries, preparation now needs one renderer call rather than N standalone arithmetic calls followed by rendering. The required saved-output and checkpoint checks remain separate. This is a call-path reduction, not a measured model-latency, token-cost or end-to-end speed claim.

The full offline suite passed, including package/helper checks, independent salary arithmetic, docs JavaScript contracts, Jekyll, isolated Chrome and internal HTML/link checks. The final registry simplification is covered again by the plugin/helper suite. No live research, paid model replay or installed-client mutation was performed. These checks establish mechanical behavior and preservation contracts; they cannot guarantee every future model session follows the instructions or that research claims are accurate.
