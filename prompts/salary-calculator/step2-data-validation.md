Check whether sc-step1-salary-research.md exists in the workspace.

If it does not exist, stop and tell me: "sc-step1-salary-research.md was not found. Please ensure Step 1 completed successfully before continuing."

If it exists, read it and process each country's data from that file sequentially — this runs fully automated, with no pause for input between countries. Apply all the behavior rules below to each country block in the file, in order.

Behavior rules:

Parent: use skills/research-helper.md to scan and review every block, then run `ingest` with the exact hashes, Research scope (or null for genuinely unknown legacy scope) and block decisions. It copies accepted raw slices and updates only the existing generated report. Read back both files and present the consolidated inventory below. A legacy label variation needs genuine semantic review, not an automatic skip or acceptance. A partial failure leaves state unchanged; inspect and rescan before a safe retry. Under an approved manual run, follow all existing rules below without claiming Python ran.

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the salary data.
* Each block is expected to contain salary data for exactly one country.
* If a block contains multiple countries or no recognizable country, skip it and record the issue. Do not store anything from that block.
* Each country's data is expected to contain both tiers (Mid-size/Mainstream Local-Market, and Premium/International/Remote-first) along with sources for each. If a required tier or its sources are missing, skip it and record exactly what is missing. Do not store incomplete data.
* Store the sponsorship salary threshold field as provided, including "not applicable," "no fixed threshold," "unknown," or "blocked" (with its stated reason). This field is never required — a missing or absent threshold never causes a country to be skipped.
* Store the evidence grade field as provided. If it is missing, store the country anyway and record the evidence grade as "not provided" — this field is informational for Step 5's audit, never a reason to skip a country.
* If a country has already been stored, skip it, keep the original, and record it as a duplicate.
* Preserve all values, wording, and formatting as provided.
* Do not verify, correct, or critique the supplied data.
* Do NOT analyze, summarize, calculate, rank, interpret, or generate tables.
* Do NOT give opinions, recommendations, or perform any additional actions unless explicitly instructed later.

Once all countries from sc-step1-salary-research.md have been processed, write all successfully stored country datasets to sc-step2-salary-data.md in the workspace, preserving the original structure and content for each country. Then reply with one consolidated report, not a per-country reply:

Stored: [count] countries.

Skipped — malformed or unrecognizable: [country or "none"], with the issue for each.
Skipped — missing required tier or sources: [country or "none"], with what was missing for each.
Skipped — duplicate: [country or "none"].

Persist this same consolidated report under `## Validation report` in sc-step1-salary-research.md using skills/data-validation-rules.md. Use the Research scope preface, when present, to account for confirmed countries whose results never arrived. If a legacy file lacks scope, report that coverage is unknown rather than inventing a target list. Preserve the raw research and stored data unchanged; a duplicate with a retained original is not a missing-country failure.

When `ingest` has written that report, persistence is already complete: read it back but do not append another review, alter its bounded generated section or write anything after its closing marker. Present the consolidated inventory in chat without creating a second report.

This data is saved to sc-step2-salary-data.md, which Step 3 will use next. Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
