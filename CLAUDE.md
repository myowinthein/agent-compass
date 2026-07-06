# Claude Compass

## 1. Project Identity

**Name:** claude-compass  
**Version:** 0.1.0  
**Type:** Claude Code plugin (no runtime code — pure markdown)  
**Purpose:** Two slash commands for globally-minded job seekers: discover countries for remote hire or visa sponsorship, then calculate realistic local-market salaries. Grounded in user-provided research, never in Claude's assumptions.  
**Blast radius:** Low. No external services, no databases, no code execution. Changes affect prompt behavior in consumer workspaces only.

## 2. Project Config

```
git-solo: true
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
| `skills/data-validation-rules.md` | Cross-pipeline ingestion constraints (one item per message, no silent overwrites, no analysis during ingestion) |
| `skills/evidence-quality-rules.md` | Confidence-lowering rules for vague or unsourced research claims |
| `skills/exclusion-transparency-rules.md` | Every filtered-out item requires a specific, evidence-based reason |

**Pipeline pattern:** Each command is a thin orchestrator. All logic lives in numbered prompt files under `prompts/`. State persists across sessions via JSON files written to the consumer's workspace (`.country-finder-state.json`, `.salary-calculator-state.json`). Profile data persists via `profile.md` and `situational-profile.md`.

**Integration point:** After Country Finder step 5, Claude offers to hand off a single country to Salary Calculator. The salary-calculator command accepts this scoped invocation and skips the country-list question in step 1.

**Reality check steps** (country-finder step 6, salary-calculator step 5) are optional — Claude must ask and wait for explicit user confirmation before running them.

## 5. Behavior Rules

- Never skip, combine, or summarize pipeline steps.
- If a step instructs Claude to stop and wait, it must stop and wait. No placeholder answers, no assumptions on the user's behalf.
- Vague answers to criteria questions (e.g. "good," "reasonable," "flexible") are not accepted. Claude must ask for an exact number, currency, or clear yes/no before continuing.
- Remote hire and visa sponsorship are separate tracks throughout Country Finder. Never blend them.
- Salary research targets local-market compensation only. Exclude expat, FAANG-only, US-skewed, contractor, and equity-heavy data.

## 6. Hard Safety Rules

- Never infer, guess, or fill gaps in user-provided data.
- Never silently overwrite or duplicate a stored item — always ask.
- Never treat vague or unsourced claims as strong evidence.
- Never drop an item from a filtered list without a stated, evidence-based reason.
- Do not create or modify `.claude/rules` files without explicit user instruction.

## 7. Known Traps

_(none yet)_

<!-- last-reviewed: c9c4903489645d2cc5b0bb680bdf412b31e716be -->
