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
If I was handed a single country from Country Finder, use only that one. Otherwise, ask me for my target country list.

CANDIDATE PROFILE:
Read profile.md from the workspace and use it as the candidate profile.

[TARGET ROLE] above should be filled using the current or target job title from the candidate profile.

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
