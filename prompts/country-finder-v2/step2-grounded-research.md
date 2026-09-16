# Step 2: Grounded country research

Require `cfv2-step1-criteria.md` and `profile.md`. Read them. Read `skills/country-finder-v2-scoring-rules.md` completely before researching.

## Country universe

- If Step 1 contains an explicit country list, use it.
- If Step 1 says to use the default, read `data/default-preferred-countries.md`, show it grouped by region, ask the user to confirm it, and wait.
- Apply exclusions exactly.
- Save the final ordered universe to `cfv2-step2-country-universe.md` before research.

## Research execution

Perform live web research. If live web research is unavailable, generate ready-to-copy batch prompts containing every rule in this step, save them to `cfv2-step2-manual-research-prompts.md`, tell the user, and stop.

When parallel agents are available:

- Batch by the region headings in the default data file, or use batches of about 8 to 12 countries.
- Give each agent the complete candidate context, exact countries, scoring rules, evidence rules, and required output schema.
- Each agent writes only to a unique file named `cfv2-step2-batch-<slug>.md`.
- Never let two agents append to the same file.
- The parent waits for every batch, validates country coverage, and consolidates the results.

For every country research both tracks and collect:

### Remote

- Current roles or employer policies explicitly accepting the candidate's current country, region, or worldwide.
- Number and quality of relevant senior target-role examples.
- Stated compensation or credible local/global compensation evidence.
- Timezone, async, flexibility, and overlap requirements.
- Employee, EOR, contractor, payroll, or location restrictions.
- Required working language.

### Sponsorship

- Current official visa or work-permit route.
- Plausible occupation or duty mapping for the target role.
- Current direct employer evidence of visa, work-permit, immigration, or entry-permit support.
- Relevant target-role market depth.
- Legal salary threshold and a recruiter-friendly market band.
- Working-language accessibility.
- Processing/employer burden, citizenship-specific restrictions if evidenced, and dependant practicality.

For every material claim record the URL and source/access date. Distinguish direct employer evidence from aggregator evidence. Record negative evidence too, such as location restrictions, existing-work-right requirements, or explicit no-sponsorship language.

Produce a provisional component score for each track using the exact rubric, but do not assign the final tier yet.

The parent writes the consolidated, one-country-per-section result to `cfv2-step2-research.md`, including a coverage check that lists every input country exactly once. Update state to Step 2 and continue automatically to Step 3.

