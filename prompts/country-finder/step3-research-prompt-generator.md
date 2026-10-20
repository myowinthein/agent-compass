Check whether cf-step2-candidates.md exists in the workspace. If it does not exist, stop and tell me: "cf-step2-candidates.md was not found. Please ensure Step 2 completed successfully before continuing."

Read cf-step2-candidates.md, profile.md, and situational-profile.md from the workspace. For each country recorded in cf-step2-candidates.md, generate one ready-to-copy research prompt, based on its Remote and Sponsorship "Suitable" values from Step 2:

- If only Remote is "yes," generate a prompt with the Remote Track section only.
- If only Sponsorship is "yes," generate a prompt with the Sponsorship Track section only.
- If both are "yes," generate a single combined prompt with both sections.
- If neither is "yes," skip this country — it did not survive Step 2.

Each generated prompt must embed directly as literal text — never by reference to "the candidate" or "the situational profile" — the candidate's target role and skillset from profile.md, and, for any Sponsorship Track section, the candidate's citizenship and any noted immigration friction from situational-profile.md. This keeps each prompt self-contained, so the researcher can work from its own brief without reading either workspace file or relying on the parent's conversation.

For sponsorship thresholds, read skills/sponsorship-threshold-rules.md and include the relevant age/date-of-birth reference, residence, work-rights/status, and candidate-category research instructions directly in the brief. Preserve unknown or declined age/status as unknown; do not select an age-dependent threshold by assumption.

Each generated prompt must instruct the researcher to use current web research (prioritizing sources from the last 12 months), not memory or general reputation. Do not include a claim unless it is supported by a real, dated source.

Evidence hierarchy, in order of preference: current official government immigration or labour sources; current direct employer vacancy or policy pages; official sponsor or accredited-employer registers (proof of capability only, never of intent); credible specialist job boards, recruiters, or salary surveys; aggregators and search snippets, which need direct verification before use rather than being cited on their own. Instruct the researcher to note which tier each source falls into.

Remote Track section should ask for:

- confirmed realistic remote salary range for this candidate's role and skillset in this country, with currency, pay period, and gross/base versus net basis (or explicitly unknown)
- evidence of remote hiring volume or frequency for this role (job postings, hiring reports, company remote policies)
- typical payment structure norms (local currency vs USD, contractor vs employee status)
- sources with dates

Sponsorship Track section should ask for a pathway where a local employer is the sponsor — a standard employer-sponsored work visa or work permit tied to a job offer, not a digital-nomad, remote-worker, long-stay, or self-qualifying visa (these do not involve a local employer sponsoring the candidate, even if prominent in search results). If the country has both an employer-sponsored route and a digital-nomad-style visa, research the employer-sponsored one only. Ask for:

- full name of the specific employer-sponsored work-visa pathway, and the official source describing it
- minimum salary threshold required by that visa, if any
- realistic employer willingness to sponsor this specific role and skillset (based on recruiter behavior, hiring examples, not assumption)
- realistic processing time for the visa
- any quota, cap, or annual limit on this pathway
- family or dependent sponsorship provisions, if relevant
- citizenship-specific complications or restrictions, based on the situational profile
- sources with dates

Required answer format (instruct the researcher to use this exact structure):

Country: [name]

Remote Track (include only if applicable):
- Confirmed salary range: [amount] [currency]
- Hiring prevalence evidence: [details]
- Payment structure norms: [details]
- Sources: [list with URLs and dates]

Sponsorship Track (include only if applicable):
- Visa or pathway name: [name]
- Minimum salary threshold: [amount] [currency], or "none known"
- Employer willingness: [details]
- Processing time: [estimate]
- Quota or cap limitations: [details, or "none known"]
- Family or dependent provisions: [details]
- Citizenship-specific considerations: [details]
- Sources: [list with URLs and dates]

Notes: [anything relevant not covered above]

Output:

- One ready-to-copy research prompt per country, clearly labeled with the country name and which track(s) it covers
- Do not attempt to answer the research questions yourself in this step

Parent: run the generated prompts using the research-delegation rule in prompts/shared/runtime.md, including its capability checks, task-brief rules, and manual fallback. Each task covers exactly one country. The parent collects the returned results into cf-step3-country-research.md in the workspace.

Once all results are saved to cf-step3-country-research.md, tell me in a few lines how many countries were researched and that the full per-country findings are saved there for Step 4 to validate and store. Do not reproduce the per-country research findings in this summary. Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
