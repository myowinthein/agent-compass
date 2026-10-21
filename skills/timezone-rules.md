---
name: Timezone Rules
description: Shared reference-date, daylight-saving, and multi-zone handling for remote suitability and mandatory working-hours comparisons.
---

# Timezone rules

For supplied zones/instants or explicit dated schedules, read `skills/comparison-helper.md` and run `tz-offsets`. This verifies only those instants and overlap, not transition coverage or local tzdata freshness. Establish seasonal coverage with the dated sources below; never promote sampled offsets into proof of a whole-year maximum. Missing tzdata uses the shared fallback without installation.

- Use the candidate's explicitly provided city/timezone and a target job location or researched work hub. Resolve named timezones using current IANA timezone/DST information or an equivalent dated authoritative source. Record the zones, source, and reference date in the existing Reason or audit text. A city alone does not establish the candidate's availability or willingness to work particular hours.
- Unless the user supplied a work period, assess recurring remote compatibility over the next 12 months from the research date, not just today's UTC offsets. Compare simultaneous offsets at relevant DST transitions in both places. Use the maximum absolute offset difference over that period for a stated maximum-time-difference rule; state both the seasonal range and that maximum. Do not combine offsets from dates that never occur together.
- For multi-timezone countries, assess relevant researched job hubs separately. Never reject the entire country's Remote track using one arbitrarily chosen city. Mark a country unsuitable for the timezone rule only if all assessed relevant hubs fail and coverage supports that conclusion. If only some hubs pass, retain a conditional Remote finding and name the qualifying locations and seasonal limitations in Reason. If coverage or the candidate's zone cannot be established, report timezone suitability as unverified rather than inventing an exclusion; ask the parent for clarification when needed.
- In Job Screener, compare actual mandatory working hours in the JD with explicitly stated candidate availability, including DST over the stated job period. Without sufficient hours/zone information, compatibility is unknown, not a blocker. Country Finder's maximum offset preference is not proof of working-hours availability.
- A Country Finder timezone rejection affects Remote only. It never removes Sponsorship suitability, because that track assumes relocation. Skip maximum-offset filtering entirely when the user chose "no limit".
