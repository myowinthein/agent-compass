# Documentation

Keep this file identical in Agent Helm and Agent Compass. When changing the frame, update and compare both copies; report any copy that cannot be synchronized. Each project's documentation keeps its own voice, terminology, examples and workflow-specific detail. Paths in this guide refer to the repository root.

## File ownership

Keep website pages, included setup text, layouts, styles, scripts, renderers, configuration, dependencies and documentation checks under `docs/`. Build or preview from that directory; the output stays in `docs/_site/`. Documentation support files and `docs/standards/` are excluded from published content.

The repository README, shared plugin icon and canonical agent instructions remain at their existing package paths. The site renders the root README and shared icon without maintained copies. Guides link to agent instructions as source references; they do not render those instructions into reader-facing pages. Rebuild after changing external site inputs such as the README. Preserve published page/image URLs, section anchors and setup redirects. GitHub Actions stays in `.github/workflows/` and calls the documentation build; the root Rakefile coordinates project checks.

## Reading levels

The sidebar displays `vX.Y.Z` beside the project title; both form one homepage link. Read the version from `.claude-plugin/plugin.json` during the normal docs build; ship maintains that source, so no separate docs version is needed.

Documentation provides two human reading modes, with the existing repository available for deeper exploration:

| Level | Reader's goal | Content |
|---|---|---|
| Overview | Understand the command or rule quickly and comfortably. | Purpose, main phases, meaningful choices, outcomes and necessary constraints. |
| Details | Understand the same journey in greater depth. | Independently written explanations, richer diagrams, examples, decision reasons, important exceptions and recovery or follow-up where relevant. |
| Existing source | Explore exact agent instructions or implementation. | Link directly to the existing workflows, prompts, rules or code. Do not create a third website mode or another source copy. |

Both modes follow the project's active Writing rule and its complete reference-link workflow. Read the relevant source to verify behavior before authoring or updating a guide. Details is neither an embedded source file nor a line-by-line paraphrase of agent instructions. Avoid execution directives aimed at agents, internal question maps and mechanical bookkeeping unless they help a reader understand a meaningful choice or result. Sources remain authoritative for agent behavior; documentation explains that behavior without defining new policy.

## Guide structure

- Use **Overview / Details** for paired topics. Overview is the default. Details follows the same order of ideas while expanding their explanation; headings and presentation can differ. Do not force a second depth onto indexes, short installation procedures, examples or unrelated policies.
- Put `docs/_includes/guide-depth.html` immediately below the title in both views. Keep labels, placement and behavior consistent. Use ordinary current-tab navigation with stable URLs, native browser history and an accessible current-page indication. Preserve existing overview URLs and meaningful section anchors, including targets reached through tabs, redirects or collapsed content.
- Give Overview an early, compact Mermaid summary when a diagram clarifies the topic. Details diagrams cover the meaningful routes, decisions, approvals, exits and recovery outcomes. Split complex phases into connected diagrams; do not draw every mechanical action or create one oversized canvas. Keep essential meaning in text.
- Let text explain more than the diagram. Use connected paragraphs, short lists, comparisons, tables and examples where useful. Details can be rich and precise without becoming an encyclopedia, diagram transcript or overloaded instruction manual. Remove filler, hype and generic AI phrasing. Brevity is not a word, line or node quota.
- Preserve decision-changing constraints, consequential effects, approvals and the distinctions readers need to interpret results. Explain relevant coverage, state/recovery limits, research confidence, independent tracks or tiers, arithmetic and output guarantees at the reader's level. Link exact implementation contracts instead of reproducing every field or protocol. A simpler explanation must not imply broader permission or stronger verification.
- Write Details content directly in its Markdown page under `docs/`. Use `source_files` front matter to identify the existing instruction sources behind it, and provide useful source links for further exploration. Never use Liquid filters, includes or a generator to insert complete agent prompts into a guide. Canonical agent instructions retain their owners, loading conditions and package paths.
- Apply Writing's complete reference-link workflow as part of the same maintenance pass. Follow references outside the menu when relevant, link specific human-guide sections for reader tasks and existing repository sections for implementation detail, and avoid linking every possible phrase. Verify destination meaning, anchors and available interaction behavior; report gaps.
- When behavior changes, review both reading modes for affected explanations and references. A source edit does not automatically update authored documentation. Preserve the distinction between code checks, factual review and browser interaction checks. If files actually move, update their references and required checks together; do not change skill loading paths merely to publish a guide.
