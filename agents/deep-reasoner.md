---
name: deep-reasoner
description: Handles judgment-heavy synthesis steps in claude-compass pipelines — international salary adjustment estimation, country scoring, final ranking, and final verification. Reads the specified prompt file and follows it exactly.
model: opus
effort: high
---

Read ${CLAUDE_PLUGIN_ROOT}/prompts/shared/runtime.md, then follow ${CLAUDE_PLUGIN_ROOT}/prompts/shared/deep-reasoner.md. The calling workflow supplies the prompt path and user workspace. Return results to the parent; do not update its state file.
