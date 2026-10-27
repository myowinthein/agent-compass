---
title: "Step 5: Final verification"
parent: salary-calculator
grand_parent: Commands
nav_order: 5
---

# Step 5: Final verification

Checks whether the salary framework fits your target role and the saved evidence. It runs whenever at least one country has been calculated.

## Flow

```mermaid
flowchart TD
  Start(["Draft the career ladder for your actual role<br/>Or reuse a matching confirmed ladder"]) --> Confirm{"Confirmed for this target?"}
  Confirm -->|No| Edit["Show the ladder<br/>Wait for your confirmation or edits"]
  Edit --> Confirm
  Confirm -->|Yes| Model["Offer the optional deep-reasoner<br/>Or use your current model"]
  Model --> Audit["Audit candidate positioning, framework calibration,<br/>each country and framework recommendations"]
  Audit --> Current{"Essential current visa evidence missing?"}
  Current -->|Yes| Choice["Wait for your choice<br/>Refresh evidence, use the dated snapshot or stop"]
  Choice -->|Approved evidence or snapshot| Verdict
  Current -->|No| Verdict{"Market revision supported?"}
  Verdict -->|Yes| Recal["Revise affected targets from evidence<br/>Recheck visa rules and your salary floor"]
  Verdict -->|No| Keep["Keep valid targets<br/>Distinguish supported from inconclusive"]
  Recal --> Final["Render and check the final table<br/>Record any approved visa-only update separately"]
  Keep --> Final
  Final --> Save["Save checks, verdict, table and skip reasons<br/>Leave earlier research and Step 4 unchanged"]
  Save --> End(["Show the standard caption and final table<br/>Report audited count and any inconclusive findings"])
```

## Confirming your career ladder

The assistant drafts a progression suited to your actual IT/tech role, shows it and waits for confirmation or edits. The confirmed ladder is saved to `salary-calculator-05a-career-ladder.md`.

An existing ladder is reused only when its confirmation, role and target level match this run. The specialist does not ask you to confirm it again.

Saving the confirmed ladder completes substep 5a. The checkpoint remains at Step 4 until the final audit is saved and its required checks pass.

## The four checks

1. Candidate positioning: assess your current and target levels using the confirmed ladder. Price the target role, not your highest historical responsibility.
2. Framework calibration: separate genuine compensation drivers from inflated assumptions about titles, specialist premiums or employer types.
3. Country-by-country verification: review Mainstream and Premium positioning, recruiter comfort, sponsorship realism, overseas hiring and evidence quality.
4. Framework recommendation: assess whether the employer segments and underlying assumptions remain appropriate.

Percentile bands need a comparable published distribution. Salary ranges or isolated postings alone do not establish one; without it, the audit says the percentile is not estimable and continues qualitatively.

## Recalibration

Targets change upward or downward only when evidence supports a revision. Otherwise, the verdict distinguishes supported unchanged estimates from **unchanged, market verification inconclusive**.

Revised targets use the same [calculation rules](step4-table-calculation.html#calculation-rules). Visa warnings and your hard-floor flags are rechecked using raw values. Market targets are never changed just to clear a minimum.

Arithmetic corrections, older-table formatting changes and approved visa-evidence updates are recorded separately from market recalibration.

## Dated evidence

This is an audit of saved evidence, not a fresh legal or market check. If essential current route status is missing, you choose a targeted refresh, the dated snapshot with its limitation, or stop.

Approved refreshed evidence is cited in the final audit. Any changed visa state or threshold is reflected in the final table, without overwriting earlier files or implying that other routes were assessed.

The approved refresh takes precedence over older visa evidence even when market targets are recalibrated in the same audit.

## Your result

`salary-calculator-05b-final-results.md` saves the four checks, recalibration verdict, standard caption, final table and Summary. It preserves calculated/skipped counts and reasons; no row is invented for an uncalculated country.

Chat shows the saved caption and final table, followed by the audited count and outcome. Inconclusive market findings are disclosed rather than described as verified.

The pre-audit `salary-calculator-04-salary-table.md` stays unchanged. Completed runs replay their saved final result without migration.

For model choices and approval, see [Specialist agents]({{ '/docs/specialist-agents.html' | relative_url }}).
