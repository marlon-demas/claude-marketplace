---
name: dispatch-guard:status
description: "Show recent dispatch-guard decisions from ~/.claude/dispatch-guard.log. Tails the last 50 lines and prints a summary of PASS / BLOCK / WARN counts."
allowed-tools: [Bash, Read]
---

# /dispatch-guard:status

Show the most recent dispatch-guard decisions and a quick tally.

## Steps

1. Check whether `~/.claude/dispatch-guard.log` exists:
   - If missing: tell the user the log doesn't exist yet (no dispatches have been evaluated since the plugin was installed) and stop.

2. Tail the last 50 lines of the log and display them verbatim.

3. Count PASS, BLOCK, and WARN occurrences across the full log:
   ```bash
   grep -c " PASS " ~/.claude/dispatch-guard.log 2>/dev/null || echo 0
   grep -c " BLOCK " ~/.claude/dispatch-guard.log 2>/dev/null || echo 0
   grep -c " WARN " ~/.claude/dispatch-guard.log 2>/dev/null || echo 0
   ```

4. Print a one-line summary: `Total: N lines | PASS: X | BLOCK: Y | WARN: Z`

Do not modify the log. Read-only command.
