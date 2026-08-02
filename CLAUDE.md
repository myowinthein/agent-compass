# Claude Compass

## 1. Project Identity

**Name:** claude-compass  
**Version:** 1.8.0  
**Type:** Claude Code plugin (no runtime code — pure markdown)  
**Purpose:** Four slash commands for globally-minded IT/tech job seekers: discover countries for remote hire or visa sponsorship, calculate realistic local-market salaries, find verified job portals per country, and screen job descriptions against the candidate's resume. Biased toward the IT/tech industry (the target audience) but not toward any single IT role. Grounded in user-provided research, never in Claude's assumptions.  
**Blast radius:** Low. No external services, no databases, no code execution. Changes affect prompt behavior in consumer workspaces only.

## 2. Project Config

```
git-strategy: solo
git-auto-commit: true
readme-style: custom
```

## 3. Dev Commands

No build or install steps for the plugin itself — it is markdown-only. The repo does have one test command, for the GitHub Pages docs site: `bundle exec rake test` builds the Jekyll site and validates it with HTML-Proofer (broken links, images, scripts). Run it after any change under `docs/` or to `_config.yml`.

To use the plugin locally, install it from the repo root in a Claude Code workspace.

## 4. Architecture Pointers

| File | Why it matters |
|------|----------------|
| `.claude-plugin/plugin.json` | Plugin identity and version |
| `commands/country-finder.md` | Orchestrator for the 6-step Country Finder pipeline; owns state file and resume logic |
| `commands/salary-calculator.md` | Orchestrator for the 5-step Salary Calculator pipeline; runs standalone after Country Finder |
| `commands/portal-finder.md` | Orchestrator for the 1-step Portal Finder pipeline; no state file, no resume required |
| `commands/job-screener.md` | Orchestrator for the 1-step Job Screener; needs `profile.md`, keeps no state, re-invoke on drift |
| `prompts/shared/resume-extraction-prompt.md` | Shared first step for Country Finder, Salary Calculator, and Job Screener; produces `profile.md` in the consumer workspace |
| `prompts/portal-finder/step1-portal-research.md` | Single step for Portal Finder; does live web research and groups portals by type (not scope) for a given country |
| `prompts/job-screener/step1-match-analysis.md` | Single step for Job Screener; screens pasted JDs against `profile.md` with a deterministic decision waterfall, then drafts application writing |
| `skills/data-validation-rules.md` | Cross-pipeline ingestion constraints; referenced at runtime by both data-ingestion steps |
| `skills/evidence-quality-rules.md` | Confidence-lowering rules for vague or unsourced research claims; referenced at runtime by the scoring step |
| `skills/exclusion-transparency-rules.md` | Every filtered-out item requires a specific, evidence-based reason; referenced at runtime by the scoring step |
| `skills/situational-profile-questions.md` | Shared situational profile questions and save/reuse logic; referenced at runtime by CF step1 and SC step3 |
| `agents/deep-reasoner.md` | Routes scoring, international adjustment, and reality checks to Opus/high effort |
| `agents/calculator.md` | Routes final salary table calculation to Opus/max effort |
| `_config.yml` | Jekyll + just-the-docs GitHub Pages site config; excludes plugin dirs (`agents/`, `commands/`, `prompts/`, `skills/`, `.claude/`) from the public site |
| `.claude/helm/refactor-log.json` | Refactoring ledger — tracks open/fixed/skipped findings across runs; not source code |

**Pipeline pattern:** Each command is a thin orchestrator. All logic lives in numbered prompt files under `prompts/`. Pipeline state persists across sessions via JSON files written to the consumer's workspace (`.country-finder-state.json`, `.salary-calculator-state.json`). Intermediate step outputs also persist to workspace files prefixed `cf-` or `sc-` (e.g. `cf-step5-scoring-results.md`, `sc-step3-adjustment-values.md`) so Opus subagents can read real data without relying on conversation memory. Profile data persists via `profile.md` and `situational-profile.md`.

**Skill file pattern:** Skill files are not auto-loaded — they are referenced explicitly by the prompt files that need them (`Read and apply skills/...`). This is the single-source-of-truth for shared rules and logic; do not inline skill content in prompts.

**Reality check steps** (country-finder step 6, salary-calculator step 5) are optional — Claude must ask and wait for explicit user confirmation before running them.

## 5. Domain Rules

