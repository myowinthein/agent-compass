Check whether cf-step5-scoring-results.md exists in the workspace. If it does not exist, stop and tell me: "cf-step5-scoring-results.md was not found. Please ensure Step 5 completed successfully before continuing."

Read cf-step5-scoring-results.md from the workspace. Also read cf-step2-candidates.md, cf-step4-country-data.md, cf-step1-criteria.md, situational-profile.md, and profile.md from the workspace. cf-step2-candidates.md is the full candidate universe — use it to detect any country that was a Step 2 candidate but never reached Step 4. Base the audit only on these files, not on prior conversation memory.

Goal

Perform a focused audit on the Step 5 results across two checks.

1. Confidence Calibration Check

For each country marked "High confidence," verify the underlying evidence is genuinely specific, sourced, and dated, not just confidently worded. Flag any confidence level that seems inflated relative to the actual evidence quality, and explain why.

2. Missing Candidate Check

Compare cf-step2-candidates.md against the countries that actually reached Step 4 and Step 5, and also consider any country that would commonly be expected to appear but is absent. For each missing country, state whether the absence was a real, evidence-based elimination (cite the reason from earlier steps) or a process gap — such as being on a Step 2 candidate list but never researched or never reaching Step 4.

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

Priority Table

After the Summary above, produce one additional Markdown table.

Columns: Country | Tier | Remote Fit | Sponsorship Fit

Tier is two independent parts — a word and a medal.

The word identifies which application track is usable. Remote Fit and Sponsorship Fit for this table are read directly from cf-step5-scoring-results.md — Step 5 is the authoritative source for these two values. Never substitute a Step 6 recalibration here, even if the Summary above revised a country's classification; this table's Fit columns must trace back to Step 5's original ratings only.
- Both: Remote Fit and Sponsorship Fit are each Strong or Moderate.
- Remote: Remote Fit is Strong or Moderate; Sponsorship Fit is Weak or unavailable.
- Sponsorship: Sponsorship Fit is Strong or Moderate; Remote Fit is Weak or unavailable.
- Limited: Neither track reaches Moderate.

The medal (🥇 / 🥈 / 🥉 / 🎗️) is a holistic judgment of expected application priority for this specific candidate — never calculated mechanically from the two Fit values alone, and never based solely on confidence. This is where Step 6's own audit work feeds in: use this step's evidence-quality and confidence-calibration findings to weigh how much to trust the underlying evidence, without changing the Fit values themselves. Assign the medal using:
- Direct match to the candidate's seniority, skills, and target industries, from profile.md.
- Quantity and recency of relevant job opportunities.
- Evidence that remote positions accept the candidate's current location.
- Evidence that employers sponsor this specific profession.
- Salary compatibility.
- Visa practicality, processing time, and employer burden.
- Language and citizenship barriers.
- Strength and reliability of the supporting evidence, informed by this step's Confidence Calibration Check.

Medal meanings:
- 🥇: Highest expected return — concentrate application time here.
- 🥈: Good opportunity, but with a narrower market or meaningful limitation.
- 🥉: Selective opportunity with material barriers or lower expected conversion.
- 🎗️: Limited opportunity because neither track reaches Moderate — always paired with the word "Limited."

There is no fixed quota or required number of countries for any medal. A country with Moderate Remote Fit and Moderate Sponsorship Fit can still receive 🥉 if hiring volume is low, evidence is weak, language barriers are substantial, or expected application conversion is poor.

Valid Tier values: 🥇 Both, 🥇 Remote, 🥇 Sponsorship, 🥈 Both, 🥈 Remote, 🥈 Sponsorship, 🥉 Both, 🥉 Remote, 🥉 Sponsorship, 🎗️ Limited.

Sort the table by medal first (🥇, then 🥈, then 🥉, then 🎗️). Within the same medal, sort by the candidate's expected chance of obtaining a suitable job in that country, using the same factors above — never alphabetically as a first pass. If countries remain effectively tied, apply these tie-breakers in order:
1. Stronger match to the candidate's stated domain expertise, industry background, and target role, from profile.md.
2. More concrete named-employer or current-job evidence.
3. Better accessibility from the candidate's current location, or clearer sponsorship willingness.
4. Better salary and processing timeline.
5. Higher evidence confidence.
6. Alphabetical order, only as the final tie-breaker.

Formatting rules:
- Place the country's flag emoji directly after its name.
- Remote Fit and Sponsorship Fit may contain only: Strong, Moderate, Weak, or — (Unicode em dash, for unavailable, excluded, or unresearched data).
- Do not add notes, asterisks, citations, explanations, or footnotes to this table.
- Include every country from the Summary above exactly once.
- Output only the table for this section — no surrounding commentary.

Use this exact header:

| Country | Tier | Remote Fit | Sponsorship Fit |
|---|---|---|---|

Save the Summary and the Priority Table to cf-step6-reality-check.md in the workspace — this is the final, post-audit classification, and later steps or pipelines should prefer it over cf-step5-scoring-results.md if both exist.

Step complete — stop here and wait for the main command.
