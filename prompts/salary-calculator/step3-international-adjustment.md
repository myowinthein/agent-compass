Check whether sc-step2-salary-data.md exists in the workspace. If it does not exist, stop and tell me: "sc-step2-salary-data.md was not found. Please ensure Step 2 completed successfully before continuing."

Read sc-step2-salary-data.md and proceed with the international adjustment.

Read situational-profile.md from the workspace and treat it as the single source of truth for location, citizenship, language, and salary minimum. (It was collected by the main command before this step.)

Read profile.md from the workspace and treat it as the single source of truth for the candidate's actual education and experience.

Goal

Estimate the realistic international candidate adjustment that may apply when an overseas candidate negotiates with local employers compared to the local-market midpoint salary.

This is an estimate of practical hiring and negotiation behavior, not a rule or guaranteed outcome.

Assume the situational profile remains the single source of truth across all countries.

Only vary the adjustment based on country-specific hiring practices, employer behavior, and current market conditions.

For each country, provide:

- International candidate adjustment range (%)
- Typical midpoint adjustment (%)
- Adjustment level: Small, Moderate, or Significant
- Confidence: High, Medium, or Low
- Brief explanation

Consider:

- openness to international hiring
- employer willingness to sponsor overseas candidates
- visa complexity
- local talent availability
- language tolerance in the workplace
- relocation friction
- remote interview logistics
- perceived hiring risk for overseas candidates
- current hiring market conditions (most recent 12 months)

Important:

- This is NOT about legal pay discrimination.
- This is NOT a prediction of the candidate's future salary.
- Treat every adjustment as a realistic market estimate rather than a fixed rule.
- Focus on practical recruiter and employer behavior for overseas candidates compared with local candidates.
- Do not focus heavily on tax, lifestyle, or permanent residence pathways.
- "Employer willingness to sponsor" and "visa complexity" above are about negotiation dynamics — how sponsorship friction realistically affects an employer's offered pay during negotiation, not whether a legally mandated minimum salary exists. That is a separate, hard eligibility question handled later in Step 4 and must never be folded into this percentage.
- If a country's visa route has an education requirement (e.g. a degree related to the occupation), check it against the candidate's actual degree(s) in profile.md before treating it as a friction factor. Do not assume a mismatch based on generic assumptions about the occupation as a class — a candidate can hold multiple degrees, and any one of them being relevant is enough to satisfy a relevance requirement.
- Formal recognition of a specific degree or institution (as opposed to its relevance) is not something you can verify through research — it requires a country's actual credential-assessment body. Never assert that a degree does or doesn't formally qualify. If a country's route has a named formal-recognition or equivalency requirement, state it as a plain process caveat in that country's Brief explanation (e.g. "may require formal degree recognition via [body]; not independently verified") — this is informational only and must never affect the adjustment percentage.
- If situational-profile.md states the candidate already lives in, or already has some form of work authorization for, a country being calculated, weigh relocation friction, remote interview logistics, and perceived hiring risk much lighter for that country specifically — she isn't relocating and can interview locally, so these largely don't apply. This is independent of sponsorship: if her stated status there would still require employer sponsorship to take the job, weigh employer willingness to sponsor and visa complexity normally — being already resident reduces relocation-driven friction, not sponsorship-driven friction. If situational-profile.md doesn't cover a given country, treat the candidate as not already resident there.

Keep the output compact and present the results country by country.

Save the full adjustment output to sc-step3-adjustment-values.md in the workspace.

Step complete — stop here and wait for the main command.
