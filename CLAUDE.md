# Claude Compass

## 1. Project Identity

**Name:** claude-compass  
**Version:** 1.14.0
**Type:** Claude Code plugin (no runtime code, pure markdown)  
**Purpose:** Four slash commands for globally-minded IT/tech job seekers: discover countries for remote hire or visa sponsorship, calculate realistic local-market salaries, find verified job portals per country, and screen job descriptions against the candidate's resume. Biased toward the IT/tech industry (the target audience) but not toward any single IT role. Grounded in sourced evidence, never in Claude's assumptions.
**Blast radius:** Low. No external services, no databases, no code execution. Changes affect prompt behavior in consumer workspaces only.

## 2. Project Config

```
git-strategy: solo
git-auto-commit: true
readme-style: custom
```

## 3. Dev Commands

No build or install steps for the plugin itself; it is markdown-only. The repo does have one test command, for the GitHub Pages docs site: `bundle exec rake test` builds the Jekyll site and validates it with HTML-Proofer (broken links, images, scripts). Run it after any change under `docs/` or to `_config.yml`.

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
| `prompts/portal-finder/step1-portal-research.md` | Single step for Portal Finder; does live web research, groups portals by type into 3 groups (general, tech-specific, professional/community networks) for a given country |
| `prompts/job-screener/step1-match-analysis.md` | Single step for Job Screener; screens pasted JDs against `profile.md` with a deterministic decision waterfall, then drafts application writing |
| `skills/data-validation-rules.md` | Cross-pipeline ingestion constraints; referenced at runtime by both data-validation steps |
| `skills/evidence-quality-rules.md` | Confidence-lowering rules for vague or unsourced research claims; referenced at runtime by the scoring step |
| `skills/exclusion-transparency-rules.md` | Every filtered-out item requires a specific, evidence-based reason; referenced at runtime by the scoring step |
| `skills/situational-profile-questions.md` | Shared situational profile questions (location, citizenship, language, salary minimum with hard-floor/context distinction, existing work authorization, age) and save/reuse logic; referenced at runtime by CF step1 and SC step3 |
| `skills/sponsorship-threshold-rules.md` | Governs sponsorship salary threshold collection and comparison; referenced at runtime by SC steps 1, 4, and 5b |
| `data/default-preferred-countries.md` | Shipped, continent-grouped default country list for CF step2 when no Step 1 Include list was given; requires explicit user confirmation before use |
| `agents/deep-reasoner.md` | Routes scoring, final ranking, international adjustment, and final verification to Opus/high effort |
| `agents/calculator.md` | Routes salary table calculation to Opus/max effort |
| `_config.yml` | Jekyll + just-the-docs GitHub Pages site config; excludes plugin dirs (`agents/`, `commands/`, `prompts/`, `skills/`, `data/`, `.claude/`) from the public site |
| `.claude/helm/refactor-log.json` | Refactoring ledger: tracks open/fixed/skipped findings across runs; not source code |

**Pipeline pattern:** Each command is a thin orchestrator. All logic lives in numbered prompt files under `prompts/`. Pipeline state persists across sessions via JSON files written to the consumer's workspace (`.country-finder-state.json`, `.salary-calculator-state.json`). Intermediate step outputs also persist to workspace files prefixed `cf-` or `sc-` (e.g. `cf-step5-scoring-results.md`, `sc-step3-adjustment-values.md`) so Opus subagents can read real data without relying on conversation memory. Every step writes to exactly one such file; no step splits its output across two files. Profile data persists via `profile.md` and `situational-profile.md`.

**Skill file pattern:** Skill files are not auto-loaded; they are referenced explicitly by the prompt files that need them (`Read and apply skills/...`). This is the single-source-of-truth for shared rules and logic; do not inline skill content in prompts.

