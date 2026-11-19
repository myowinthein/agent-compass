---
name: Salary Calculation Helper
description: Shared numeric helper interface for Salary Calculator Step 4 and Step 5b, including execution, input validation and manual fallback.
---

# Salary calculation helper

Use this procedure for newly calculated Step 4 targets and any newly rendered Step 5b targets, including recalibration and unfinished legacy presentation. Completed workflows still replay their saved final result without running calculations again.

Read skills/helper-runtime.md for execution and the shared run-scoped fallback. Step 4's prompt owns the semantic calculation procedure; data/output-contracts.json owns the literal formatting and mechanical bounds. Both hosts reuse `helpers/salary_targets.py` for arithmetic. The shared `render-salary` operation in helpers/compass.py calls that same implementation and renders the canonical table under skills/output-helper.md. Neither researches, chooses visa states or interprets eligibility.

## Execution and handoff

The parent reads the required workspace inputs and normally calls `render-salary` once for all eligible rows under skills/output-helper.md. That call already returns each country's exact `calculations` and the canonical table; do not first run a separate per-country calculation for the same rows. Give any optional calculator specialist that request and its actual results as task context, not a new workspace file. The specialist checks echoed inputs against the original files and applies the table rules. No eligible rows means the existing skip-only path, without numeric/rendering calls.

For new calculations discovered during an audit, a specialist returns a pending calculation request to the parent, with the country, exact raw inputs and evidence-backed reason for any revision. It does not save an unfinished final result, ask the user or advance state. The parent runs the helper and continues the approved assignment under the pending-request rule in `prompts/shared/runtime.md`. When running without a specialist, the parent does both tasks.

Execution, paths, Python availability and the run-scoped manual choice follow skills/helper-runtime.md; reuse that resolution in the same execution environment. For isolated arithmetic when complete rendering inputs are not ready, the retained v1 CLI accepts one country:

```text
python3 -I -B "<plugin-root>/helpers/salary_targets.py"
```

Send the input below through stdin. This CLI writes no files and creates no rendering result. Its exact results can be reused while source inputs, contract and execution context match; a later rendering call supplies its own calculations. Keep requests/results transient and save shown work only in the existing Markdown output. Use no generated wrapper or arithmetic program.

## Input

Use this shape with actual values from the stored research and adjustments. This example is fictional, not current market or visa guidance:

```json
{
  "schema_version": 1,
  "country": "Germany",
  "currency": "EUR",
  "pay_basis": "gross_base",
  "segments": {
    "mainstream": {"market_midpoint": "62500", "adjustment_percent": "6.8"},
    "premium": {"market_midpoint": "80000", "adjustment_percent": "6.8"}
  },
  "comparisons": {
    "visa": {"amount": "58275", "period": "annual", "currency": "EUR", "pay_basis": "gross_base"}
  }
}
```

- Both segments are required. For initial targets, use the researched Market Midpoint and Step 3's typical adjustment, expressed as percentage points (`"6.8"`, not `"0.068"`). Use the country's same adjustment independently for both segments. Adjustments stay within the readable contract's bounds.
- For an evidence-supported recalibrated segment, replace its entire object with `{"raw_annual_target": "60000"}`. Keep the other segment's original inputs unless it is also revised. Do not supply both a raw target and midpoint/adjustment, derive a revision from a rounded display value or bypass Step 3's cap by inventing a raw target.
- All amounts and percentages are nonnegative plain decimal strings, at most 100 characters, without separators, exponents or surrounding whitespace. JSON numeric amounts, fractions, NaN and infinity are rejected. `schema_version` is the integer `1`.
- `comparisons` is optional. Its only supported entries are `visa` and `candidate_minimum`, each with all four fields shown above. Period is `annual` or `monthly`; currency must exactly match the targets and pay basis must be confirmed `gross_base`. No FX, tax or eligible-component conversion is inferred.
- Supply `visa` only for a verified, comparable numeric threshold under `skills/sponsorship-threshold-rules.md`, including a monthly rule's official annualization/pay-schedule basis. This arithmetic interface assumes annual/12 for monthly comparisons; it does not establish legal comparability. If that basis is unknown or incompatible, omit the numeric comparison and render Unknown under the shared rules, preserving the known legal figure and limitation in shown work. Keep No fixed threshold, Not applicable and Blocked distinct. Never invent a zero threshold for any nonnumeric state.
- Supply `candidate_minimum` only after establishing an exactly comparable amount under `skills/salary-comparison-rules.md`. Record any sourced, dated FX normalization in existing shown work. Do not round a recurring FX result to fit this interface; verify such a comparison separately with exact arithmetic and disclose that method. An unknown rate or pay basis remains unverified, not a proven shortfall.

For FX normalization, exact ranges, recurring intermediate amounts and national-average multiples, use `compare` under skills/comparison-helper.md. Do not truncate its rational result to fit the older per-country input. Save the separate exact comparison and dated source in the existing shown work. Manual processing follows the same run-scoped approval, never an extra consent prompt for each operation.

## Result and failure handling

On success, stdout contains `input` (the supplied values unchanged) and `segments`. Each segment returns `raw_annual`, `raw_monthly`, integer `annual_display` and `monthly_display`, and `comparisons`. Each requested comparison contains `target_in_period`, `meets` and `shortfall` in that comparison's period. Raw amounts and shortfalls are exact strings, either integers or `numerator/denominator` fractions; retain them in shown work, never round them before comparing. Equality gives `meets: true`. A comparison result is not overall visa eligibility.

Check the echoed country, segment inputs, currency, pay basis and periods against the source files before using the result. A successful calculation cannot establish that its inputs were transcribed correctly or that the research is reliable. Use the shared renderer and check the saved result under skills/output-helper.md, not host-specific formatting code.

Use skills/helper-runtime.md for failures and the explicit repair/manual choice. The standalone CLI reports invalid input as exit `2` and insufficient Python as exit `3`; a usage error is no result, and missing packaged code stops for installation repair. Invalid data cannot be bypassed with manual arithmetic. Keep the checkpoint unchanged until the applicable calculation, review and saved-output checks succeed.

Record `Calculation method: shared Python helper` or `Calculation method: manual (user approved)` in Step 4's Show Your Work and in Step 5b's Recalibration section when it computes new values. Record the scope of any manual approval in that same prose. Reuse an explicitly run-scoped choice rather than asking twice; on resume, use its saved disclosure only when that scope is clear. Otherwise ask. Note any separately verified comparison. Do not add state/profile fields, overwrite the pre-audit table or write an extra output file.
