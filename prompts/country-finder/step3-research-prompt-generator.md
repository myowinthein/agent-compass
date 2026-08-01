Check whether cf-step2-candidates.md exists in the workspace. If it does not exist, stop and tell me: "cf-step2-candidates.md was not found. Please ensure Step 2 completed successfully before continuing."

Read cf-step2-candidates.md from the workspace. For each country recorded there, generate one ready-to-copy research prompt, based on its Remote and Sponsorship "Suitable" values from Step 2:

- If only Remote is "yes," generate a prompt with the Remote Track section only.
- If only Sponsorship is "yes," generate a prompt with the Sponsorship Track section only.
- If both are "yes," generate a single combined prompt with both sections.
- If neither is "yes," skip this country — it did not survive Step 2.

Each generated prompt must instruct the researcher to use current web research (prioritizing sources from the last 12 months), not memory or general reputation. Do not include a claim unless it is supported by a real, dated source.

Remote Track section should ask for:

- confirmed realistic remote salary range for this candidate's role and skillset in this country, with currency
- evidence of remote hiring volume or frequency for this role (job postings, hiring reports, company remote policies)
- typical payment structure norms (local currency vs USD, contractor vs employee status)
- sources with dates

Sponsorship Track section should ask for:

- full name of the specific work-visa or sponsorship pathway, and the official source describing it
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
- Sources: [list with dates]

Sponsorship Track (include only if applicable):
- Visa or pathway name: [name]
- Minimum salary threshold: [amount] [currency], or "none known"
- Employer willingness: [details]
- Processing time: [estimate]
- Quota or cap limitations: [details, or "none known"]
- Family or dependent provisions: [details]
- Citizenship-specific considerations: [details]
- Sources: [list with dates]

Notes: [anything relevant not covered above]

Output:

- One ready-to-copy research prompt per country, clearly labeled with the country name and which track(s) it covers
- Do not attempt to answer the research questions yourself in this step

After generating these prompts, run each one as a separate, isolated research task. If you are able to run these as isolated sub-agent tasks, do so with the following strict brief per agent:

- Each agent receives only one country's prompt. Its only job is to run that research and return the results for that one country. It must not answer, draft, or save results for any other country.
- Each agent works from its own prompt only, with no access to your prior reasoning in this conversation and no access to research or conclusions reached for other countries.

Append each country's results to cf-step3-country-research.md in the workspace as each agent completes. If you cannot guarantee that isolation, show me the prompts and wait for me to bring back the results myself before continuing.

Once all results are saved to cf-step3-country-research.md, step complete — stop here and wait for the main command.
