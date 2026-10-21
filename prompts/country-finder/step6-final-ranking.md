Check whether cf-step5-scoring-results.md exists in the workspace. If it does not exist, stop and tell me: "cf-step5-scoring-results.md was not found. Please ensure Step 5 completed successfully before continuing."

Read cf-step5-scoring-results.md from the workspace. Also read cf-step2-candidates.md, cf-step4-country-data.md, cf-step1-criteria.md, situational-profile.md, and profile.md from the workspace. cf-step2-candidates.md is the full candidate universe — use it to detect any country that was a Step 2 candidate but never reached Step 4. Base the audit only on these files, not on prior conversation memory.

Use recorded, user-confirmed run-only clarifications under the shared runtime as saved context, not hidden memory. Preserve assessed candidate/role/level, path/location and evidence dates with the file-only audit, outside canonical rendered sections. Material changed-input or contradicted-exclusion issues return to the parent for the shared repair choice before finalisation; never silently override an early reason or rewrite completed outputs.

Read and apply skills/evidence-quality-rules.md and skills/exclusion-transparency-rules.md when auditing classifications, assigning priorities, and summarizing limitations.

Read data/output-contracts.json as data and skills/output-helper.md. After choosing the evidence-supported final decisions below, use `render-cf` with the full candidate universe, original early exclusions and ingestion dispositions. Save its returned Summary and Priority Table sections verbatim, keep its audit notes with the three checks, and run `check-saved` before completion. Pure helper requests unavailable to a specialist return to the parent under the shared runtime. Under an explicitly approved manual run, read this same contract for the format and perform the same checks; do not claim automated rendering ran.

Goal

Perform a focused audit on the Step 5 results across three checks.

Save the three named audit checks and Recalibration verdict at the top of cf-step6-final-ranking.md, before Summary, Priority Table, and Effort Allocation. All audit details stay file-only. This step writes only that existing final file; leave source research and Step 5 outputs untouched.

1. Confidence Calibration Check

For each country marked "High confidence," verify the underlying evidence is genuinely specific, sourced, and dated, not just confidently worded. Flag any confidence level that seems inflated relative to the actual evidence quality, and explain why.

2. Missing Candidate Check

Compare cf-step2-candidates.md against the countries that actually reached Step 4 and Step 5, and also consider any country that would commonly be expected to appear but is absent. For each missing country, state whether the absence was a real, evidence-based elimination (cite the reason from earlier steps) or a process gap — such as being on a Step 2 candidate list but never researched or never reaching Step 4.

Reconcile this per track, not just per country. Preserve each explicit Step 2 "no" and its recorded reason as Excluded, including timezone rejections; missing downstream research after that rejection is expected, not a process gap. Apply this even when resuming from an older Step 5 output that omitted the earlier exclusion. "no evidence found" or absent research without an explicit rejection remains a missing-data case, not Excluded. Never let an earlier exclusion on one track remove the other track.

If cf-step3-country-research.md exists, read its Validation report and available raw blocks to distinguish never-supplied research from researched data rejected in Step 4. Record the exact rejection reason or state that the legacy ingestion outcome is unknown. A duplicate whose original was retained is not a missing country. Do not reinterpret an ingestion error as an evidence-based country exclusion.

3. Evidence Misuse Check

For each scored country, check the stored Reason text for these specific misreadings:
- Domestic-only remote-work evidence (a policy or listing that only covers workers already inside that country) counted as proof of cross-border remote hiring.
- A legal visa route or sponsor-eligibility register treated as proof of actual employer willingness to sponsor this candidate's role, rather than proof that sponsorship is merely possible.
- A single job vacancy or hiring example treated as evidence of deep, ongoing market demand.

Flag any country whose fit classification or confidence rests on one of these misreadings, and explain what the underlying evidence actually supports.

Recalibration

If the confidence calibration check found inflated confidence levels, or the evidence misuse check found a misreading that changes a country's real fit:
- Revise the affected country's confidence level
- If the inflated confidence or evidence misuse was masking a genuinely weaker fit, revise the classification too
- Explain what evidence caused each change

If recalibration is not supported, distinguish evidence-supported unchanged fits from an inconclusive audit, naming each material gap rather than always claiming the results remain appropriate. When the only applicable support for a stored track is invalidated, use "not scored (no data)" with the specific reason; raw ingestion is not proof of usable evidence. Weak requires evidence of a weak fit. Keep original research and Step 5 untouched.

