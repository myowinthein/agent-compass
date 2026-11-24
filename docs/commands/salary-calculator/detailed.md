---
title: "Salary calculator"
parent: Commands
nav_exclude: true
has_toc: false
overview: /docs/commands/salary-calculator.html
permalink: /docs/commands/salary-calculator/detailed.html
title_category: Details
description: "Salary Calculator builds an evidence-based salary framework for your role in selected countries. It separates two local-employer segments, estimates only supported adjustments and audits the resulting targets before presenting the final comparison."
source_files:
  - workflows/salary-calculator.md
---

# Salary calculator

{% include guide-depth.html %}

Salary Calculator builds an evidence-based salary framework for your role in selected countries. It separates two local-employer segments, estimates only supported adjustments and audits the resulting targets before presenting the final comparison.

## Flow

The diagrams split one salary search into research and calculation. After validation stores usable country evidence, continue to Step 3 in the second diagram. Viewing saved results ends without new research; a resumed run returns to its next unfinished step.

### Run selection and research

```mermaid
flowchart TD
  Start(["Select this chat and person"]) --> Status{"Matching salary search?"}
  Status -->|Completed and View chosen| Replay(["Show the saved final result"])
  Status -->|Unfinished and Resume chosen| Resume(["Resume the saved next unfinished step<br/>Keep completed work"])
  Status -->|No match or Start fresh chosen| Profile["Create a separate run<br/>Reuse or confirm this person's profile"]
  Status -->|Needs repair| Recover(["Explain the issue<br/>Offer repair or a fresh run"])
  Profile --> S1["1. Confirm countries<br/>Research local salaries and reference visa salary rules"]
  S1 --> S2["2. Validate and store research"]
  S2 --> Stored{"Any country stored?"}
  Stored -->|No| Repair(["Record what is known<br/>Offer evidence repair or stop"])
  Stored -->|Yes| Continue["Continue below with supported country evidence"]
```

### Adjustment, calculation and verification

```mermaid
flowchart TD
  S3["3. Estimate supported international adjustments"]
  S3 --> S4["4. Calculate comparable salary targets<br/>Record skipped countries"]
  S4 --> Usable{"Any country calculated?"}
  Usable -->|No| Repair(["Save the skip-only outcome<br/>Offer evidence repair or stop"])
  Usable -->|Yes| Ladder["5a. Draft or reuse the matching career ladder<br/>Wait for confirmation if needed"]
  Ladder --> Audit["5b. Audit the salary framework<br/>Revise only when evidence supports it"]
  Audit --> Fresh{"Essential evidence needs refresh?"}
  Fresh -->|Yes| Choice["Wait: refresh evidence, retain a disclosed snapshot or stop"]
  Choice -->|Evidence or approved snapshot| Final["Save and check the full audit"]
  Choice -->|Stop or still blocked| Pending["Preserve earlier outputs; keep the final audit unfinished"]
  Fresh -->|No| Final
  Final --> End(["Show the final salary table and audit outcome"])
```

## Start the command

Run salary-calculator for the selected person. If no confirmed resume profile is available, provide a resume and confirm the extracted profile. Situational facts such as current location, citizenship, working languages and work rights are reused when already confirmed, including applicable answers from Country Finder. Only missing material context needs clarification.

A personal pay minimum is optional. If you supply one, its currency, pay basis and whether it is firm or contextual matter for the later comparison; it does not set either market target. Leaving it unspecified allows the salary research to proceed.

New chats start fresh. The same chat can view a completed search, resume an unfinished one or start a separate fresh run. Earlier profiles and outputs remain preserved rather than being replaced with whichever result is newest.

## What to expect

### Choose countries and collect local benchmarks

[Research](step1-research-prompt-generator.html) confirms the country list. Your supplied list is used exactly. Otherwise, the previous CF/SC search for this person in this chat can supply its full country scope, with own/default-list alternatives. Excluded or skipped countries remain available because this reuses names rather than conclusions. There is no remote-versus-relocation scope question: both salary segments describe employees paid locally in the target country.

Mainstream covers mid-size or mainstream local-market employers, while Premium covers premium, international or remote-first employers. They are researched separately rather than treated as lower and upper points of one generic range. Research collects gross annual base-pay benchmarks, supporting sources and a separately identified visa salary rule. A local salary estimate does not establish cross-border Remote pay or an employer's willingness to sponsor you.

### Preserve evidence and assess the adjustment

[Validation](step2-data-validation.html) checks required content and stores accepted research unchanged. Missing or rejected country data is explained, and original duplicates are retained.

[International adjustment](step3-international-adjustment.html) estimates a defensible reduction from local benchmarks for this candidate's position in that market. Without enough evidence, it records that the adjustment cannot be estimated instead of assuming 0%. A well-supported zero and a lack of information have different implications.

### Calculate and verify the framework

[Calculation](step4-table-calculation.html) applies the supported inputs consistently, produces annual and monthly references, and reports visa-pay comparisons separately. Targets are not inflated to clear a visa rule or your personal minimum.

Before the [final audit](step5b-final-verification.html), you review the career ladder suited to the role. The audit then checks level positioning, the two segments, adjustments, arithmetic and evidence. Adjustment, calculation review and the final audit run on your current model and effort without model-selection prompts. A calculable search still needs that final verification.

## Your result

Chat shows local-currency annual and monthly targets for both segments and the Visa salary rule. The saved report carries the reasoning, limitations and calibration behind that compact table.

A salary rule is only one part of immigration eligibility. A higher target does not prove sponsorship, and a range that crosses a threshold cannot be reported as entirely below it. Currency, gross/net basis, pay period and source dates must be comparable before drawing those conclusions.

If no country has usable estimates, the workflow saves the required outcome and offers evidence repair or stop. It does not ask for a career ladder or manufacture an empty final table. If an audit needs fresh evidence, you choose refresh, a dated-snapshot continuation with limitations, or stop.

The final figures are role-specific estimates grounded in the cited snapshot, not guaranteed offers. Country Finder may later offer the saved research country names without inheriting these conclusions. See [calculation runtime](step4-table-calculation.html#calculation-runtime) for the execution and fallback requirements.

## Explore the source

For implementation details, read [workflows/salary-calculator.md](https://github.com/myowinthein/agent-compass/blob/main/workflows/salary-calculator.md).
