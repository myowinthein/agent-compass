---
title: /salary-calculator
parent: Commands
nav_order: 3
has_children: true
---

# /salary-calculator

Runs the full Salary Calculator pipeline. Generates ready-to-copy research prompts for local-market salary data, ingests your research results, applies an international candidate adjustment, produces a salary table with shown calculations, and audits it with a mandatory final verification. Runs standalone or after Country Finder. Resumes from the last completed step if interrupted.

Both employer segments are local-employee benchmarks, not automatic cross-border remote-pay quotes. The assistant clarifies a materially unclear target role or employment path before research. Unsupported adjustments are recorded as not estimable, not assumed to be 0%.

## Usage

Claude:

```
/agent-compass:salary-calculator
```

Codex: type `$` and select `salary-calculator` from Agent Compass, or use `/skills`. In the desktop app, select the skill from the composer. Both entry points run the same workflow.

Run it once per session. The assistant resumes automatically if a `.salary-calculator-state.json` file already exists.

For model choices, effort settings and approval, see [Specialist agents]({{ '/docs/specialist-agents.html' | relative_url }}).

Research ingestion, exact comparisons and table rendering use shared Python 3.11+ helpers in both hosts, with no extra packages. The renderer reuses the existing salary arithmetic. If execution is unavailable, the assistant asks before proceeding manually and records the scope of that choice. Research and eligibility judgments remain in the workflow. See [Calculation runtime](salary-calculator/step4-table-calculation.html#calculation-runtime).

## Flow

```mermaid
flowchart TD
  Start([User runs /salary-calculator]) --> Profile{profile.md\nexists?}
  Profile -->|no| Extract[Resume extraction,\nwait for upload and confirmation]
  Profile -->|yes| State
  Extract --> State

  State{.salary-calculator-state.json\nexists?} -->|yes| Resume[Inform user: resuming from step N]
  State -->|no| S1prep
  Resume --> S1prep

  S1prep[Collect or reuse situational profile\nbefore threshold research] --> S1
  S1[Step 1: Research prompt generator\nlocal-market salary prompts per country] --> S2
  S2[Step 2: Data validation\nreads sc-step1-salary-research.md] --> Stored{Any country stored?}
  Stored -->|yes| S3
  Stored -->|no| Repair[Keep output and checkpoint\nOffer evidence repair or stop]
  S3[Step 3: International adjustment\ndeep-reasoner agent] --> S4
  S4[Step 4: Table calculation\ncalculator agent, file-only,\nbrief note in chat] --> Calculated{Any country calculated?}
  Calculated -->|yes| Ladder
  Calculated -->|no| Repair

  Ladder[Confirm career ladder\non current model, before handoff] --> S5[Step 5: Final Verification\ndeep-reasoner agent, always runs\nChecks file-only, final table\nshown in chat\nOne file: sc-step5b-final-verification.md]
  S5 --> Done([Results delivered])
```

## Steps

The parent conversation owns user questions, state updates, and movement between steps. A delegated specialist completes only its assigned step and returns its saved output; the parent checks that output before continuing. After the final step, the parent presents the deliverable and ends the workflow.

### Profile check

Checks for `profile.md` in the workspace. If absent, reads `prompts/shared/resume-extraction-prompt.md`, waits for the user to provide their resume as an attachment, pasted text, or a readable local file, and waits for explicit confirmation of the extracted profile. The profile is reused on all subsequent runs without re-extraction.

### State check

Checks for `.salary-calculator-state.json`. If found, reads `last_completed_step` and informs the user which step will resume. If absent, creates the file with `last_completed_step: 0` and starts from Step 1. Updates the file only after each step and its required output are complete. Pending questions or partial research do not advance state. A run already at Step 5 reuses `sc-step5b-final-verification.md`. Invalid state or a missing final output is reported without overwriting it. The same workspace can be resumed on either host.

### [Step 1: Research prompt generator](salary-calculator/step1-research-prompt-generator.html)

First collects or reuses the situational profile, before any threshold research. If Country Finder's final output exists, offers countries with a Strong/Moderate fit in its post-audit Summary as a starting point. The pre-audit Step 5 result is used only if the final file is absent, and is identified as pre-audit. Research prompts embed the candidate's role, seniority, relevant experience and skills, plus the age/status facts needed for candidate-specific visa categories. They request realistic local-market annual base salaries, two company tiers, sourced and dated evidence, an evidence grade, and the applicable sponsorship threshold state. Unknown age or status never becomes an assumed discount category.

### [Step 2: Data validation](salary-calculator/step2-data-validation.html)

Reads `sc-step1-salary-research.md` written by Step 1 and stores each country's data automatically, no pasting. Validates each block: one country per block, both company tiers and sources present, duplicates skipped and noted. Data is preserved verbatim: no analysis or adjustments during ingestion. Stored data is written to `sc-step2-salary-data.md` for later steps.

### [Step 3: International adjustment](salary-calculator/step3-international-adjustment.html)

Reuses the situational profile collected before Step 1, with parent-side intake only if a legacy resume lacks it. The assistant asks whether to use the **deep-reasoner** subagent (host-specific model and effort); if declined, the step runs with your current model. Numeric reductions must have a stated observed or inferred evidence basis. Countries without a defensible percentage are marked **Adjustment not estimable** and skipped later with that reason. One common reduction is retained for both employer segments.

### [Step 4: Table calculation](salary-calculator/step4-table-calculation.html)

The parent runs the shared numeric helper, then offers the **calculator** specialist to check the inputs and prepare the table. Declining the specialist keeps the same arithmetic on the current model. It independently adjusts the two researched employer segments and saves a compact table: Country, Visa salary rule, Mainstream Annual, Premium Annual, Mainstream Monthly, and Premium Monthly. Salary cells contain single targets, not automatic ranges. Monthly references and threshold checks use raw annual targets before independent display rounding. Visa salary rule retains a period-labeled exact figure or an explicit No fixed minimum / Not applicable / Unknown / Blocked label, with a warning for a numeric shortfall. Visa and candidate minima never change the market estimates. Shown work, coverage/skip reasons, blocked-route notes and comparison details stay in the file; chat gets only a brief calculated/skipped count.

### [Step 5: Final Verification](salary-calculator/step5b-final-verification.html)

Mandatory after Step 4 calculates at least one country. It drafts your career ladder on the current model and waits for confirmation before any specialist handoff. An existing ladder is reused only when its confirmed role and level match this run. It then offers the **deep-reasoner** specialist; declining keeps the audit on the current model. The audit uses saved, dated evidence and revises salaries only when supported. Insufficient evidence can produce an inconclusive verdict without invented revisions or a claim that the framework was verified. Detailed checks remain in `sc-step5b-final-verification.md`; chat shows the standard caption, final table and completion message, including an inconclusive outcome when applicable. Completed results replay as saved without migration.

## Stop conditions

- **Profile not yet uploaded.** The assistant waits; it does not proceed or fill in placeholder data.
- **Any step instructs the assistant to wait.** The assistant stops and waits. No guessing, no assumptions.
- **Data validation finds an identifiable malformed block or missing tiers/sources.** It skips the item and records the reason in a consolidated report saved in the research file and carried into the final audit. Genuinely ambiguous block boundaries require clarification rather than guessed parsing.
- **No usable estimates remain.** After saving the required output and checkpoint, the assistant offers evidence repair or stop before another specialist, career-ladder question or empty final table. Before an approved repair rewrites an affected output, its checkpoint moves before the earliest rerun step. Valid originals and reports remain preserved, including on an unfinished resume; completed runs are not reset automatically.

## See also

- [`/country-finder`](country-finder.html): discover which countries are worth calculating salaries for
- [`/portal-finder`](portal-finder.html): find verified job portals for a specific country
- [`/job-screener`](job-screener.html): screen job descriptions against your resume profile
