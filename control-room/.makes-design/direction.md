# Direction — 2026-06-11

**Chosen:** Control Room Live
chosenDirection: Control Room Live
**Authored from brief:** A living dispatch-room map of the Makes agent system — requests visibly travel from intent to the right specialist, and the viewer can fire a dispatch themselves instead of reading an org chart.
**Motion budget:** signature
**Brief texture:** premium-professional

## Chosen: Control Room Live

**Signature:** A deep-space operations floor that is already alive when you arrive — dispatches pulse across a live radial map of all 27 agents, and routing a request sends your own pulse through the real network.
**Style pack anchor:** high-end-agency
**Palette anchor:** deep space #0B0E15 · surface #141927 · signal text #E8EDF8 · pulse blue #6CA8FF · tier hues #4ADE9C / #6CA8FF / #C08BFF / #FFB35C
**Type anchor:** Schibsted Grotesk (display) + JetBrains Mono (data/dispatch)
**Motion posture:** Ambient life, deliberately — the hero radial map idles with breathing pulses and a live dispatch feed on arrival (explicit user override of the former no-autoplay rule, 2026-06-11). Scroll-driven section reveals; the simulator fires a visible pulse across the radial map on every routed request; dialogs rise with scale-settle. All ambient and choreographed motion is fully suppressed under prefers-reduced-motion (designed static states, not blanks). Tier hues are data encoding, not decoration.
**References:**
- claude.ai/design handoff bundle (2026-06-11, project "Interactive Redesign", Exploration A "Control Room.html") — the authored prototype, user-voted vs B/C
- Anthropic — "Building Effective Agents": capability-ladder diagrams where the complexity gradient is the argument
- Distill.pub — hover lights up the node's neighbourhood; explanation and experiment collapse into one surface
**Anti-anchor:**
- The org-chart grid — flat tooltip grid teaches what exists, not how it decides
- Static swimlane flow diagram with callout boxes — happy-path theatre

## Rejected: Midnight Control Room

**Signature:** A dark, Stripe-grade operations floor where your request travels as a pulse of light along the routing paths, and each specialist's station glows awake when the dispatch arrives.
**Style pack anchor:** premium-editorial
**Palette anchor:** midnight #11141B · warm fog #E8E4DC · copper #D08C4A · panel #2A2F3A
**Type anchor:** Satoshi (display) + Geist (body) + JetBrains Mono (dispatch lines)
**Motion posture:** Choreographed light — the request travels as an eased pulse along SVG route paths (400–500ms legs), agent stations illuminate on arrival, model-tier badges settle with a soft landing. Sequences are orchestrated but fully controllable: play, pause, scrub, replay per scenario. Glow is reserved exclusively for the active route.
**References:**
- Anthropic — "Building Effective Agents": capability-ladder diagrams where the complexity gradient is the argument
- Josh Comeau — "Making Sense of React Server Components": toggling between strategies makes the delta felt, not described
- Tailscale — "How Tailscale Works": each diagram removes one constraint from the last
**Anti-anchor:**
- Static swimlane flow diagram with callout boxes — happy-path theatre that hides the decision logic

*(Built and verified PASS 2026-06-11; rejected by user on viewing the real surface — register read too quiet for the showpiece intent. Superseded by Control Room Live.)*

## Rejected: Annotated Field Atlas

**Signature:** A warm-paper interactive field guide where the agent system is explained the way Ciechanowski explains gears — every concept is a widget you manipulate, and the prose feels hand-annotated rather than marketed.
**Style pack anchor:** minimalist
**Palette anchor:** paper #F7F3EC · ink #211E19 · terracotta #C2603D · slate blue #5B7B9A
**Type anchor:** Fraunces (display) + Newsreader (body)
**Motion posture:** Reader-driven, never performative — the dispatch flow scrubs with scroll or drag, widgets answer manipulation instantly (200–250ms transforms), agent cards lift gently on focus. The signature budget is spent on responsiveness depth (everything touchable responds) rather than choreography. The reader is the playhead: no animation runs that the reader didn't initiate, and every animated sequence can be scrubbed, stepped, or replayed. Annotation marks (terracotta underlines, margin notes) settle in as the reader reaches them.
**References:**
- Bartosz Ciechanowski — interactive physics essays: zero passive content; every concept lives inside a manipulable widget
- Josh Comeau — "An Interactive Guide to Flexbox": concrete spatial metaphor precedes every explanation; the widget teaches the mental model
- Distill.pub — "A Gentle Introduction to Graph Neural Networks": hovering a node lights up its neighbourhood; explanation and experiment collapse into one surface
**Anti-anchor:**
- The org-chart grid — 26 agents in a flat tooltip grid teaches what exists, not how it decides
- Auto-play looping animation the viewer cannot pause, step, or replay

---

## Audit trail
- 2026-06-11 · direction authored, three candidates with live previews · user voted Annotated Field Atlas
- 2026-06-11 · shipped + verified PASS under Annotated Field Atlas
- 2026-06-11 · REDESIGN 1: superdesign comparison · user voted Midnight Control Room · built + verified PASS
- 2026-06-11 · user rejected Midnight Control Room on viewing · claude.ai/design exploration commissioned (3 directions, real data)
- 2026-06-11 · REDESIGN 2: user voted Exploration A "Control Room Live"; explicitly confirmed override of the no-autoplay REJECTED constraint (ambient hero, showpiece intent) · previous direction archived to direction-2026-06-11-midnight-copper.md
- 2026-06-12 · SPECNO RE-SKIN: user-pinned brand override (specno-brand-guidelines). Direction concept unchanged (Control Room Live — operations floor, ambient life, tier hues as data encoding); palette + type anchors re-projected: floor #0a122e (Specno Dark Blue) · surface #111b3e · pulse #489dda / #7dc7fa · tier hues #a0d468 / #489dda / #ac92ec / #fc6e51 · danger #ed5565 · Nunito (headings) + Inter (body) + JetBrains Mono (data). Specno token projection lives in sos-toolkit/.makes-design/tokens.json; this contract's tokens.md/tokens.json remain the record of the original 2026-06-11 palette (still shipped in the Makes-branded guide).
