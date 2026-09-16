---
name: Country Finder v2 Scoring Rules
description: Defines evidence standards, numeric remote and sponsorship scoring, priority calculation, tiers, and cutoffs for Country Finder v2.
---

# Country Finder v2 Scoring Rules

## Track separation

Score two independent tracks:

- **Remote:** an employer linked to the country hires the candidate while the candidate remains in the stated current country.
- **Sponsorship:** an employer supports a work visa or permit and the candidate relocates.

Domestic-only remote work is not cross-border remote work. A legal visa route is not proof that employers use it for the candidate's occupation.

## Evidence hierarchy

Prefer, in order:

1. Current official government immigration or labour sources.
2. Current direct employer vacancy or policy pages.
3. Official sponsor or accredited-employer registers, used only to prove capability, not intent.
4. Credible specialist job boards, recruiters, salary surveys, or relocation services.
5. Aggregators and search snippets, treated as leads that require direct verification.

For visa facts, use current official sources whenever available. For market claims, prefer evidence from the last 180 days. Record the URL and access or publication date. Say "no evidence found" instead of inferring.

High confidence normally requires an official route plus multiple current direct-employer or direct-market examples. One worldwide vacancy proves one accessible opening, not deep market volume.

## Remote score, 0 to 100

| Component | Maximum |
|---|---:|
| Explicit eligibility from the candidate's current country, region, or worldwide | 35 |
| Relevant opportunity volume at the target role and seniority | 25 |
| Competitive compensation likelihood for this profile | 15 |
| Flexible or async schedule, or workable timezone overlap | 10 |
| Practical employee, EOR, contractor, or international payroll mechanism | 10 |
| Required working-language accessibility | 5 |

Rules:

- A role saying only "remote" receives no cross-border-access credit.
- A country-specific or Europe-only role receives no credit when the candidate is outside that area.
- One explicit current worldwide or regional vacancy may establish accessibility, but cannot by itself earn high volume points.
- If the user set no timezone limit, do not exclude a country; reward explicit flexibility and note adverse overlap.

## Sponsorship score, 0 to 100

| Component | Maximum |
|---|---:|
| Legal pathway and plausible occupation eligibility | 25 |
| Demonstrated employer willingness or occupation-relevant sponsor ecosystem | 25 |
| Relevant opportunity volume at the target role and seniority | 20 |
| Recruiter-friendly market salary can clear the legal threshold | 15 |
| Required working-language accessibility | 10 |
| Processing burden, citizenship friction, and dependant practicality | 5 |

Rules:

- A government route earns pathway points, not employer-willingness points.
- A sponsor register proves that an organisation may sponsor, not that a vacancy will be sponsored.
- An application checkbox asking about sponsorship is operational evidence, not a promise.
- "Relocation support" counts as visa evidence only when immigration, visa, permit, entry permit, or sponsorship is explicit.
- For countries where employer-filed visas are the standard mechanism for virtually all expatriate employees, that system may support ecosystem points, but current role evidence is still required for high scores.
- Do not assume a product-design title maps to an eligible occupation. Compare actual duties and official classifications.

## Salary treatment

- Historical salary is context, never a universal international anchor.
- Unless the user gives a hard minimum, assess a recruiter-friendly local-market midpoint or middle-to-upper-middle senior band: not a low-ball figure and not a top-decile demand.
- For sponsorship, the proposed band must also clear the applicable legal threshold.
- Label salary bands as screening or negotiation guidance, not guaranteed medians.
- Worldwide employers may geo-adjust compensation; verify their policy before presenting a firm ask.

## Classification and priority

- **Strong:** 70 to 100
- **Moderate:** 55 to 69
- **Weak:** 40 to 54
- **Very weak:** 0 to 39

Priority score:

1. Take the higher of the Remote and Sponsorship scores.
2. Add 5 points if the other score is at least 55.
3. Cap the result at 100.

Tiers:

- **Gold, 70+:** primary focus and custom applications.
- **Silver, 55 to 69:** alerts and vacancy-led applications.
- **Bronze, 40 to 54:** opportunistic only.
- **Ribbon, below 40:** deprioritise.

Always show two distinct operational boundaries:

- The **human-effort cutoff** is after Gold.
- The **broad active-monitoring cutoff** is after Silver.

## Audit rules

- Reopen decisive URLs and verify that they support the exact claim.
- Downgrade generic pathways, stale vacancies, search snippets, and aggregator-only tags.
- Do not convert one vacancy into country-wide market depth.
- Recalculate every component total and the priority formula.
- Use audited scores in the final table. Never force the final output to use pre-audit values.
- Account for every input country, including countries with insufficient evidence.

