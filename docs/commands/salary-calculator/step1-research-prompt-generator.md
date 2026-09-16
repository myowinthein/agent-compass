---
title: Step 1: Salary research
parent: /salary-calculator
grand_parent: Commands
nav_order: 1
---

# Step 1: Salary research

Confirms the active target countries and researches one broad, practical salary market per country.

## Country selection

Claude prefers `cf-step6-final-ranking.md` when available. It proposes countries above the active-application cutoff, or the Gold group when medals are used, preserves Priority Table order, and waits for confirmation.

## Research basis

Every country uses the confirmed role, level, and employment basis. Local-relocation pay and cross-border remote pay are never blended.

The broad-market sample can include mainstream employers, established startups, scale-ups, ordinary international employers, and sponsor-capable employers. It excludes elite-only compensation, contractor rates unless relevant, equity-heavy total compensation, junior roles, and obvious low-wage outliers.

## Required evidence

Claude aims for at least three independent current sources per country, including direct-employer postings, recruiter guides, or strong local datasets where available. Each source records its URL, date, role, level, location, salary figure, period, and compensation basis.

Research produces:

- Market Low
- Realistic midpoint
- Market Strong
- Currency and market coverage
- Compensation basis
- Candidate-applicable sponsorship threshold record
- Source and limitation notes

The figures must satisfy `Low <= Midpoint <= Strong`.

## Isolation and output

Each country runs as an isolated research task. Agents return results to the main agent rather than appending to a shared file. The main agent writes one country file at a time under `sc-research/`, updates state, and assembles `sc-step1-salary-research.md` in confirmed order.
