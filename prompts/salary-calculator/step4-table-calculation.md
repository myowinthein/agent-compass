Check whether sc-step2-salary-data.md exists in the workspace. If it does not exist, stop and tell me: "sc-step2-salary-data.md was not found. Please ensure Step 2 completed successfully before continuing."

Check whether sc-step3-adjustment-values.md exists in the workspace. If it does not exist, stop and tell me: "sc-step3-adjustment-values.md was not found. Please ensure Step 3 completed successfully before continuing."

If both files exist, read them. Using the adjustment values from sc-step3-adjustment-values.md and the salary data from sc-step2-salary-data.md, calculate adjusted salary targets for each country.

Read and apply skills/salary-calculation-helper.md. The parent first checks whether any country qualifies under the data/comparability rules below, then runs the shared numeric helper before an optional calculator handoff. If none qualify, save a skip-only record with every country/reason and a zero-calculated Summary, complete this checkpoint and apply the workflow's no-usable-estimates stop; no empty table or calculator handoff is needed. Both hosts otherwise use the same implementation and its exact results for every supported calculation. Manual arithmetic requires the explicit user choice described there. Do not compute by intuition; precision takes priority over speed.

When at least one row qualifies, read data/output-contracts.json as data and skills/output-helper.md. The parent prepares `render-salary` inputs/results with the numeric work, and supplies them to any specialist. Use the canonical returned caption/table, then run `check-saved` on the saved table before completion. Skip-only records have no rendered table and do not invoke `render-salary` or `check-saved`; verify their skip coverage and checkpoint instead. A specialist needing revised helper work returns a pending request, never improvises. Under approved manual fallback, read the same contract and follow the identical presentation/check rules without claiming automation ran.

Read situational-profile.md. Note whether a salary minimum was given there and, if so, whether it was marked a hard floor or context only — this is used only for the flag described under Summary below, never to change Mainstream or Premium.

Read and apply skills/sponsorship-threshold-rules.md for the Visa salary rule column. This shared rule is the canonical source of its display states, period labels, and warning behavior.

Read and apply skills/salary-comparison-rules.md for the candidate's minimum, including currency/period/basis normalization and comparison-only FX. Record the dated rate and unrounded calculation in Show Your Work or Summary, not the salary table. An unavailable or non-comparable minimum check is unverified, not a proven shortfall.

Only calculate countries that have BOTH:

- salary data
- a supported numeric international candidate adjustment, including a supported zero

Skip countries with missing data or "Adjustment not estimable", preserving the stated reason. Never convert an unestimable adjustment into 0% or produce a partial-tier row.

Before preparing helper inputs, read only the benchmark-scope and benchmark-metadata requirements in prompts/salary-calculator/step1-research-prompt-generator.md as reference; do not execute its country questions or research orchestration. Establish each tier's actual role/level, geography, hours, local currency and annual gross-base normalization, and trace its single Realistic amount to the recorded source/method. Legacy metadata can be recovered from the stored evidence but not invented. Flag incompatible units, pay components or role scope and Low > Realistic or Realistic > Strong; ask for a material clarification or skip with the reason rather than sorting, correcting or deriving missing values. Different stated geographies require disclosure and a comparable explanation, not automatic rejection. Mainstream above Premium alone is not a contradiction and must not be corrected to force a tier ordering.

Also read the Research scope and Validation report in sc-step1-salary-research.md if available. Reconcile the confirmed scope, research/ingestion rejections, salary datasets, and adjustment datasets: every expected country must be calculated or listed as skipped with its actual reason. Do not fabricate table rows for rejected data or count a rejected duplicate whose original survived as a skipped country. If legacy scope/report information is missing, say which coverage or ingestion outcome cannot be established instead of silently claiming complete coverage.

Ordering: check whether cf-step6-final-ranking.md exists in the workspace.
- If it exists, read its Priority Table and order the countries in this step's output to match that table's order, top to bottom.
- Append calculated countries not present in that Priority Table afterward, alphabetically by country name. Do not omit user-added countries.
- If it does not exist, order countries alphabetically by country name (A→Z).

Definitions

- Market Midpoint = the "Realistic" value for the relevant tier, as provided in the salary dataset. Do not average, estimate, or derive it any other way.
- Mainstream uses the Mid-size / Mainstream Local-Market tier.
- Premium uses the Premium / International / Remote-first tier.
- These are employer segments, not guarantees, personal salary floors, or automatic visa-qualifying offers. Do not estimate new tiers or derive Premium by adding a generic uplift to Mainstream.

