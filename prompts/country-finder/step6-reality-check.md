Check whether cf-step5-scoring-results.md exists in the workspace. If it does not exist, stop and tell me: "cf-step5-scoring-results.md was not found. Please ensure Step 5 completed successfully before continuing."

Read cf-step5-scoring-results.md from the workspace. Use it alongside all previously generated data and results from this conversation.

Goal

Perform a focused audit on the Step 5 results across two checks.

1. Confidence Calibration Check

For each country marked "High confidence," verify the underlying evidence is genuinely specific, sourced, and dated, not just confidently worded. Flag any confidence level that seems inflated relative to the actual evidence quality, and explain why.

2. Missing Candidate Check

Identify any country that would commonly be expected to appear but is absent from either track's results. For each one, state whether the absence was a real, evidence-based elimination (cite the reason from earlier steps) or a process gap — such as never being researched or never reaching Step 4.

Recalibration

Only if the confidence calibration check found inflated confidence levels:
- Revise the affected country's confidence level
- If the inflated confidence was masking a genuinely weaker fit, revise the classification too
- Explain what evidence caused each change

If recalibration is not supported, state explicitly that the Step 5 results remain appropriate, and do not alter them.

Summary

Output a Summary section that reorganizes Step 5's final scores (including any revisions from this step) by country rather than by track.

For each country that has data on at least one track, show one row with both its Remote fit and Sponsorship fit side by side:

- Use the final classification (Strong / Moderate / Weak / Excluded / not scored (no data)) for each track.
- "Excluded" means the country was actively eliminated on that track during Step 5 scoring. Do not restate the reason here.
- "not scored (no data)" means no research was ever ingested for that country on that track. This is distinct from Excluded and must not be blurred with it.
- If Step 6 revised a country's confidence level or classification, add a single short note beneath it.

If the Missing Candidate Check identified countries that were never researched on either track at all, list those separately under a "Flagged but not researched" heading.

Close the Summary with counts:
- Remote: [N] scored, [N] excluded, [N] not scored (no data)
- Sponsorship: [N] scored, [N] excluded, [N] not scored (no data)

No ranking, no recommendations, no interpretation.

Step complete — stop here and wait for the main command.
