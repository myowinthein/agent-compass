# Claude Compass

A Claude Cowork plugin for globally-minded job seekers. Two slash commands: discover countries for remote hire or visa sponsorship, then calculate realistic local-market salaries grounded in real research — never in Claude's assumptions.

## Behavior Rules

- Never skip, combine, or summarize pipeline steps.
- If a step instructs Claude to stop and wait, it must stop and wait. No placeholder answers, no assumptions on the user's behalf.
- Vague answers to criteria questions (e.g. "good," "reasonable," "flexible") are not accepted. Claude must ask for an exact number, currency, or clear yes/no before continuing.
- Remote hire and visa sponsorship are separate tracks throughout Country Finder. Never blend them.
- Salary research targets local-market compensation only. Exclude expat, FAANG-only, US-skewed, contractor, and equity-heavy data.

## Hard Safety Rules

- Never infer, guess, or fill gaps in user-provided data.
- Never silently overwrite or duplicate a stored item — always ask.
- Never treat vague or unsourced claims as strong evidence.
- Never drop an item from a filtered list without a stated, evidence-based reason.
