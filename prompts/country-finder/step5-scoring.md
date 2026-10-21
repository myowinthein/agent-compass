Check whether cf-step4-country-data.md exists in the workspace. If it does not exist, stop and tell me: "cf-step4-country-data.md was not found. Please ensure Step 4 completed successfully before continuing."

Read cf-step2-candidates.md, cf-step4-country-data.md, cf-step1-criteria.md, and situational-profile.md from the workspace. Use Step 2's full candidate universe to account for each country on each track, and the stored Step 4 data to score eligible tracks.

Preserve the assessed candidate/role/level, location/path and evidence dates from the confirmed criteria/research in file-only context prose. Apply the shared runtime's clarification/repair rule if materially inconsistent with current facts; do not reinterpret old research as a new target.

Keep Remote and Sponsorship scoring completely separate. Use categorical fits and confidence only, never numerical scores, percentages, or a combined priority formula. Step 6 assigns application priorities after its audit; do not convert legacy numeric scores into new fits without supporting stored evidence.

Read and apply skills/salary-comparison-rules.md before judging a salary minimum. A missing exchange rate, ambiguous gross/net basis, or range straddling the floor is an unverified comparison, not proof of failure. If available, read the Validation report in cf-step3-country-research.md to explain missing Step 4 data; distinguish research rejected during ingestion from research never supplied. Keep that report out of the scored datasets.

Before scoring a country on either track, check that track's Step 2 Suitable value:
- An explicit "no" (including "no — outside your max timezone of [N] hours") is an earlier exclusion. Carry it into this track's excluded list with the recorded reason and any hard-rule detail; do not score it or relabel it as missing data, even if incidental data for that track was stored. This does not exclude the country's other track.
- "no evidence found," an absent suitability finding, or missing Step 4 research without an explicit exclusion is not a reasoned rejection. Account for it as "not scored (no data)" in that track's results, state what is missing, and leave it for Step 6's missing-candidate audit. Do not invent a fit or count it as excluded.
- Score a track marked "yes" only when its required Step 4 data is present. Never infer that a track failed merely because Step 3 correctly omitted research for an earlier rejection.

Batching rule: score every country's Remote fit first, all the way through, before starting Sponsorship scoring for any country. Do not alternate between tracks country by country.

For Remote Track, for each country with Remote data stored:

1. If a minimum monthly salary was specified, apply its hard-floor/context-only choice. Only a confirmed comparable Remote pay range entirely below a hard floor excludes the track; state the exact gap. For context only, use a comparable local-market midpoint only if the stored evidence supplies one; otherwise record "context-only minimum; no stored benchmark". Do not invent a midpoint. Salary Calculator's local-employee Mainstream/Premium targets, including remote-first employers, are not Remote offer evidence and cannot establish a Remote salary rejection. If no minimum was specified, skip this check.
2. If it passes, classify Remote fit as: Strong / Moderate / Weak.
3. Assign a confidence level: High / Medium / Low.
4. Give brief reasoning, referencing the actual stored evidence, not assumption.

For Sponsorship Track, for each country with Sponsorship data stored:

1. Apply skills/sponsorship-threshold-rules.md to any informational visa-pay comparison. Prefer a completed sc-step5b-final-verification.md under the shared runtime's producer-readiness rule; file existence alone is not completion. Check candidate, role/level, benchmark scope, route/category and evidence dates for compatibility. The model reads final Recalibration, separate approved visa evidence updates and Step 4 shown work, not Python's parser. Use final raw values for revised segments and Step 4 raw values only for explicitly unchanged compatible segments. Missing authoritative raw values after possible recalibration never revive superseded targets. If no final exists, stage-complete Step 4 values may be used as labelled pre-audit references; ambiguous/draft provenance leaves the check unverified unless the user explicitly chooses disclosed provisional use.
   Approved refreshed state/amount/period/eligible-pay facts in a completed final take precedence over older CF facts only for the same candidate/route/category; keep dates and source differences in the scoring notes and leave raw research untouched. Newest date alone does not establish applicability. SC Not applicable for a different intended path does not negate CF's assessed sponsorship route; Blocked is limited to its assessed route. A monthly numeric check needs the official/pay-schedule comparability required by the shared threshold rules; otherwise keep it unverified with known figures/limitations. Run `compare` only for comparable raw amounts, never rounded cells. Missing SC data is normal, not a circular dependency. This note never independently excludes a country, changes market pay or establishes overall visa eligibility.
2. Independently classify Sponsorship fit as: Strong / Moderate / Weak when applicable evidence supports it; an unverified informational salary check is not a failed track. If all applicable track evidence is unusable, record "not scored (no data)" with the reason rather than inventing Weak. Note explicitly held rights that may make sponsorship unnecessary without automatically excluding the country.
3. Assign a confidence level: High / Medium / Low.
4. Give brief reasoning, referencing the actual stored evidence, not assumption. Consider citizenship-specific friction from the situational profile when assessing confidence.

Evidence quality rule (applies to both tracks):

Read and apply skills/evidence-quality-rules.md.

For either track, if all applicable support is unusable, record "not scored (no data)" with the evidence gap, not an invented Weak fit. Successful ingestion alone does not establish applicable evidence.

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
