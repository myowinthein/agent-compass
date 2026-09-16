Check whether cf-step4-country-data.md exists in the workspace. If it does not exist, stop and tell me: "cf-step4-country-data.md was not found. Please ensure Step 4 completed successfully before continuing."

Read cf-step4-country-data.md, cf-step1-criteria.md, and situational-profile.md from the workspace. Using all country data from cf-step4-country-data.md and the criteria and situational profile, score each country.

Keep Remote and Sponsorship scoring completely separate. Do not blend them into a single score.

Batching rule: score every country's Remote fit first, all the way through, before starting Sponsorship scoring for any country. Do not alternate between tracks country by country.

For Remote Track, for each country with Remote data stored:

1. If a minimum monthly salary was specified in the situational profile, check whether it was marked a hard floor or context only. If a hard floor, exclude this country from the Remote results when the confirmed salary falls short, and state the specific gap (e.g. "confirmed salary $X, below your minimum of $Y"). If context only, do not exclude on this basis alone: weigh the confirmed salary against a recruiter-friendly local-market midpoint for this role and note it in the reasoning if it falls meaningfully below that midpoint. If no minimum was specified, skip this check entirely.
2. If it passes, classify Remote fit as: Strong / Moderate / Weak.
3. Assign a confidence level: High / Medium / Low.
4. Give brief reasoning, referencing the actual stored evidence, not assumption.

For Sponsorship Track, for each country with Sponsorship data stored:

1. If a visa minimum salary threshold was reported, prefer `sc-step5b-final-verification.md` when it exists; otherwise check `sc-step4-salary-table.md`. If the selected file contains an Expected Salary for this country, note whether it clears the threshold. If neither file exists or the country is absent, note the threshold as informational only, without judgment.
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
- List each excluded country: specific reason

Sponsorship Track Results
- List each scored country: fit classification, confidence, brief reasoning
- List each excluded country: specific reason

Summary
- Remote: [count] scored, [count] excluded
- Sponsorship: [count] scored, [count] excluded

Do not rank countries against each other beyond the Strong/Moderate/Weak classification. Do not add recommendations, next steps, or commentary beyond what is asked here.

Save the full scoring output to cf-step5-scoring-results.md in the workspace.

In your chat response, do not reproduce this detailed breakdown — Step 6 always runs next and produces the curated, human-facing result. Instead, tell me in a few lines: how many countries were scored and excluded on each track, and that the full results are saved to cf-step5-scoring-results.md.

Continue automatically into Step 6 now, in this same response — do not stop and wait here.
