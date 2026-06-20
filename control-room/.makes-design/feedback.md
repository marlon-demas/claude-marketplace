# Feedback Log — orchestrator-guide
## Surface: agent-system-guide · makes-design v1.2.2 · 2026-06-11

Entries feed future sessions as constraints. Tags: ACCEPTED / REJECTED / AESTHETIC / LUX / CORRECTION.

---

`ACCEPTED:` direction "Annotated Field Atlas" (warm-paper field guide, reader-as-playhead) chosen over "Phosphor Departures Board" (brutalist departure-board, carbon-dark, monospace) and "Midnight Control Room" (premium-dark operations floor, Stripe-grade). User voted with live disposable direction previews in `.makes-design/direction-previews/`. Previews-before-vote worked well — do this by default for direction gates.

`ACCEPTED:` all-tabbable agent cards (tabindex=0 ×27) chosen over roving tabindex (arrow-key-within-group navigation). Roving tabindex was half-implemented and unfixably fiddly for the value; the verify hard-fail `ROVING-TABINDEX-23` made the problem concrete. Honest simplicity — flat tab order across all 27 — resolved WCAG compliance with zero behavioural complexity.

`ACCEPTED:` visible "Route it" button + Enter both submit the simulator. The discover failure mode was typing-then-nothing: a user who presses Enter expects routing to fire. Adding a `keydown` Enter handler (Option A from the fix list) resolved finding `FREETEXT-ENTER-NO-SUBMIT`. Both Enter and visible button must submit; neither alone is sufficient.

`REJECTED:` org-chart flat grid for the 26-agent directory. A uniform tooltip grid teaches what agents exist, not how the system decides. The chosen pattern — domain groups + asymmetric cards + Dialog for depth — makes the routing logic explorable rather than enumerable. Anti-anchor lives in `direction.md`.

`REJECTED:` autoplay/looping animation anywhere. The reader is the playhead. Every animated sequence must be scrubable, steppable, or replayable on demand. No animation runs that the reader did not initiate. Anti-anchor lives in `direction.md`.

`REJECTED:` faux paper-grain texture to signal warmth/materiality. Warmth comes from palette (paper-100 `#F7F3EC`, ink-900 `#211E19`) and serif typefaces (Fraunces + Newsreader). Simulated material texture is the cheap version; the palette earns the register without it.

`AESTHETIC:` paper-light is the identity of this surface. Dark mode is N/A by direction — not a deferred item. The premium-professional brief and the field-guide register require the warm-paper ground. If a dark variant is ever requested, it is a separate brief, not a toggle.

`AESTHETIC:` italic reserved for `type.caption` (margin notes and true captions only). Body prose never italicizes. Verify finding `ITALIC-IN-PROSE` caught violations in the dispatch-step captions and one intro paragraph. Any italic outside a `<aside class="margin-note">` or explicit caption context is a token violation.

`AESTHETIC:` terracotta at most 10% of rendered pixels. Its roles are: annotation underlines, margin notes, the active dispatch path in the DispatchFlowWidget, focus rings. Slate (`#5B7B9A`) is exclusively for model-tier data (tier-badge foreground). Tier-badge foreground was darkened to `#3A5F7A` (from slate-500) to achieve 5.37:1 contrast on slate-100 — keep that exact value; do not revert to `#5B7B9A` without re-validating contrast.

`LUX:` committed lux properties: inevitability through restraint, time visible in detail, specificity over generality, quiet by default / voice when chosen. These are enforced structurally: one file, one column, widgets only where prose fails, no hero sections, no marketing framing. Not committing: material truth (no texture overlay), multi-sensory (no haptics/sound on web), patina-aware (roster changes too fast — the separable JS data structure is the maintenance answer). Full record in `lux-notes/agent-system-guide-2026-06-11.md`.

`LUX:` the simulator's no-match state is designed as the "orchestrator asks instead of guessing" lesson — a terracotta MarginNote with a clarifying question and the pedagogical explanation of why guessing is the failure mode. Keep it a lesson, not an error toast. Never replace the clarifying-question copy with a generic "no results" state.

