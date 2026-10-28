---
title: "Step 4: Table calculation"
parent: salary-calculator
grand_parent: Commands
nav_order: 4
---

# Step 4: Table calculation

Apply the supported adjustment independently to each employer tier. The assistant saves exact work and the table; the final audit presents it in chat.

## Flow

```mermaid
flowchart TD
  Start(["Read salary data, adjustments and research coverage"]) --> Eligible{"Any country has comparable data<br/>and a supported numeric adjustment?"}
  Eligible -->|No| Empty["Save a skip-only record and checkpoint<br/>No empty table or calculator handoff"]
  Empty --> Repair(["Offer evidence repair or stop"])
  Eligible -->|Yes| Helper["Run exact shared calculations<br/>Resolve any execution choice before handoff"]
  Helper --> Model["Offer the optional calculator specialist<br/>Or use your current model"]
  Model --> Calc["Apply the adjustment to each Realistic amount<br/>Keep raw annual and monthly values"]
  Calc --> Rules["Check comparable visa rules and your salary floor<br/>Never change targets to clear a minimum"]
  Rules --> Display["Round display values independently<br/>Render the table in the established country order"]
  Display --> Save["Save shown work, table and skipped-country reasons<br/>Check the actual saved table"]
  Save --> Next(["Show brief calculated and skipped counts<br/>Continue to Step 5"])
```

## Calculation runtime

Both hosts use bundled Python 3.11+ helpers without extra packages. They check supplied inputs, arithmetic and saved formatting, not market evidence or legal eligibility.

Unavailable execution needs your choice to repair it or use disclosed manual processing. Invalid data still needs correction; missing package files need repair. Choosing an [AI calculator specialist]({{ '/docs/specialist-agents.html' | relative_url }}#calculator-versus-python-helper) is separate from this arithmetic method.

## Calculation rules

Each segment uses its own researched **Realistic** amount:

```text
Annual Target = Realistic amount × (1 − Adjustment %)
Monthly Reference = unrounded Annual Target ÷ 12
```

Missing data, incomparable inputs or unestimable adjustment causes a reported skip, not a partial row or assumed 0%.

Display annual values to the nearest 500 and monthly references to the nearest 50, halfway upward, each from raw values. Dividing displayed annual pay may give a different monthly number. Monthly references are not necessarily payslips; no automatic salary ranges are generated.

## Visa salary rule comparison

| Display | Meaning |
|---|---|
| Exact amount with `/yr` or `/mo` | Verified candidate-applicable numeric rule. |
| No fixed minimum | No fixed numeric floor; other wage conditions may apply. |
| Not applicable | Confirmed path outside employer-sponsored relocation. |
| Unknown | Rule or comparable pay basis is unverified. |
| Blocked | Official evidence makes the assessed route unavailable to you. |

Use unrounded targets and the original rule period. Monthly checks require official pay/schedule support for annual/12; otherwise show Unknown and retain the known rule in shown work.

One ⚠️ means at least one target misses the numeric minimum. Equality passes this comparison, not overall eligibility. Shortfall and Blocked are different outcomes.

## Table format

> Gross base salary in local currency. Monthly figures are annual ÷ 12 references, not necessarily payslips; targets are market estimates, not visa-eligibility guarantees.

Fictional formatting examples; the monthly rule assumes compatible eligible pay:

| Country | Visa salary rule | Mainstream Annual | Premium Annual | Mainstream Monthly | Premium Monthly |
|---|---|---:|---:|---:|---:|
| 🇩🇪 Germany (EUR) | 45,300/yr | 59,500 | 74,500 | 4,950 | 6,200 |
| 🇳🇱 Netherlands (EUR) | 5,331/mo ⚠️ | 56,500 | 70,000 | 4,700 | 5,850 |
| 🇺🇸 United States (USD) | Not applicable | 140,000 | 175,000 | 11,650 | 14,600 |
| 🇦🇺 Australia (AUD) | Blocked | 95,000 | 118,000 | 7,900 | 9,850 |
| 🇯🇵 Japan (JPY) | No fixed minimum | 7,800,000 | 10,200,000 | 650,000 | 850,000 |
| 🇬🇧 United Kingdom (GBP) | Unknown | 60,000 | 78,000 | 5,000 | 6,500 |

Sources, dates, categories and shortfalls stay in shown work and Summary.

## Ordering

Use compatible [Country Finder Priority Table](../country-finder/step6-final-ranking.html#priority-table) order, appending user-added countries alphabetically. Without usable ordering, sort all countries alphabetically; optional ordering never blocks calculation.

## Hard-floor flag

Raw Mainstream pay below a confirmed hard floor is flagged in Summary. Comparison needs matching currency, period and basis, with dated FX where needed. Missing evidence stays unverified. Personal and visa minima never change market estimates.

## What happens next

`salary-calculator-04-salary-table.md` saves work, table and calculated/skipped counts. Every known target has a row or its actual skip reason; unknown coverage is disclosed.

Chat shows counts. With calculated countries, the workflow continues to [Final verification](step5b-final-verification.html). Otherwise, the assistant offers evidence repair or stop.
