---
name: dispatch-guard:audit
description: "Audit dispatch-guard.log: group BLOCK lines by failure mode, count occurrences, and propose memory entries or router.md updates for recurring patterns."
allowed-tools: [Bash, Read]
---

# /dispatch-guard:audit

Analyse all BLOCK and WARN lines in `~/.claude/dispatch-guard.log`, group by
failure mode, and surface actionable recommendations.

## Steps

1. Verify the log exists. If missing, tell the user and stop.

2. Extract all BLOCK lines from the full log:
   ```bash
   grep " BLOCK " ~/.claude/dispatch-guard.log
   ```

3. Group by failure mode by parsing the `reason=` field. The four failure modes are:
   - **missing-model** — `"model field is missing or empty"`
   - **invalid-model** — `"invalid model"` (includes `best` alias trap, `gpt-4`, etc.)
   - **sentinel-fable** — `"sentinel+fable is unconditionally blocked"`
   - **opus-floor** — `"opus-floor agent"` (agent dispatched below floor)

4. For each mode with 1+ occurrences, print:
   - Count and which subagent_type values appeared
   - The specific model values that triggered the block

5. Propose concrete corrective actions:
   - **missing-model** (>2 occurrences): suggest adding a memory entry reminding the
     orchestrator that `model:` is MUST-PASS on every Agent() call.
   - **invalid-model** (`best` appearing): suggest confirming `best` is removed from
     all per-dispatch sites (valid only in settings.json/frontmatter).
   - **invalid-model** (other values): identify the agent that dispatched the bad value.
   - **sentinel-fable** (any): remind that Sentinel is permanently `opus`; check if
     router.md Fable triggers were too broad.
   - **opus-floor** (>3 occurrences for the same subagent_type): propose adding a
     note to the orchestrator's dispatch checklist for that agent.

6. Extract WARN lines and list them separately. WARN = the guard encountered a
   parse error or empty stdin — these indicate a malformed dispatch call upstream.

7. End with: "Audit complete. No log modifications made."

Do not modify the log. Read-only command.
