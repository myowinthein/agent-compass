---
name: Comparison Helper
description: Exact sourced monetary comparisons, adjustment checks and bounded dated timezone calculations.
---

# Comparison helper

Apply `skills/helper-runtime.md`. Every request includes `schema_version: 1`. Amounts are nonnegative exact decimal or `numerator/denominator` strings, not floats, formatted numbers or exponents.

## Comparable pay

For a supported pay/minimum comparison, run `compare` with:

```json
{"schema_version":1,"pay":{"low":"58250","high":"60000","currency":"EUR","period":"annual","basis":"gross_base"},"minimum":{"amount":"4900","currency":"EUR","period":"monthly","basis":"gross_base","hard_floor":true}}
```

These are fictional numbers. For a single target set low and high equal. Period is annual/monthly; basis is gross_base/net. Use `null` for a genuinely unknown currency, period or basis. Unlike bases remain unverified; this tool never invents taxes or pay components. The result includes `outcome` (pass/fail/uncertain/unverified), the exact normalized minimum, FX multiplier, maximum-pay shortfall and `hard_floor_failed`. Equality passes; a straddling range is uncertain. A context-only comparison cannot fail a hard floor.

For unlike currencies add `quotes: [{base, quote, rate, date, source}]`: one unit of base equals rate units of quote. A source is the named source URL and date is YYYY-MM-DD. Supply one direct/reciprocal quote or two connecting cross-rate legs in traversal order, using the same effective date. The helper checks structure/connectivity, not that a quoted rate is real/current. Follow `skills/salary-comparison-rules.md` for source freshness and reuse. A missing quote leaves the comparison unverified. Optional `multiple` multiplies the supplied minimum exactly, for a sourced computable national-average rule; the model must establish its actual legal applicability first. Save derivation and sources in the existing shown work/Reason/Summary.

## Adjustment

Before accepting an adjustment estimate, run `adjust-check` with `{low, high, typical, label, confidence, salary_evidence}` and the required evidence text in `evidence` where the contract requires it. Values/labels/bounds come from the readable contract. It checks the range/midpoint, label and confidence cap only. A present evidence field returns `evidence_substantive: "not_checked"`; review whether the evidence really supports the estimate. No percentage is selected by Python.

## Timezones

When explicit zones and dated instants are available, run `tz-offsets` with `zones: [candidateIanaZone, targetIanaZone]` and `instants: [ISO8601-with-offset, ...]`. It returns simultaneous offset seconds and absolute differences. Optional `schedules` contains pairs of `{start, end}` local ISO datetimes without offsets, one interval per zone. Both endpoints include their dates; overnight end dates must be the next day. An empty instants array is allowed when schedules are supplied. It returns overlap seconds and asks for clarification on nonexistent/ambiguous local times.

The schedule container is an array of two-element arrays, not a list of standalone window objects. Fictional one-day example:

```json
{"schema_version":1,"zones":["Asia/Manila","Europe/Berlin"],"instants":[],"schedules":[[{"start":"2026-10-21T22:00:00","end":"2026-10-22T06:00:00"},{"start":"2026-10-21T16:00:00","end":"2026-10-22T00:00:00"}]]}
```

The output always marks `evaluated_at_supplied_instants_only: true`, seasonal coverage unverified and tzdata freshness not established. Use sourced transition dates and the existing timezone policy to establish a whole reference period. This helper does not discover all transitions, certify a 12-month maximum, infer availability, prove whole-country failure or select a legal age/category. Missing tzdata uses the explicit unavailable-execution path; never install it automatically.
