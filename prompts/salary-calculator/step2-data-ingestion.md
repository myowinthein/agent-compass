Check whether sc-step1-salary-research.md exists in the workspace.

If it does not exist, stop and tell me: "sc-step1-salary-research.md was not found. Please ensure Step 1 completed successfully before continuing."

If it exists, read it and process each country's data from that file sequentially — no user input is needed. Apply all the behavior rules below to each country block in the file, in order.

Behavior rules:

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the salary data.
* Each block is expected to contain salary data for exactly one country.
* If a block contains multiple countries or no recognizable country, stop and explain the issue. Do not store anything from that block.
* Each country's data is expected to contain both tiers (Mid-size/Mainstream Local-Market, and Premium/International/Remote-first) along with sources for each. If a required tier or its sources are missing, stop and state exactly what is missing. Do not store incomplete data.
* If a country has already been stored, skip it, keep the original, and note it in a warning at the end of processing.
* Preserve all values, wording, and formatting as provided.
* Do not verify, correct, or critique the supplied data.
* After each valid, complete block, reply ONLY with the running count of successfully stored country datasets.
* Do NOT mention country names in the count reply.
* Do NOT analyze, summarize, calculate, rank, interpret, or generate tables.
* Do NOT give opinions, recommendations, or perform any additional actions unless explicitly instructed later.

Reply format for valid data:

Received: 5

Reply format for missing fields:

Missing: [specific field]. Country not stored.

Once all countries from sc-step1-salary-research.md have been processed, write all successfully stored country datasets to sc-step2-salary-data.md in the workspace, preserving the original structure and content for each country. Any skipped duplicates are noted in a warning before stopping.

Step complete — stop here and wait for the main command.
