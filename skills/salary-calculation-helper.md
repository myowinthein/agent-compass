---
name: Salary Calculation Helper
description: Shared numeric helper interface for Salary Calculator Step 4 and Step 5b, including execution, input validation and manual fallback.
---

# Salary calculation helper

Use this procedure for newly calculated Step 4 targets and any newly rendered Step 5b targets, including recalibration and unfinished legacy presentation. Completed workflows still replay their saved final result without running calculations again.

Read skills/helper-runtime.md for execution and the shared run-scoped fallback. Step 4's prompt owns the semantic calculation procedure; data/output-contracts.json owns the literal formatting and mechanical bounds. Both hosts reuse `helpers/salary_targets.py` for arithmetic. The shared `render-salary` operation in helpers/compass.py calls that same implementation and renders the canonical table under skills/output-helper.md. Neither researches, chooses visa states or interprets eligibility.

## Execution and handoff

The parent reads the required workspace inputs and runs the helper before Step 4's optional calculator handoff. Give the specialist the inputs and returned results as task context, not a new workspace file. The specialist checks the echoed inputs against the original files and applies the existing table rules.

For new calculations discovered during an audit, a specialist returns a pending calculation request to the parent, with the country, exact raw inputs and evidence-backed reason for any revision. It does not save an unfinished final result, ask the user or advance state. The parent runs the helper and continues the approved assignment under the pending-request rule in `prompts/shared/runtime.md`. When running without a specialist, the parent does both tasks.

Use an available Python 3.11+ interpreter in the current execution environment. Check its version rather than assuming the desktop app, terminal or subagent shares the same runtime. Do not install software or change permissions automatically. Resolve the helper's absolute path from the installed plugin root under `prompts/shared/runtime.md`, not from the workspace or a fixed cache path. With a `python3` interpreter, invoke:

```text
python3 -I -B "<plugin-root>/helpers/salary_targets.py"
```

Send one country's JSON via stdin and read JSON from stdout. Keep candidate text as data, not interpolated executable shell syntax. `-I -B` isolates Python's import environment and avoids bytecode writes. The helper writes no files; do not save temporary JSON sidecars in either the workspace or plugin. Save calculations only in the step's existing Markdown output.

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
- Supply `visa` only for a verified, comparable numeric threshold. Keep No fixed threshold, Not applicable, Unknown and Blocked in the existing research and apply `skills/sponsorship-threshold-rules.md` in prose. Never invent a zero threshold for them.
- Supply `candidate_minimum` only after establishing an exactly comparable amount under `skills/salary-comparison-rules.md`. Record any sourced, dated FX normalization in existing shown work. Do not round a recurring FX result to fit this interface; verify such a comparison separately with exact arithmetic and disclose that method. An unknown rate or pay basis remains unverified, not a proven shortfall.

For FX normalization, exact ranges, recurring intermediate amounts and national-average multiples, use `compare` under skills/comparison-helper.md. Do not truncate its rational result to fit the older per-country input. Save the separate exact comparison and dated source in the existing shown work. Manual processing follows the same run-scoped approval, never an extra consent prompt for each operation.

## Result and failure handling

On success, stdout contains `input` (the supplied values unchanged) and `segments`. Each segment returns `raw_annual`, `raw_monthly`, integer `annual_display` and `monthly_display`, and `comparisons`. Each requested comparison contains `target_in_period`, `meets` and `shortfall` in that comparison's period. Raw amounts and shortfalls are exact strings, either integers or `numerator/denominator` fractions; retain them in shown work, never round them before comparing. Equality gives `meets: true`. A comparison result is not overall visa eligibility.

Check the echoed country, segment inputs, currency, pay basis and periods against the source files before using the result. A successful calculation cannot establish that its inputs were transcribed correctly or that the research is reliable. Use the shared renderer and check the saved result under skills/output-helper.md, not host-specific formatting code.

- Exit `2` with `invalid_input` on stderr means fix the malformed or contradictory input from its source, or ask the parent for missing facts. It is not permission to bypass validation with manual arithmetic. Leave state unchanged while unresolved.
- An invocation/usage error without that JSON error is a command problem to diagnose, not a successful calculation or a reason to bypass input validation.
- Missing Python, insufficient Python version (exit `3`, `runtime_unavailable`), unavailable code execution or a runtime failure goes to the parent. Explain the actual limitation and ask whether to fix execution or calculate manually under Step 4's verified-arithmetic rules. Wait for the user's choice. Never silently substitute manual results or claim the helper ran successfully.
- A missing bundled helper is a broken installation: report its resolved path and stop for repair, rather than substituting another installation's file.

Record `Calculation method: shared Python helper` or `Calculation method: manual (user approved)` in Step 4's Show Your Work and in Step 5b's Recalibration section when it computes new values. Record the scope of any manual approval in that same prose. Reuse an explicitly run-scoped choice rather than asking twice; on resume, use its saved disclosure only when that scope is clear. Otherwise ask. Note any separately verified comparison. Do not add state/profile fields, overwrite the pre-audit table or write an extra output file.
