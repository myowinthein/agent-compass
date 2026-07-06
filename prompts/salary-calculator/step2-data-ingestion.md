I'm going to feed you salary data country by country.

Behavior rules:

* Read and silently store the salary data.
* Each message is expected to contain salary data for exactly one country.
* If a message contains multiple countries or no recognizable country, stop and explain the issue. Do not store anything from that message.
* Each country's data is expected to contain both tiers (Mid-size/Mainstream Local-Market, and Premium/International/Remote-first) along with sources for each. If a required tier or its sources are missing, stop and state exactly what is missing. Do not store incomplete data.
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

Missing: [specific field]. Country not stored.

Reply format for duplicates:

Duplicate: this country was already stored. Overwrite or keep original?

Progress check command:

If I say "list countries," reply only with the country names stored so far, one per line, with no other data, analysis, or commentary.

Continue silently storing each valid country dataset until I explicitly request analysis or another task.
