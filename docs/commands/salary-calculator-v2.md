---
title: /salary-calculator-v2
parent: Commands
nav_order: 4
---

# /salary-calculator-v2

Runs a current, evidence-audited salary search and returns a simple answer for forms and interviews: one expected annual salary, its monthly equivalent, and a short interview range for each country.

## Usage

```text
/claude-compass:salary-calculator-v2
```

The command resumes from `.salary-calculator-v2-state.json` only when its saved input fingerprint still matches the confirmed profile, positioning, and country list.

## What is different

- The target role and career level are confirmed before salary research begins.
- Country scope can reuse Country Finder's Gold or active-application list while preserving its priority order.
- Research uses one broad practical employer market, rather than asking the candidate to classify every company into salary tiers.
- Each country is researched independently with direct, dated sources and then audited by reopening decisive evidence.
- Recruiter-attraction positioning uses a small, evidence-based adjustment capped at 12 percent. It never uses passport prestige, race, ethnicity, or generic nationality rankings.
- Candidate-applicable visa thresholds act as floors when they are official, current, numeric, and comparable with base salary.
- Arithmetic and interview ranges are deterministic. The final audit may change a value only for a documented evidence, applicability, or calculation correction.
- All state and outputs use v2-specific names, so the command cannot overwrite Salary Calculator v1 work.

## Flow

1. **Intake and positioning:** confirms the target role, level, countries, employment path, work rights, salary-floor meaning, and career ladder.
2. **Grounded research:** researches a practical local employer market and the applicable sponsorship route for each country.
3. **Evidence audit:** reopens sources, normalizes comparable base salary, corrects weak claims, and grades evidence.
4. **Recruiter adjustment:** selects one evidence-backed positioning adjustment from 0, 3, 5, 7, 10, or 12 percent.
5. **Calculation:** applies the audited market data, candidate floors, visa floor, currency-aware rounding, and deterministic interview-range rules.
6. **Final verification:** checks every source, threshold, formula, and table label before presenting the final result.

## Final table

| Country | Visa Minimum | Expected Annual | Expected Monthly | Interview Range Annual |
|---|---:|---:|---:|---:|

`Visa Minimum` distinguishes a verified number, `None` when there is no fixed threshold, `N/A` when sponsorship is not the chosen path, and `?` when the current rule could not be confirmed.

## Output files

| File | Contents |
|---|---|
| `scv2-step1-positioning.md` | Confirmed role, level, candidate facts, employment paths, and country order |
| `scv2-research/[country].md` | Isolated source record for one country |
| `scv2-step2-salary-research.md` | Consolidated research in priority order |
| `scv2-step3-audited-data.md` | Reopened, normalized, evidence-graded market and visa data |
| `scv2-step4-adjustments.md` | Recruiter-attraction adjustments and supporting reasons |
| `scv2-step5-salary-table.md` | Full calculations and the pre-audit compact table |
| `scv2-step6-final-verification.md` | Final audit, corrections, caveats, grades, and delivered table |

The command does not edit an Obsidian vault, profile, application tracker, or portal list automatically.

## See also

- [`/country-finder`](country-finder.html): identify countries worth targeting
- [`/salary-calculator`](salary-calculator.html): use the original two-tier salary workflow
- [`/portal-finder`](portal-finder.html): find verified job portals for a specific country
