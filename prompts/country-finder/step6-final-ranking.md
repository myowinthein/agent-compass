Check whether country-finder-05-assessment.md exists in the workspace. If it does not exist, stop and tell me: "country-finder-05-assessment.md was not found. Please ensure Step 5 completed successfully before continuing."

Read country-finder-05-assessment.md from the workspace. Also read country-finder-02-candidates.md, country-finder-04-validated-data.md, country-finder-01-criteria.md, situational-profile.md, and profile.md from the workspace. country-finder-02-candidates.md is the full candidate universe — use it to detect any country that was a Step 2 candidate but never reached Step 4. Base the audit only on these files, not on prior conversation memory.

Use recorded, user-confirmed run-only clarifications under the shared runtime as saved context, not hidden memory. Preserve assessed candidate/role/level, path/location and evidence dates with the file-only audit, outside canonical rendered sections. Material changed-input or contradicted-exclusion issues return to the parent for the shared repair choice before finalisation; never silently override an early reason or rewrite completed outputs.

Read and apply [skills/country-assessment-rules.md](../../skills/country-assessment-rules.md), [skills/evidence-quality-rules.md](../../skills/evidence-quality-rules.md) and [skills/exclusion-transparency-rules.md](../../skills/exclusion-transparency-rules.md) when auditing classifications, assigning priorities, and summarizing limitations.

Read data/output-contracts.json as data and [skills/output-helper.md](../../skills/output-helper.md). After choosing the evidence-supported final decisions below, use `render-cf` with `format: "tracks"`, separate evidence-led orders and track decisions, the full candidate universe, original early exclusions and ingestion dispositions. Save its returned Summary and Priority Table sections (the latter contains separate Remote and Relocation tables) verbatim, keep its audit notes with the three checks, and run `check-saved` before completion. Pure helper requests unavailable to a specialist return to the parent under the shared runtime. Under an explicitly approved manual run, read this same contract for the format and perform the same checks; do not claim automated rendering ran.

## Goal

Perform a focused audit on the Step 5 results across three checks.

Save the three named audit checks and Recalibration verdict at the top of country-finder-06-final-results.md, before Summary, Priority Table, and Effort Allocation. All audit details stay file-only. This step writes only that existing final file; leave source research and Step 5 outputs untouched.

## 1. Confidence Calibration Check

For each country marked "High confidence," verify the underlying evidence is genuinely specific, sourced, and dated, not just confidently worded. Flag any confidence level that seems inflated relative to the actual evidence quality, and explain why.

## 2. Missing Candidate Check

Compare country-finder-02-candidates.md against the countries that actually reached Step 4 and Step 5. For each missing country, state whether the absence was a real, evidence-based elimination (cite the reason from earlier steps) or a process gap, such as a non-excluded track receiving no detailed research or never reaching Step 4. Check any apparent selection mistake against the confirmed criteria and recorded scope. An evidenced omission from that scope returns to the parent for the existing repair choice; do not add countries during this audit. A discovery no-evidence finding is not a valid reason to omit detailed research in a new run.

Reconcile this per track, not just per country. Preserve each explicit Step 2 "no" and its recorded reason as Excluded, including timezone rejections; missing downstream research after that rejection is expected, not a process gap. Apply this even when resuming from an older Step 5 output that omitted the earlier exclusion. "no evidence found" or absent research without an explicit rejection remains a missing-data case, not Excluded. Never let an earlier exclusion on one track remove the other track.

If country-finder-03-research.md exists, read its Validation report and available raw blocks to distinguish never-supplied research from researched data rejected in Step 4. Record the exact rejection reason or state that the legacy ingestion outcome is unknown. A duplicate whose original was retained is not a missing country. Do not reinterpret an ingestion error as an evidence-based country exclusion.

## 3. Evidence Misuse Check