Summary

Write a Summary section into the file (not shown in chat — the Priority Table below is the only thing from this step shown in chat) that reorganizes Step 5's final scores (including any revisions from this step) by country rather than by track.

For each country that has ingested research or a recorded exclusion on at least one track, show one row with both its Remote fit and Sponsorship fit side by side:

- Use the final classification (Strong / Moderate / Weak / Excluded / not scored (no data)) for each track.
- "Excluded" means the country was explicitly eliminated on that track in Step 2 or Step 5. Preserve the original reason and hard-rule detail in the file's audit findings; do not substitute a missing-data explanation.
- "not scored (no data)" means required research was not ingested or applicable evidence proved unusable, without a supported explicit exclusion. Preserve the precise missing/invalidated-evidence reason; do not relabel a known weak fit or an early exclusion as uncertainty.
- If Step 6 revised a country's confidence level or classification, keep the short revision note in Recalibration with the audit checks, not inside the verbatim generated Summary sections.

If the Missing Candidate Check identified countries with neither ingested research nor a recorded exclusion on either track, account for them separately. Keep the existing "Flagged but not researched" heading for research genuinely never supplied. Add a file-only note for "Researched but not ingested" with the validation reason when research was rejected, or "Ingestion outcome unknown" for unsupported legacy cases. Do not label rejected research as never researched or put intentionally excluded countries in a process-gap list. These notes do not add Summary fit categories; the Priority Table below renders their missing-data tracks as Unknown.

In those reasons identify the stage: "discovery found no evidence; detailed research not run" is different from no discovery result or rejected detailed research. An all-Pending final is a valid evidence-gap outcome, not a claim every country is unsuitable; do not automatically expand research scope to fix it.

Close the Summary with counts:
- Remote: [N] scored, [N] excluded, [N] not scored (no data)
- Sponsorship: [N] scored, [N] excluded, [N] not scored (no data)

Count each Step 2 candidate once per track, including all separately noted missing-data/ingestion cases. Count explicit early rejections as excluded, not missing data. Report any additional expected-but-absent countries separately from these candidate-universe totals.

The Summary itself contains no ranking, recommendations, or interpretation beyond the classifications above — ranking is reserved for the Priority Table below.

Priority Table

Below the Summary in the file, also write this Priority Table. Unlike the Summary, show this table directly in your chat response too — this is the only thing from this step shown in chat.

The column order and literal display tokens are defined once in the `country` object of data/output-contracts.json. The renderer also supplies a fixed-header Summary table for newly generated results; legacy Summaries remain model-read and are not rewritten on completed replay.

Read Remote Fit and Sponsorship Fit from this step's post-audit Summary, including every supported recalibration and carried exclusion. The Summary is authoritative for final fit classifications; do not copy a superseded Step 5 rating into this table. Leave cf-step5-scoring-results.md untouched as the pre-audit record.

Fit display:
- Strong, Moderate, Weak, and Excluded retain their exact Summary classification.
- Render "not scored (no data)" as Unknown in this table only, including missing-data cases accounted for in the Summary's separate notes. Keep the Summary's original wording and counts unchanged for downstream consumers.
- Unknown is missing or unusable evidence, not a weak fit or a proven exclusion. Do not use a dash to collapse these states.

Priority is a holistic judgment of application effort for this specific candidate, not a numerical score, probability, or formula derived from the two fits. Having two usable tracks does not automatically earn a bonus. Use this step's evidence-quality and confidence-calibration findings alongside the final fits; assigning priority must not independently change those fits. Weigh:
- Direct match to the candidate's seniority, skills, and target industries, from profile.md.
- Quantity and recency of relevant job opportunities.
- Evidence that remote positions accept the candidate's current location.
- Evidence that employers sponsor this specific profession.
- Salary compatibility.
- Visa practicality, processing time, and employer burden.
- Language and citizenship barriers.
- Strength and reliability of the supporting evidence, informed by this step's Confidence Calibration Check.

Valid Priority values and decision boundaries:
- 🥇 Focus: at least one track is Strong or Moderate, with the highest supported expected return; concentrate application effort here.
- 🥈 Selective: at least one track is Strong or Moderate, but a narrower market or material limitation makes well-matched openings the better use of effort.
- 🥉 Monitor: at least one track is Strong or Moderate, but limited current opportunities or substantial barriers favor alerts and occasional exceptional matches.
- 🎗️ Deprioritize: both tracks are known Weak or Excluded; neither is currently usable.
- Pending evidence: neither track is Strong or Moderate and at least one is Unknown. This is unranked, not a negative recommendation; resolve the evidence gap before judging application priority.