**Chat-output pattern:** Non-terminal steps save their findings to file and give only a brief chat note (what happened, how many, where saved), never the raw per-item detail. Each pipeline's terminal step (CF step6, SC step5b) shows its actual deliverable table in chat, table only with no surrounding commentary; everything else that step also computes (CF step6's Summary and Effort Allocation note, SC step5b's four detailed checks) stays file-only even though it's saved in the same file as the table.

**Country Finder step6 (Final Ranking) and Salary Calculator step5 (career ladder + final verification) both always run**: unlike every other optional Opus-routable step, neither is ever skipped or asked about, since each produces its pipeline's actual final result (the Priority Table; the audited/possibly-revised salary table). Only their Opus routing remains a user choice at each step.

## 5. Domain Rules

- Remote hire and visa sponsorship are two separate tracks throughout Country Finder; never blended, always scored/labeled independently.
- Country Finder step2's candidate-universe base is the Step 1 Include list if one was given (applied silently), otherwise the shipped `data/default-preferred-countries.md`, the one exception to "silent": Claude shows it and asks whether to proceed with it or provide different countries, and waits, rather than ever applying it silently. There is no personal/workspace-level override file anymore.
- Country Finder step6's missing-candidate check compares Step 5 results against the full Step 2 candidate list (`cf-step2-candidates.md`, covering both tracks), not just what reached later steps, so a candidate dropped silently between steps is caught.
- Country Finder step6's audit runs three checks, not two: confidence calibration, missing candidate, and evidence misuse (domestic-only remote counted as cross-border, a legal visa route counted as employer willingness, one vacancy counted as deep market volume). Recalibration can be triggered by either the confidence or the evidence-misuse check.
- Country Finder step6 must save its Summary, Priority Table, and Effort Allocation note to `cf-step6-final-ranking.md`; if both it and `cf-step5-scoring-results.md` exist, step6's file is the one every later reader (Salary Calculator, a future session) should prefer, since it reflects any recalibration and carries the priority ranking. The Effort Allocation note is file-only, like the Summary, never shown in chat.
- Country Finder steps 2 and 3 instruct researchers to prefer sources in this order: official government sources, direct employer pages, official sponsor/accredited-employer registers (capability only, never intent), specialist job boards/recruiters/salary surveys, then aggregators (which need direct verification before use). Sources are recorded with name and URL, not name alone.
- Sponsorship salary thresholds (government-mandated minimums for employer-sponsored work-visa relocation) are handled entirely within Salary Calculator (step1 collects, step4 applies), not Country Finder. They are a hard eligibility flag, never folded into step3's international-candidate discount (a market-negotiation estimate) and never used to silently raise Safe or Stretch; the two facts are always shown side by side. Not applicable to remote/contractor arrangements, so this is scoped to sponsorship-relevant research only. If step5b recalibrates the table, the Legal Requirement column must be recomputed against the revised figures, not carried forward from step4. The column always shows both Annual and Monthly threshold equivalents in one cell (deriving whichever period wasn't originally reported via ×12/÷12), never just the reported figure.
- Salary Calculator's sponsorship threshold uses five distinct states (`skills/sponsorship-threshold-rules.md`): Verified numeric, No fixed threshold, Not applicable, Unknown, and Blocked. "No fixed threshold" and "Not applicable" render as an em dash; "Unknown" renders as `?`; "Blocked" renders as the literal word `Blocked`, shown even over an otherwise-confirmed figure. None of these ever collapse into each other, since "couldn't confirm," "genuinely nothing to check," and "a real route is currently closed to this candidate" all mean different things to the candidate. A Blocked country's Safe/Stretch figures are flagged reference-only in the Summary, never adjusted or hidden.
- Salary Calculator step1 asks each researcher to self-assess an evidence grade (High/Medium/Low) per country, stored by step2 (missing grade recorded as "not provided," never a reason to skip a country). Step3 caps its adjustment Confidence at Medium for any country with a Low grade; step5b's Country-by-Country Verification factors the grade into how confidently positioning is stated.
- Salary Calculator step3's international-candidate adjustment must never be based on race, ethnicity, passport prestige, or a generic nationality ranking; it must tie to concrete, candidate-applicable friction. The typical midpoint adjustment is capped at 15%, and anything above 10% requires citing specific, concrete evidence rather than general market difficulty. Friction factors (including lack of prior local employment history and weaker local reference/network signal) are weighed cumulatively, never requiring a separately priced cost per factor, but the same underlying issue is never counted twice under different labels.
- Salary Calculator step4 reads `situational-profile.md` and, if a hard-floor salary minimum was given there, flags in the Summary (prose, not a table column) any country whose Safe Fixed value falls short of it — a flag only, following the same "never silently raise" principle as the Legal Requirement column. Step5b re-checks this flag against any revised Safe value if recalibration occurs.
- Salary Calculator step3 reads `profile.md` and checks a visa route's education requirement against the candidate's actual degree(s) before treating it as a friction factor, never a generic assumption about the occupation as a class. Formal recognition of a specific degree or institution is a different, unverifiable-by-research question; it's noted as a process caveat in the per-country explanation, never asserted as pass/fail and never folded into the adjustment percentage.
- The situational profile's 7th question (existing residency/work authorization) is never guessed: if a candidate's status for a given country isn't stated, Salary Calculator step3 treats her as not already resident there. When it is stated and matches a country being calculated, relocation friction, remote interview logistics, and perceived hiring risk are weighed lighter for that country, but sponsorship-specific friction (visa complexity, employer willingness to sponsor) is not; the two are independent, and being already resident only reduces the former.
- The situational profile's 6th question (salary minimum) also records whether the figure is a hard floor or context only. Country Finder step5 excludes on a hard floor but only weighs context-only figures against a recruiter-friendly market midpoint, never excluding on that basis alone. The 8th question (date of birth or age) exists because some visa salary thresholds vary by age; it is used by Salary Calculator's sponsorship-threshold checks, not by Country Finder directly.
- Salary Calculator's step5 career ladder must be drafted and confirmed by the user on the calling model before any Opus handoff; confirmation cannot happen inside a subagent, since the subagent has no access to prior conversation turns.
- Salary Calculator step1 offers Country Finder's scored output (`cf-step6-final-ranking.md`, falling back to `cf-step5-scoring-results.md`) as a starting country list if either exists, always shown for confirmation rather than silently applied. Never `data/default-preferred-countries.md` for this: that's Country Finder's unscored search scope, not a result.
- Salary Calculator step4 (Table Calculation) also orders its table to match `cf-step6-final-ranking.md`'s Priority Table when that file exists, falling back to alphabetical order otherwise.
- Salary Calculator step5b writes to exactly one file, `sc-step5b-final-verification.md`: the four detailed checks, the recalibration verdict, and the resulting final table (unchanged or revised) all live in that single file. There is no separate table file; a revised table is never written anywhere but into `sc-step5b-final-verification.md` alongside the audit that produced it.
- Situational profile (`situational-profile.md`) is asked once and reused across Country Finder step1 and Salary Calculator step3, never re-asked if the file already exists.
- Portal Finder groups portals by type only (general, tech-specific, professional/community networks); scope (country-dedicated vs global) is a per-portal note, never a grouping axis, and each portal belongs to exactly one group. Government/official employment-service portals are deliberately excluded: citizen/PR-oriented or expat/relocation-info focused, not reliable third-party job listings. Portals carry no verified-attribute tags (remote/sponsorship/no-account); that mechanism was removed as not worth the research overhead.
- Job Screener's verdict is a deterministic waterfall applied silently in order: Skip (any 🚫 blocker) beats Maybe (2+ unmet required quals) beats Apply, never re-derived per JD.
- Job Screener 🚫 blockers are limited to objective, non-negotiable disqualifiers (missing work authorization, unmet required clearance/language/certification, no-remote mandatory on-site, unmeetable timezone overlap, missing core tech stack). Years-of-experience gaps and unmet preferred (not required) qualifications are never 🚫.