For each scored country, check the stored Reason text for these specific misreadings:
- Domestic-only remote-work evidence (a policy or listing that only covers workers already inside that country) counted as proof of cross-border remote hiring.
- A legal visa route or sponsor-eligibility register treated as proof of actual employer willingness to sponsor this candidate's role, rather than proof that sponsorship is merely possible.
- A single job vacancy or hiring example treated as evidence of deep, ongoing market demand.

Flag any country whose fit classification or confidence rests on one of these misreadings, and explain what the underlying evidence actually supports.

## Recalibration

If the confidence calibration check found inflated confidence levels, or the evidence misuse check found a misreading that changes a country's real fit:
- Revise the affected country's confidence level
- If the inflated confidence or evidence misuse was masking a genuinely weaker fit, revise the classification too
- Explain what evidence caused each change

If recalibration is not supported, distinguish evidence-supported unchanged fits from an inconclusive audit, naming each material gap rather than always claiming the results remain appropriate. When the only applicable support for a stored track is invalidated, use "not scored (no data)" with the specific reason; raw ingestion is not proof of usable evidence. Weak requires evidence of a weak fit. Keep original research and Step 5 untouched.

## Summary

Write a Summary section into the file (not shown in chat — the Priority Table below is the only thing from this step shown in chat) that reorganizes Step 5's final scores (including any revisions from this step) by country rather than by track.

For each country that has ingested research or a recorded exclusion on at least one track, show one row with both its Remote fit and Sponsorship fit side by side:

- Use the final classification (Strong / Moderate / Weak / Excluded / not scored (no data)) for each track.
- "Excluded" means the country was explicitly eliminated on that track in Step 2 or Step 5. Preserve the original reason and hard-rule detail in the file's audit findings; do not substitute a missing-data explanation.
- "not scored (no data)" means required research was not ingested or applicable evidence proved unusable, without a supported explicit exclusion. Preserve the precise missing/invalidated-evidence reason; do not relabel a known weak fit or an early exclusion as uncertainty.
- If Step 6 revised a country's confidence level or classification, keep the short revision note in Recalibration with the audit checks, not inside the verbatim generated Summary sections.

If the Missing Candidate Check identified countries with neither ingested research nor a recorded exclusion on either track, account for them separately. Keep the existing "Flagged but not researched" heading for research genuinely never supplied. Add a file-only note for "Researched but not ingested" with the validation reason when research was rejected, or "Ingestion outcome unknown" for unsupported legacy cases. Do not label rejected research as never researched or put intentionally excluded countries in a process-gap list. These notes do not add Summary fit categories; the Priority Table below renders their missing-data tracks as Unknown.

In those reasons identify the stage: "discovery found no evidence; detailed research not run" is different from completed research that remains inconclusive or rejected research. Expected work not performed returns to the parent for scoped recovery before completion; do not silently certify it as complete. An unfinished legacy run whose old discovery gate omitted tracks needs the existing explicit repair choice before new research. Substantive research with documented remaining gaps may still finish unresolved; do not invent fits or expand scope to force recommendations.

Close the Summary with counts:
- Remote: [N] scored, [N] excluded, [N] not scored (no data)
- Sponsorship: [N] scored, [N] excluded, [N] not scored (no data)

Count each Step 2 candidate once per track, including all separately noted missing-data/ingestion cases. Count explicit early rejections as excluded, not missing data. Report selection gaps against the confirmed scope separately from these candidate-universe totals.

The Summary itself contains no ranking, recommendations, or interpretation beyond the classifications above — ranking is reserved for the Priority Table below.

## Priority Table

Keep this existing section heading for links and downstream compatibility. New results contain **Remote priorities** and **Relocation priorities** as separate tables, each covering the full candidate universe exactly once. Sponsorship remains the internal track name and authoritative Summary label; Relocation is the human-facing priority heading.

Use `country.track_headers`, `track_priorities`, confidence and verification-state vocabularies from data/output-contracts.json through skills/output-helper.md. Read fits from this step's post-audit Summary, including every supported recalibration and carried exclusion, including candidates in its separate missing-data/ingestion notes. Keep the Summary's original wording and counts unchanged; only display `not scored (no data)` as Unknown in tables. A change in presentation never changes an assessment.

