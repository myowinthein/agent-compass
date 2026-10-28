---
name: country-finder
description: Runs the full Country Finder pipeline — criteria intake, grounded country discovery, per-country research, scoring, and a final priority ranking.
---

Read and apply [shared runtime instructions](../../prompts/shared/runtime.md), then follow the [Country Finder workflow](../../workflows/country-finder.md).

Resolve these links relative to this SKILL.md's actual file location, not the user's workspace. Pass any invocation arguments to the workflow.

Claude-only session hint: `${CLAUDE_SESSION_ID}`. Use it under skills/run-workspaces.md only when the host is Claude and the value was actually substituted; other hosts and literal placeholders use that rule's host-ID or tool-generated fallback.
