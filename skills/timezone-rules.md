---
name: Timezone Rules
description: Shared reference-date, daylight-saving, and multi-zone handling for remote suitability and mandatory working-hours comparisons.
---

# Timezone rules

Use `tz-offsets` under `skills/comparison-helper.md` for supplied zones/instants or dated schedules. It verifies those instants/overlap only, not seasonal coverage or tzdata freshness. Establish coverage from dated authoritative sources; samples do not prove a whole-year maximum. Missing tzdata follows the shared fallback without installation.

- Use the candidate's explicit city/zone and the target job location or researched hub. Resolve zones with current IANA timezone/DST information or an equivalent dated authority. Record zones, source and reference date in existing Reason/audit text. A city establishes neither availability nor willingness to work particular hours.
- Unless the user specifies a period, assess the next 12 months from research. Compare simultaneous offsets at relevant transitions in both places; report the seasonal range and maximum absolute difference for a maximum-time-difference rule. Never combine offsets that do not occur simultaneously.
- Assess relevant hubs separately in multi-zone countries. A whole-country Remote rejection requires all assessed relevant hubs to fail and sufficient coverage. Partial passes retain an otherwise-supported conditional Remote finding, naming locations and seasonal limits. Missing candidate zone or coverage leaves suitability unverified; ask the parent when needed.
- Job Screener compares mandatory JD hours with explicit candidate availability, including DST over the job period. Missing hours/zones remain unknown, not blockers. Country Finder's offset preference does not establish working-hours availability.
- Timezone rejection affects Remote only, never relocation-based Sponsorship. Skip maximum-offset filtering when the user chose "no limit".
