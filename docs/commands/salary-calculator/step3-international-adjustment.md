---
title: Step 3: Recruiter-attraction adjustment
parent: /salary-calculator
grand_parent: Commands
nav_order: 3
---

# Step 3: Recruiter-attraction adjustment

Chooses a small strategic discount from the verified local-market midpoint when concrete international-hiring friction makes that useful.

## Purpose

The adjustment supports a simple mass-application strategy: competitive enough to attract recruiters, but not a low-ball figure and not premium pricing.

It is not a claim that foreign candidates deserve lower pay, and it does not use passport rankings or presumed nationality prestige.

## Allowed values

Claude chooses one of:

- 0 percent
- 3 percent
- 5 percent
- 7 percent
- 10 percent
- 12 percent

Twelve percent is the default hard maximum.

## Evidence

Relevant factors include sponsorship requirements, documented administrative burden, relocation friction, local residence or work authorization, genuine workplace-language requirements, sponsor availability, direct role fit, and current hiring conditions.

General hiring difficulty does not automatically justify a large salary discount. When evidence is insufficient, the default is 5 percent with Low confidence.

## Output

Each country record includes its midpoint, adjustment, level, confidence, evidence, and concise reason. Results are saved to `sc-step3-adjustment-values.md`.
