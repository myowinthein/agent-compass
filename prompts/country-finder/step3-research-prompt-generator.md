Check whether country-finder-02-candidates.md exists in the workspace. If it does not exist, stop and tell me: "country-finder-02-candidates.md was not found. Please ensure Step 2 completed successfully before continuing."

Read country-finder-02-candidates.md, profile.md, and situational-profile.md from the workspace. For each country recorded in country-finder-02-candidates.md, generate one ready-to-copy research prompt, based on its Remote and Sponsorship "Suitable" values from Step 2:

- If only Remote is "yes," generate a prompt with the Remote Track section only.
- If only Sponsorship is "yes," generate a prompt with the Sponsorship Track section only.
- If both are "yes," generate a single combined prompt with both sections.
- If neither is "yes," run no detailed research for this country. Preserve the distinction between explicit rejection and discovery finding no evidence; neither is silently removed from the final candidate accounting.

Each generated prompt must embed the relevant confirmed facts directly as literal text, never by reference to "the candidate" or a workspace file: settled target role/level, relevant dated experience or unknown, skills, current residence/location, spoken and required work languages, explicit work rights/status, salary-minimum comparison facts and relocation timeline where applicable. Sponsorship sections also include citizenship and noted immigration friction. Read criteria context too; carry user-confirmed run-only clarifications under the shared runtime. Do not paste whole profiles or rely on a title to imply seniority. Preserve the scoped candidate/role context in each country's Notes for later compatibility checks.

For sponsorship thresholds, read skills/sponsorship-threshold-rules.md and include the relevant age/date-of-birth reference, residence, work-rights/status, and candidate-category research instructions directly in the brief. Preserve unknown or declined age/status as unknown; do not select an age-dependent threshold by assumption.

Each generated prompt must instruct the researcher to use current web research (prioritizing sources from the last 12 months), not memory or general reputation. Do not include a claim unless it is supported by a real, dated source.

Evidence hierarchy, in order of preference: current official government immigration or labour sources; current direct employer vacancy or policy pages; official sponsor or accredited-employer registers (proof of capability only, never of intent); credible specialist job boards, recruiters, or salary surveys; aggregators and search snippets, which need direct verification before use rather than being cited on their own. Instruct the researcher to note which tier each source falls into.

Remote Track section should ask for:

- realistic remote pay for the supplied role/level while working from the supplied current location, with amount/range, currency, period, gross/base versus net basis and engagement type (or explicitly unknown). Require evidence of location acceptance; domestic-only or local-employee evidence is not cross-border offer evidence. Local remote is valid if the candidate already lives there.
- evidence of remote hiring volume or frequency for this role (job postings, hiring reports, company remote policies)
- typical payment structure norms (local currency vs USD, contractor vs employee status)
- sources with dates

Read skills/salary-comparison-rules.md and embed the applicable normalization/FX and hard-floor/context-only uncertainty rules in Remote briefs. Request relevant working-language evidence without inventing national-language barriers. Salary Calculator's local-employee targets cannot substitute for this Remote pay evidence.

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
- Confirmed salary range: [amount or range] [currency], [period], [gross/base or net or unknown], [employee/EOR/contractor and location applicability]
- Hiring prevalence evidence: [details]
- Payment structure norms: [details]
- Sources: [list with URLs and dates]

Sponsorship Track (include only if applicable):
- Visa or pathway name: [name]
- Minimum salary threshold: [state under skills/sponsorship-threshold-rules.md; for a verified number include amount, currency and original period; retain applicable route/category, effective date, official source and eligible-pay basis in this field or Notes]
- Employer willingness: [details]
- Processing time: [estimate]
- Quota or cap limitations: [details, or "none known"]
- Family or dependent provisions: [details]
- Citizenship-specific considerations: [details]
- Sources: [list with URLs and dates]

Notes: [dated candidate/role/level and location/path context; working-language findings; applicable threshold category, assumptions and monthly-pay comparability; anything relevant not covered above]

Output:

- One ready-to-copy research prompt per country, clearly labeled with the country name and which track(s) it covers
- Do not attempt to answer the research questions yourself in this step

Parent: run the generated prompts using the research-delegation rule in prompts/shared/runtime.md, including its capability checks, task-brief rules, and manual fallback. Each task covers exactly one country. The parent collects the returned results into country-finder-03-research.md in the workspace.

The parent embeds the shared threshold states and relevant instructions as literal text, not the template's resource path. Before collection, record eligible countries in a country-only `## Research scope` preface in this file. If no track is eligible, write `## Research scope` followed by `none` and run the scan with `expected: []` and `required_tracks: {}`; there are no research tasks to await. Step 4 creates the legitimate empty stored record/report so Steps 5-6 can account for early exclusions and discovery-only evidence gaps. Do not claim those countries were never checked in discovery.

Once all results are saved to country-finder-03-research.md, tell me in a few lines how many countries were researched and that the full per-country findings are saved there for Step 4 to validate and store. Do not reproduce the per-country research findings in this summary. Step complete. Follow the step-completion rule in prompts/shared/runtime.md.

Before marking completion, run `research-scan` under skills/research-helper.md using the Step 2 eligible countries and their expected tracks. Resolve missing results before continuing; ingestion itself belongs to Step 4. The shared explicit manual fallback applies if execution is unavailable.
