# Verify — dashboard.html Specno re-skin (v0.2.1, 2026-06-12)

Served the marketplace copy via `CONTROL_ROOM_PORT=4980 node server/serve.mjs` with the
real `~/.claude/control-room/events.jsonl` replayed (200-line SSE replay) — populated
ledger, fleet rail, live header stats. Playwright at 1440×900.

## Verdict: PASS

- Title "Specno Control Room — Live"; brand = white Specno logo (20px minimum) + "· Control Room"
- Background `#0a122e` (Specno Dark Blue); cards `#111b3e` royal-tinted surfaces
- Fonts: Inter (body/ledger) + JetBrains Mono (data) loaded; Nunito loads on demand for
  running-card agent names (`document.fonts.load('700 16.5px Nunito')` → loaded; verified
  visually with an injected sample card — Atlas / fable / orange tier accents)
- Tier palette: Specno secondaries throughout (ledger dots, card borders, pills, fleet
  active rows, LOG_KIND glyphs) — single mapping, count-asserted in the splice
- SSE live indicator on; 13 dispatches / 887k tokens / 6 sessions rendered from real events
- Console: 0 errors
- prefers-reduced-motion block and all keyframes carried over verbatim

Screenshots (kept out of the shipped plugin): `~/.claude/control-room/verify-screenshots/`
Side effects cleaned: verify server stopped; `server.pid` restored to the live 4517 server's pid.
Build script: `/tmp/specno-guide/splice-dashboard.py` + `specno-dashboard.css`.

## Addendum — v0.2.2 light toggle (same day)

Verified against the LIVE 4517 server (file re-read per request; 6 agents running).
Tweaks → Theme → light: bg #ffffff, logo #489dda (Specno Blue variant), tierpill text
color-mix result ≈ #406e93 (AA on white), running cards / ledger / fleet / log glyphs all
readable. Toggle back to dark: byte-identical to v0.2.1 rendering (bg #0a122e, white logo).
Console 0 errors both ways. Theme persists via the existing crl-tweaks localStorage.
Screenshot: ~/.claude/control-room/verify-screenshots/specno-dash-light.png
