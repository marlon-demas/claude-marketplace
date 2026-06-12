---
name: control-room
description: Start, stop, or check the Control Room — the live agent-dispatch dashboard. Use whenever the user wants to watch agents running visually, says "open the control room", "start the agent dashboard", "show me the agents live", "watch the dispatches", or asks whether the dispatch viewer is running — even if they just say "put the agents on screen".
allowed-tools: [Bash, Read]
---

# Control Room

A localhost dashboard (port 4517) that renders agent dispatches live: a radial map of the
roster where dispatched agents pulse and glow, a Running Now panel with elapsed timers, and a
real dispatch feed. Events come from this plugin's observer hooks via
`~/.claude/control-room/events.jsonl`.

## Start

```bash
node "$(dirname "$(find ~/.claude/plugins/marketplaces/marlon-demas/control-room -name serve.mjs)")/serve.mjs" > /tmp/control-room.log 2>&1 &
sleep 1 && open http://127.0.0.1:4517/
```

If port 4517 is already serving, just `open http://127.0.0.1:4517/` — the server is a
singleton per machine; a second start fails to bind, which is fine.

## Stop

```bash
kill "$(cat ~/.claude/control-room/server.pid)" 2>/dev/null && echo stopped
```

(Or `lsof -ti :4517 | xargs kill` if the pidfile is stale.)

## Status

```bash
lsof -ti :4517 >/dev/null && echo "server: up — http://127.0.0.1:4517/" || echo "server: down"
wc -l < ~/.claude/control-room/events.jsonl 2>/dev/null | xargs -I{} echo "{} events captured"
tail -3 ~/.claude/control-room/events.jsonl 2>/dev/null
```

## Notes for the assistant

- The hooks capture events whether or not the server runs; starting the server later replays
  the last 200 events. So "nothing happened yet" usually means no agents were dispatched, not
  a broken pipeline — check Status before debugging.
- Events contain agent names, models, and 140-char task excerpts only (no prompt bodies, no
  file contents). The server binds 127.0.0.1 — never expose it on another interface.
- If the dashboard shows a stale "running" row, the session likely ended without a Stop event
  reaching the log; it clears on the next Stop or page reload.
