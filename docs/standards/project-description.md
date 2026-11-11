# Project descriptions

Use the same description frame in Agent Helm and Agent Compass, with facts and wording suited to each project. Follow the project's active Writing rule. GitHub About is the public main description; the [plugin manifest](../../.claude-plugin/plugin.json) stores that approved text in versioned source.

| Form | What it expresses | Expected maximum | Owner |
|---|---|---|---|
| Main | Two sentences: product type, audience and supported clients, then the main outcomes. Group capabilities instead of listing every command. | 250 characters. | Plugin manifest `description`. |
| Summary | One sentence covering the product's purpose, clients and broad outcomes. Preserve the main description's facts while selecting what fits this shorter form. | 160 characters. | [Site configuration](../_config.yml) `description`. |
| Marketplace | One installation-focused sentence naming the product, what users install and supported clients. | 160 characters. | Marketplace's top-level `description`. |
| README introduction | Identity and audience, followed by benefits and broad capabilities in the project's voice. | 20 / 50 words. | [README introduction](readme.md#introduction). |

Character counts include spaces and punctuation. These are project writing limits, not platform limits or promises about search-result display. Preserve material meaning and necessary qualifications. Taglines keep their separate role as short category labels or brand phrases.

## Copies and variants

| Location | Treatment |
|---|---|
| GitHub repository About description | Exact copy of Main. |
| `.claude-plugin/plugin.json` description | Owns Main. |
| `.codex-plugin/plugin.json` description, when present | Exact copy of Main; preserve other client-specific fields. |
| `.claude-plugin/marketplace.json` matching plugin entry's description, when already declared | Exact copy of Main. Preserve an intentionally absent field. |
| `docs/_config.yml` description | Owns Summary. |
| `README.md` front matter description | Exact copy of Summary. |
| `.claude-plugin/marketplace.json` top-level description | Marketplace variant, describing installation rather than repeating the product introduction. |
| README introduction | Written variant under its existing paragraph frame; retain the same product facts without requiring identical wording. |
| Page, command, skill and specialist descriptions | Describe their own subjects. A `description` field alone does not make text a copy of the whole-project description. |

Existing legal descriptions retain their own meaning and review requirements. Use the normal owning review if an actual factual change affects them; this standard starts no legal rewrite.

## Updating descriptions

Check the actual workflows before changing product claims. Update each owner and its exact-copy consumers together, preserving versions, plugin identity, packaging and client constraints. Keep this standard identical in both sibling repositories; their approved description text can differ. Record no second copy of the approved strings in this guide.

Verify the selected lengths, exact copies, related package checks and rendered homepage metadata. Review written variants for semantic agreement rather than forcing them into copied text. Keep this maintainer guide outside the published site and plugin runtime.

Changing source does not update GitHub About. When that setting change is authorized, read its current value, update only the description and read back the result. Preserve website URLs, topics and unrelated settings. Local commits, GitHub settings and later source publication are separate outcomes; an unavailable or changed target stays a reported gap. Keep pushes under the project's publication policy.
