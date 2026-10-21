CANDIDATE PROFILE:
Read profile.md from the workspace and use it as the candidate profile. [TARGET ROLE] below should be filled using the target or desired role from the candidate profile if one is stated; otherwise use the current or most recent title.

Read situational-profile.md before generating research. If absent, the parent applies skills/situational-profile-questions.md and waits for answers first. Every generated country brief must embed the target role, seniority, relevant years of experience (or explicitly unknown), skills, and relevant citizenship/residence/work-authorization and age facts as literal text, including their reference dates. Never rely on a job title to imply the profile or ask a fresh-context researcher to read workspace files. Include the candidate-specific threshold instructions from skills/sponsorship-threshold-rules.md directly in each brief, not merely a path reference.

Countries:
Check whether cf-step6-final-ranking.md exists in the workspace; if not, check cf-step5-scoring-results.md.
- If the final file exists, select countries exclusively from its post-audit Summary: include each country once if at least one final track is Strong or Moderate. Do not select from the Priority Table, medals, audit prose, or original Step 5 ratings, even if a legacy final file contains conflicting sections. A Weak, Excluded, or not scored track is not eligible by itself. If the Summary is missing or cannot be interpreted, explain the problem and ask me for a target list rather than silently falling back to pre-audit data.
- Only when the final file is absent, use the scored Strong/Moderate countries from cf-step5-scoring-results.md and explain that this is the pre-audit result.
- Show the resulting list: "Country Finder found these countries worth calculating salaries for: [list]. Use this list as-is, add to it, remove some, or start fresh?" Wait for my answer. If the eligible list is empty, say no countries currently meet that criterion and ask me to provide a target list or stop; never resurrect an older rating to populate it.
- If neither file exists, or I choose to start fresh, ask me for my target country list.

Generate individual research prompts to estimate realistic local-market annual base salary ranges for a [TARGET ROLE] in each country given above. Do not estimate salaries directly — only generate ready-to-copy research prompts. Estimate what a local candidate with a similar profile would realistically earn in that country — local-market salary only.

Read and apply skills/sponsorship-threshold-rules.md — each generated prompt must also ask for the country's government-mandated minimum salary threshold for employer-sponsored work-visa relocation, following that skill's rules for what counts as a usable figure.

Important:
Each generated prompt must instruct the researcher to perform the analysis completely from scratch using current web research and real-world market conditions only, prioritizing sources from the last 12 months. Do not rely on previous conversations, memory, earlier country discussions, or assumed preferences.

Exclude from research:
- expat salary and relocation premium
- FAANG-only data (including levels.fyi)
- Glassdoor US
- inflated global or remote-first compensation
- contractor or freelance rates
- equity-heavy total compensation
- US-skewed compensation data

For each country, create one ready-to-copy research prompt asking for:

- realistic gross annual base salary range in local currency, with any source's different or unknown pay basis stated explicitly
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
- government-mandated minimum salary threshold for employer-sponsored work-visa relocation, if one exists and is a usable figure per skills/sponsorship-threshold-rules.md — not applicable to remote or independent-contractor arrangements

Prioritize:
- realistic local-market compensation
- actual hiring behavior
- practical market salary ranges
- non-FAANG and non-outlier compensation
- salary consistency across multiple local sources

Each prompt must also instruct the researcher to self-assess an evidence grade for the country: High if at least three independent, current, mutually consistent sources support the figures; Medium if the evidence is useful but has a material coverage or comparability limitation; Low if the evidence is sparse, old, indirect, or conflicting.

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

Sponsorship salary threshold: [amount] [currency], [annual or monthly], or state which applies: "no fixed threshold" (route exists but has no fixed numeric minimum), "not applicable" (not an employer-sponsored relocation path), "unknown" (a plausible route exists but the figure couldn't be confirmed), or "blocked" (a real route exists but current official rules make it unavailable to this specific candidate right now, e.g. exhausted quota, paused category, or an eligibility cutoff this candidate doesn't meet — state the concrete reason)

Evidence grade: [High / Medium / Low]

Notes: [anything relevant not covered above]

Output format:
- one ready-to-copy research prompt per country
- clearly separated by country name
- do not attempt to answer the research questions yourself in this step

Parent: run the generated prompts using the research-delegation rule in prompts/shared/runtime.md, including its capability checks, task-brief rules, and manual fallback. Each task covers exactly one country. The parent collects the returned results into sc-step1-salary-research.md in the workspace.

Before collecting results, record the confirmed target countries under a `## Research scope` preface in sc-step1-salary-research.md so validation and later audits can account for omitted or rejected countries after a resume. Keep the existing Country fields and dataset structure; collect blocks under the shared data-validation boundaries.

After collection and before completion, run `research-scan` under skills/research-helper.md with that confirmed scope. Resolve ambiguous boundaries or missing researcher results without dropping successful blocks. Step 2 owns ingestion. The shared explicit manual fallback applies if execution is unavailable.

Once all results are saved to sc-step1-salary-research.md, tell me in a few lines: how many countries were researched, and that the full results are saved for Step 2 to validate and store. Do not reproduce the per-country research findings in this summary. Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
