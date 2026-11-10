# Documentation

Keep this file identical in Agent Helm and Agent Compass. When changing the frame, update and compare both copies; report any copy that cannot be synchronized. Each project's documentation and README keep their own voice, terminology, examples and workflow-specific detail. Paths in this guide refer to the repository root.

## File ownership

Keep website pages, included setup text, layouts, styles, scripts, renderers, configuration, dependencies and documentation checks under `docs/`. Build or preview from that directory; the output stays in `docs/_site/`. Documentation support files and this authoring standard are excluded from published content.

The repository README, shared plugin icon and canonical agent instructions remain outside `docs/`. The site renders those authoritative inputs without maintained copies. Rebuild after changing external inputs, since the website watcher covers `docs/`. Preserve published page/image URLs, section anchors and setup redirects when moving sources. GitHub Actions stays in `.github/workflows/` and calls the documentation build; the root Rakefile coordinates project checks.

## Guide structure

Write guides that people can read comfortably to understand how a command, rule or supporting workflow works. Follow the project's active Writing rule for prose and its complete reference-link workflow. Cover relevant guides, supporting pages outside navigation and included explanatory content.

- Use **Overview / Details** for paired topics. Overview is the default: explain purpose, main phases, meaningful choices, outcomes and necessary constraints. The Details view expands the same journey with complete procedures, conditions, examples, exceptions and recovery. Headings may differ; keep the sequence of ideas aligned. Do not force a second depth onto indexes, short installation procedures, examples or unrelated policies.
- Put `docs/_includes/guide-depth.html` immediately below the title in both views. Keep labels, placement and behavior consistent. Use ordinary current-tab navigation with stable URLs, native browser history and an accessible current-page indication. Preserve existing overview URLs and section anchors, including targets reached through setup tabs, redirects or collapsed content.
- Give Overview an early, compact Mermaid summary that establishes the main flow. Diagrams in Details cover all meaningful routes, questions, approvals, exits and recovery outcomes. Split complex phases into connected diagrams; do not draw every mechanical action or create one oversized canvas. Use diagrams only when they clarify the subject, without forcing a process onto conceptual material. Keep essential meaning in text.
- Let text explain more than the diagram. Use connected paragraphs, short lists, comparisons, tables and examples where useful. Keep both views approachable; the Details view can be rich and precise without becoming an encyclopedia, diagram transcript or collection of overloaded paragraphs. Remove filler, hype and generic AI phrasing. Brevity is not a word, line or node quota. Readers needing implementation detail can follow source links or inspect the code.
- Preserve decision-changing constraints, consequential effects, approvals, coverage semantics and state/recovery protections. Preserve research coverage and evidence quality, independent tracks/tiers, uncertainty, candidate-data boundaries, checkpoints, arithmetic/output contracts and final audits where applicable. Overview can omit internal mechanics while keeping necessary warnings visible. The Details view retains complete behavior, including rare consequential cases.
- Keep one authoritative plain Markdown instruction source for each workflow, prompt and rule. Details pages render those sources through `docs/_plugins/guide_content.rb`; introductions and diagrams add reading context without defining competing policy. Skills load canonical Markdown without website controls, diagrams or navigation. Supporting procedures retain their owners and load conditions.
- Apply the Writing rule's complete reference-link workflow during documentation maintenance. Follow links and includes to affected content outside the menu, and link authoritative standards instead of reproducing them. Verify relevant destinations, anchors and interactions with available tools; report gaps.
- Migrate a source with its skill links, shared references, package validation and relevant tests. Remove the old copy only after the replacement is verified. Preserve operational meaning during readability edits; relocation and a passing site build alone do not establish behavior equivalence. Rebuild after changing excluded instruction sources; restart the preview after renderer or configuration changes.

## README structure

### Introduction

Use two introductory paragraphs between the banner and the documentation link, following the project's active Writing rule and checking claims against the actual workflows.

| Element | Purpose | Expected maximum |
|---|---|---|
| First paragraph: identity | State what the project is, who it serves and which platforms it supports. Use one direct sentence. | 20 words. |
| Second paragraph: value | Explain what users can accomplish and how the main capabilities work together. Lead with the benefit, then cover the broad scope in one or two sentences. | 50 words. |

Keep the paragraphs' roles distinct and use wording suited to the project's audience. Group related capabilities and leave individual command details for **When I use it**. These are expected limits; preserve material meaning and necessary qualifications.

### Command entries

Use this frame for every entry in the README's **When I use it** section. Follow the project's active Writing rule and check claims against the canonical workflow and relevant supporting instructions. Retain the project's personal voice and existing heading anchors.

| Element | Purpose | Expected maximum |
|---|---|---|
| Heading | Identify the command by name alone. | Command name only. |
| First paragraph | Explain when I use it and the benefit I want. Link a meaningful purpose phrase to the command's Overview guide. | 45 words. |
| Invocation block | Show both client invocations in one `text` block: `Codex → $<command>    Claude → /<command>`, replacing `<command>` with the actual command name. | One line. |
| Closing paragraph | Explain the main actions, concrete result and important choices, approvals or limits without repeating the first paragraph. | 70 words. |

Use two prose paragraphs per entry. These are expected limits, not reasons to remove essential warnings or approval boundaries. Keep deeper explanation and argument examples in the linked guides; add other contextual links only when they help readers take a distinct next step. Keep command names bare in general prose. Follow the Writing rule's reference-link workflow and use absolute published documentation URLs for this project's site so links work on GitHub and the site.

### Closing sections

End with two separate level-two sections: **Contributing**, then **License**. Contributing uses one short paragraph inviting bug reports, feedback on unclear guides and ideas through a meaningful issue-tracker link. Ask briefly for useful context and match the project's voice; do not invent a PR process or promise response times. License uses one sentence stating the actual project license with a link. Preserve existing license meaning and old section anchors.
