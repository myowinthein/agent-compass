Check whether `cf-step3-country-research.md` exists in the workspace.

If it does not exist, stop and tell me: "cf-step3-country-research.md was not found. Please ensure Step 3 completed successfully before continuing."

If it exists, read it and process each country's data from that file sequentially — this runs fully automated, with no pause for input between countries. Apply all the behavior rules below to each country block in the file, in order.

Behavior rules:

Parent: use skills/research-helper.md to scan and review every block, then run `ingest` with the exact hashes, expected eligible countries, required tracks and block decisions. It copies accepted raw slices and updates only the existing generated report. Read back both files and present the consolidated inventory below. A legacy label variation needs genuine semantic review, not an automatic skip or acceptance. A partial failure leaves state unchanged; inspect and rescan before a safe retry. Under an approved manual run, follow all existing rules below without claiming Python ran.

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the data.
* Identify country blocks using skills/data-validation-rules.md, not chat-message boundaries. Each block is expected to contain data for exactly one country.
* If an explicitly bounded block contains multiple country datasets or no recognizable country, skip it and record the issue. Do not store anything from that block. If the boundaries themselves are ambiguous, the parent asks for clarification under the shared rule.
* Check which track(s) this country was marked suitable for ("yes") in cf-step2-candidates.md from the workspace.
* If the data is missing a section or required field for a track this country was expected to cover, skip it and record exactly what is missing. Do not store incomplete data.
* If a country was not marked suitable for at least one track in cf-step2-candidates.md, never store it automatically — skip it and record it as unlisted, so it can be reviewed and manually added back if it wasn't a mistake.
* If a country has already been stored, skip it, keep the original, and record it as a duplicate.
* Preserve all values, wording, and formatting as provided.
* Do not verify, correct, or critique the supplied data.
* Do NOT analyze, summarize, calculate, rank, interpret, or generate tables.
* Do NOT give opinions, recommendations, or perform any additional actions unless explicitly instructed later.

Once all countries from cf-step3-country-research.md have been processed, write all successfully stored country datasets to cf-step4-country-data.md in the workspace, preserving the original structure and content for each country. Then reply with one consolidated report, not a per-country reply:

Stored: [count] countries.

Skipped — malformed or unrecognizable: [country or "none"], with the issue for each.
Skipped — missing required fields: [country or "none"], with what was missing for each.
Skipped — duplicate: [country or "none"].
Skipped — not on either candidate list: [country or "none"]. Review these and tell me if any should be added.

Persist this same consolidated report under `## Validation report` in cf-step3-country-research.md using skills/data-validation-rules.md. Keep the country research and stored output unchanged; record any expected Step 2 eligible countries for which no block arrived. This makes ingestion failures available to later steps without a new dataset or state schema.

When `ingest` has written that report, persistence is already complete: read it back but do not append another review, alter its bounded generated section or write anything after its closing marker. Present the consolidated inventory in chat without creating a second report.

This data is saved to cf-step4-country-data.md, which Step 5 will score next.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