`CORRECTION:` Google Fonts CDN `@font-face` is a ship-blocker on static-html profiles. Fonts must be base64-inlined woff2 (Latin subsets only). Variable fonts collapse 5 separate weight files to 3 variable-axis files — approximately 340 KB total for the Fraunces + Newsreader pair. Subagent sandboxes block outbound network; the main session must download font binaries before handing off. Enforce this at the brief level for every static-html surface: "fonts must be self-hosted, no CDN."

## 2026-06-11 — Redesign 2 (Control Room Live)

- **CORRECTION (constraint override):** The REJECTED entry "no autoplay/looping animation — the reader is the playhead" is SUPERSEDED by explicit user confirmation (2026-06-11, claude.ai/design redesign): ambient life is now part of the identity — the hero radial map idles with breathing pulses and a live dispatch feed on arrival. Bounds on the override: ambient motion is atmosphere, never instruction (lessons still fire only on user action); ALL ambient + choreographed motion fully suppressed under prefers-reduced-motion with designed static states. The other REJECTED entries (org-chart flat grid, faux textures) remain in force.
- **REJECTED:** Midnight Control Room (copper register) — approved on superdesign preview, built, verified PASS, rejected by user on viewing the real surface. Lesson: a static preview vote is weaker evidence than a built-surface viewing; quiet-premium read as flat against a showpiece intent.
- **AESTHETIC (supersedes paper-light entry):** the surface is now a showpiece — audience weighting shifted from "non-technical learners first" to "impress first, still teach". Plain-language glosses stay; the register may be loud.
- **MISSED (2026-06-11, post-step-11):** dialog opened top-right — `* { margin: 0 }` reset kills native <dialog> centering; verify never asserted dialog position. Fixed (`margin: auto; inset: 0`). Verify rubric should assert dialog[open] viewport centering. (missed/agent-system-guide-2026-06-11.md)

## 2026-06-11 — Contract close-out (Step 13 + 14)

`ACCEPTED:` Control Room Live direction arrived as a claude.ai/design handoff bundle (gzip tar: README + chat transcript + prototype HTML). Three explorations authored with real agent data baked in; user voted Exploration A. Implementing FROM the prototype file and porting our quality bar (a11y, reduced-motion, AT strategy, base64 fonts) proved faster and truer to intent than restyling our own file. The prototype carried real routing logic and real dispatch lines; the quality bar carried structural correctness. Each contributed what the other could not.

`ACCEPTED:` dialog centering fix `margin: auto; inset: 0` on `dialog.agent-dialog`. Root cause: the global `* { margin: 0 }` reset silently kills the browser's default `margin: auto` for native `<dialog>` centering. The fix must be explicit and load-bearing — removing it reverts to top-right positioning. Any project using a global margin reset with native `<dialog>` must apply this fix.

