# Project descriptions

Use the same description frame in Agent Helm and Agent Compass, with facts and wording suited to each project. Follow the project's active Writing rule. Main means the description text in GitHub About: it supplies the approved main wording, and the [plugin manifest](../../.claude-plugin/plugin.json) keeps its versioned mirror.

| Form | What it expresses | Source |
|---|---|---|
| Main | Product type, audience, supported clients and main outcomes. Group capabilities instead of listing every command. | GitHub About description. |
| Summary | A shorter account of the product's purpose, clients and broad outcomes, preserving Main's facts while selecting what fits. | [Site configuration](../_config.yml) `description`, derived from Main. |
| Marketplace | Installation-focused wording naming the product, what users install and supported clients. | Marketplace's top-level `description`, derived from Main. |
| README introduction | Identity and audience, followed by benefits and broad capabilities in the project's voice. | Derived from Main; follow the [README introduction standard](readme.md#introduction) for structure and length. |

Keep each form concise and respect actual destination constraints without losing material meaning or necessary qualifications. No fixed character or sentence count applies here, and no search-result display length is promised. Taglines keep their separate role as short category labels or brand phrases.

## Copies and variants

| Location | Treatment |
|---|---|
| GitHub repository About description | Source of Main. |
| `.claude-plugin/plugin.json` description | Versioned exact copy of Main. |
| `.codex-plugin/plugin.json` description, when present | Exact copy of Main; preserve other client-specific fields. |
| `.claude-plugin/marketplace.json` matching plugin entry's description, when already declared | Exact copy of Main. Preserve an intentionally absent field. |
| `docs/_config.yml` description | Owns Summary. |
| `README.md` front matter description | Exact copy of Summary. |
| `.claude-plugin/marketplace.json` top-level description | Marketplace variant, describing installation rather than repeating the product introduction. |
| README introduction | Written variant under its existing paragraph frame; retain the same product facts without requiring identical wording. |
| Page, command, skill and specialist descriptions | Describe their own subjects. A `description` field alone does not make text a copy of the whole-project description. |

Existing legal descriptions retain their own meaning and review requirements. Use the normal owning review if an actual factual change affects them; this standard starts no legal rewrite.

## Updating descriptions

When maintaining project descriptions, read the current GitHub About description and compare the mapped locations. Check claims against the actual workflows. Report mismatches and reconcile them with source facts and already-approved changes before replacing either About or its mirror; ask only when the intended approved wording remains unclear. If About is unavailable, report the verification gap rather than silently making a local copy authoritative.

Update affected copies and variants together, preserving versions, plugin identity, packaging and client constraints. Verify exact copies, applicable destination constraints, related package checks and rendered homepage metadata. Review written variants for semantic agreement rather than forcing identical wording.

Keep this standard identical in both sibling repositories; their approved description text can differ. Record no second copy of the approved strings in this guide. Keep this maintainer guide outside the published site and plugin runtime.

Changing source does not update GitHub About. When that setting change is authorized, read its current value, update only the description and read back the result. Preserve website URLs, topics and unrelated settings. Local commits, GitHub settings and later source publication are separate outcomes; an unavailable or changed target stays a reported gap. Keep pushes under the project's publication policy.
