Check whether cf-step1-criteria.md exists in the workspace. If it does not exist, stop and tell me: "cf-step1-criteria.md was not found. Please ensure Step 1 completed successfully before continuing."

Read cf-step1-criteria.md, profile.md, and situational-profile.md from the workspace.

Read and apply skills/salary-comparison-rules.md for any salary-minimum comparison. Include its applicable normalization/FX requirements directly in each generated research brief so the researcher need not read bundled files. Never reject Remote suitability because unlike currencies or pay bases could not be compared.

Part A — Build the candidate universe (no research needed, apply immediately)

1. Determine the base:
   - If cf-step1-criteria.md has an Include list (not "none"), the base is that Include list. Apply this silently.
   - Else, read data/default-preferred-countries.md (shipped with the plugin). Show me its countries grouped by continent, and ask: "You didn't specify preferred countries in Step 1 — do you want to proceed with this default list, or provide your own countries?" Wait for my answer before continuing.
     - If I confirm proceeding with the default, the base is every country in data/default-preferred-countries.md.
     - If I provide my own countries instead, the base is that list.
2. If cf-step1-criteria.md has an Exclude list (not "none"), remove every listed country from the base.

Other than the default-list question above, do this without telling me which source the base came from or asking whether to use it — apply it silently. Show the resulting final country list before continuing.

Part B — Research each country for both tracks together

Batch the final country list for parallel research:

- Read skills/research-helper.md and run `batch-partition` on the confirmed list, preserving the `##` regions from data/default-preferred-countries.md when applicable. Its maximum comes from data/output-contracts.json; chunks are contiguous in list order, not balanced. For an ungrouped list, use one batch-group label. Use the returned complete expected list for coverage.
- There is no total batch cap; queue batches within the client's concurrency limit and never drop a country to fit agent slots. Approved manual fallback uses this same readable contract and partition rule.

For each batch, generate one ready-to-copy research prompt. Each prompt must embed directly as literal text — never by reference to a label like "the candidate universe" — all of the following, so it can run from its own brief without relying on the parent's conversation:

- The exact list of countries in this batch, and only this batch
- The candidate's target role and skillset, read from profile.md (use the target or desired role if one is stated; otherwise the current or most recent title)
- The minimum monthly salary, currency, gross/net basis, and hard-floor/context-only choice from situational-profile.md, if specified; explicitly mark absent facts as unknown, and state if no minimum was specified
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

Evidence hierarchy, in order of preference: current official government immigration or labour sources; current direct employer vacancy or policy pages; official sponsor or accredited-employer registers (proof of capability only, never of intent); credible specialist job boards, recruiters, or salary surveys; aggregators and search snippets, which need direct verification before use rather than being cited on their own. Instruct the researcher to note which tier each source falls into.

Required answer format per country (instruct the researcher to use this exact structure):

Country: [name]

Remote:
- Suitable: [yes / no / no evidence found]
- Reason: [evidence-based reasoning, or "no evidence found"]
- Source: [name and URL of source, or "none"]
- Date: [date of source, or "n/a"]

Sponsorship:
- Suitable: [yes / no / no evidence found]
- Reason: [evidence-based reasoning, or "no evidence found"]
- Source: [name and URL of source, or "none"]
- Date: [date of source, or "n/a"]

Output:

- One ready-to-copy research prompt per batch, clearly labeled with the batch's region (or batch number, if unbatched by region) and the exact countries it covers
- Do not attempt to answer the research questions yourself in this step

Parent: run the generated prompts using the research-delegation rule in prompts/shared/runtime.md, including its capability checks, task-brief rules, and manual fallback. Each task covers exactly the countries in its assigned batch. The parent collects the returned country results into cf-step2-candidates.md in the workspace.

Part C — Mark timezone suitability

Before Part C, run `research-scan` under skills/research-helper.md with stage discovery and the full confirmed expected list. Resolve ambiguous boundaries and missing researcher results before completing this step; preserve successful results. This scan does not store, verify facts or apply timezone decisions.

Read and apply skills/timezone-rules.md. If cf-step1-criteria.md has a maximum timezone difference, assess relevant job hubs against my current location over the rule's reference period. Only for a supported whole-country failure, overwrite Remote "Suitable" with "no — outside your max timezone of [N] hours," replacing whatever Part B found for Remote, and record the reference date, zones/hubs, seasonal difference range, and maximum in Reason. Preserve the existing answer fields. If only some locations pass, retain any otherwise-supported Remote suitability conditionally and name those locations in Reason; if timezone evidence is insufficient, mark the timezone check unverified rather than creating a rejection. Never change Sponsorship suitability for timezone. If no maximum was provided, skip this part entirely.

Once cf-step2-candidates.md exists in the workspace, and Part C has been applied if applicable, tell me in a few lines: how many countries were researched, how many came back Suitable on each track, and that the full per-country findings are saved to cf-step2-candidates.md for Step 3 to use. Do not reproduce the per-country Suitable/Reason/Source/Date findings in this summary.

Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
