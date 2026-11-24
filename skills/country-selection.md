---
name: Country Selection
description: Shared exact-list, previous-scope and default-country choices for fresh Country Finder and Salary Calculator searches.
---

# Country selection

Use this for CF/SC country questions. Apply skills/run-workspaces.md first: select the person and resolve View, Resume or Start fresh. View replays saved results; Resume retains its confirmed scope and recorded source without this question. New chats do not discover other chats' countries. An approved changed-scope repair still uses the runtime's preservation rules.

## Choose the source

1. A supplied country list is the exact scope. Expand regions and apply explicit edits, clarifying material boundary ambiguity only. Never append defaults or offer another source instead. An explicit default or saved-source request also takes precedence over an automatic offer.
2. Otherwise offer the most recently used CF/SC search for this person in this chat, retained before starting the new run under skills/run-workspaces.md. This covers CF → SC, CF → CF, SC → CF and SC → SC. Use the actual invocation association, not file modification times or a guessed newest run. If only one eligible prior source exists, it is unambiguous. If several exist and their order cannot be established, name the alternatives in the country-choice question alongside own/default-list choices; do not add a routine source-approval gate. Never select another person's run or search other chats. Explicit saved-path requests retain the existing identity checks.
3. Read skills/research-helper.md and call `research-scope` with the selected source's absolute workspace and workflow. CF reads its Step 2 candidate scope; SC reads its Step 1 research scope. Use the full confirmed list, including countries later excluded, rejected, missing or skipped. Do not select names from fit ratings, priorities, salary rows or Country blocks. A names-only list does not require completion or a valid producer checkpoint; disclose known unfinished/imported status without implying research succeeded.

If the source has no readable nonempty scope, offer the user's own list or the default without silently falling back to an older run. Unsafe paths, duplicate aliases and ambiguous metadata keep their existing clarification rules. Read no unrelated outputs to manufacture a list.

## Show and ask

Print every country in ordinary chat before the question. Name the source command and identify its search with a brief label/date or saved path when needed; never expose chat IDs. Long lists can use continent groups where available or short lines in source order. Never truncate the list, hide it solely in a file/tool payload or put every country into a separate choice.

Introduce the displayed list with: "Your last [command] search used:". After the full list, ask: "Reuse this country list?" Offer **Reuse this list / Choose other countries / Use the default list**, allowing a replacement list or explicit edits through normal custom input. Do not repeat a long list inside the question panel. Use the QM equivalents when the host cannot represent all three choices.

Reuse confirms the displayed names only. Explicit replacements or edits define the new exact scope; do not ask again for an already clear selection. Choosing other countries asks: "Which countries should we research? List countries/regions, or choose the default list." With no previous list, use that same question. An explicit no-preference answer leads to the default offer; silence, Skip or an unanswered question is not consent to reuse or defaults.

For a default request, read data/default-preferred-countries.md and print its complete list grouped by continent in ordinary chat before asking: "Use this default country list?" Offer **Use this list / Edit this list / Choose other countries**. Wait for the answer; requesting an unseen default does not confirm its individual countries. Clear edits need no duplicate approval. An empty list needs revised countries or stop before research. Add no separate exclusion questionnaire or automatic additional-country discovery.

## Retain the decision

CF saves custom/default/previous-list intent, the confirmed full scope and source provenance as prose in its existing criteria file, preserving Include/Exclude labels. Step 2 writes the country-only `## Research scope` in its candidates file before research. Legacy criteria with an unseen default or otherwise unresolved scope use this choice at Step 2; a previously confirmed list needs no repeat question.

SC writes the full country-only `## Research scope` in its research file before collection. Retain source command/run/path and the names-only confirmation in conversation until the step's existing Notes can carry it: embed that provenance literally in research briefs for researchers to echo, without editing returned country blocks. Add no metadata file or checkpoint field. Both commands leave the source's files/checkpoints untouched.

Names transfer no market fits, salary figures, visa conclusions or readiness. SC may use a selected CF source for presentation order only after the runtime's separate substantive-readiness checks; an SC source or unusable CF ordering uses alphabetical order. On later resumes, retain the chosen list/source rather than rebind to a newer search.
