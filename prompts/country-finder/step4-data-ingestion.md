Check whether `step3-country-research.md` exists in the workspace.

If it does not exist, stop and tell me: "step3-country-research.md was not found. Please ensure Step 3 completed successfully before continuing."

If it exists, read it and process each country's data from that file sequentially — no user input is needed. Apply all the behavior rules below to each country block in the file, in order, as if it had been pasted.

Behavior rules:

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the data.
* Each message is expected to contain data for exactly one country.
* If a message contains multiple countries or no recognizable country, stop and explain the issue. Do not store anything from that message.
* Check which track(s) this country was expected to cover, based on step2-remote-candidates.md and step2-sponsorship-candidates.md from the workspace.
* If the pasted data is missing a section or required field for a track this country was expected to cover, stop and state exactly what is missing. Do not store incomplete data.
* If a country was not part of either Step 2 candidate list, stop and ask whether it should still be stored or whether it's a mistake. Do not store until I answer.
* If a country has already been stored, skip it, keep the original, and note it in a warning at the end of processing.
* Preserve all values, wording, and formatting as provided.
* Do not verify, correct, or critique the supplied data.
* After each valid, complete message, reply ONLY with the running count of successfully stored country datasets.
* Do NOT mention country names in the count reply.
* Do NOT analyze, summarize, calculate, rank, interpret, or generate tables.
* Do NOT give opinions, recommendations, or perform any additional actions unless explicitly instructed later.

Reply format for valid data:

Received: 5

Reply format for missing fields:

Missing: [specific field or section]. Country not stored.

Reply format for unexpected country:

Not on either candidate list from Step 2. Store anyway, or is this a mistake?

Once all countries from step3-country-research.md have been processed, step complete — stop here and wait for the main command.
