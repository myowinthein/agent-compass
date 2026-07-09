I'm going to feed you research data country by country.

Behavior rules:

* Read and apply the cross-pipeline data validation rules in skills/data-validation-rules.md, then follow the additional rules below.
* Read and silently store the data.
* Each message is expected to contain data for exactly one country.
* If a message contains multiple countries or no recognizable country, stop and explain the issue. Do not store anything from that message.
* Check which track(s) this country was expected to cover, based on the Remote candidate list and Sponsorship candidate list from Step 2.
* If the pasted data is missing a section or required field for a track this country was expected to cover, stop and state exactly what is missing. Do not store incomplete data.
* If a country was not part of either Step 2 candidate list, stop and ask whether it should still be stored or whether it's a mistake. Do not store until I answer.
* If a country has already been stored, stop and ask whether to overwrite the existing data or keep the original. Do not store until I answer.
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

Reply format for duplicates:

Duplicate: this country was already stored. Overwrite or keep original?

Progress check command:

If I say "list countries," reply only with the country names stored so far and which track(s) each one covers (Remote, Sponsorship, or Both), one per line, with no other data, analysis, or commentary.

Continue silently storing each valid country dataset until I explicitly request analysis or another task.