When one track is Strong or Moderate and the other is Unknown, assign Focus, Selective, or Monitor using only the supported usable track and explain the material limitation. Never assume the unknown track helps or fails. There is no quota per priority and no automatic mapping from Strong versus Moderate or confidence alone: a Moderate/Moderate country can still warrant Monitor because of opportunity volume or barriers.

Main limitation:
- Write one short, country-specific phrase naming the most decision-relevant constraint or evidence gap for the candidate's usable track(s), or the reason for Deprioritize/Pending evidence.
- Use only stored findings and this audit. Do not invent a barrier, perform new research, or turn an informational visa salary threshold into a confirmed salary shortfall. If a constraint affects only one track, identify that track.
- For Pending evidence, name the missing or rejected research; keep the detailed ingestion reason in the audit. For Deprioritize, summarize the supported weakness or exclusion. If no material limitation is supported, write "None identified"; do not manufacture one to fill the cell.
- Full reasons and source references stay in the audit, not in this compact phrase.

Sort by Priority: Focus, Selective, Monitor, Deprioritize, then Pending evidence. Within the same assessed priority, sort by the candidate's supported expected chance of obtaining a suitable job using the same factors above, never alphabetically as a first pass. If countries remain effectively tied, apply these tie-breakers in order:
1. Stronger match to the candidate's stated domain expertise, industry background, and target role, from profile.md.
2. More concrete named-employer or current-job evidence.
3. Better accessibility from the candidate's current location, or clearer sponsorship willingness.
4. Better salary and processing timeline.
5. Higher evidence confidence.
6. Alphabetical order, only as the final tie-breaker.

Sort Pending evidence alphabetically by country name, ignoring flag emoji; do not imply an evidence-based ranking among those countries.

Formatting rules:
- Place the country's flag emoji directly before its name (e.g., "🇭🇰 Hong Kong").
- Remote Fit and Sponsorship Fit may contain only: Strong, Moderate, Weak, Excluded, or Unknown.
- Include every country accounted for in the Summary exactly once, including candidates in its separate missing-data/ingestion notes. These candidates receive Unknown on tracks without a recorded fit or exclusion. Do not promote additional expected-but-absent countries outside the candidate universe from audit commentary into the table.
- Do not add scores, percentages, redundant track words such as Both, citations, asterisks, or footnotes anywhere in the table. Explanatory prose belongs only in Main limitation.
- Output only the table for this section, with no surrounding commentary.

Use the contract's exact header, produced by `render-cf`, rather than a second template.

Effort Allocation

Below the Priority Table in the file only (never shown in chat), add a short paragraph expanding its action labels into a practical plan: focused effort and tailored applications for Focus, well-matched openings for Selective, alerts and occasional exceptional matches for Monitor, no active effort for Deprioritize, and research gaps to resolve for Pending evidence. Use the same candidate-specific evidence as the table; do not contradict its labels or allocate effort by an invented numerical formula.

Before saving, check that the Summary and Priority Table agree on every country's final fits (only "not scored (no data)" becomes Unknown for display), that every candidate is accounted for exactly once, that each Priority follows its decision boundary, that each Main limitation is supported and consistent with the audit, and that counts preserve early exclusions. Save the audit checks, Recalibration verdict, Summary, Priority Table, and Effort Allocation to cf-step6-final-ranking.md in the workspace. Its post-audit Summary is the authoritative classification for later steps or pipelines; prefer it over cf-step5-scoring-results.md if both exist. Salary Calculator still selects countries from this Summary and uses the Priority Table's row order, not its Priority labels or limitation text.

Keep existing output filenames, Summary classifications, and pipeline state unchanged. Completed runs replay their saved final result under the shared runtime; do not migrate or rewrite an older four-column result merely to apply this presentation change.

After saving, tell me the pipeline is complete: "Country Finder is complete. Results are saved to cf-step6-final-ranking.md if you want to revisit them later without re-running the pipeline. Review the ranked results above." Do not imply a Focus country or an actionable target exists when all results are Deprioritize or Pending evidence. If every row is Pending evidence, replace the final sentence with "Application priorities are pending evidence; see the saved audit for missing research." If there are no rows, replace it with "No countries could be ranked; see the saved audit for exclusions or missing research."

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
