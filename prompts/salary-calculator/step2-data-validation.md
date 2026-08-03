Check whether sc-step1-salary-research.md exists in the workspace.

If it does not exist, stop and tell me: "sc-step1-salary-research.md was not found. Please ensure Step 1 completed successfully before continuing."

If it exists, read it and process each country's data from that file sequentially — this runs fully automated, with no pause for input between countries. Apply all the behavior rules below to each country block in the file, in order.

Behavior rules:

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the salary data.
* Each block is expected to contain salary data for exactly one country.
* If a block contains multiple countries or no recognizable country, skip it and record the issue. Do not store anything from that block.
* Each country's data is expected to contain both tiers (Mid-size/Mainstream Local-Market, and Premium/International/Remote-first) along with sources for each. If a required tier or its sources are missing, skip it and record exactly what is missing. Do not store incomplete data.
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

Step complete — stop here and wait for the main command.
