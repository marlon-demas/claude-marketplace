#!/usr/bin/env python3
"""control-room emit.py — observer hook that appends one JSON line per Claude Code
hook event to ~/.claude/control-room/events.jsonl.

Fail-open doctrine (same as dispatch-guard): this script must NEVER affect the
session. Any error -> exit 0 silently. It writes a log line or it doesn't; it
never blocks, never prints hook output, never exits non-zero.
"""
import json
import os
import sys
import time

LOG_DIR = os.path.expanduser("~/.claude/control-room")
LOG = os.path.join(LOG_DIR, "events.jsonl")
ROTATE_BYTES = 5 * 1024 * 1024
TASK_EXCERPT = 140


def _token_hint(resp):
    """Best-effort token count from an Agent tool_response — the schema isn't
    contractual, so scan defensively for the usual usage keys. None when absent."""
    try:
        def walk(d, depth=0):
            if depth > 3 or not isinstance(d, dict):
                return None
            for k in ("subagent_tokens", "total_tokens", "totalTokens"):
                v = d.get(k)
                if isinstance(v, int) and v > 0:
                    return v
            u = d.get("usage")
            if isinstance(u, dict):
                s = sum(v for v in u.values() if isinstance(v, int))
                if s > 0:
                    return s
            for v in d.values():
                r = walk(v, depth + 1)
                if r:
                    return r
            return None
        return walk(resp)
    except Exception:
        return None


def _target_hint(tool, ti):
    """Short, sanitized hint of what a tool call touches — basenames and first
    words only; never full commands, contents, or prompts."""
    try:
        if tool in ("Read", "Edit", "Write", "NotebookEdit"):
            return os.path.basename(ti.get("file_path") or "") or None
        if tool == "Bash":
            return (ti.get("command") or "").strip().split()[0][:30] or None
        if tool in ("Grep", "Glob"):
            return (ti.get("pattern") or "")[:30] or None
        if tool == "Skill":
            return ti.get("skill") or None
        if tool in ("WebFetch", "WebSearch"):
            u = ti.get("url") or ti.get("query") or ""
            return u.split("/")[2] if u.startswith("http") else u[:30] or None
        if tool == "ToolSearch":
            return (ti.get("query") or "")[:30] or None
    except Exception:
        pass
    return None


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name") or ""
    out = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": event,
        "session": (data.get("session_id") or "")[:8],
        "cwd": os.path.basename(data.get("cwd") or "") or None,
    }

    tool = data.get("tool_name") or ""
    if event in ("PreToolUse", "PostToolUse") and tool in ("Agent", "Task"):
        tool_input = data.get("tool_input") or {}
        out["id"] = data.get("tool_use_id")
        out["agent"] = tool_input.get("subagent_type") or "general-purpose"
        out["model"] = tool_input.get("model") or None
        task = tool_input.get("description") or tool_input.get("prompt") or ""
        out["task"] = " ".join(task.split())[:TASK_EXCERPT] or None
        if event == "PostToolUse":
            resp = data.get("tool_response")
            err = isinstance(resp, dict) and (
                resp.get("is_error") or resp.get("error") or resp.get("interrupted")
            )
            out["ok"] = not err
            out["tok"] = _token_hint(resp)
    elif event == "PreToolUse":
        # Activity inside a dispatched subagent: the payload self-identifies via
        # agent_type/agent_id (verified empirically 2026-06-12). Main-session tool
        # calls carry no agent_type and are not logged — only agents-at-work are.
        agent = data.get("agent_type")
        if not agent:
            return
        out["event"] = "tool"
        out["agent"] = agent
        out["aid"] = (data.get("agent_id") or "")[:8] or None
        out["tool"] = tool
        out["target"] = _target_hint(tool, data.get("tool_input") or {})
    elif event == "UserPromptSubmit":
        # Word count only — prompt content stays out of the event log.
        out["words"] = len((data.get("user_prompt") or data.get("prompt") or "").split())
    # SessionStart / Stop / SubagentStop / SessionEnd: common fields are enough.

    os.makedirs(LOG_DIR, exist_ok=True)
    try:
        if os.path.getsize(LOG) > ROTATE_BYTES:
            os.replace(LOG, LOG + ".1")
    except OSError:
        pass
    with open(LOG, "a") as f:
        f.write(json.dumps({k: v for k, v in out.items() if v is not None}) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