- Job Screener's verdict is a deterministic waterfall applied silently in order — Skip (any 🚫 blocker) beats Maybe (2+ unmet required quals) beats Apply — never re-derived per JD.
- Job Screener 🚫 blockers are limited to objective, non-negotiable disqualifiers (missing work authorization, unmet required clearance/language/certification, no-remote mandatory on-site, unmeetable timezone overlap, missing core tech stack). Years-of-experience gaps and unmet preferred (not required) qualifications are never 🚫.
- Portal Finder groups portals by type only (general, tech-specific, agency, network, government); scope (country-dedicated vs global) is a per-portal note, never a grouping axis, and each portal belongs to exactly one group.
- Situational profile (`situational-profile.md`) is asked once and reused across Country Finder step1 and Salary Calculator step3 — never re-asked if the file already exists.
- Salary Calculator's step5 career ladder must be drafted and confirmed by the user on the calling model before any Opus handoff — confirmation cannot happen inside a subagent, since the subagent has no access to prior conversation turns.
- Country Finder step6's missing-candidate check compares Step 5 results against the full Step 2 candidate list (`cf-step2-candidates.md`, covering both tracks), not just what reached later steps, so a candidate dropped silently between steps is caught.

## 6. Behavior Rules

- Never skip, combine, or summarize pipeline steps.
- If a step instructs Claude to stop and wait, it must stop and wait. No placeholder answers, no assumptions on the user's behalf.
- Vague answers to criteria questions (e.g. "good," "reasonable," "flexible") are not accepted. Claude must ask for an exact number, currency, or clear yes/no before continuing.
- Remote hire and visa sponsorship are separate tracks throughout Country Finder. Never blend them.
- Salary research targets local-market compensation only. Exclude expat, FAANG-only, US-skewed, contractor, and equity-heavy data.
- Opus routing for judgment-heavy steps (scoring, international adjustment, reality checks) is user opt-in at each step — never assume automatic routing.

## 7. Hard Safety Rules

- Never infer, guess, or fill gaps in user-provided data.
- Never silently overwrite or duplicate a stored item. During automated ingestion, keep the original, skip the duplicate, and report it in a warning; in interactive steps, ask before overwriting.
- Never treat vague or unsourced claims as strong evidence.
- Never drop an item from a filtered list without a stated, evidence-based reason.
- Do not create or modify `.claude/rules` files without explicit user instruction.

## 8. Known Traps

- **Sub-agent scope is fragile.** Steps 2 and 3 of country-finder spawn isolated sub-agents with strict single-task briefs — step2's agents are batched by region and each checks both Remote and Sponsorship for its own countries only; step3's agents are one per country. Broadening a sub-agent's brief — even slightly — causes it to freelance work outside its scope (e.g. a region-batch agent producing results for a country outside its batch). Subagents also do not inherit prior conversation turns, so any step routed to `deep-reasoner` or `calculator` must read its inputs from workspace files (`cf-`/`sc-` prefixed outputs, `profile.md`, `situational-profile.md`), never from "what was discussed earlier."
- **`docs/commands/*.md` serves dual purpose.** These files are plugin documentation AND live GitHub Pages site pages. Editing them changes both the repo docs and the public site simultaneously. Step detail pages live under `docs/commands/country-finder/` and `docs/commands/salary-calculator/`.
- **Docs and prompts drift with no automated check.** `docs/commands/*.md` describes what a `prompts/*.md` file does, but nothing enforces that they stay in sync — editing one without the other is a silent, easy mistake (e.g. a doc page claiming a step reads a file the actual prompt never instructs it to read). Whenever a prompt's behavior changes, grep for its filename and any file paths it reads/writes across `docs/`, `commands/`, and other `prompts/` files in the same change, and update every match.
- **`.claude/helm/refactor-log.json` is not source code.** It is the refactor command's memory ledger (moved here from `.claude/refactor-log.json`). Do not include it in any scan, analysis, or refactoring pass.

## Rules

This project follows the rules shipped in claude-helm:
- ~/.claude/plugins/marketplaces/claude-helm/rules/git.md
- ~/.claude/plugins/marketplaces/claude-helm/rules/safety.md

At the start of every session, check whether the paths above exist on this machine.
If either is missing, inform the user: "helm rules are referenced in CLAUDE.md but the
plugin is not installed on this machine. Install it with: /plugin install claude-helm"

<!-- last-reviewed: 80901f83131fc363d1ca02f341f75f6b28b30c99 -->
