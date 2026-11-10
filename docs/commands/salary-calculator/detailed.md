---
title: "salary-calculator"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator.html
guide_source: workflows/salary-calculator.md
permalink: /docs/commands/salary-calculator/detailed.html
title_category: Details
description: "Complete procedure, choices, constraints and outcomes for salary-calculator."
---

# salary-calculator

{% include guide-depth.html %}

Estimate salary targets for your role in selected countries, then audit their realism. Mainstream and Premium describe two employer segments paying local employees in the target country, not remote offers from your home country.

## Flow

```mermaid
flowchart TD
  Start(["Select this chat and person"]) --> Status{"Matching salary search?"}
  Status -->|Completed and View chosen| Replay(["Show the saved final result"])
  Status -->|Unfinished and Resume chosen| Resume["Resume the next unfinished step"]
  Status -->|No match or Start fresh chosen| Profile["Create a separate run<br/>Reuse or confirm this person's profile"]
  Profile --> Resume
  Status -->|Needs repair| Recover(["Explain the issue<br/>Offer repair or a fresh run"])
  Resume --> S1["1. Confirm countries<br/>Research local salaries and reference visa salary rules"]
  S1 --> S2["2. Validate and store research"]
  S2 --> Stored{"Any country stored?"}
  Stored -->|No| Repair(["Save the report and checkpoint<br/>Offer evidence repair or stop"])
  Stored -->|Yes| Continue["Continue below with supported country evidence"]
```

The calculation phase records unusable countries rather than inventing values. A usable run confirms the career ladder before its final audit.

```mermaid
flowchart TD
  S3["3. Estimate supported international adjustments"]
  S3 --> S4["4. Calculate comparable salary targets<br/>Record skipped countries"]
  S4 --> Usable{"Any country calculated?"}
  Usable -->|No| Repair
  Usable -->|Yes| Ladder["5a. Draft or reuse the matching career ladder<br/>Wait for confirmation if needed"]
  Ladder --> Audit["5b. Audit the salary framework<br/>Revise only when evidence supports it"]
  Audit --> Fresh{"Essential evidence needs refresh?"}
  Fresh -->|Yes| Choice["Wait: refresh evidence, retain a disclosed snapshot or stop"]
  Choice -->|Evidence or approved snapshot| Final["Save and check the full audit"]
  Choice -->|Stop or still blocked| Pending["Preserve earlier outputs; leave final checkpoint pending"]
  Fresh -->|No| Final
  Final --> End(["Show the final salary table and audit outcome"])
```

## Complete procedure

{{ page.guide_source | guide_full }}
