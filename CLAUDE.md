# Claude Compass

## 1. Project Identity

**Name:** claude-compass  
**Version:** 0.5.1  
**Type:** Claude Code plugin (no runtime code — pure markdown)  
**Purpose:** Two slash commands for globally-minded job seekers: discover countries for remote hire or visa sponsorship, then calculate realistic local-market salaries. Grounded in user-provided research, never in Claude's assumptions.  
**Blast radius:** Low. No external services, no databases, no code execution. Changes affect prompt behavior in consumer workspaces only.

## 2. Project Config

```
git-solo: true
git-auto-commit: true
```

## 3. Dev Commands

No build, test, or install steps. This is a markdown-only plugin.

To use locally, install the plugin from the repo root in a Claude Code workspace.

## 4. Architecture Pointers

| File | Why it matters |
|------|----------------|
| `.claude-plugin/plugin.json` | Plugin identity and version |
| `commands/country-finder.md` | Orchestrator for the 6-step Country Finder pipeline; owns state file and resume logic |
| `commands/salary-calculator.md` | Orchestrator for the 5-step Salary Calculator pipeline; accepts single-country handoff from Country Finder |
| `prompts/shared/resume-extraction-prompt.md` | Shared first step for both pipelines; produces `profile.md` in the consumer workspace |
| `skills/data-validation-rules.md` | Cross-pipeline ingestion constraints; referenced at runtime by both data-ingestion steps |
| `skills/evidence-quality-rules.md` | Confidence-lowering rules for vague or unsourced research claims; referenced at runtime by the scoring step |
| `skills/exclusion-transparency-rules.md` | Every filtered-out item requires a specific, evidence-based reason; referenced at runtime by the scoring step |
| `agents/deep-reasoner.md` | Routes scoring, international adjustment, and reality checks to Opus/high effort |
| `agents/calculator.md` | Routes final salary table calculation to Opus/max effort |
| `_config.yml` | Jekyll + just-the-docs GitHub Pages site config; also controls which plugin files Jekyll excludes |
| `.claude/refactor-log.json` | Refactoring ledger — tracks open/fixed/skipped findings across runs; not source code |

**Pipeline pattern:** Each command is a thin orchestrator. All logic lives in numbered prompt files under `prompts/`. State persists across sessions via JSON files written to the consumer's workspace (`.country-finder-state.json`, `.salary-calculator-state.json`). Profile data persists via `profile.md` and `situational-profile.md`.

**Skill file pattern:** Skill files are not auto-loaded — they are referenced explicitly by the prompt files that need them (`Read and apply skills/...`). This is the single-source-of-truth for shared rules; do not inline rule content in prompts.

**Integration point:** After Country Finder step 5, Claude offers to hand off a single country to Salary Calculator. The same offer appears if the user declines the step 6 reality check. The salary-calculator command accepts this scoped invocation and skips the country-list question in step 1.

**Reality check steps** (country-finder step 6, salary-calculator step 5) are optional — Claude must ask and wait for explicit user confirmation before running them.

## 5. Behavior Rules

- Never skip, combine, or summarize pipeline steps.
- If a step instructs Claude to stop and wait, it must stop and wait. No placeholder answers, no assumptions on the user's behalf.
- Vague answers to criteria questions (e.g. "good," "reasonable," "flexible") are not accepted. Claude must ask for an exact number, currency, or clear yes/no before continuing.
- Remote hire and visa sponsorship are separate tracks throughout Country Finder. Never blend them.
- Salary research targets local-market compensation only. Exclude expat, FAANG-only, US-skewed, contractor, and equity-heavy data.
- Opus routing for judgment-heavy steps (scoring, international adjustment, reality checks) is user opt-in at each step — never assume automatic routing.

## 6. Hard Safety Rules

- Never infer, guess, or fill gaps in user-provided data.
- Never silently overwrite or duplicate a stored item — always ask.
- Never treat vague or unsourced claims as strong evidence.
- Never drop an item from a filtered list without a stated, evidence-based reason.
- Do not create or modify `.claude/rules` files without explicit user instruction.

## 7. Known Traps

- **Sub-agent scope is fragile.** Steps 2 and 3 of country-finder spawn isolated sub-agents with strict single-task briefs. Broadening a sub-agent's brief — even slightly — causes it to freelance work outside its scope (e.g. the remote agent producing sponsorship output without the right context).
- **`docs/commands/*.md` serves dual purpose.** These files are plugin documentation AND live GitHub Pages site pages. Editing them changes both the repo docs and the public site simultaneously. Step detail pages live under `docs/commands/country-finder/` and `docs/commands/salary-calculator/`.
- **`.claude/refactor-log.json` is not source code.** It is the refactor command's memory ledger. Do not include it in any scan, analysis, or refactoring pass.

## Rules

This project follows the rules shipped in claude-helm:
- ~/.claude/plugins/marketplaces/claude-helm/rules/git.md
- ~/.claude/plugins/marketplaces/claude-helm/rules/safety.md

At the start of every session, check whether the paths above exist on this machine.
If either is missing, inform the user: "helm rules are referenced in CLAUDE.md but the
plugin is not installed on this machine. Install it with: /plugin install claude-helm"

<!-- last-reviewed: 8eea269319e35d3ae3a06da6033ee6442e842941 -->
