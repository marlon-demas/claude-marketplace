# control-room — live agent-dispatch dashboard

Watch agents work instead of reading a terminal. A localhost page in the **Control Room
Live** aesthetic (same design contract as the orchestrator-guide): a radial map of the
roster where dispatched agents pulse with their model-tier color and glow while running, a
**Running Now** panel with live elapsed timers, and a real **dispatch feed**
(`→ agent | model | task — 47s ✓`) with per-session color badges.

```
Claude Code hooks (observer, fail-open)
        ↓ one JSON line per event
~/.claude/control-room/events.jsonl
        ↓ SSE (replay last 200, then tail)
serve.mjs (zero-dep Node, 127.0.0.1:4517)
        ↓
dashboard.html (single file, fonts inlined)
```

## Use

`/control-room:control-room` — start / stop / status. Or by hand:
`node server/serve.mjs` then open http://127.0.0.1:4517/.

The hooks capture events whether or not the server is running — start the dashboard any
time and it replays recent history before going live.

## What gets captured (and what doesn't)

Per dispatch: timestamp, event type, 8-char session id, cwd **basename**, tool_use_id,
agent name, model, and the first **140 characters** of the task description. User prompts
log a **word count only**. No prompt bodies, no file contents, no tool output. The server
binds `127.0.0.1` explicitly.

## Guarantees

- **Fail-open observer** (dispatch-guard doctrine): `emit.py` exits 0 on any error — a
  broken observer must never block or slow a session. Hook timeout 5 s.
- Unknown agents (Explore, Plan, plugin agents) render on an inner "visitors" arc — the
  dashboard never breaks on an id outside the roster.
- A `pre` with no `post` (blocked by dispatch-guard, denied, or crashed) shows as
  "ended — no completion" when its session stops.
- Log rotates at 5 MB (`events.jsonl` → `events.jsonl.1`).

## Porting note (sos-toolkit)

Shipping this to the team marketplace needs an AI-Committee call: the CONTRIBUTING
"no global directives" rule covers session-wide hooks, and while this one is a read-only
observer (changes nothing, injects nothing), observer hooks are a new category the rule
doesn't yet name. Until then it stays personal.
