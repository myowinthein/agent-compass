---
name: Country Reference Offer
description: Copies the country wealth-tier dataset into the workspace once, then points to it whenever a step is about to ask the candidate to name a country, region, or country list. Reused by country-finder step1, salary-calculator step1, and portal-finder.
---

# Country Reference Offer

Check if country-wealth-tiers.md exists in the workspace. If it does not, copy the full contents of data/country-wealth-tiers.md into a new file named country-wealth-tiers.md in the workspace.

Immediately before asking me to name, include, exclude, or list any country, say:

"For country ideas grouped by wealth tier (GNI per capita), see country-wealth-tiers.md in this folder."

Then ask your question as normal.