`AESTHETIC:` tier hues (haiku #4ADE9C / sonnet #6CA8FF / opus #C08BFF / fable #FFB35C) are semantic data-encoding tokens — never decorative. They communicate the model tier of each agent as a visual data channel: SVG ring dots, tier pills, card hover bars. Pulse blue (#6CA8FF) is the single brand accent. The fact that sonnet shares a hex with pulse is a coincidence of the palette; the tokens are distinct (`--pulse` vs `--sonnet`) and their roles must never be conflated.

`LUX:` "quiet by default" formally retired for the Control Room Live surface (showpiece override, 2026-06-11). The Annotated Field Atlas field-guide register required silence; the operations-floor register requires ambient life to establish "this is real infrastructure." The surviving constraint is narrower: ambient is atmosphere, never instruction. Lessons (no-match, sentinel pin) still fire only on user action. The override does not bleed into the pedagogical layer. Full record in lux-notes/agent-system-guide-live-2026-06-11.md.

`CORRECTION:` design handoff bundles from claude.ai/design arrive as gzip tar archives containing a README, a chat transcript, and one or more HTML prototypes. The chat transcript carries intent (including constraint overrides that must be surfaced to the user — in this case the ambient-autoplay override) and the prototypes may include a HUB/index page rather than the design itself. Protocol: (1) unpack and inventory all files before assuming which is the working prototype; (2) read the chat transcript for stated intent and any constraint overrides; (3) confirm direction with the user before implementing; (4) record any constraint overrides in direction.md and feedback.md.

## 2026-06-12 — dashboard surface (design-review pass, score 59/100 pre-fix)
- CORRECTION: derived surfaces inherit the AA fix history, not just the palette. The dashboard
  re-introduced `--text-faint` on six informational selectors (aside h2, footer, idle label,
  model names, now-line) that tokens.md had already documented as fixed. Rule: `--text-faint`
  is for decorative/aria-hidden text ONLY; informational text floors at `--text-dim`.
- CORRECTION: never style via inline element opacity (nowLabel 0.55) — it stacks invisibly on
  color contrast and can't be overridden by media queries. Use a CSS class.
- INSIGHT: live activity lines need a two-tier treatment — static label at --text-dim, live
  verb at --pulse-bright with ellipsis overflow — or they're either noisy or invisible.

## 2026-06-12 — dashboard v0.2: Ops Ledger adopted (claude.ai/design handoff)
- ACCEPTED: direction "A · Ops Ledger" replaces the radial map for the LIVE surface — work
  first (running session cards with log tails), dense dispatch ledger, fleet as a quiet
  right rail that lights with the agent's current tool call. User verdict from the design
  chats: the radial map "wastes space / is gimmicky" for a live view; active work was
  "buried in a sidebar". The radial map remains correct for the GUIDE (educational surface).
- AESTHETIC: Midnight Control Room palette carries over unchanged; hierarchy now comes from
  size/weight/placement, not color dimming.
- CORRECTION (applied on adoption): the static design repeated --text-faint on informational
  text (hstat labels, seclabels, meta, group headers, fleet domains) — all floored to
  --text-dim per the standing AA rule. Mock-only data columns (cost) ship hidden by default;
  tokens proved real (hook tool_response carries usage — extracted defensively).

## 2026-06-12 — Specno re-skin (v0.2.1)
- ACCEPTED: dark-Specno full-screen treatment (matches the Specno guide's hero) over a
  light dashboard — ops monitors read dark; brand approves dark blue for these surfaces.
- AESTHETIC: tier hues re-encoded on the Specno secondary palette (haiku→green #a0d468,
  sonnet→blue #489dda, opus→purple #ac92ec, fable→orange #fc6e51, danger→red #ed5565);
  LOG_KIND glyph colors follow the same mapping so tool glyphs stay tier-coherent.
- INSIGHT: re-skin executed as a count-asserted splice (style block swap + exact-string JS
  patches) — markup/data/behavior untouched by construction. Same method as the guide.

## 2026-06-12 — Light theme toggle (v0.2.2)
- ACCEPTED: user wanted a light option after seeing dark-only; shipped as a tweaks-panel
  toggle (dark default) rather than prefers-color-scheme — explicit control fits the
  existing tweaks framework and ops monitors usually stay pinned.
- INSIGHT: theming inline JS colors — the two literal-color sites (tierpill cssText,
  log-glyph style.color) were converted to custom props (--tier / --glyph) so CSS owns
  the theme-aware derivation; a single --tier-mix percentage var themes every
  tier-as-text site without duplicating rules.

## 2026-06-21 — Constellation Control Room (v0.3.0)
`AESTHETIC:` direction "Constellation Control Room" (Option A) locked. Fleet rail DOM list replaced with a live radial constellation canvas (orchestrator fixed at center, agents on domain-group arcs, idle nodes ~35% opacity, dispatched nodes scale + glow ring + pulse); SVG dispatch-arc layer draws center → target on each pre-dispatch event, fades ~1200ms post-dispatch. Hard constraint: the live data path (hooks/emit.py, hooks/hooks.json, server/serve.mjs, EventSource('/events')) must remain untouched — the dashboard is localhost-only and the canvas is purely a rendering layer over the same SSE event stream. Dead --fable token and all fable references removed (ADR-0002 compliance). Specno 4-square stroke-dashoffset loader replaces "connecting…" text as the SSE-connect state in the constellation panel.
