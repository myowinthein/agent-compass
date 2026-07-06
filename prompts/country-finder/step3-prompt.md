Using the Remote candidate list and Sponsorship candidate list from Step 2, generate one ready-to-copy research prompt per country.

For each country, check which list(s) it appeared in:

- If it appeared only in the Remote candidate list, generate a prompt with the Remote Track section only.
- If it appeared only in the Sponsorship candidate list, generate a prompt with the Sponsorship Track section only.
- If it appeared in both lists, generate a single combined prompt with both sections.

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

After generating these prompts, run each one as a separate, isolated research task with no access to your own prior reasoning in this conversation, and no access to conclusions reached for other countries, so each country's research is genuinely fresh. If you are able to run these as isolated sub-agent tasks, do so and bring back the real results. If not, tell me clearly that you cannot guarantee isolation, show me the prompts, and wait for me to bring back real results myself before continuing.

Save each country's results to country-research.md in the workspace, appending as each one completes. Do not proceed to Step 4 until all results are saved.
