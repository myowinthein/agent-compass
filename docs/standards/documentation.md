# Documentation

Help developers understand and use the project comfortably. Choose detail for the reader's task and reading level; the amount of agent instruction or implementation detail available does not determine what belongs in a guide.

Keep this standard identical in Agent Helm and Agent Compass. Update and compare both copies when changing it; report any copy that cannot be synchronized. Each project's guides keep their own voice, terminology, examples and workflow-specific detail. Paths below refer to the repository root.

## File ownership

Keep website source, tooling, dependencies and checks under `docs/`. Build or preview there, with output in `docs/_site/`. Exclude documentation support files and `docs/standards/` from the published site.

The root README, shared plugin icon and canonical agent instructions retain their existing paths. Render the README and icon without maintained copies; rebuild when those external site inputs change. Preserve published URLs, section anchors and setup redirects. Use the existing build and checks rather than adding another publishing arrangement.

## Reading levels

Documentation provides two human reading modes, with existing source available for implementation depth:

| Level | Reader's goal | Content |
|---|---|---|
| Overview | Understand the command or rule quickly and comfortably. | Purpose, main phases, meaningful choices, outcomes and necessary constraints. |
| Details | Understand the same journey more fully. | Independently written reasons, examples, material exceptions and recovery guidance where they help someone understand or decide. Exhaustive workflow coverage is not required. |
| Existing source | Explore exact agent instructions or implementation. | Link to the existing workflows, prompts, rules or code. Do not create a third website mode or another source copy. |

Follow the project's active Writing rule, including its reference-link workflow. Verify behavior against the relevant source. Sources define agent behavior; human guides explain it without introducing new policy. Agent execution directives, internal question maps and mechanical bookkeeping belong in source unless a reader needs them to understand a meaningful choice or result.

## Guide structure

- Use **Overview / Details** for paired topics, with Overview as the default. Keep a compatible reading order, adding depth only where useful; headings and presentation can differ. Do not pad every topic or force a second view onto indexes, short installation procedures, examples or unrelated policies.
- Put `docs/_includes/guide-depth.html` immediately below the title in both views. Keep labels and placement consistent, with current-tab navigation, native browser history and an accessible current-page indication. Preserve existing overview URLs and section targets, including those reached through tabs, redirects or collapsed content.
- Give Overview an early, compact Mermaid summary when it clarifies the topic. Details can show relevant decisions, approvals, exits and recovery without tracing every mechanical branch. Split a complex diagram when helpful. Text and diagrams should complement each other; use prose to explain reasons or conditions rather than repeat every node, and keep essential meaning available in text.
- Use connected paragraphs, short lists, tables and examples when they help the reader. Preserve meaningful choices, consequential effects, approvals and limits needed to interpret results, at the reader's level. Simpler wording must not imply broader permission or stronger verification. Brevity is not a word, line or diagram-node quota.
- Author Details directly in its Markdown page under `docs/`, with `source_files` front matter and useful links to existing sources for exact contracts. Do not embed complete agent prompts through Liquid, includes or generators, or paraphrase instructions line by line. Canonical instructions retain their owners and loading conditions.

## Maintenance

When behavior changes, review both reading modes for affected explanations and references. Rewrite the affected passage at its intended depth instead of appending an explanation for every changed instruction. Merge related information and remove obsolete or repeated explanations within scope. Details adds useful understanding; it is not a destination for everything omitted from Overview. Leave exact protocols in linked source unless readers need them to act or interpret the outcome.

Preserve useful existing structure and unrelated content. Check that the revised explanation is accurate, comfortable to follow and sufficient for the reader's task. Verify affected references through Writing's reference-link workflow and preserve required project checks. Distinguish source review from rendered-page and browser-interaction evidence, reporting relevant gaps in the normal handoff. File moves require related reference and check updates; publishing a guide does not justify moving skill entry points.
