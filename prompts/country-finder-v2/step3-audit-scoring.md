# Step 3: Independent audit and final scoring

Require and read:

- `cfv2-step1-criteria.md`
- `cfv2-step2-country-universe.md`
- `cfv2-step2-research.md`
- `profile.md`
- `skills/country-finder-v2-scoring-rules.md`

Audit the research rather than merely checking that fields exist.

When parallel agents are available, give each auditor a non-overlapping country batch and require a unique output file named `cfv2-step3-audit-<slug>.md`. An auditor must reopen decisive sources and challenge the provisional score. The parent consolidates all audits and resolves inconsistencies.

For every country:

1. Verify official legal claims against current official sources.
2. Verify decisive remote or sponsorship claims against direct employer pages where possible.
3. Downgrade an aggregator label when the direct page is silent, narrower, closed, or contradictory.
4. Ensure domestic remote has not been counted as cross-border remote.
5. Ensure a legal route or sponsor register has not been counted as employer willingness.
6. Ensure one vacancy has not been counted as deep market volume.
7. Check language, citizenship, age, salary, occupation mapping, and location constraints against the actual candidate.
8. Recalculate the six Remote components, six Sponsorship components, classifications, priority score, and tier.
9. Assign evidence confidence: High, Medium, or Low.
10. State the decisive reason and any uncertainty in one or two sentences.

The audited score is authoritative. Later steps must never substitute the provisional score.

Save one final table plus concise per-country audit notes to `cfv2-step3-audited-scores.md`. The table columns are:

`Country | Remote score and class | Sponsorship score and class | Priority | Tier | Confidence | Decisive reason`

Account for every country in the Step 2 universe exactly once. If evidence is insufficient, score conservatively and say so instead of dropping the country.

Update state to Step 3 and continue automatically to Step 4.

