---
title: "Step 5: Final Verification"
parent: /salary-calculator
grand_parent: Commands
nav_order: 5
---

# Step 5: Final Verification

An independent audit of the salary table from Step 4. Always runs; this is the only step in the pipeline with no skip option, since it produces the pipeline's final result. The four detailed checks are file-only, like Step 4's own work, but the resulting final table is the one thing this step does show you, copied from the file into chat with only Step 4's standard gross-base/monthly-reference caption. Whether recalibration happened is stated as a plain fact in the completion message afterward, not as extra commentary attached to the caption and table. Everything (checks, verdict, and table) is written to a single file, `sc-step5b-final-verification.md`; this step never creates more than one file. The assistant asks whether to use the **deep-reasoner** subagent (host-specific model and effort) for higher reasoning accuracy. If you decline, the step runs with your current model.

For model choices, effort settings and approval, see [Specialist agents]({{ '/docs/specialist-agents.html' | relative_url }}).

New calculations use the same shared helper as [Step 4](step4-table-calculation.html#calculation-runtime), including recalibration and unfinished legacy tables. If a specialist needs revised numbers, it sends the raw inputs to the parent for calculation and continues with the returned results as part of the approved handoff. It does not save a partial final result while waiting. The method and exact values are recorded in Recalibration, without an extra output file. An unchanged current-format table can be copied without another helper run only when it records the helper or an approved manual method and its inputs still match the source files. Older tables without that disclosure are verified first; any arithmetic correction is recorded separately from market recalibration and never overwrites Step 4.

## Flow

```mermaid
flowchart TD
  Start([Step 5 begins]) --> Ladder[Command drafts career ladder\non current model, wait for\nconfirmation, save to\nsc-step5a-career-ladder.md]
  Ladder --> Confirm{Career ladder\nconfirmed?}
  Confirm -->|no| EditLadder[Adjust ladder per feedback]
  EditLadder --> Confirm
  Confirm -->|yes| SpecialistQ{Use specialist for\nhigher accuracy?}
  SpecialistQ -->|yes| DeepReasoner[Route to deep-reasoner\nhost-specific model and effort]
  SpecialistQ -->|no| CurrentModel[Run with your\ncurrent model]
  DeepReasoner --> C1
  CurrentModel --> C1[1. Candidate positioning\nUse the confirmed ladder from\nsc-step5a-career-ladder.md]
  C1 --> C2[2. Framework calibration review\nIs the framework conservative · calibrated\nor inflated?]
  C2 --> C3[3. Country-by-country verification\nMainstream positioning · Premium positioning\nrecruiter comfort · overseas hiring realism]
  C3 --> C4[4. Framework recommendation\nIs Mainstream / Premium philosophy still appropriate?]
  C4 --> Recal{Evidence supports\nrecalibration?}
  Recal -->|yes| Revise[5. Recalibrate: revise affected countries\nRecompute Visa salary rule column\nRevised table becomes the final table]
  Recal -->|no| Confirm2[Confirm existing framework is appropriate\nPreserve estimates and normalize\nlegacy presentation only if needed]
  Revise --> SaveAll[Write checks, verdict, and\nfinal table into ONE file:\nsc-step5b-final-verification.md]
  Confirm2 --> SaveAll
  SaveAll --> ShowTable[Show final table in chat\ncopied from the file,\nstandard caption and table]
  ShowTable --> Done([Completion message])
```

## What it reads

- `sc-step4-salary-table.md`: the final salary table from Step 4
- `sc-step2-salary-data.md` and `sc-step3-adjustment-values.md`: the underlying salary data and adjustment values
- `profile.md`: used to assess candidate positioning and career level
- `situational-profile.md`: used for candidate-minimum comparisons
- Step 4's prompt and the shared threshold, salary-comparison, and evidence-quality rules: the canonical calculation and display contract
- `sc-step5a-career-ladder.md`: the career ladder drafted and confirmed with you before the step runs

All inputs come from workspace files, so the audit is safe to route to the deep-reasoner specialist. The career ladder is confirmed on your current model before any specialist handoff, so the subagent never has to pause for interactive confirmation.

All four checks and the recalibration verdict are saved to file only; not reproduced in chat, since the raw reasoning would overwhelm rather than help. The resulting final table (whether unchanged or revised) is written into that same file, then also shown directly in chat, copied from what was just saved, preceded only by the standard gross-base/monthly-reference caption.

## The four checks

_(File-only, written to `sc-step5b-final-verification.md`, not shown in chat. The final table further down is the exception.)_

**1. Candidate positioning**

The career ladder for your role is drafted from `profile.md` and confirmed with you by the main command *before* the step runs, then saved to `sc-step5a-career-ladder.md`. It assumes an IT/tech professional but is inferred from your actual role (any IT role, not assumed to be backend) using that role's real progression and title conventions (software engineering might run Mid → Senior → Staff → Principal, while data, DevOps, QA, security, product, or design each have their own ladder). The step uses that confirmed ladder to determine your likely current level and target role level. Compensation is benchmarked against the target role, not the highest historical responsibility.

**2. Framework calibration review**

Assesses whether the overall salary framework is conservative, recruiter-safe, appropriately calibrated, slightly inflated, or heavily inflated.

Evaluates legitimate compensation drivers (experience, technical depth, leadership scope, business impact, domain expertise) separately from potential inflation sources (premium employer weighting, multinational bias, niche specialist premium, higher-level title interpretation, AI optimism bias).

**3. Country-by-country verification**

For each country, evaluates:

- Mainstream positioning: percentile band and classification (conservative to top-tier)
- Premium positioning: classification (realistic stretch to international remote premium)
- Recruiter comfort: how likely is this to convert interviews?
- Sponsorship realism: if Step 4 set a Visa salary rule flag for this country, that concrete result feeds into this judgment rather than being assessed independently of it; a "Blocked" state makes sponsorship through the assessed route unavailable regardless of salary; it does not establish that every other possible route is blocked
- Overseas hiring realism: adjusted for your profile as an international candidate
- Evidence grade: a Low grade from Step 2 tempers how confidently this country's positioning is stated, even if the classification itself doesn't change

Approximate percentile bands are used only when stored evidence provides a representative compensation distribution or published percentiles comparable to the target role, seniority, location, and company tier. Salary ranges, individual postings, and analyst-selected Low/Realistic/Strong figures alone do not establish a percentile distribution. Without suitable evidence, the audit states **"percentile not estimable from available evidence"** and continues the qualitative positioning assessment, noting its limitations. Missing percentile evidence does not by itself trigger salary recalibration.

**4. Framework recommendation**

Determines whether the Mainstream/Premium philosophy, employer segmentation, and percentile assumptions remain appropriate. If improvements are recommended, explains what assumption caused the issue and what structural change is recommended.

## Recalibration

Only if the evidence genuinely supports it:
- Affected countries are revised upward or downward
- A revised table is generated using the current six-column format and caption from [Step 4](step4-table-calculation.html#table-format), **including the Visa salary rule column**; it is recomputed against the revised Mainstream and Premium figures, not carried forward from Step 4. Recalibration can push a country below a threshold it previously cleared, or above one it previously missed.
- If Step 4 flagged any country as below the candidate's hard-floor salary minimum, that flag is re-checked against any revised Mainstream value and restated in this file's Summary if it still applies. Mainstream and Premium are never adjusted to clear it.
- If Step 4 marked any country "Blocked," that classification is re-verified against current evidence (a route can open or close), carried into the revised table exactly as "Blocked" if it still applies, and restated in the Summary. A Blocked country's Mainstream/Premium figures never override the block.
- Priority is given to recruiter comfort, interview conversion, sponsorship realism, and realistic overseas positioning
- This revised table becomes the final table.

If recalibration is not supported, the existing framework is explicitly confirmed as appropriate; Step 4's table is copied in unchanged when it already uses the current format, with no salary revision. An unfinished legacy Safe/Stretch table is rendered as Mainstream/Premium using the current six-column contract: ranges are omitted, raw arithmetic is recovered from research and adjustments, and visa states are resolved from underlying research rather than ambiguous old dashes. Unrecoverable states are Unknown. This presentation-only normalization is not salary recalibration and never rewrites the Step 4 record.

Either way, the resulting final table (unchanged or revised) is written into `sc-step5b-final-verification.md`, in the same file as the four checks and the recalibration verdict. `sc-step4-salary-table.md` is left untouched as the pre-audit record. This step never creates a second file.

The final Summary carries calculated/skipped counts and every known skip reason, including ingestion failures recorded in Step 1's Validation report. No salary row is invented for an uncalculated country; missing legacy coverage remains explicit. Revised calculations reuse Step 4's raw-value rounding policy and the recorded FX/pay-basis comparison, unless the quote is explicitly refreshed and affected checks recomputed.

Completed runs continue to replay their saved final result without migration, new research, or state changes. Filename and research-schema compatibility is preserved. Negotiation ranges are not generated from fixed percentages; any saved negotiation discussion requires employer-segment evidence.

## Output

- `sc-step5b-final-verification.md`: the only file this step writes. Always contains the full audit (all four checks, file-only) plus the recalibration verdict and the resulting final table (unchanged or revised).

The standard caption and final table are also shown directly in chat, copied from the file. The four checks themselves are not reproduced in chat. The assistant closes with a completion message naming how many countries were audited, whether recalibration occurred, and confirming where the full audit is saved.

## Stop condition

A specialist returns its saved final output to the parent. The parent presents the required final table and completion message, then ends the workflow. When running the step itself, the parent delivers the results directly.
