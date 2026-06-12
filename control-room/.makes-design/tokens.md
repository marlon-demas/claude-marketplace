# Design Tokens — agent-system-guide
**Stack:** static-html · **Direction:** Control Room Live · **Authored:** 2026-06-11
Tokens are a projection of the built `index.html` `:root` block and component CSS.
Do not edit values here without updating `tokens.json` to match.

---

## Color

### Deep-space surface scale (6 tokens)

Base: `#0B0E15`. Steps lighten the blue-black hue by ~3–4 pts HSL per level.
Used strictly as surface/background layers — never as text.

| Token name | Hex | Role |
|---|---|---|
| `color.bg` | `#0B0E15` | Page background — deepest surface |
| `color.bg-2` | `#0F131D` | Secondary background (simulator shell) |
| `color.surface` | `#141927` | Card / panel background |
| `color.surface-2` | `#1A2032` | Elevated surface (dialogs, rail dots) |
| `color.line` | `rgba(148,170,220,0.13)` | Hairline rule, card borders |
| `color.line-2` | `rgba(148,170,220,0.22)` | Stronger border on hover / focus context |

### Text scale (3 shades)

| Token name | Hex | Contrast on `--bg` | Contrast on `--surface` | Role |
|---|---|---|---|---|
| `color.text` | `#E8EDF8` | 14.1:1 | 12.9:1 | Body text, headings |
| `color.text-dim` | `#8B96B0` | 5.5:1 | 5.0:1 | Secondary text, labels, descriptors |
| `color.text-faint` | `#5A6480` | 2.9:1 | 2.6:1 | DECORATIVE/LABELS only (see rule below) |

**`--text-faint` decorative-only rule:** `#5A6480` achieves 2.9:1 on `--bg` and 2.6:1 on `--surface` — both below WCAG 2.1 AA 4.5:1 for body text. The token is intentionally reserved for purely decorative chrome that is not independently read by assistive technology: `aria-hidden` feed labels, `aria-hidden` pipe separators, `aria-hidden` titlebar chrome, `aria-hidden` divider text, `::placeholder` text (which is non-normative under WCAG 2.1 SC 1.4.3), and the `sim-input` placeholder. It must NOT be used for any informational content.

