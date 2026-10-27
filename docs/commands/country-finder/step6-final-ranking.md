---
title: "Step 6: Final ranking"
parent: country-finder
grand_parent: Commands
nav_order: 6
---

# Step 6: Final ranking

Audits the assessments and turns them into a practical application priority for each country. This step always runs, even if you decline a specialist.

## Flow

```mermaid
flowchart TD
  Start(["Offer the optional deep-reasoner<br/>Or use your current model"]) --> C1["Check confidence<br/>Is it backed by specific, dated evidence?"]
  C1 --> C2["Check missing countries and tracks<br/>Preserve early exclusions<br/>Distinguish missing from rejected research"]
  C2 --> C3["Check evidence use<br/>Local remote is not cross-border hiring<br/>A visa route is not employer willingness<br/>One vacancy is not a deep market"]
  C3 --> Verdict{"Evidence supports a revision?"}
  Verdict -->|Yes| Revise["Revise affected fits or confidence<br/>Explain the evidence"]
  Verdict -->|No| Keep["Keep supported assessments<br/>Name inconclusive findings"]
  Revise --> Summary["Build the post-audit Summary<br/>Account for every candidate on both tracks"]
  Keep --> Summary
  Summary --> Priority["Assign application priorities and limitations<br/>Check the saved Summary and table agree"]
  Priority --> Save["Save audit, Summary, Priority Table<br/>and Effort Allocation"]
  Save --> End(["Show the Priority Table in chat<br/>Confirm completion and saved file"])
```

## What the audit protects

An early timezone or suitability rejection stays Excluded with its reason. Missing research, rejected data and unusable evidence stay distinct from a supported Weak fit.

An exclusion on one track does not supply research for the other. Without ingested research, that other track remains unscored and appears as Unknown.

If an audit invalidates a track's only usable evidence, that track becomes `not scored (no data)`. The table displays it as Unknown. The audit does not silently undo an early exclusion or reinterpret research for a changed profile; those issues require a repair choice.

## Priority Table

Priority describes where to spend application effort:

- 🥇 Focus: concentrate effort on the best supported opportunities.
- 🥈 Selective: apply to well-matched openings despite a narrower market or limitation.
- 🥉 Monitor: watch for occasional strong matches.
- 🎗️ Deprioritize: both tracks are known Weak or Excluded.
- Pending evidence: neither track is Strong or Moderate and at least one is Unknown.

Focus, Selective and Monitor each need at least one Strong or Moderate track. Assignment considers your role match, opportunities, accessibility, pay, visa practicality and evidence quality. It is not a formula, probability or reward for having two usable tracks.

These fictional examples show the table's possible outcomes:

| Country | Priority | Remote Fit | Sponsorship Fit | Main limitation |
|---|---|---|---|---|
| 🏳️ Example A | 🥇 Focus | Strong | Moderate | None identified |
| 🏳️ Example B | 🥈 Selective | Weak | Strong | Sponsorship: limited relevant openings |
| 🏳️ Example C | 🥈 Selective | Strong | Unknown | Sponsorship: research missing |
| 🏳️ Example D | 🥉 Monitor | Moderate | Moderate | Low current opportunity volume |
| 🏳️ Example E | 🎗️ Deprioritize | Weak | Weak | Few suitable openings on either track |
| 🏳️ Example F | 🎗️ Deprioritize | Excluded | Excluded | Remote: timezone limit; sponsorship: no eligible pathway |
| 🏳️ Example G | Pending evidence | Unknown | Weak | Remote: research missing |
| 🏳️ Example H | Pending evidence | Excluded | Unknown | Sponsorship: research rejected at validation |
| 🏳️ Example I | Pending evidence | Unknown | Unknown | Research not supplied for either track |

Assessed priorities are grouped in the order above, then ordered by supported opportunity for your profile. Alphabetical order is the final tie-breaker. Pending evidence rows are alphabetical, not ranked as recommendations.

Main limitation is a short, supported constraint or gap. Detailed reasons and sources stay in the audit.

## What is saved

`country-finder-06-final-results.md` contains the three audit checks, Recalibration verdict, post-audit Summary, Priority Table and Effort Allocation.

Every candidate is accounted for once per track, including early exclusions and missing or rejected research. A duplicate with a retained original is not missing. Extra countries mentioned only as audit observations do not become table rows.

Only the Priority Table and completion message appear in chat. The message does not assume an actionable country exists when everything is Deprioritize or Pending evidence.

## Using the result

The post-audit Summary is authoritative. [Salary Calculator](../salary-calculator.html) selects eligible countries from it and uses the Priority Table only for row order.

Original research and Step 5 remain unchanged. Completed runs replay their saved results, including older table formats, without migration.

For model choices and approval, see [Specialist agents]({{ '/docs/specialist-agents.html' | relative_url }}).
