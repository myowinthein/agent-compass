---
title: "Step 5: Scoring"
parent: country-finder
grand_parent: Commands
nav_order: 5
---

# Step 5: Scoring

Assess Remote and Sponsorship separately using categorical fits and confidence, without numerical scores.

## Flow

```mermaid
flowchart TD
  Start(["Offer the optional deep-reasoner<br/>Or use your current model"]) --> Carry["Read all Step 2 countries<br/>Carry explicit exclusions with their reasons"]
  Carry --> Remote["Assess all Remote tracks first<br/>Missing or unusable evidence stays not scored"]
  Remote --> Floor{"Whole comparable range below a hard floor?"}
  Floor -->|Yes| Exclude["Exclude Remote<br/>Record the exact shortfall"]
  Floor -->|No or unverified| Fit["Assign supported fit and confidence where possible<br/>Do not invent a failed comparison"]
  Exclude --> Sponsorship["Assess all Sponsorship tracks independently<br/>Keep any visa-pay comparison informational"]
  Fit --> Sponsorship
  Sponsorship --> Coverage["Account for every country on each track<br/>Fit, exclusion or missing-data reason"]
  Coverage --> Save["Save country-finder-05-assessment.md<br/>Keep reasoning and evidence in the file"]
  Save --> Next(["Show brief scored and excluded counts<br/>Continue to the final audit"])
```

## Fit and confidence

Supported tracks receive Strong, Moderate or Weak fit and High, Medium or Low confidence. Vague, old or unsourced evidence lowers confidence. No usable evidence means `not scored (no data)`, not an invented Weak fit.

Earlier exclusions retain their reasons and affect only their own track.

## Salary checks

Remote exclusion needs a comparable pay range entirely below your hard floor. Context-only minima, missing conversion or a straddling range do not prove failure.

Sponsorship can use an optional compatible Salary Calculator [visa-pay comparison](../salary-calculator/step4-table-calculation.html#visa-salary-rule-comparison). Completed final figures take precedence over pre-audit values. This does not independently exclude a country or establish visa eligibility; local-employee targets do not prove cross-border Remote pay.

## What happens next

The assistant saves `country-finder-05-assessment.md` and shows brief counts. An optional [specialist]({{ '/docs/specialist-agents.html' | relative_url }}) can run the step; [Final ranking](step6-final-ranking.html) always follows.