Apply the assessment rules independently to each track:

- 🥇 Focus: supported Strong/Moderate fit, access and pay feasibility, with the strongest supported return on application effort.
- 🥈 Selective: the same support requirements, but a narrower opportunity set or meaningful limitation favors targeted applications.
- Investigate next: supported Strong/Moderate fit, with material access or pay feasibility Unverified. This is a lead to verify, not an application-ready recommendation. Do not drop the supported fit simply because an offer term is unpublished.
- 🥉 Monitor: supported Strong/Moderate fit, access and pay feasibility, but sparse current openings or substantial practical limitations favor alerts and exceptional matches.
- 🎗️ Deprioritize: this track is Weak or Excluded, regardless of the other track's state.
- Pending evidence: this track remains unscored after completed research/recovery accounting. Keep it unranked; missing facts do not prove poor fit.

For each table show the track's Fit, Confidence, Main limitation and Next action. Scored confidence is High/Medium/Low; unscored/excluded confidence is Not assessed. The limitation names the most important supported constraint or unresolved condition, or None identified. The next action is a concise concrete instruction grounded in findings: target the relevant employer/role cluster, verify a named location/pay/sponsor condition, set an alert, or resolve a specific research gap. Do not invent contacts or send messages.

Choose each track's order independently. Sort priority buckets in contract order; within assessed buckets weigh role/domain/level match, recurring relevant opportunities, shortage/trend evidence, practical access, pay feasibility and confidence. Prefer supported expected usefulness to this person's search, not general popularity or a numerical score/probability. Geographic/working-language conditions and material transition gaps remain visible. Alphabetical order is the final tie-breaker; Pending evidence is alphabetical and has no implied opportunity ranking. An unknown second track supplies neither a bonus nor a penalty.

The helper checks coverage, exact early reasons and consistency of typed decisions. It does not judge source truth. Save the returned Summary and both tables verbatim, retaining audit notes with the three checks. If a later audit invalidates required support, revise the affected fit/access/pay/priority together; do not retain a Focus recommendation on unusable evidence.

Salary Calculator still selects countries exclusively from the post-audit Summary. For new results it uses the Relocation priorities row order for local-employee salary presentation; legacy compatible outputs use the Priority Table's row order. Missing ordering remains an alphabetical fallback, never a reason to block calculation. Do not select countries from priority labels or treat Investigate next as confirmed eligibility.

## Effort Allocation

In the saved file, briefly explain the leading opportunities, the concrete checks needed for Investigate next, and the main supported reasons for deprioritizing each track. Name coverage limitations and distinguish application effort from further research. Do not allocate effort by invented percentages, force a minimum number of targets or imply an offer probability. Lifestyle factors apply only to confirmed relevant preferences.

Before completing, verify each table's full coverage and agreement with the authoritative Summary, the independent orders, priority/access/pay consistency and source-supported limitations/actions. Save the three audit checks, Recalibration, Summary, Priority Table and Effort Allocation to the resolved country-finder-06-final-results.md. Run `check-saved` with the exact render input before state advancement. Step 5 and raw research stay untouched.

Completed results replay as saved: do not migrate or rewrite an older four-column result, a combined five-column result, or a completed new two-table result. New behavior applies to fresh work or explicitly approved repair, never silent resets of old checkpoints or research.

Final response gate: show only the two rendered priority tables and this completion message, using the resolved saved filename: "Country Finder is complete. Results are saved to country-finder-06-final-results.md. Remote and Relocation priorities are assessed separately; Investigate next identifies conditions to verify before focusing applications." When no track has an assessed fit, replace the last sentence with "Application priorities remain unresolved; the tables identify the research gaps." Do not append audit findings, scoring-change commentary, check summaries, file lists or execution notes. Keep those details in the saved file. Completed legacy replays retain their saved table format.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
