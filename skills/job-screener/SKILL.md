---
name: job-screener
description: Screens job descriptions against your resume profile and outputs a structured match report. Paste one JD at a time; re-invoke if the session drifts.
---

Read and apply [shared runtime instructions](../../prompts/shared/runtime.md), then follow the [Job Screener workflow](../../workflows/job-screener.md).

Resolve these links relative to this SKILL.md's actual file location, not the user's workspace. Pass any invocation arguments to the workflow.

Claude-only session hint: `${CLAUDE_SESSION_ID}`. Use it under skills/run-workspaces.md only when the host is Claude and the value was actually substituted; other hosts and literal placeholders use that rule's host-ID or tool-generated fallback.