## 6. Behavior Rules

- Never skip, combine, or summarize pipeline steps.
- If a step instructs Claude to stop and wait, it must stop and wait. No placeholder answers, no assumptions on the user's behalf. Steps only stop when they're actually asking something; every other step chains automatically into the next within the same response, with no new user message required. Genuine checkpoints: CF step1's criteria questions, CF step2's conditional default-list confirmation, CF step3's/SC step1's conditional manual-research fallback, SC step1's conditional country-list confirmation, SC step5a's career-ladder confirmation, and every Opus-routing yes/no question.
- Vague answers to criteria questions (e.g. "good," "reasonable," "flexible") are not accepted. Claude must ask for an exact number, currency, or clear yes/no before continuing.
- Salary research targets local-market compensation only. Exclude expat, FAANG-only, US-skewed, contractor, and equity-heavy data.
- Opus routing for judgment-heavy steps (scoring, final ranking, international adjustment, final verification) is user opt-in at each step; never assume automatic routing. This is separate from whether the step itself runs: Country Finder step6 always runs regardless of the Opus choice.
- Prose in `docs/` avoids em dashes; use a comma, semicolon, colon, or restructure the sentence instead. Does not apply to `prompts/` or other files outside `docs/`.

## 7. Hard Safety Rules

- Never infer, guess, or fill gaps in user-provided data.
- Never silently overwrite or duplicate a stored item. During automated ingestion, keep the original, skip the duplicate, and report it in a warning; in interactive steps, ask before overwriting.
- Never treat vague or unsourced claims as strong evidence.
- Never drop an item from a filtered list without a stated, evidence-based reason.
- Do not create or modify `.claude/rules` files without explicit user instruction.

