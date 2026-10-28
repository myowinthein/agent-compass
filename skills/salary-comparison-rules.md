---
name: Salary Comparison Rules
description: Shared normalization, currency conversion, and uncertainty rules for comparing researched salaries or JD pay with a candidate's salary minimum.
---

# Salary comparison rules

Apply to candidate-minimum comparisons in research, scoring, salary flags and job screening. Keep salary tables in local currency and sponsorship rules separate.

For supported arithmetic, use `compare` under `skills/comparison-helper.md` with sourced amounts, dates and quote direction. Save exact normalized results in the calling step's existing notes. The helper checks comparability/arithmetic, not truth; only the calling step determines permitted exclusions, flags or blockers. Missing facts stay unverified. Use the shared explicit fallback when execution is unavailable.

- Establish currency, period and gross base versus net/take-home basis. Annual base / 12 is a monthly reference, not a payslip promise. Do not compare unlike bases or include bonuses/equity as base pay.
- Normalize hourly/daily rates only with established hours, paid weeks/payment schedule and comparable compensation. Retain original terms and derivation; assume neither 40 hours nor 52 paid weeks. Contractor revenue is not automatically employee gross base. Unsupported normalization stays unverified: do not send unsupported periods to the helper or infer floor failure. Salary Calculator still excludes contractor benchmarks and estimates local-employee pay, not cross-border offers; Job Screener uses actual JD pay.
- Clarify material unknown currency, period or basis with the parent, or report unverified. Missing evidence never proves floor failure. Invent neither taxes nor a currency from `$` alone.
- For unlike currencies, convert the candidate's minimum into the researched currency for comparison only. Use a dated central-bank or other named reliable financial source. Record its URL, effective date, quote direction (`1 unit of minimum currency = R local units`), converted minimum and calculation in existing Reason, Notes, shown work or Summary, not a new column.
- Use the latest published rate at the research date, noting weekends, holidays or lag. Reuse that quote per pair throughout the run and on resume unless explicitly refreshed with every affected comparison recomputed. Show reciprocal/cross-rate derivations with compatible effective dates. Historical fixtures retain their recorded rates.
- Without a usable dated quote, report "salary-floor comparison unverified: exchange rate unavailable". Do not guess, exclude or declare a blocker from unlike-currency amounts. Specialists return missing facts to the parent.
- Compare unrounded normalized values. Equality clears a hard floor; a range fails only when its entire comparable range is below the floor. A straddling range is uncertain.
- Apply a hard floor only through the calling step's permitted exclusion/flag. Context-only minima never exclude. Do not change market estimates to satisfy a minimum or turn comparison-only FX into a USD salary table.
