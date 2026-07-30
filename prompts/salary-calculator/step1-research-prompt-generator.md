Generate individual research prompts to estimate realistic local-market annual base salary ranges for a [TARGET ROLE] in each country below.

Do not estimate salaries directly. Only generate ready-to-copy research prompts.

Important:
Each generated prompt must instruct the researcher to perform the analysis completely from scratch using current web research and real-world market conditions only, prioritizing sources from the last 12 months. Do not rely on previous conversations, memory, earlier country discussions, or assumed preferences.

Goal:
Estimate what a local candidate with a similar profile would realistically earn in that country.

Estimate local-market salary only.

Exclude:
- expat salary
- relocation premium
- FAANG-only salary
- inflated global remote salary
- contractor or freelance rates
- equity-heavy total compensation
- US-skewed compensation data

Countries:
Ask me for my target country list.

CANDIDATE PROFILE:
Read profile.md from the workspace and use it as the candidate profile.

[TARGET ROLE] above should be filled using the target or desired role from the candidate profile if one is stated; otherwise use the current or most recent title.

For each country, create one ready-to-copy research prompt asking for:

- realistic annual base salary range in local currency
- local-market salary only
- current data only, prioritizing sources from the last 12 months
- salary for local candidates with similar seniority and profile
- evidence from local employers, local job boards, recruiter salary guides, employer postings, and LinkedIn salary/job data where useful
- source for each number, and how recent that source is
- separation of local-company salary vs international or remote-first salary if relevant
- separate salary figures for two company tiers:
  - mid-size or mainstream local-market companies
  - premium, international, or remote-first companies
- national range and major tech hub range if salary varies significantly by city (name the city used)
- practical low, realistic, and strong ranges within each tier

Exclude from research:
- levels.fyi
- FAANG-only data
- Glassdoor US
- US-skewed compensation data
- inflated top-end global or remote compensation

Prioritize:
- realistic local-market compensation
- actual hiring behavior
- practical market salary ranges
- non-FAANG and non-outlier compensation
- salary consistency across multiple local sources

Required answer format (instruct the researcher to use this exact structure):

Country: [name]

Mid-size / Mainstream Local-Market tier:
- Low: [amount] [currency]
- Realistic: [amount] [currency]
- Strong: [amount] [currency]
- City used (if applicable): [city]
- Sources: [list with dates]

Premium / International / Remote-first tier:
- Low: [amount] [currency]
- Realistic: [amount] [currency]
- Strong: [amount] [currency]
- City used (if applicable): [city]
- Sources: [list with dates]

Notes: [anything relevant not covered above]

Output format:
- one ready-to-copy research prompt per country
- clearly separated by country name
- do not attempt to answer the research questions yourself in this step

After generating these prompts, run each one as a separate, isolated research task. If you are able to run these as isolated sub-agent tasks, do so with the following strict brief per agent:

- Each agent receives only one country's prompt. Its only job is to run that research and return the results for that one country. It must not answer, draft, or save results for any other country.
- Each agent works from its own prompt only, with no access to your prior reasoning in this conversation and no access to research or conclusions reached for other countries.

Append each country's results to sc-step1-salary-research.md in the workspace as each agent completes. If you cannot guarantee that isolation, show me the prompts and wait for me to bring back the results myself before continuing.

Once all results are saved to sc-step1-salary-research.md, step complete — stop here and wait for the main command.