Calculation Rules

1. Apply the country's typical midpoint international candidate adjustment independently to each segment's Market Midpoint:

Annual Target = Market Midpoint x (1 - Adjustment %)

2. Keep both Annual Targets unrounded internally. Monthly Reference = unrounded Annual Target / 12. Use raw amounts, never displayed rounded figures, for sponsorship-threshold and candidate-minimum comparisons only when comparable under the relevant shared rules.

3. Round each displayed salary independently, once, at final formatting using the salary increments and tie rule in data/output-contracts.json. Use decimal/rational or otherwise verified arithmetic to avoid floating-point tie errors. Recomputing Monthly from the displayed Annual may differ from the displayed Monthly; retain the raw calculation.

4. Do not generate automatic -5%/+10% ranges or a universal interview range. Retain the original researched Low/Realistic/Strong figures in their existing research and stored-data files; they are not automatically a negotiation range. Any discussion of a negotiation range belongs in the saved audit, tied to the applicable employer segment and actual evidence, not an invented percentage band.

5. Compare both raw segment targets with the candidate-specific sponsorship threshold using skills/sponsorship-threshold-rules.md. The Visa salary rule column is independent of market targets; never change targets to clear it.

File format (write this structure to sc-step4-salary-table.md; only a brief calculated/skipped count is shown in chat at this step):

Show Your Work

For every country and segment, record Market Midpoint, typical midpoint Adjustment %, raw Annual Target, raw Monthly Reference, and independently rounded display values. Record the sourced threshold in its original period, applicable candidate category, effective date and official source, comparison arithmetic, and which segment misses it when applicable. Keep any additional wage conditions visible in the saved explanation.

Preserve the confirmed local-employee benchmark scope, intended path, geography/pay basis and Realistic selection method, plus Step 3's observed/inferred adjustment basis and confidence limits. Numeric monthly visa checks need the eligibility/annualization confirmation in skills/sponsorship-threshold-rules.md; otherwise render Unknown and explain the unavailable comparison, not an annual/12 pass. Do not describe an inferred adjustment as a measured overseas-pay penalty.

Include the calculation-method disclosure from skills/salary-calculation-helper.md. Check the helper's echoed inputs against the source files and preserve exact fractional raw amounts when needed.

Table

Copy the renderer's complete `markdown`, using the single canonical caption, column order and alignment from the `salary` object in data/output-contracts.json. Do not maintain another template here.

- One row per calculated country, in the order specified above.
- Place the flag before the country name and put the local currency code after it, e.g. "🇩🇪 Germany (EUR)".
- Each of the four salary cells contains a single comma-formatted number, with no range, parentheses, currency symbol, or repeated currency code. No USD conversion.
- Right-align the four numeric salary columns; left-align Country and Visa salary rule.
- Render Visa salary rule using skills/sponsorship-threshold-rules.md: a period-labeled exact threshold, or the distinct explicit state label. Do not replace it with a status-only check.
- No extra columns, inline citations, revision markers, or footnotes. Explanations and sources stay in Show Your Work and Summary.

Summary

- Countries calculated: X
- Countries skipped: Y

List every skipped country with its actual reason, including earlier ingestion failures carried from the Research scope and Validation report. Do not invent a row for missing data or count a retained duplicate as a skipped country.

For a hard-floor candidate salary minimum, flag any raw Mainstream target below it with the normalized amounts and specific gap. Preserve an unverified comparison as unverified when currency, period, or pay basis cannot be established. This is a Summary flag only; never change either target to meet it.

For each Blocked route, retain its concrete reason and state that both salary targets are reference-only for sponsorship through that route. For No fixed minimum, retain any prevailing-wage, occupation-rate, or other pay conditions; absence of a fixed number does not mean there are no salary requirements. A threshold comparison alone never establishes overall visa eligibility.

Save shown work, caption, table, and Summary to sc-step4-salary-table.md in the workspace. Keep the original research, profile files, and state schema unchanged.

In chat, do not reproduce calculations or the table. Give only a brief calculated/skipped count and confirmation that results are saved to sc-step4-salary-table.md. If none were calculated, apply the workflow's no-usable-estimates stop; otherwise Step 5 runs next and presents the final caption and table.

Do not perform additional analysis, ranking, or recommendations.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
