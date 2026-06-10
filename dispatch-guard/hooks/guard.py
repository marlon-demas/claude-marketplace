#!/usr/bin/env python3
"""
dispatch-guard v0.2.0 — PreToolUse hook for the Agent/Task tool.

Validates four invariants before every subagent dispatch:
  (a) model field present and non-empty
  (b) model is one of: haiku, sonnet, opus, fable
  (c) hard-floor agents (atlas, sentinel, orchestrator) must be at opus or fable;
      soft-floor agents (cipher, scout, oracle) must be at sonnet or above —
      sonnet is allowed with an advisory warning, haiku is always blocked
      (unless DISPATCH_GUARD_ALLOW_DOWNGRADE=1 for the hard-floor set)
  (d) sentinel + fable → always blocked (unconditional)

Router doctrine source: CLAUDE.md → Agent System → Opus-downgrade clause
  - Atlas, Sentinel: non-downgradable pins (no sonnet, no haiku)
  - Cipher, Scout, Oracle: downgradable to sonnet when task matches
    router.md Sonnet-OK conditions; haiku never allowed

Fail-open: any internal error allows the call through and writes a WARN line.
Log: ~/.claude/dispatch-guard.log (append-only, one line per dispatch).
"""

import json
import os
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_MODELS = {"haiku", "sonnet", "opus", "fable"}

# Agents that must be dispatched at opus or fable — sonnet/haiku are blocked.
# Atlas may legally run at fable (router: "Atlas any task" is a Fable trigger);
# fable >= opus floor, so it passes cleanly.
# DISPATCH_GUARD_ALLOW_DOWNGRADE=1 is the escape hatch for this set only.
HARD_OPUS_FLOOR: set[str] = {"atlas", "sentinel", "orchestrator"}

# Agents whose frontmatter pins opus but whose doctrine permits sonnet for
# specific task types (router.md Sonnet-OK conditions).
# Sonnet → allowed with an advisory warning.
# Haiku → always blocked (no doctrine ever warrants these agents at haiku).
SOFT_OPUS_FLOOR: set[str] = {"cipher", "scout", "oracle"}

LOG_PATH = os.path.expanduser("~/.claude/dispatch-guard.log")


# ---------------------------------------------------------------------------
# Logging helper
# ---------------------------------------------------------------------------

def append_log(decision: str, subagent_type: str, model: str, reason: str) -> None:
    """Append one line to the dispatch-guard log. Silently swallows I/O errors."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{ts} {decision} subagent_type={subagent_type!r} model={model!r} reason={reason!r}\n"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(line)
    except OSError:
        pass  # Never fail the session over a log write


# ---------------------------------------------------------------------------
# Decision helpers
# ---------------------------------------------------------------------------

def deny(subagent_type: str, model: str, reason: str) -> dict:
    append_log("BLOCK", subagent_type, model, reason)
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny"
        },
        "systemMessage": f"[dispatch-guard] BLOCK — {reason}"
    }


def allow(subagent_type: str, model: str, reason: str) -> dict:
    append_log("PASS", subagent_type, model, reason)
    return {}


def warn_allow(subagent_type: str, model: str, reason: str) -> dict:
    """Fail-open path: allow but surface a non-blocking message."""
    append_log("WARN", subagent_type, model, reason)
    return {"systemMessage": f"[dispatch-guard] WARN — {reason}"}


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

def validate(tool_input: dict) -> dict:
    """Run the four checks. Returns the output dict for Claude Code."""
    model = tool_input.get("model") or ""
    model = model.strip()
    subagent_type = (tool_input.get("subagent_type") or "").strip().lower()

    # (a) model must be present and non-empty
    if not model:
        return deny(subagent_type, model, "model field is missing or empty — every Agent dispatch must pass model: explicitly")

    # (b) model must be a valid per-dispatch value
    if model not in VALID_MODELS:
        return deny(subagent_type, model,
                    f"invalid model {model!r} — per-dispatch whitelist is haiku|sonnet|opus|fable "
                    f"(note: 'best' is rejected by the Agent tool enum; use 'fable' for the top tier)")

    # (d) sentinel + fable → unconditional block (checked before floor rules so the
    #     more specific rule fires first and the reason string is maximally clear)
    if subagent_type == "sentinel" and model == "fable":
        return deny(subagent_type, model,
                    "sentinel+fable is unconditionally blocked — the safety classifier "
                    "auto-falls-back to Opus 4.8 for ~5% of sentinel sessions; paying 2× "
                    "Fable rate to usually get Opus is pure waste. Use model: 'opus' for sentinel.")

    # (c-hard) hard-floor agents must be at opus or fable
    if subagent_type in HARD_OPUS_FLOOR and model in {"haiku", "sonnet"}:
        allow_downgrade = os.environ.get("DISPATCH_GUARD_ALLOW_DOWNGRADE", "") == "1"
        if allow_downgrade:
            return warn_allow(subagent_type, model,
                              f"downgrade allowed via DISPATCH_GUARD_ALLOW_DOWNGRADE=1 "
                              f"(hard-floor agent {subagent_type!r} dispatched at {model!r})")
        return deny(subagent_type, model,
                    f"hard-floor agent {subagent_type!r} cannot be dispatched at {model!r} "
                    f"(floor is opus). Set DISPATCH_GUARD_ALLOW_DOWNGRADE=1 to override.")

    # (c-soft) soft-floor agents: haiku always blocked; sonnet allowed with advisory
    if subagent_type in SOFT_OPUS_FLOOR:
        if model == "haiku":
            return deny(subagent_type, model,
                        f"soft-floor agent {subagent_type!r} cannot be dispatched at haiku "
                        f"(minimum is sonnet; opus is the default — downgrade to sonnet only "
                        f"when the task matches a router.md Sonnet-OK condition)")
        if model == "sonnet":
            return warn_allow(subagent_type, model,
                              f"soft-floor agent {subagent_type!r} dispatched at sonnet — "
                              f"advisory: this is doctrine-legal only when the task matches a "
                              f"router.md Sonnet-OK condition (e.g. Cipher: CRUD spec; "
                              f"Scout: simple decomposition; Oracle: single dbt model/query). "
                              f"Default is opus when in doubt.")

    return allow(subagent_type, model, "all checks passed")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            # Empty stdin — fail open
            result = warn_allow("(unknown)", "(unknown)", "empty stdin — cannot validate, failing open")
            print(json.dumps(result))
            return

        input_data = json.loads(raw)

        # Belt-and-suspenders: pass through immediately for non-dispatch tools.
        # hooks.json matcher (Agent|Task) is the primary gate; this is defence-in-depth.
        tool_name = input_data.get("tool_name", "")
        if tool_name not in ("Agent", "Task"):
            print(json.dumps({}))
            return

        tool_input = input_data.get("tool_input") or {}
        result = validate(tool_input)
        print(json.dumps(result))

    except json.JSONDecodeError as exc:
        # Unparseable stdin — fail open
        msg = f"stdin JSON parse error ({exc}) — failing open"
        append_log("WARN", "(unknown)", "(unknown)", msg)
        print(json.dumps({"systemMessage": f"[dispatch-guard] WARN — {msg}"}))

    except Exception as exc:  # noqa: BLE001
        # Any unexpected error — fail open
        msg = f"unexpected error: {exc}"
        append_log("WARN", "(unknown)", "(unknown)", msg)
        print(json.dumps({"systemMessage": f"[dispatch-guard] WARN — {msg}"}))

    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