## 8. Known Traps

- **Sub-agent scope is fragile.** Steps 2 and 3 of country-finder spawn isolated sub-agents with strict single-task briefs: step2's agents are batched by region and each checks both Remote and Sponsorship for its own countries only; step3's agents are one per country. Broadening a sub-agent's brief, even slightly, causes it to freelance work outside its scope (e.g. a region-batch agent producing results for a country outside its batch). Subagents also do not inherit prior conversation turns, so any step routed to `deep-reasoner` or `calculator` must read its inputs from workspace files (`cf-`/`sc-` prefixed outputs, `profile.md`, `situational-profile.md`), never from "what was discussed earlier."
- **`docs/commands/*.md` serves dual purpose.** These files are plugin documentation AND live GitHub Pages site pages. Editing them changes both the repo docs and the public site simultaneously. Step detail pages live under `docs/commands/country-finder/` and `docs/commands/salary-calculator/`.
- **Docs and prompts drift with no automated check.** `docs/commands/*.md` describes what a `prompts/*.md` file does, but nothing enforces that they stay in sync; editing one without the other is a silent, easy mistake (e.g. a doc page claiming a step reads a file the actual prompt never instructs it to read). Whenever a prompt's behavior changes, grep for its filename and any file paths it reads/writes across `docs/`, `commands/`, and other `prompts/` files in the same change, and update every match.
- **`.claude/helm/refactor-log.json` is not source code.** It is the refactor command's memory ledger (moved here from `.claude/refactor-log.json`). Do not include it in any scan, analysis, or refactoring pass.

## Rules

This project follows the rules shipped in claude-helm:
- ~/.claude/plugins/marketplaces/claude-helm/rules/git.md
- ~/.claude/plugins/marketplaces/claude-helm/rules/safety.md

At the start of every session, check whether the paths above exist on this machine.
If either is missing, inform the user: "helm rules are referenced in CLAUDE.md but the
plugin is not installed on this machine. Install it with: /plugin install claude-helm"

<!-- last-reviewed: 6011ac5b0efc3cc47d6a3a49e2cf5b0bb51cd29a -->