**AA contrast fix history (2026-06-11 post-verify):** verify pass identified six informational selectors incorrectly using `--text-faint`. All six were promoted to `--text-dim` (#8B96B0, 5.5:1 on `--bg`, 5.0:1 on `--surface`, AA at all sizes and weights used):

| Selector fixed | Was | Now | Notes |
|---|---|---|---|
| `.hero-map-static-caption` | `--text-faint` | `--text-dim` | Shown only under reduced-motion; informational explanation |
| `.group-head .count` | `--text-faint` | `--text-dim` | Group agent counts ("14 agents") — informational |
| `.sp-label` | `--text-faint` | `--text-dim` | "Scenarios" group label, used as `aria-labelledby` |
| `.trace-empty` | `--text-faint` | `--text-dim` | Placeholder routing instruction (15px, not aria-hidden) |
| `.dlg-sec h4` | `--text-faint` | `--text-dim` | Dialog section labels ("Owns", "When it fires", "Real example") |
| `footer` | `--text-faint` | `--text-dim` | Footer identity text including "27 AGENTS" count |

The `--text-faint` usages that remain in the built file are all confirmed `aria-hidden` or non-normative: `.feed-label` (aria-hidden parent), `.fl-req` (aria-hidden parent), `.pipe` separators (aria-hidden / decorative), `.sim-titlebar` text (aria-hidden), `.sim-divider` (aria-hidden), `.rail-stop span` (aria-hidden rail), `.tr-label` (aria-hidden rail), `sim-input::placeholder`.

### Pulse / brand accent (2 tokens)

| Token name | Hex | Role |
|---|---|---|
| `color.pulse` | `#6CA8FF` | Primary brand accent — eyebrows, rail progress, focus rings, dispatch arrows |
| `color.pulse-bright` | `#A7CBFF` | Elevated pulse (dispatch line text, hover highlights) |

The pulse blue is the only brand-decorative accent. It is NOT a tier hue (sonnet coincidentally shares the same hex, but `--pulse` and `--sonnet` are separate tokens with separate roles — see tier hues below).

### Model tier hues (4 tokens — data encoding only)

These colors exist to encode the four model tiers as a visual data channel. They are never used decoratively, as background fills, or as general accent color. Their only roles are: SVG radial map ring-dot color, `.tier-pill` foreground + background tint, `.agent-card::after` hover bar, and `.agent-card` `--tier-color` CSS custom property for glow.

| Token name | Hex | Tier | Contrast on `--surface` |
|---|---|---|---|
| `color.tier.haiku` | `#4ADE9C` | haiku | ~8.1:1 |
| `color.tier.sonnet` | `#6CA8FF` | sonnet | ~8.7:1 |
| `color.tier.opus` | `#C08BFF` | opus | ~6.0:1 |
| `color.tier.fable` | `#FFB35C` | fable | ~6.5:1 |

Tier pill rendering: foreground = tier hue; background = `color-mix(in srgb, var(--tier-color) 14%, transparent)` on `--surface`; border = `color-mix(in srgb, var(--tier-color) 30%, transparent)`. All four tiers meet 4.5:1 AA on dark surface.

### Status (1 token)

| Token name | Hex | Role |
|---|---|---|
| `color.danger` | `#FF7A6C` | Sentinel special-note border/bg tint, live-dot in feed label (aria-hidden) |

This is a distinct semantic token — not a tier hue. Used exclusively for the sentinel/security aside and the decorative feed live-dot.

---

## Typography

### Typefaces

Two variable-axis fonts, fully base64-inlined as woff2 (Latin subsets only — unicode-range `U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD`). Zero external font requests.

| Token name | Family | Style | Weight axis | Use |
|---|---|---|---|---|
| `font.display` | Schibsted Grotesk | normal | 400–900 variable | All body text, headings, buttons |
| `font.mono` | JetBrains Mono | normal | 400–500 variable | Dispatch lines, tier pills, eyebrows, labels, simulator |

Stack fallbacks: `'Schibsted Grotesk', system-ui, -apple-system, sans-serif` / `'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace`.

`font-display: swap` on both `@font-face` declarations.

### Type scale

| Context | Font | Size | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|---|
| H1 hero | display | clamp(44px, 4.6vw, 68px) | 800 | 1.02 | -0.03em |
| H2 section | display | clamp(32px, 3.2vw, 46px) | 700 | 1.1 | -0.025em |
| H3 stage / group | display | 20–22px | 700 | — | -0.01em |
| Body base | display | 17px | 400 | 1.6 | — |
| Body large | display | 18px | 400 | — | — |
| Body small | display | 14–15px | 400–500 | — | — |
| Mono eyebrow | mono | 12px | 400 | — | 0.18em uppercase |
| Mono brand | mono | 13px | 400 | — | 0.14em uppercase |
| Mono dispatch | mono | clamp(16px, 1.8vw, 22px) | 400 | — | — |
| Mono feed | mono | 13px | 400 | — | — |
| Tier pill | mono | 11px | 400 | — | 0.08em |
| Dialog H3 name | display | 26px | 800 | — | -0.02em |
| Dialog H4 (post-fix) | mono | 11px | 400 (was text-faint; now text-dim) | — | 0.16em uppercase |
| Simulator label | mono | 11–12px | 400 | — | 0.12–0.16em uppercase |
| Footer | mono | 12.5px | 400 | — | 0.08em |

---

## Spacing

No named spacing scale token; spacing is defined in component CSS using these values:

| Usage | Value |
|---|---|
| Section horizontal padding (desktop) | 48px |
| Section vertical padding (desktop) | 110px |
| Hero top nav padding | 28px 48px |
| Card padding | 20px |
| Stage padding | 30px 28px |
| Dialog padding | 28px 30px / 22px 30px 30px |
| Simulator left/right padding | 28px / 28px 32px |
| Footer padding | 60px 48px |
| Gap between agent cards | 14px |
| Gap between stages | 20px |

Responsive breakpoints: `max-width: 980px` (tablet — collapse two-column hero, single-column stages/sim), `max-width: 480px` (small tablet/large phone), `max-width: 375px` (small phone).

---

## Radii

| Context | Value |
|---|---|
| Agent card | 12px |
| Stage card | 14px |
| Dialog | 16px |
| Simulator shell | 18px |
| Button (primary/ghost) | 8px |
| Tier pill | 99px (full-round) |
| Dispatch code block | 9–10px |
| Sentinel aside | 14px |
| Rail dot | 50% (circle) |

---

## Shadows

| Context | Value |
|---|---|
| Agent card hover | `0 14px 34px rgba(0,0,0,0.45), 0 0 20px color-mix(in srgb, var(--tier-color) 12%, transparent)` |
| Stage hover | `0 12px 40px rgba(0,0,0,0.4), 0 0 24px rgba(108,168,255,0.08)` |
| Dialog | `0 32px 90px rgba(0,0,0,0.7)` |
| Rail stop lit | `0 0 18px rgba(108,168,255,0.7)` |
| Focus ring | `0 0 0 2px var(--bg), 0 0 0 4px var(--pulse)` |
| Button primary hover | `0 4px 28px rgba(108,168,255,0.45)` |
| Dispatch line shown | `0 0 32px rgba(108,168,255,0.15)` |
| Pulse glow (hero H1 accent) | `text-shadow: 0 0 36px rgba(108,168,255,0.45)` |

---

## Motion tokens

### Ambient feed
| Property | Value |
|---|---|
| Base interval | 2200ms |
| Jitter | +rand(0–800ms) = 2200–3000ms per step |
| Feed line animation | `feedIn 500ms cubic-bezier(0.2,0.6,0.2,1)` — opacity 0→1 + translateY 14px→0 |
| document.hidden pause | `visibilitychange` listener sets `docHidden` flag; `ambientStep()` returns early and reschedules without updating DOM |
| Brand dot breathe | `breathe` keyframe (opacity 1→0.35→1) — started by JS to respect reduced-motion + document.hidden |

### Dialog
| Property | Value |
|---|---|
| `dialogIn` duration | 320ms |
| `dialogIn` easing | `cubic-bezier(0.2,0.9,0.3,1.2)` (slight overshoot settle) |
| `dialogIn` from | `opacity: 0; transform: translateY(24px) scale(0.96)` |
| `dialogIn` to | `opacity: 1; transform: none` |
| Reduced-motion | `animation: none` — no blank state, dialog appears instantly |

### Section reveal
| Property | Value |
|---|---|
| `.reveal` | `opacity 700ms cubic-bezier(0.2,0.6,0.2,1), transform 700ms` — translateY 28px→0 |
| `.reveal-stagger > *` | `opacity 600ms cubic-bezier(0.2,0.6,0.2,1), transform 600ms` — translateY 22px→0 |
| Stagger children | nth-child(2): 120ms delay · nth-child(3): 240ms · nth-child(4): 360ms |

### Simulator trace
| Property | Value |
|---|---|
| Trace row reveal | `opacity 450ms cubic-bezier(0.2,0.6,0.2,1), translateX -18px→0` |
| Rail progress | `width 600ms cubic-bezier(0.4,0,0.2,1)` |
| Rail dot light | `all 350ms cubic-bezier(0.2,0.9,0.3,1.3)` — scale 1→1.15 |
| Dispatch line appear | `all 500ms cubic-bezier(0.2,0.9,0.3,1.2)` — opacity + translateY 12px→0 |
| Gloss appear | `opacity 500ms 200ms delay` |
| No-match lesson | `feedIn 400ms` (same keyframe as feed, on `.shown` toggle) |

### General interactions
| Property | Value |
|---|---|
| Agent card hover | `border-color 220ms, transform 220ms, box-shadow 220ms` — translateY -4px |
| Stage hover | `border-color 250ms, transform 250ms, box-shadow 250ms` — translateY -4px |
| Preset button hover | `all 200ms cubic-bezier(0.2,0.6,0.2,1)` — translateX +4px |
| Nav link hover | `color 200ms` |
| Button transitions | `transform 180ms, box-shadow 180ms, background 180ms` |

### Reduced-motion policy
All ambient motion (breathe, feedIn, dialogIn, reveal/reveal-stagger, rail progress, trace row slide, dispatch line appear) is fully suppressed under `@media (prefers-reduced-motion: reduce)`. Designed static states are shown in place of blanks:
- Reveal classes: `opacity: 1 !important; transform: none !important; transition: none !important`
- Dialog: `animation: none` — appears immediately
- Hero map: `.hero-map-static-caption` shown (text: "27 agents — radial map (animation paused)")
- Feed: JS reads `reduceMotion` flag; CSS `.feed-line.animated` conditional suppressed; feed renders a static sample
- Trace rows: `opacity: 1 !important; transform: none !important; transition: none !important`
- Rail: `transition: none !important` on both `rail-progress` and `rail-dot`
