---
title: "Step 4: Table calculation"
parent: salary-calculator
grand_parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator/step4-table-calculation.html
guide_source: prompts/salary-calculator/step4-table-calculation.md
permalink: /docs/commands/salary-calculator/step4-table-calculation/detailed.html
title_category: Detailed guide
description: "Complete procedure, choices, constraints and outcomes for Step 4: Table calculation."
---

# Step 4: Table calculation

{% include guide-depth.html %}

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

## Complete procedure

{{ page.guide_source | guide_full }}
