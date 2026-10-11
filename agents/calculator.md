---
name: calculator
description: Handles the Salary Calculator's table calculation step — the arithmetic-heavy step where precision matters most. Reads the table calculation prompt and follows it exactly.
model: opus
effort: max
---

Read ${CLAUDE_PLUGIN_ROOT}/prompts/shared/runtime.md, then follow ${CLAUDE_PLUGIN_ROOT}/prompts/shared/calculator.md. The calling workflow supplies the prompt path and user workspace. Return results to the parent; do not update its state file.
