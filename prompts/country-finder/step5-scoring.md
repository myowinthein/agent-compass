Check whether cf-step4-country-data.md exists in the workspace. If it does not exist, stop and tell me: "cf-step4-country-data.md was not found. Please ensure Step 4 completed successfully before continuing."

Read cf-step2-candidates.md, cf-step4-country-data.md, cf-step1-criteria.md, and situational-profile.md from the workspace. Use Step 2's full candidate universe to account for each country on each track, and the stored Step 4 data to score eligible tracks.

Keep Remote and Sponsorship scoring completely separate. Use categorical fits and confidence only, never numerical scores, percentages, or a combined priority formula. Step 6 assigns application priorities after its audit; do not convert legacy numeric scores into new fits without supporting stored evidence.

Read and apply skills/salary-comparison-rules.md before judging a salary minimum. A missing exchange rate, ambiguous gross/net basis, or range straddling the floor is an unverified comparison, not proof of failure. If available, read the Validation report in cf-step3-country-research.md to explain missing Step 4 data; distinguish research rejected during ingestion from research never supplied. Keep that report out of the scored datasets.

Before scoring a country on either track, check that track's Step 2 Suitable value:
- An explicit "no" (including "no — outside your max timezone of [N] hours") is an earlier exclusion. Carry it into this track's excluded list with the recorded reason and any hard-rule detail; do not score it or relabel it as missing data, even if incidental data for that track was stored. This does not exclude the country's other track.
- "no evidence found," an absent suitability finding, or missing Step 4 research without an explicit exclusion is not a reasoned rejection. Account for it as "not scored (no data)" in that track's results, state what is missing, and leave it for Step 6's missing-candidate audit. Do not invent a fit or count it as excluded.
- Score a track marked "yes" only when its required Step 4 data is present. Never infer that a track failed merely because Step 3 correctly omitted research for an earlier rejection.

Batching rule: score every country's Remote fit first, all the way through, before starting Sponsorship scoring for any country. Do not alternate between tracks country by country.

For Remote Track, for each country with Remote data stored:

1. If a minimum monthly salary was specified in the situational profile, check whether it was marked a hard floor or context only. If a hard floor, exclude this country from the Remote results when the confirmed salary falls short, and state the specific gap (e.g. "confirmed salary $X, below your minimum of $Y"). If context only, do not exclude on this basis alone: weigh the confirmed salary against a recruiter-friendly local-market midpoint for this role and note it in the reasoning if it falls meaningfully below that midpoint. If no minimum was specified, skip this check entirely.
2. If it passes, classify Remote fit as: Strong / Moderate / Weak.
3. Assign a confidence level: High / Medium / Low.
4. Give brief reasoning, referencing the actual stored evidence, not assumption.

For Sponsorship Track, for each country with Sponsorship data stored:

1. If a visa minimum salary threshold was reported, prefer a completed sc-step5b-final-verification.md over sc-step4-salary-table.md. Establish completion through `state-check` under skills/helper-runtime.md or explicit trustworthy saved completion metadata; file existence alone is not completion. The model reads the final Recalibration and Step 4 shown work, not Python's parser. Use final raw values for revised segments; reuse Step 4 raw values only for explicitly unchanged segments whose inputs still match. If a completed final was or may have been recalibrated but its raw values cannot be established, do not silently fall back to superseded Step 4 figures. If final is absent, Step 4 raw values may be used; a draft without completion evidence never overrides them. Run `compare` under skills/comparison-helper.md for a comparable numeric check. Missing/ambiguous completion evidence or authoritative raw inputs leaves the comparison unverified. Never judge from rounded salary cells. Keep the threshold informational when no valid comparison can be made, and never turn this note into an exclusion or overall eligibility conclusion.
2. If it passes, classify Sponsorship fit as: Strong / Moderate / Weak.
3. Assign a confidence level: High / Medium / Low.
4. Give brief reasoning, referencing the actual stored evidence, not assumption. Consider citizenship-specific friction from the situational profile when assessing confidence.

Evidence quality rule (applies to both tracks):

Read and apply skills/evidence-quality-rules.md.

Exclusion transparency rule:

Read and apply skills/exclusion-transparency-rules.md.

File format (write this structure to cf-step5-scoring-results.md — this is not what you show in chat, see below):

Remote Track Results
- List each scored country: fit classification, confidence, brief reasoning
- List each excluded country: specific reason, including exclusions carried from Step 2
- Account for each unresearched country/track as "not scored (no data)" with what is missing

Sponsorship Track Results
- List each scored country: fit classification, confidence, brief reasoning
- List each excluded country: specific reason, including exclusions carried from Step 2
- Account for each unresearched country/track as "not scored (no data)" with what is missing

Summary
- Remote: [count] scored, [count] excluded
- Sponsorship: [count] scored, [count] excluded

Excluded counts include earlier Step 2 exclusions; do not count those tracks as scored. Missing-data tracks belong to neither count and must still be accounted for in the track results above.

Do not rank countries against each other beyond the Strong/Moderate/Weak classification. Do not add recommendations, next steps, or commentary beyond what is asked here.

Save the full scoring output to cf-step5-scoring-results.md in the workspace.

In your chat response, do not reproduce this detailed breakdown — Step 6 always runs next and produces the curated, human-facing result. Instead, tell me in a few lines: how many countries were scored and excluded on each track, and that the full results are saved to cf-step5-scoring-results.md.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
