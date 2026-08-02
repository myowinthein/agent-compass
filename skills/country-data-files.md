---
name: Country Data Files
description: Copies the country wealth-tier dataset (shipped) and the saved preferred-countries list (personal, gitignored) into the workspace root if missing. Standalone — not referenced automatically by any command or prompt; invoke explicitly.
---

# Country Data Files

Check if `country-wealth-tiers.md` already exists in the workspace root. If it does not, copy it there from `data/country-wealth-tiers.md`.

Check if `data/preferred-countries.md` already exists in the workspace. If it does not, copy it there from the plugin's own `data/preferred-countries.md`. This one stays under `data/` — not the workspace root — because that is the exact path Country Finder step2 reads.

Do nothing else — no questions, no confirmation, no showing the content back. Just copy whichever is missing.
