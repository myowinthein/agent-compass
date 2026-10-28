Check whether salary-calculator-02-validated-data.md exists in the workspace. If it does not exist, stop and tell me: "salary-calculator-02-validated-data.md was not found. Please ensure Step 2 completed successfully before continuing."

Read salary-calculator-02-validated-data.md and proceed with the international adjustment.

Read situational-profile.md from the workspace as the saved source for location, citizenship, language and salary minimum. Recorded user-confirmed run-only clarifications under the shared runtime take precedence for this run; preserve their date/scope in the adjustment output without editing the profile. (The main command collected the profile before this step.)

Read profile.md from the workspace and treat it as the single source of truth for the candidate's actual education and experience.

Read the local employee benchmark and reference visa scope in each country's stored Notes. A reference sponsorship assessment does not establish an actual relocation plan. Apply relocation/sponsorship factors only when supported by the candidate's recorded circumstances, not because an employer is international or remote-first. Do not reopen Step 1's fixed scope as an employment-path question or invent a relocation scenario; disclose unsupported circumstances instead. Other material missing candidate facts may go to the parent for clarification.

Goal

Estimate the realistic international candidate adjustment that may apply when an overseas candidate negotiates with local employers compared to the local-market midpoint salary.

This is an estimate of practical hiring and negotiation behavior, not a rule or guaranteed outcome.

Adjustment percentages are nonnegative reductions from the local-market midpoint, not increases. A supported zero is allowed; do not invent a discount to fill a label. Read data/output-contracts.json as data for adjustment bounds, display bands and confidence values. Keep the typical midpoint inside its estimated range and state uncertainty. Labels are display conventions, not independently researched market bands, and do not determine the percentage. Read skills/comparison-helper.md and run `adjust-check` on every supplied estimate before accepting it; the shared explicit fallback applies. The helper checks the supplied metadata, never whether the evidence substantively supports the estimate.

For every numeric estimate, state its evidence basis in the existing explanation: observed local-versus-overseas offer evidence, or a judgmental inference with cited candidate-applicable evidence and an explanation supporting the numerical range. Country reputation, sponsorship cost or generic market difficulty alone does not quantify a pay reduction. Review the stored research and apply skills/evidence-quality-rules.md; do not claim fresh research you did not perform. If the evidence cannot support a percentage, record "Adjustment not estimable" with the reason and missing evidence, omit the numeric range/midpoint/level, and do not invoke `adjust-check` for that country. Step 4 skips it explicitly rather than substituting 0%. A supported 0% remains a numeric estimate and must state its basis. Keep one common percentage for both tiers, but do not generalize tier-specific observations to both without support; if no common estimate is defensible, use the not-estimable path.

Use those same confirmed situational facts across countries, including applicable recorded run-only clarifications rather than silently reverting to superseded saved values.

Only vary the adjustment based on country-specific hiring practices, employer behavior, and current market conditions.

For each country with a supported numeric estimate, provide:

- International candidate adjustment range (%)
- Typical midpoint adjustment (%)
- Adjustment level: Small, Moderate, or Significant
- Confidence: High, Medium, or Low
- Brief explanation

For each unestimable country, provide its name, "Adjustment not estimable", and the specific reason/missing evidence. Account for every stored country once; do not silently omit it. Report the salary evidence grade as supplied, including "not provided"; a missing grade is neither a fabricated Low nor proof of High confidence. Justify confidence from the available evidence and disclose its limits.

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
- no prior employment history in the target country or market
- fewer local references or less local professional network signal

Weigh these factors cumulatively rather than requiring each one to carry a separately priced cost, but do not count the same underlying issue twice under different labels (e.g. "visa complexity" and "relocation friction" describing the same fact).

Important:

- This is NOT about legal pay discrimination.
- This is NOT a prediction of the candidate's future salary.
- Treat every adjustment as a realistic market estimate rather than a fixed rule.
- Focus on practical recruiter and employer behavior for overseas candidates compared with local candidates.
- Do not focus heavily on tax, lifestyle, or permanent residence pathways.
- Never base the adjustment on race, ethnicity, passport prestige, or a generic nationality ranking. Every adjustment must be tied to concrete, candidate-applicable friction (visa complexity, employer sponsorship risk, relocation logistics, language or market unfamiliarity), never a generalized assumption about people from the candidate's country.
- Apply the contract's maximum and evidence-above boundary to the typical midpoint. A typical midpoint above that boundary requires citing a specific, concrete piece of evidence in the brief explanation, not general market difficulty. A field being present is not proof that it is substantive.
- Apply the contract's Low-baseline confidence cap when the salary evidence grade (from Step 1/Step 2) is Low, since the adjustment is calibrated against a less certain baseline.
- "Employer willingness to sponsor" and "visa complexity" above are about negotiation dynamics — how sponsorship friction realistically affects an employer's offered pay during negotiation, not whether a legally mandated minimum salary exists. That is a separate, hard eligibility question handled later in Step 4 and must never be folded into this percentage.
- If a country's visa route has an education requirement (e.g. a degree related to the occupation), check it against the candidate's actual degree(s) in profile.md before treating it as a friction factor. Do not assume a mismatch based on generic assumptions about the occupation as a class — a candidate can hold multiple degrees, and any one of them being relevant is enough to satisfy a relevance requirement.
- Formal recognition of a specific degree or institution (as opposed to its relevance) is not something you can verify through research — it requires a country's actual credential-assessment body. Never assert that a degree does or doesn't formally qualify. If a country's route has a named formal-recognition or equivalency requirement, state it as a plain process caveat in that country's Brief explanation (e.g. "may require formal degree recognition via [body]; not independently verified") — this is informational only and must never affect the adjustment percentage.
- If situational-profile.md states the candidate already lives in, or already has some form of work authorization for, a country being calculated, weigh relocation friction, remote interview logistics, and perceived hiring risk much lighter for that country specifically: the candidate may not need relocation. Work authorization alone does not establish residence or local interview availability; use the actual location and intended path. This is independent of sponsorship: if their stated status there would still require employer sponsorship to take the job, weigh employer willingness to sponsor and visa complexity normally. If the profile does not establish a material status, report that limit rather than assuming it.

Keep the output compact and present the results country by country.

Save the full adjustment output to salary-calculator-03-adjustments.md in the workspace.

Tell me in a few lines how many countries received a numeric estimate and how many were not estimable, and that the full results are saved for Step 4 to apply. Do not reproduce the per-country adjustment reasoning in this summary. Step complete. Follow the step-completion rule in prompts/shared/runtime.md.
