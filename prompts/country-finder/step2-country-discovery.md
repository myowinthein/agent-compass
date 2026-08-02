Check whether cf-step1-criteria.md exists in the workspace. If it does not exist, stop and tell me: "cf-step1-criteria.md was not found. Please ensure Step 1 completed successfully before continuing."

Read cf-step1-criteria.md, profile.md, and situational-profile.md from the workspace.

Part A — Build the candidate universe (no research needed, apply immediately)

1. Determine the base:
   - If data/preferred-countries.md exists in the workspace, the base is every country listed there.
   - Else if cf-step1-criteria.md has an Include list (not "none"), the base is that Include list.
   - Else, stop and tell me: "No Include list was provided in Step 1. Please list the countries you want considered." Wait for my answer, then use it as the base.
2. If the base came from data/preferred-countries.md AND cf-step1-criteria.md also has an Include list, add every country from that Include list to the base that isn't already present — place each one under its matching `##` region heading so it batches correctly in Part B.
3. If cf-step1-criteria.md has an Exclude list (not "none"), remove every listed country from the base.

Other than the stop condition above, do this without telling me which source the base came from or asking whether to use it — apply it silently. Show the resulting final country list before continuing.

Part B — Research each country for both tracks together

Batch the final country list for parallel research:

- data/preferred-countries.md is organized under `##` region headings — use those regions as the batches, one sub-agent per region present in the final list.
- If, for some reason, the final list has no usable region grouping, split it into batches of roughly 15 countries each, capped at 8 batches total.

For each batch, generate one ready-to-copy research prompt. Each prompt must embed directly as literal text — never by reference to a label like "the candidate universe" — all of the following, since the sub-agent running it has no access to this conversation:

- The exact list of countries in this batch, and only this batch
- The candidate's target role and skillset, read from profile.md (use the target or desired role if one is stated; otherwise the current or most recent title)
- The minimum monthly salary from situational-profile.md, if one was specified — state explicitly if none was specified, since the Remote check below is skipped in that case
- The candidate's citizenship, and any noted immigration friction, from situational-profile.md

Each prompt must instruct the researcher to use current web research (prioritizing sources from the last 12 months), not memory or general reputation, and must require the researcher to check, for every country in the batch, both of the following:

Remote suitability:
- Is remote hiring for this candidate's role and skillset a common, well-established practice in this country, not a rare exception?
- If a minimum monthly salary was specified, does typical remote salary for this role realistically meet or exceed it? Skip this check if none was specified.
- Evidence must come from remote job boards, remote hiring reports, salary surveys, or company remote-hiring policies.

Sponsorship suitability:
- Does a real, named, documented work-visa pathway exist where a local employer is the sponsor — a standard employer-sponsored work visa or work permit tied to a job offer? Digital-nomad, remote-worker, long-stay, or self-qualifying visas do not count, even if well-known or highly ranked in search results — they do not involve a local employer sponsoring the candidate, which is what this track requires. If a country has both an employer-sponsored route and a digital-nomad-style visa, evaluate only the employer-sponsored one.
- Does the candidate's occupation appear on any official shortage-occupation or in-demand skills list, if one exists? Being listed is a positive factor (often easing salary thresholds or approval) and, for the minority of visas that make it an explicit legal requirement, check whether that applies to the pathway already identified. Absence from a shortage list does not by itself make Suitable "no" unless the identified pathway explicitly requires it.
- Consider citizenship-specific visa reciprocity, restrictions, or friction, based on the situational profile.
- Evidence must come from official government immigration sources, visa program pages, or recruiter sponsorship guides.
- Do not determine Suitable by comparing a visa's salary threshold to the candidate's own stated minimum salary — that minimum reflects what the candidate would accept, not what a real employer would offer. If a salary threshold applies, note it in the Reason field as a fact for later steps to weigh against real market data; it must never by itself make Suitable "no."

Important rule for every prompt:

Do not report a finding based on reputation alone. If a country is commonly assumed to be a good fit but no real, dated source supports it, report "no evidence found" for that track rather than guessing.

Required answer format per country (instruct the researcher to use this exact structure):

Country: [name]

Remote:
- Suitable: [yes / no / no evidence found]
- Reason: [evidence-based reasoning, or "no evidence found"]
- Source: [name of source, or "none"]
- Date: [date of source, or "n/a"]

Sponsorship:
- Suitable: [yes / no / no evidence found]
- Reason: [evidence-based reasoning, or "no evidence found"]
- Source: [name of source, or "none"]
- Date: [date of source, or "n/a"]

Output:

- One ready-to-copy research prompt per batch, clearly labeled with the batch's region (or batch number, if unbatched by region) and the exact countries it covers
- Do not attempt to answer the research questions yourself in this step

After generating these prompts, run each one as a separate, isolated research task. If you are able to run these as isolated sub-agent tasks, do so with the following strict brief per agent:

- Each agent receives only its own batch's prompt. Its only job is to research the countries in that batch and return results for exactly those countries — no others.
- Each agent works from its own prompt only, with no access to your prior reasoning in this conversation and no access to research or conclusions reached by any other agent.

Append each country's results to cf-step2-candidates.md in the workspace as each agent completes. If you cannot guarantee that isolation, show me all the prompts and wait for me to bring back the results myself before continuing.

Part C — Mark timezone suitability

If cf-step1-criteria.md has a maximum timezone difference, calculate the UTC time difference between each country in cf-step2-candidates.md and my current location (from situational-profile.md). For any country outside that maximum, overwrite its Remote "Suitable" value with "no — outside your max timezone of [N] hours," replacing whatever Part B found for Remote. Never touch Sponsorship suitability this way — relocation removes the timezone constraint. If no maximum was provided, skip this part entirely.

Once cf-step2-candidates.md exists in the workspace, and Part C has been applied if applicable, tell me in a few lines: how many countries were researched, how many came back Suitable on each track, and that the full per-country findings are saved to cf-step2-candidates.md for Step 3 to use. Do not reproduce the per-country Suitable/Reason/Source/Date findings in this summary.

Step complete — stop here and wait for the main command.
