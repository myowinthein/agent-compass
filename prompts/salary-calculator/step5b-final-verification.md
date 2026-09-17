Read sc-step4-salary-table.md from the workspace. Also read sc-step2-salary-data.md and sc-step3-adjustment-values.md for the underlying salary data and adjustment values, profile.md for the candidate profile and target role, and sc-step5a-career-ladder.md for the career ladder already confirmed with me before this step. Base the audit only on these files, not on prior conversation memory.

Goal

Perform a strict recruiter market audit of the FINAL salary framework.

Challenge assumptions where warranted.

Do NOT automatically defend the existing salary numbers.

Do NOT automatically lower the numbers unless the evidence genuinely supports doing so.

Follow the evidence.

Framework Definitions (used by the checks below)

- Safe = Market Midpoint (the "Realistic" value) from the Mid-size / Mainstream Local-Market tier
- Stretch = Market Midpoint (the "Realistic" value) from the Premium / International / Remote-first tier

The salary data (with its sources and exclusions) and the international adjustment values are already in the files you read above — work from those directly rather than from any assumed methodology.

Save all four checks below and the recalibration verdict to file only — do not reproduce that detailed reasoning in your chat response, since it would overwhelm rather than help. The resulting final table is different: show it directly in your chat response too, copied from what you save to file — table only, no surrounding commentary. This is the one thing in this step you do show me — the four checks themselves stay file-only, and whether recalibration happened is stated as a plain fact in the completion message, not as extra commentary around the table.

File format (write the following structure, including the final table, to sc-step5b-final-verification.md — this is the only file this step writes; the four checks are file-only, see below for what also goes in chat):

---

1. Candidate Positioning

CAREER LEVELS FOR THIS ROLE:

Use the career ladder in sc-step5a-career-ladder.md — it was drafted from profile.md and confirmed with me before this step. Do not redraft it or ask me to confirm it again; treat it as settled.

First determine:
- likely career level
- likely target role level

Benchmark compensation primarily against the TARGET role being applied for, not the highest historical responsibility.

Do not assume a level near the top of the ladder unless both the candidate profile and target role clearly support that level. Use the level names from the confirmed ladder, which reflect my actual IT role — do not force backend or software-engineering titles onto a different IT role.

---

2. Framework Calibration Review

Determine whether the overall framework is:
- conservative
- recruiter safe
- appropriately calibrated
- slightly inflated
- heavily inflated
- under market

Evaluate whether the following legitimately increase compensation expectations:
- years of experience
- technical or domain depth
- leadership responsibility
- ownership scope
- business impact
- specialization scarcity
- cross functional influence
- stakeholder complexity
- domain expertise
- employer relevance
- international experience
- proven delivery history

Separately identify factors that commonly inflate salary expectations beyond practical recruiter behavior.

Examples:
- premium employer weighting
- niche industry weighting
- multinational weighting
- higher-level title interpretation (e.g. treating a Senior profile as Staff or Principal)
- leadership title inflation
- remote company bias
- niche specialist premium
- AI optimism bias

Clearly separate:
A. Legitimate compensation drivers
B. Potential inflation sources

---

3. Country by Country Verification

For each country:

Evaluate:
- Safe positioning
- Stretch positioning
- recruiter comfort
- sponsorship realism — if this country has a Legal Requirement flag from Step 4, factor that concrete result in rather than judging realism independently of it; if the state is "Blocked," sponsorship realism for that country is zero regardless of how attractive the salary figures look
- overseas hiring realism
- interview conversion impact
- the underlying salary data's evidence grade from Step 2, if provided — a Low grade should temper how confidently this country's positioning is stated, even if the classification itself doesn't change

Use approximate percentile bands rather than precise percentiles.

Examples:
- 50-60%
- 60-70%
- 70-80%
- 80-90%

Avoid false precision.

Classify Safe as:
- conservative
- recruiter comfortable
- appropriately calibrated
- slightly aggressive but realistic
- strong senior pricing
- top tier compensation

Classify Stretch as:
- realistic stretch
- strong senior stretch
- elite employer compensation
- high end specialist compensation
- international remote premium compensation

For both Safe and Stretch, distinguish between:
- commonly achievable
- theoretically achievable

---

4. Framework Recommendation

Determine whether:
- Safe philosophy remains appropriate
- Stretch philosophy remains appropriate
- employer segmentation remains appropriate
- percentile assumptions remain appropriate

If improvements are recommended, explain:
- why
- what assumption caused the issue
- what structural change is recommended

Also evaluate whether:
- Safe should use broader market employers instead of strong market employers
- Stretch should be derived from Safe plus a realistic premium
- premium employers should remain upper bound references rather than baseline inputs
- target role should carry more weight than historical title
- international candidate adjustments remain appropriate

---

5. Recalibration

Only if the evidence genuinely supports recalibration:
- revise the affected countries
- adjust salary ranges upward or downward where appropriate
- prioritize recruiter comfort
- prioritize interview conversion
- prioritize sponsorship realism
- prioritize broad market achievability
- prioritize realistic overseas positioning

If recalibration is not supported, explicitly state that the existing framework remains appropriate and do not generate a revised salary table. Copy the table from sc-step4-salary-table.md into this file as the final table, unchanged.

If recalibration is required, generate a revised table using the same format and country order as Step 4 — including the Legal Requirement column. Read and apply skills/sponsorship-threshold-rules.md and recompute that column against the revised Safe and Stretch Fixed values, using the same threshold data from Step 1. A country's Legal Requirement result from Step 4 does not carry forward automatically — recalibration can push a figure below a threshold it previously cleared, or above one it previously missed, so it must be re-evaluated against whatever the revised figures actually are. This revised table becomes the final table.

If Step 4 flagged any country as below the candidate's hard-floor salary minimum, re-check that flag against any revised Safe value too, and restate it in this file's Summary if it still applies. Never adjust Safe or Stretch to clear it, the same principle as the Legal Requirement column.

If Step 4 marked any country "Blocked," verify that classification is still correct against current evidence (a route can open or close), carry it into the revised table's Legal Requirement column exactly as "Blocked" if it still applies, and restate the reference-only note in this file's Summary. Never let a Blocked country's attractive Safe/Stretch figures override the block in the final table or Summary.

Either way — unchanged or revised — write the resulting final table into sc-step5b-final-verification.md, in the same file as the four checks and the recalibration verdict. sc-step4-salary-table.md is left untouched as the pre-audit record; this step never creates any other file. sc-step5b-final-verification.md is the only file this step writes.

After saving, show the final table directly in your chat response — copied from what you just wrote to the file, same format. Output only the table — no surrounding commentary, and do not reproduce the four detailed checks themselves in chat.

Then tell me the pipeline is complete: if revised, "Salary Calculator is complete. [N] countries audited, recalibration applied — see the table above. Full audit saved to sc-step5b-final-verification.md." If not revised, "Salary Calculator is complete. [N] countries audited, no recalibration needed — see the table above. Full audit saved to sc-step5b-final-verification.md."

Overall Principles

- Be analytical.
- Be recruiter focused.
- Be evidence driven.
- Challenge assumptions when warranted.
- Do not defend the framework.
- Do not attack the framework.
- Follow the evidence.

Step complete — stop here and wait for the main command.
